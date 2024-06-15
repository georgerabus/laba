import streamlit as st
import Pages.DarkMode
import Pages.AI

def write():
    st.write("# QuickFinder Demo")

    st.write("""Use Cases:
             \n1)You can ask a question, and the AI will respond to your question.
             \n2) To ensure you get the most affordable laptop, try taking a quiz.""")

if __name__ == "__main__":
    write()
