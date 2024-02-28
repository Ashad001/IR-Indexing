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