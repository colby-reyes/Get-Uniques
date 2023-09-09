# mini webapp to get unique values from a list, text file, CSV file, or Excel column(s)


import pandas as pd
import streamlit as st

pg_icon = "/Get-Uniques/getUniques_pg_icon.png"

st.set_page_config(
    page_title="Get-Uniques WebApp",
    page_icon=pg_icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Report a bug": "https://github.com/colby-reyes/Get-Uniques/issues/new/choose",
        "About": """# A simple `stremlit` app to get unique values from an input.<hr> 
        Input can be typed/pasted in a text box or an uploaded text, csv, or Excel file.""",
    },
)


def get_input_data(
    input_format: str = "Type/Paste", input_file: str = "", input_text: str = ""
):
    if input_format == "Upload" and input_file.endswith(".csv"):
        df = pd.read_csv(input_file)
    elif input_format == "Upload" and (
        input_file.endswith(".xlsx") or input_file.endswith(".xls")
    ):
        df = pd.read_excel(input_file)
    elif input_format == "Upload" and input_file.endswith(".txt"):
        with open(input_file, "r") as fh:
            text_data = fh.readlines()
    else:
        text_data = input_text

    if df:
        return df
    else:
        return text_data


def get_uniques(
    input_format: str = "Type/Paste",
    sep: str = "New Line",
    input_file: str = None,
    input_text: str = None,
):
    sep_mapper = {
        "New Line": "\n",
        "comma (`,`)": ",",
        "pipe (`|`)": "|",
        "space (` `)": " ",
    }

    data = get_input_data(input_format, input_file, input_text)
    


if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

c1, c2 = st.comlumns(2)
input_choice = c1.selectbox(
    "Input format:",
    ("Type/Paste", "Upload"),
    key="visibility",
)

sep_choice = c2.selectbox(
    "How is your data separated?",
    ("New Line", "comma (`,`)", "pipe (`|`)", "space (` `)"),
    disabled=st.session_state.disabled,
)


st.text_area(
    "Type/Paste list here:",
    value="",
    height=None,
    max_chars=None,
    key=None,
    help=None,
    on_change=None,
    args=None,
    kwargs=None,
    placeholder=None,
    disabled=False,
    label_visibility="visible",
)
