# mini webapp to get unique values from a list, text file, CSV file, or Excel column(s)


import streamlit as st
import pandas as pd

pg_icon="/Get-Uniques/getUniques_pg_icon.png"

st.set_page_config(
    page_title="Get-Uniques WebApp",
    page_icon=pg_icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "https://github.com/colby-reyes/Get-Uniques/issues/new/choose",
        'About': "# A simple `stremlit` app to get unique values from an input.<hr> Input can be typed/pasted in a text box or an uploaded text, csv, or Excel file."
    }
)

def get_uniques(input_format:str="Text Box", sep:str="New Line"):
    sep_mapper = {
        "New Line":"\n",
        "comma (`,`)":",",
        "pipe (`|`)":"|",
        "space (` `)":" "
    }

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

c1, c2 = st.columns(2)
input_choice = c1.selectbox(
    "Input format:",
    ("Type/Paste", "Upload"),
    key="visibility",
)

sep_choice = c2.selectbox(
    "How is your data separated?",
    ("New Line","comma (`,`)","pipe (`|`)","space (` `)"),
    disabled=st.session_state.disabled,
)


if input_choice == "Type/Paste":
    user_input = st.text_area(
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
        label_visibility="visible")
else:
    col_name = st.text_input("Name of column with data:",)
    user_input = st.file_uploader("Select `csv` file:", type=['csv'],accept_multiple_files=False)


def getUniques_from_textInput(user_input:str, sep:str):
    inp_list = user_input.split(sep)
    uniques_list = list(set(inp_list))

    return uniques_list

def getUniques_from_csvInput(file_upload, data_col:str):
    df = pd.read_csv(file_upload)
    data_list = df[data_col].to_list()
    uniques_list = list(set(inp_list))

    return uniques_list


if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

def click_button():
    st.session_state.button_clicked = not st.session_state.button_clicked


