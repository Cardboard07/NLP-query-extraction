import streamlit as st
import subprocess
import sys

st.title("DEBUG MODE: python -m pip freeze")

out = subprocess.check_output(
    [sys.executable, "-m", "pip", "freeze"]
).decode()

st.code(out)
st.stop()
