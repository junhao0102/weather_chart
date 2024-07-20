import streamlit as st
from func import *



def main():
   
   col1, col2 = st.tabs(["搜尋區域", "台北市各區溫度情況搜尋區域"])
   weather_df = parse_weather_data()
   
   with col1:
      st.header("請輸入台北市區名稱")
      search_loc = st.text_input("",placeholder="信義區", max_chars=3)
      search_btn = st.button("搜尋") 
    
      if search_btn:
         if search_loc== "":
               st.warning("⚠️ 不能為空")
         elif search_loc not in weather_df["Location"].unique():
               st.warning("⚠️ 請輸入台北市區名稱")
         else:
               search_df = weather_df[weather_df["Location"] == search_loc]
               temperature_line_chart(search_df)

   with col2:
         temperature_line_chart(weather_df)


if __name__ == "__main__":
    main()
