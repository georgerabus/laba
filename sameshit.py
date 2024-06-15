import streamlit as st
from streamlit_chatbox import *
import time
import simplejson as json


llm = FakeLLM()
chat_box = ChatBox()
chat_box.use_chat_name("chat1")  # add a chat conversation

def on_chat_change():
    chat_box.use_chat_name(st.session_state["chat_name"])
    chat_box.context_to_session()  # restore widget values to st.session_state when chat name changed

# Sidebar for Chat Session Selection and Options
with st.sidebar:
    st.subheader('Start to Chat using Streamlit')
    chat_name = st.selectbox("Chat Session:", ["default", "chat1"], key="chat_name", on_change=on_chat_change)
    chat_box.use_chat_name(chat_name)
    streaming = st.checkbox('Streaming', key="streaming")
    in_expander = st.checkbox('Show Messages in Expander', key="in_expander")
    show_history = st.checkbox('Show Session State', key="show_history")
    chat_box.context_from_session(exclude=["chat_name"])  # save widget values to chat context

    st.divider()

    btns = st.container()

    file = st.file_uploader("Chat History JSON", type=["json"])

    if st.button("Load JSON") and file:
        data = json.load(file)
        chat_box.from_dict(data)

# Title and Open/Close Chat Buttons
st.title("Chat Interface")

if not st.session_state.get("show_chat", False):
    if st.button("Open Chat"):
        st.session_state["show_chat"] = True
else:
    if st.button("Close Chat"):
        st.session_state["show_chat"] = False

# Display chat interface if show_chat is True
if st.session_state.get("show_chat", False):
    chat_box.output_messages()

    def on_feedback(feedback, chat_history_id: str = "", history_index: int = -1):
        reason = feedback["text"]
        score_int = chat_box.set_feedback(feedback=feedback, history_index=history_index)  # convert emoji to integer
        # do something
        st.session_state["need_rerun"] = True

    feedback_kwargs = {
        "feedback_type": "thumbs",
        "optional_text_label": "Welcome to feedback",
    }

    if query := st.chat_input('Input your question here'):
        chat_box.user_say(query)
        if streaming:
            generator = llm.chat_stream(query)
            elements = chat_box.ai_say(
                [
                    Markdown("Thinking", in_expander=in_expander, expanded=True, title="Answer"),
                    Markdown("", in_expander=in_expander, title="References"),
                ]
            )
            time.sleep(1)
            text = ""
            for x, docs in generator:
                text += x
                chat_box.update_msg(text, element_index=0, streaming=True)
            # update the element without focus
            chat_box.update_msg(text, element_index=0, streaming=False, state="complete")
            chat_box.update_msg("\n\n".join(docs), element_index=1, streaming=False, state="complete")
            chat_history_id = "some id"
            chat_box.show_feedback(
                **feedback_kwargs,
                key=chat_history_id,
                on_submit=on_feedback,
                kwargs={"chat_history_id": chat_history_id, "history_index": len(chat_box.history) - 1}
            )
        else:
            text, docs = llm.chat(query)
            chat_box.ai_say(
                [
                    Markdown(text, in_expander=in_expander, expanded=True, title="Answer"),
                    Markdown("\n\n".join(docs), in_expander=in_expander, title="References"),
                ]
            )

    cols = st.columns(2)
    if cols[0].button('Show me the multimedia'):
        chat_box.ai_say(Image('https://tse4-mm.cn.bing.net/th/id/OIP-C.cy76ifbr2oQPMEs2H82D-QHaEv?w=284&h=181&c=7&r=0&o=5&dpr=1.5&pid=1.7'))
        time.sleep(0.5)
        chat_box.ai_say(Video('https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4'))
        time.sleep(0.5)
        chat_box.ai_say(Audio('https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4'))

    if cols[1].button('Run Agent'):
        chat_box.user_say('run agent')
        agent = FakeAgent()
        text = ""

        # streaming:
        chat_box.ai_say()  # generate a blank placeholder to render messages
        for d in agent.run_stream():
            if d["type"] == "complete":
                chat_box.update_msg(expanded=False, state="complete")
                chat_box.insert_msg(d["llm_output"])
                break

            if d["status"] == 1:
                chat_box.update_msg(expanded=False, state="complete")
                text = ""
                chat_box.insert_msg(Markdown(text, title=d["text"], in_expander=True, expanded=True))
            elif d["status"] == 2:
                text += d["llm_output"]
                chat_box.update_msg(text, streaming=True)
            else:
                chat_box.update_msg(text, streaming=False)

    btns.download_button(
        "Export Markdown",
        "".join(chat_box.export2md()),
        file_name=f"chat_history.md",
        mime="text/markdown",
    )

    btns.download_button(
        "Export JSON",
        chat_box.to_json(),
        file_name="chat_history.json",
        mime="text/json",
    )

    if btns.button("Clear History"):
        chat_box.init_session(clear=True)
        st.experimental_rerun()

    if show_history:
        st.write(st.session_state)


def main():
    st.title("QuickFinder")
    if "page" not in st.session_state:
        st.session_state.page = 0

    def next_page():
        st.session_state.page += 1

    def prev_page():
        st.session_state.page -= 1

    pages = [
        "Welcome to the quiz! Prepare yourself.",
        "Question 1: What is your favorite color?",
        "Question 2: What is your favorite animal?",
        "Question 3: What is your favorite food?",
        "Question 4: What is your favorite movie?",
        "Question 5: What is your favorite book?",
        "Thank you for completing the quiz!"
    ]

    st.write(pages[st.session_state.page])

    col1, col2 = st.columns(2)
    if st.session_state.page > 0:
        col1.button("Previous", on_click=prev_page)
    if st.session_state.page < len(pages) - 1:
        col2.button("Next", on_click=next_page)

if __name__ == "__main__":
    main()
