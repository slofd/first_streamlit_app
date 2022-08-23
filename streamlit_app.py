import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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

#function
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized




#dropdown from api response
streamlit.header("Fruityvice Fruit Advice!(Dropdown list values from api response)")
try:
    fruit_choice=streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        fruityvice_normalized=get_fruityvice_data(fruit_choice)
        streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()



#function
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select fruit_name from fruit_load_list")
        return my_cur.fetchall()


if streamlit.button('Get Fruit Load List'):
    streamlit.header("Fruit load list:")
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)
    my_cnx.close()


def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('"+new_fruit+"')")
        return "Thanks for adding " + new_fruit


add_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button("Add a fruit to load list"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_fruit)
    streamlit.text(back_from_function)
    my_cnx.close()

# streamlit.stop();

# get data from snowflake
# snowflake.connector.paramstyle = 'qmark'
streamlit.header("Fruityvice Fruit Advice!(Dropdown list values from snowflake)")
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select fruit_name from fruit_load_list")
my_data_rows=get_fruit_load_list()
my_data_rows.set_index(0)
fruits_selected = streamlit.multiselect("What fruit would you like to add?", list(my_data_rows))
streamlit.write("Thanks for adding ",fruits_selected)
my_cnx.close()




