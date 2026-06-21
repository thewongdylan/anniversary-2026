import streamlit as st

st.title("Anniversary 2026")
st.caption("We have come full circle!")

if st.button("Wordle"):
    st.switch_page("pages/wordle.py")