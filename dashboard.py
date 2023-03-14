import pandas as pd
import streamlit as st


class Dashboard():

    def read_df(self, raw_data):
        self.original_df = pd.read_csv(raw_data, sep = ",").drop(columns=["Dead"])

        return self


    def get_metrics(self, df):
        self.max_lvl = df.Level.max()
        self.min_lvl = df.Level.min()
        self.average_lvl = round(df.Level.mean(), 2)
        self.total_character = df.shape[0]
        self.unique_people = df.Account.nunique()
        
        return self
    

    def get_list_all_classes(self):
        self.all_classes = sorted(self.original_df.Class.unique())
        
        return self


    def get_selected_class(self):
        self.selected_class = st.selectbox("Choose class", options = ["All classes", *self.all_classes], index = 0)

        return self


    def show_all_classes_df(self):
        self.show_overall_and_searching_fields()

        if len(self.search_by_account) != 0:
            with st.expander("Searched by account", expanded = True):
                st.dataframe(self.original_df[self.original_df.Account == self.search_by_account], use_container_width = True)

        if len(self.search_by_character) != 0:
            with st.expander("Searched by character name", expanded = True):
                st.dataframe(self.original_df[self.original_df.Character == self.search_by_character], use_container_width = True)

        if len(self.search_by_account) == 0 and len(self.search_by_character) == 0:
            with st.expander("Table", expanded = True):
                st.dataframe(self.original_df, use_container_width = True)

        return self


    def show_overall_and_searching_fields(self):
        search_by_account, overall_col, search_by_character = st.columns(3)

        with search_by_account:
            self.search_by_account = st.text_input("Search by account")

        with overall_col:
            st.header("Overall table")

        with search_by_character:
            self.search_by_character = st.text_input("Search by character name")

        return self


    def display_metrics(self):
        unique_players, total_character, min_lvl, max_lvl, average_lvl = st.columns(5)

        with unique_players:
            st.metric("Unique players", self.unique_people)

        with total_character:
            st.metric("Total character", self.total_character)

        with min_lvl:
            st.metric("Min level", self.min_lvl)

        with max_lvl:
            st.metric("Max level", self.max_lvl)

        with average_lvl:
            st.metric("Average level", self.average_lvl)
        
        return self


    def read_selected_class_df(self):
        self.selected_class_df = self.original_df[self.original_df.Class == self.selected_class]

        return self


    def show_selected_class_df(self):
        self.show_overall_and_searching_fields()

        if len(self.search_by_account) != 0:
            with st.expander("Searched by account", expanded = True):
                st.dataframe(self.selected_class_df[self.selected_class_df.Account == self.search_by_account], use_container_width = True)

        if len(self.search_by_character) != 0:
            with st.expander("Searched by character", expanded = True):
                st.dataframe(self.selected_class_df[self.selected_class_df.Character == self.search_by_character], use_container_width = True)

        if len(self.search_by_account) == 0 and len(self.search_by_character) == 0:
            with st.expander("Table", expanded = True):
                st.dataframe(self.selected_class_df, use_container_width = True)

        return self
            


dashboard = Dashboard()

raw_data_input = st.empty()
raw_data = raw_data_input.file_uploader("Load your CSV file here", type = ["csv"])
if raw_data != None:
    dashboard.read_df(raw_data)
    raw_data_input.empty()

    dashboard.get_list_all_classes().get_selected_class()

    if dashboard.selected_class == "All classes":

        dashboard.get_metrics(dashboard.original_df)\
            .show_all_classes_df()\
            .display_metrics()

    else:
        dashboard.read_selected_class_df()\
            .show_selected_class_df()\
            .get_metrics(dashboard.selected_class_df)\
            .display_metrics()







