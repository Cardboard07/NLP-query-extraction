import streamlit as st
import pandas as pd
from pipeline import parse_query
import io
st.title('NLP query extraction')
st.write('choose doc uploader or text input')
choice = st.radio("How would you like to provide data?", ["Text Input", "File Upload"])
rows = []
if(choice=='File Upload'):
    input=st.file_uploader('upload file here',type='txt')
    if input is not None:
        stringio = io.StringIO(input.getvalue().decode("utf-8"))
        for line in stringio:
            clean_line = line.strip()
            if clean_line:
                result = parse_query(clean_line)
                row = {"query": clean_line}
                row.update(result)
                rows.append(row)
        df = pd.DataFrame(rows)
else:
    input=st.text_input('query')
    result = parse_query(input)
    row = {"query": input}
    row.update(result)
    rows.append(row)

df = pd.DataFrame(rows)
st.write(df)

buffer = io.BytesIO()

with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df.to_excel(writer, index=False)

buffer.seek(0)  # CRITICAL

st.download_button(
    label="Download Excel",
    data=buffer,
    file_name="my_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    icon=":material/download:",
)