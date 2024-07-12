import streamlit as st
from func import *


def main():
   weather_df = parse_weather_data()
   temperature_line_chart(weather_df)
   
   
if __name__ == "__main__":
    main()
