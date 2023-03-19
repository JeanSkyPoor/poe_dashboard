import streamlit as st
from dashboard_class import Dashboard
st.set_page_config(layout="wide")


db = Dashboard()

raw_data_input = st.empty()
raw_data = raw_data_input.file_uploader("Load your CSV file here", type = ["csv"])
if raw_data != None:
    db.read_dropped_file(raw_data)
    raw_data_input.empty()

    db.get_all_classes_list()\
        .draw_table_interface()\
        .draw_filtered_df()\
        .draw_df_metrics()\
        .draw_class_dist_graph()\
        .draw_lvl_dist_graph()\
        .draw_count_character_graph()