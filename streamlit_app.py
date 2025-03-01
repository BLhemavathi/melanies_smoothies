# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
    f"""Check the fruits you want in your custom Smoothie!
    """
)
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:",name_on_order)

cnx = st.connection("snowflake")
session  = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
#st.dataframe(data = my_dataframe , use_container_width= True)
ingredients_list = st.multiselect(
    'choose upto 5 ingredients:',
    my_dataframe    
)
if ingredients_list :
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_String = ''
    for fruit_chosen in ingredients_list:
        ingredients_String += fruit_chosen +' '

    #st.write(ingredients_String)
   
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_String + """')"""
    time_to_insert = st.button("Submit Orders")
    

    #st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered !', icon= "✅")
       
