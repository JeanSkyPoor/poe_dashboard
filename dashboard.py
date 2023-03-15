import pandas as pd
import streamlit as st
import plotly.express as px

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


    def get_selected_class_and_lvl_range(self):
        self.selected_class = st.selectbox("Choose class", options = ["All classes", *self.all_classes], index = 0)
        self.create_lvl_search_slider()
        return self


    def show_all_classes_df(self):
        self.show_overall_and_searching_fields()
        self.original_df = self.original_df[(self.original_df.Level >= self.min_search_lvl) & (self.original_df.Level <= self.max_search_lvl)]

        if len(self.search_by_account) != 0:
            with st.expander("Searched by account", expanded = True):
                searched_df = self.original_df[self.original_df.Account == self.search_by_account]
                st.dataframe(searched_df, use_container_width = True)
                #self.get_metrics(searched_df)

        if len(self.search_by_character) != 0:
            with st.expander("Searched by character name", expanded = True):
                searched_df = self.original_df[self.original_df.Character == self.search_by_character]
                st.dataframe(searched_df, use_container_width = True)
                #self.get_metrics(searched_df)

        if len(self.search_by_account) == 0 and len(self.search_by_character) == 0:
            with st.expander("Table", expanded = True):
                st.dataframe(self.original_df, use_container_width = True)
                #self.get_metrics(self.original_df)
        return self


    def show_overall_and_searching_fields(self):
        search_by_account, overall_col, search_by_character = st.columns(3)

        with search_by_account:
            self.search_by_account = st.text_input("Search by account").strip()

        with overall_col:
            st.header("Overall table")

        with search_by_character:
            self.search_by_character = st.text_input("Search by character name").strip()

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
        self.selected_class_df = self.selected_class_df[(self.selected_class_df.Level >= self.min_search_lvl) & (self.selected_class_df.Level <= self.max_search_lvl)]
        if len(self.search_by_account) != 0:
            with st.expander("Searched by account", expanded = True):
                searched_df = self.selected_class_df[self.selected_class_df.Account == self.search_by_account]
                st.dataframe(searched_df, use_container_width = True)
                #self.get_metrics(searched_df)

        if len(self.search_by_character) != 0:
            with st.expander("Searched by character", expanded = True):
                searched_df = self.selected_class_df[self.selected_class_df.Character == self.search_by_character]
                st.dataframe(searched_df, use_container_width = True)
                #self.get_metrics(searched_df)


        if len(self.search_by_account) == 0 and len(self.search_by_character) == 0:
            with st.expander("Table", expanded = True):
                st.dataframe(self.selected_class_df, use_container_width = True)
                #self.get_metrics(self.selected_class_df)

        return self
            

    def draw_lvl_dist_graph(self, df):
        self.lvl_dist_df = df.Level.value_counts()
        fig = px.bar(self.lvl_dist_df, x = self.lvl_dist_df.index.values, y = self.lvl_dist_df.values, text_auto = True)
        fig.update_layout(title = 'Level distribution', 
            xaxis_title = "Level", 
            yaxis_title = 'Count', 
            width = 800, 
            height = 500, 
            titlefont=dict(size=40))
        fig.update_xaxes(tickangle=280, tickfont=dict(size=15), titlefont=dict(size=25))
        fig.update_yaxes(titlefont=dict(size=25))

        st.plotly_chart(fig, theme="streamlit")

        return self

    def draw_class_dist_all_classes_graph(self):
        self.class_dist_df = self.original_df.Class.value_counts()        
        fig = px.bar(self.class_dist_df, x = self.class_dist_df.index.values, y = self.class_dist_df.values, text_auto = True)
        fig.update_layout(title = 'Сlass distribution', 
            xaxis_title = "Classes", 
            yaxis_title = 'Count', 
            width = 800, 
            height = 500, 
            titlefont=dict(size=40))
        fig.update_xaxes(tickangle=280, tickfont=dict(size=15), titlefont=dict(size=25))
        fig.update_yaxes(titlefont=dict(size=25))    
        st.plotly_chart(fig, theme="streamlit")

        return self

    def draw_count_character_graph(self):
        self.count_character_per_acc_df = self.original_df.groupby("Account").agg({"Character":"count"}).Character.value_counts()
        fig = px.bar(self.count_character_per_acc_df, x = self.count_character_per_acc_df.index.values, y = self.count_character_per_acc_df.values, text_auto = True)
        fig.update_layout(title = 'Count character per account', 
            xaxis_title = "Character per account", 
            yaxis_title = 'Count', 
            width = 800, 
            height = 500, 
            titlefont=dict(size=40))
        fig.update_xaxes(tickangle=280, tickfont=dict(size=15), titlefont=dict(size=25))
        fig.update_yaxes(titlefont=dict(size=25))    
        st.plotly_chart(fig, theme="streamlit")

        return self
    

    def create_lvl_search_slider(self):
        select_slider_data = st.slider("Choose lvl range for searching", min_value = 1, max_value = 100, step = 1, value = [1,100])
        self.min_search_lvl = select_slider_data[0]
        self.max_search_lvl = select_slider_data[1]

dashboard = Dashboard()

raw_data_input = st.empty()
raw_data = raw_data_input.file_uploader("Load your CSV file here", type = ["csv"])
if raw_data != None:
    dashboard.read_df(raw_data)
    raw_data_input.empty()

    dashboard.get_list_all_classes().get_selected_class_and_lvl_range()

    if dashboard.selected_class == "All classes":

        dashboard.show_all_classes_df()\
            .get_metrics(dashboard.original_df)\
            .display_metrics()\
            .draw_class_dist_all_classes_graph()\
            .draw_lvl_dist_graph(dashboard.original_df)\
            .draw_count_character_graph()

    else:
        dashboard.read_selected_class_df()\
            .show_selected_class_df()\
            .get_metrics(dashboard.selected_class_df)\
            .display_metrics()\
            .draw_lvl_dist_graph(dashboard.selected_class_df)








