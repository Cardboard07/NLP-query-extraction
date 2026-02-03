import streamlit as st
import subprocess

st.title("DEBUG MODE: pip freeze")

out = subprocess.check_output(["pip", "freeze"]).decode()
st.code(out)

st.stop()
