import streamlit as st

class FeatureActivator:
    def __init__(self):
        self.on = st.sidebar.toggle("DarkMode🌙")
        self.off = st.sidebar.toggle("WhiteMode☀️")

    def run(self):
        if self.on:
            st.write("Feature activated!")
            
        else:
            st.write("Feature deactivated.")
            self.on = st.sidebar.toggle("WhiteMode☀️")


if __name__ == "__main__":
    app = FeatureActivator()
    app2 = FeatureActivator()
    app.run()
    app2.run()