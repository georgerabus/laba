import streamlit as st
from pages.util.DarkMode import *
import pages.AI

st.set_page_config(
    page_title="QuickSearch",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded",
)


def get_step():
    return st.session_state.get('step', 1)

def next_step():
    st.session_state['step'] = get_step() + 1

def write():


    app = FeatureActivator()

    app.run()

    st.write("# QuickFinder Demo")

    st.write("""Use Cases:
             \n1) You can ask a question, and the AI will respond to your question.
             \n2) To ensure you get the most affordable laptop, try taking a quiz.""")

st.button("Next", on_click=next_step)

if __name__ == "__main__":
    write()
