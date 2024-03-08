# https://discuss.streamlit.io/t/customize-theme/39156/5
# https://discuss.streamlit.io/t/is-there-a-function-called-by-text-input-change-everytime-when-i-input-a-character/41438/2
# https://docs.streamlit.io/library/api-reference/widgets/st.download_button
# https://github.com/gagan3012/streamlit-tags?tab=readme-ov-file

# import streamlit as st
# from st_keyup import st_keyup

# value = st_keyup("Enter a value", key="0")

# # Notice that value updates after every key press
# st.write(value)

# # If you want to set a default value, you can pass one
# with_default = st_keyup("Enter a value", value="Example", key="1")

# # If you want to limit how often the value gets updated, pass `debounce` value, which
# # will force the value to only update after that many milliseconds have passed
# with_debounce = st_keyup("Enter a value", debounce=500, key="2")

import streamlit as st
class StreamlitApp:
    def __init__(self):
        self.title = "Information Retrieval System"
        self.description = "This is a simple information retrieval system that uses the extended boolean model to search for documents in a collection of research papers."
        self.query = ""
        self.query_results = []
        self.query_result = None
        
    def toggle_theme(self):        
        dark = '''
        <style>
            .stApp {
            background-color: black;
            }
        </style>
        '''

        light = '''
        <style>
            .stApp {
            background-color: white;
            }
        </style>
        '''

        st.markdown(light, unsafe_allow_html=True)

        # Create a toggle button
        toggle = st.button("Toggle theme")

        # Use a global variable to store the current theme
        if "theme" not in st.session_state:
            st.session_state.theme = "light"

        # Change the theme based on the button state
        if toggle:
            if st.session_state.theme == "light":
                st.session_state.theme = "dark"
            else:
                st.session_state.theme = "light"

        # Apply the theme to the app
        if st.session_state.theme == "dark":
            st.markdown(dark, unsafe_allow_html=True)
        else:
            st.markdown(light, unsafe_allow_html=True)
        
    def main(self):
        st.title(self.title)
        st.write(self.description)
        # self.toggle_theme()
        self.query = st.text_input("Enter a query")
        self.query_results = st.button("Search")
        if self.query_results:
            self.query_result = self.proximity_query(self.query)
            st.write(self.query_result)
        st.write("The query results will be displayed here")
        
if __name__=="__main__":
    app = StreamlitApp()
    app.main()
