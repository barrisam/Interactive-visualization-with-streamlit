import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


# To set a webpage title, header and subtitle
st.set_page_config(page_title = "Movies analysis",layout = 'wide')
st.header("Interactive Dashboard")
st.subheader("Interact with this dashboard using the sidebar to find out more")


#read in the file
movies_data = pd.read_csv("https://raw.githubusercontent.com/danielgrijalva/movie-stats/7c6a562377ab5c91bb80c405be50a0494ae8e582/movies.csv")
movies_data.drop_duplicates(inplace = True)  # drop_duplicates


#read in the tips file
tips = pd.read_csv("tips.csv")
tips.drop_duplicates(inplace = True)  # drop_duplicates

with st.expander("Plot with Matplotlib and Plotly: Click to expand"):
    # creating a bar graph with matplotlib
    st.write("""
    Average Movie Budget, Grouped by Genre
    """)
    avg_budget = movies_data.groupby('genre')['budget'].mean().round()
    avg_budget = avg_budget.reset_index()
    genre = avg_budget['genre']
    avg_bud = avg_budget['budget']

    fig = plt.figure(figsize = (19, 10))

    plt.bar(genre, avg_bud, color = 'maroon')
    plt.xlabel('genre')
    plt.ylabel('budget')
    plt.title('Matplotlib Bar Chart Showing The Average Budget of Movies in Each Genre')
    st.pyplot(fig)

    # Creating a line chart with plotly
    st.write("""
    ##### Average User Rating, Grouped by Genre #####
    """)
    avg_rating = movies_data.groupby('genre')['score'].mean().round(1)
    avg_rating = avg_rating.reset_index()

    figpx = px.line(avg_rating, x = 'genre', y = 'score', title = 'Plotly Line Chart Showing The Average User Rating of Movie in Each Genre')
    st.plotly_chart(figpx)


# Creating sidebar widget filters from movies dataset
directors_list = movies_data['director'].unique().tolist()
score_rating = movies_data['score'].unique().tolist()
genre_list = movies_data['genre'].unique().tolist()


# Add the filters. Every widget goes in here
with st.sidebar:

    new_score_rating = st.slider(label = "Move the slider to make the dataframe change values:",
                                 min_value = min(score_rating),
                                 max_value = max(score_rating),
                                 value = (min(score_rating), max(score_rating)))


    new_genre_list = st.multiselect("Select and deselect the genre you wish to view",
                                        genre_list, default = ['Animation', 'Horror', 'Comedy', 'Action', 'Biography', 'Fantasy', 'Romance'])

    radio_viz = st.radio("Choose a visualization:",
                        ('Total_bills', 'Tips', 'Piechart'))


#filter for slider
score_info = (movies_data['score'].between(*new_score_rating))
score_infos= movies_data[score_info]

#filter for genre and average reviews with multiselect
genre_avg_score = (movies_data['genre'].isin(new_genre_list))
avg_rating = movies_data[genre_avg_score].groupby('genre')['score'].mean().round(1)
avg_rating = avg_rating.reset_index()


#VISUALIZATION SECTION
#group the columns needed for visualizations
col1, col2 = st.columns([1,3])
with col1:
    directors = (round(movies_data[score_info].groupby('director').score.mean(),1))
    directors.reset_index()
    st.dataframe(directors)

with col2:
    figpx = px.line(avg_rating, x = 'genre', y = 'score', title = 'Genre and average rating by year')
    st.plotly_chart(figpx)

if radio_viz == "Total_bills":
    st.write('You selected', radio_viz)
    fig5 = px.bar(tips, x = 'sex', y = 'total_bill', color = 'time', barmode = 'group', height = 400)
    st.plotly_chart(fig5)

elif radio_viz == "Tips":
    st.write('You selected', radio_viz)
    fig6 = px.bar(tips, x = 'sex', y = 'tip', color = 'time', barmode = 'group', height = 400)
    st.plotly_chart(fig6)

elif radio_viz == "Piechart":
    st.write('You selected', radio_viz)
    fig7 = px.pie(tips, values='tip', names='day', color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig7)
else:
    st.write("Pick a radio button")
