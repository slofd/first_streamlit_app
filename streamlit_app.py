import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title("My parents healthy dinner")
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

# dropdown list that read data from txt file
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


# show api response data using pandas lib
streamlit.header("Data table from api.")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

# get data from snowflake
# snowflake.connector.paramstyle = 'qmark'
streamlit.header("Fruityvice Fruit Advice!(Dropdown list values from snowflake)")
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select fruit_name from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.dataframe(my_data_row)
# my_data_row = my_data_row.set_index(0)
# fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')

fruits_selected = streamlit.multiselect("What fruit would you like information about?", list(my_data_row))
streamlit.dataframe(fruits_selected)

