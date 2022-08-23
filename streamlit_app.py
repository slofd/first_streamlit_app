
import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title("My parents healthy dinner")

streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)


# get data from snowflake
streamlit.header("Fruityvice Fruit Advice!")
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select fruit_name from fruit_load_list")
my_data_row = my_cur.fetchall()
my_data_row =my_data_row.set_index('fruit_name');

# fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
fruits_selected=streamlit.multiselect("What fruit would you like information about?", list(my_data_row.index),['Avocado','Strawberries'])

streamlit.write('The user entered ', fruits_selected)

# show api response data
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("select fruit_name from fruit_load_list")
# # my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION(),current_database(), current_schema(),current_role()")
# my_data_row = my_cur.fetchall()
# streamlit.header("Load fruit list:")
# streamlit.dataframe(my_data_row)




