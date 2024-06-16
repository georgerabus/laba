import streamlit as st
import os

class FeatureActivator:
    def __init__(self):
        st.sidebar.toggle("DarkMode🌙", key="t1", value=False)
        self.current_command = 1 

    def run(self):
        current_dir = os.getcwd()
        config_path = os.path.join(current_dir, '.streamlit', 'config.toml')
        
        if  st.session_state.t1  == True:
            
            with open(config_path, "w+") as f:
                f.write("""
                    [theme]
                    base = "dark"
                """)
        if  st.session_state.t1  == False:
            with open(config_path, "w+") as f:
                f.write("""
                    [theme]
                    base = "light"
                """)


    # def run(self):
    #     current_dir = os.getcwd()
    #     config_path = os.path.join(current_dir, '.streamlit', 'config.toml')
        
    #     if self.on == True:
    #         st.write("Second-Hand activated")
            
    #         with open(config_path, "w+") as f:
    #             f.write("""
    #                 [theme]
    #                 base = "dark"
    #             """)
    #     if self.on == False:
    #         st.write("First-Hand activated.")
    #         with open(config_path, "w+") as f:
    #             f.write("""
    #                 [theme]
    #                 base = "light"
    #             """)