import streamlit as st


def calculate_electricity_consumption(distance_year,consumption_100km,number_cars):
    consumption_year=((distance_year/100)*consumption_100km*number_cars)/1E9
    return consumption_year

