import streamlit as st

def main():
    DarkMode = st.toggle(" DarkMode ")
   

    if DarkMode:
        st.write("Feature activated!")
    else :
        st.write("Feature deactivated!")

if __name__ == '__main__':
    main()