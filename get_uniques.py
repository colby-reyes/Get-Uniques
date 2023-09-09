# mini webapp to get unique values from a list, text file, CSV file, or Excel column(s)


from collections import namedtuple

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

input_dataStruct = namedtuple("input_DataStruct", ["data", "dtype"])


def get_input_data(
    input_format: str = "Type/Paste", input_file: str = "", input_text: str = ""
):
    if input_format == "Upload" and input_file.endswith(".csv"):
        df = pd.read_csv(input_file)
        input_data = input_dataStruct(df, "df")
    elif input_format == "Upload" and (
        input_file.endswith(".xlsx") or input_file.endswith(".xls")
    ):
        df = pd.read_excel(input_file)
        input_data = input_dataStruct(df, "df")
    elif input_format == "Upload" and input_file.endswith(".txt"):
        with open(input_file, "r") as fh:
            text_data = fh.readlines()
        input_data = input_dataStruct(text_data, "text")
    else:
        input_data = input_dataStruct(input_text, "text")

    return input_data


def get_uniques(
    input_format: str = "Type/Paste",
    sep: str = "New Line",
    input_text: str = "",
    input_file: str = None,
    input_col: str = None,
):
    sep_mapper = {
        "New Line": "\n",
        "comma (`,`)": ",",
        "pipe (`|`)": "|",
        "space (` `)": " ",
    }

    input_data = get_input_data(input_format, input_file, input_text)

    if input_data.dtype == "text":
        input_txt = input_data.data
        output_lst = input_txt.split(sep_mapper[sep_choice])
    elif input_data.dtype == "df":
        input_df = input_data.data
        output_lst = input_df[input_col].uniques().to_list()
    else:
        st.error("Something went very wrong!")

    return output_lst


if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

c1, c2, c3 = st.columns(3)
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

data_container = st.container()

with data_container:
    st.session_state.disabled = False
    if input_choice == "Type/Paste":
        user_data_input = st.text_area(
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
    else:
        st.session_state.disabled = True
        user_data_input = st.file_uploader(
            "Upload file here:", ["csv", "xls", "xlsx"], accept_multiple_files=False
        )
        if user_data_input:
            try:
                temp_df = pd.read_csv(user_data_input)
            except:
                temp_df = pd.read_excel(user_data_input)
            col_list = temp_df.columns
            desired_column = st.selectbox(
                "Name of column with data to extract: ", options=col_list, index=0
            )

output_formats = ["Comma", "New Line", "Pipe", "Semicolon", "Space"]
output_sep_mapper = {
    "New Line": "\n",
    "Comma": ",",
    "Pipe": "|",
    "Semicolon": ";",
    "Space": " ",
}

if user_data_input:
    output_format = c3.selectbox("Select output text separator:", output_formats)
    output_lst = get_uniques(
        input_choice,
        sep_choice,
        input_text=user_data_input,
        input_file=user_data_input,
        input_col=desired_column,
    )
