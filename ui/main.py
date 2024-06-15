import streamlit as st
from pages.util.DarkMode import *
import pages.AI

def write():
    app = FeatureActivator()
    app.run()
    
    st.write("# QuickFinder Demo")

    st.write("""Use Cases:
             \n1)You can ask a question, and the AI will respond to your question.
             \n2) To ensure you get the most affordable laptop, try taking a quiz.""")

if __name__ == "__main__":
    write()
