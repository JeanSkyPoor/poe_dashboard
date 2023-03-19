import pandas as pd
import streamlit as st
import plotly.express as px


class Dashboard():
    def read_dropped_file(self, df):
        self.orig_df = pd.read_csv(df, sep = ",").drop(columns = ["Dead"])

        return self


    def draw_table_interface(self):
        self.draw_selected_class()

        search_by_account, slider, search_by_character = st.columns([1, 2, 1])

        with search_by_account:
            self.draw_search_by_account()

        with slider:
            self.draw_lvl_slider()

        with search_by_character:
            self.draw_search_by_character()

        
        return self


    def get_all_classes_list(self):
        self.all_classes_list = sorted(self.orig_df.Class.unique())

        return self


    def draw_selected_class(self):
        help_message = "You can select only from the list of classes that are present in the file in the Class column"
        self.selected_class = st.selectbox("Choose class", options = ["All classes", *self.all_classes_list], help = help_message)

        return self


    def draw_lvl_slider(self):
        help_message = "Select the level range to filter"
        slider_data = st.slider("Choose lvl range for searching", min_value = 1, max_value = 100, step = 1, value = [1,100], help = help_message)
        self.min_lvl_search = slider_data[0]
        self.max_lvl_search = slider_data[1]

        return self


    def draw_search_by_account(self):
        help_message = "Enter the account name to filter by it"
        self.search_by_account = st.text_input("Search by account", help = help_message ).strip()

        return self


    def draw_search_by_character(self):
        help_message = "Enter character name to filter by it"
        self.search_by_character = st.text_input("Search by character", help = help_message).strip()

        return self


    def filter_df(self):
        self.filtered_df = self.orig_df[(self.orig_df.Level >= self.min_lvl_search) & (self.orig_df.Level <= self.max_lvl_search)]

        if self.selected_class != "All classes":
            self.filtered_df = self.filtered_df.query(f"Class == '{self.selected_class}'")

        if len(self.search_by_account) != 0 and len(self.search_by_character) != 0:
            self.filtered_df = self.filtered_df.query(f"Account == '{self.search_by_account}' and Character == '{self.search_by_character}'")
        
        if len(self.search_by_account) != 0 and len(self.search_by_character) == 0:
            self.filtered_df = self.filtered_df.query(f"Account == '{self.search_by_account}'")

        if len(self.search_by_character) != 0 and len(self.search_by_account) == 0:
            self.filtered_df = self.filtered_df.query(f"Character == '{self.search_by_character}'")


    def draw_filtered_df(self):

        self.filter_df()

        with st.expander("Filtered table", expanded = True):
            st.dataframe(self.filtered_df, use_container_width = True)

        
        return self


    def get_metrics(self):
        self.max_lvl_metric = self.filtered_df.Level.max()
        self.min_lvl_metric = self.filtered_df.Level.min()
        self.average_lvl_metric = round(self.filtered_df.Level.mean(), 2)
        self.total_character_metric = self.filtered_df.shape[0]
        self.unique_people_metric = self.filtered_df.Account.nunique()

        return self


    def draw_df_metrics(self):
        self.get_metrics()

        unique_players, total_character, min_lvl, max_lvl, average_lvl = st.columns(5)

        with unique_players:
            st.metric("Unique players", self.unique_people_metric)

        with total_character:
            st.metric("Total character", self.total_character_metric)

        with min_lvl:
            st.metric("Min level", self.min_lvl_metric)

        with max_lvl:
            st.metric("Max level", self.max_lvl_metric)

        with average_lvl:
            st.metric("Average level", self.average_lvl_metric)
        
        return self


    def draw_class_dist_graph(self):
        if self.selected_class == "All classes":
            if self.filtered_df.shape[0] != 0:
                filtered_df = self.filtered_df.Class.value_counts().reset_index().rename(columns={"index":"Class", "Class": "Total_count"})
                fig = px.bar(filtered_df, x = "Class", y = "Total_count", text_auto = True, template='seaborn')
                fig.update_layout(title = 'Сlass distribution', 
                    xaxis_title = "Classes", 
                    yaxis_title = 'Count', 
                    height = 600, 
                    titlefont=dict(size=40))
                fig.update_xaxes(tickangle=280, tickfont=dict(size=15), titlefont=dict(size=25))
                fig.update_yaxes(titlefont=dict(size=25))   
                fig.update_traces(width=0.5) 
                st.plotly_chart(fig, theme="streamlit", use_container_width = True)
            else:
                st.warning("I can't plot empty data")
        return self


    def draw_lvl_dist_graph(self):
        if self.filtered_df.shape[0] != 0:
            filtered_df = self.filtered_df.Level.value_counts().reset_index().rename(columns = {"index": "Level", "Level": "Total_count"})
            fig = px.bar(filtered_df, x = "Level", y = "Total_count", text_auto = True, template='seaborn')
            fig.update_layout(title = 'Level distribution', 
                xaxis_title = "Level", 
                yaxis_title = 'Count', 
                height = 600, 
                titlefont=dict(size=40))
            fig.update_xaxes(tickangle=280, tickfont=dict(size=15), titlefont=dict(size=25), range = [0, 102])
            fig.update_yaxes(titlefont=dict(size=25))
            fig.update_traces(width=1)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        else:
            st.warning("I can't plot empty data")

        return self


    def draw_count_character_graph(self):
        if self.filtered_df.shape[0] != 0:
            filtered_df = self.filtered_df.groupby("Account").agg({"Character": "count"})\
                .Character.value_counts().reset_index().rename(columns = {"index": "Character per account",
                                                                            "Character": "Total people with same sum"})
            fig = px.bar(filtered_df, x = "Character per account", y = "Total people with same sum", text_auto = True, template='seaborn')
            fig.update_layout(title = 'Count character per account', 
                xaxis_title = "Character per account", 
                yaxis_title = 'Count',
                height = 600, 
                titlefont=dict(size=40))
            fig.update_xaxes(tickangle=280, tickfont=dict(size=15), titlefont=dict(size=25))
            fig.update_yaxes(titlefont=dict(size=25))    
            st.plotly_chart(fig, theme="streamlit", use_container_width = True)
        else:
            st.warning("I can't plot empty data")

        return self