import requests
import json
import pandas as pd
import streamlit as st
import plotly.express as px



# ----讀取config.json檔案----
def read_config():
    with open("config.json", "r") as f:
        config = json.load(f)
    url = config["url"]
    params = {}
    params["Authorization"] = config["Authorization"]
    return url, params


# ----取得氣象資料----
def get_weather_data():
    url, params = read_config()
    # 使用 requests 模塊發送 GET 請求
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return extract_weather_data(data)
    except requests.exceptions.HTTPError as e:
        return str(e)


# ----提取氣象資料----
def extract_weather_data(data):
    weather_datas = []
    for i in data["records"]["locations"][0]["location"]:
        for weatherElement in i["weatherElement"]:
            weather_data = {}
            weather_data["locationName"] = i["locationName"]
            weather_data["weatherElement"] = weatherElement
            weather_datas.append(weather_data)
    return weather_datas


#  ----將weather_datas轉為dataframe----
def parse_weather_data():
    data = get_weather_data()
    records = []
    
    for location in data:
        for i in range(len(location["weatherElement"]["time"])):
            record = {
                "Location": location["locationName"],
                "Description": location["weatherElement"]["description"],
                "Start_time": location["weatherElement"]["time"][i]["startTime"],
                "End_time": location["weatherElement"]["time"][i]["endTime"],
                "ElementValue": location["weatherElement"]["time"][i]["elementValue"][0]["value"],
            }

            # 將數據添加到 records 列表中
            records.append(record)
            weather_df = pd.DataFrame(records)

    return weather_df

# ----製作溫度折線圖----
def temperature_line_chart(weather_df):
    # 獲取所有地點
    locations = weather_df["Location"].unique()
    for location in locations:

        # 篩選出不同溫度描述的數據
        tem_avg = weather_df[(weather_df["Description"] == "平均溫度")& (weather_df["Location"] == location)]
        tem_min = weather_df[(weather_df["Description"] == "最低溫度")& (weather_df["Location"] == location)]
        tem_max = weather_df[(weather_df["Description"] == "最高溫度")& (weather_df["Location"] == location)]
        tem_max_feel = weather_df[(weather_df["Description"] == "最高體感溫度")& (weather_df["Location"] == location)]
        tem_min_feel = weather_df[(weather_df["Description"] == "最低體感溫度")& (weather_df["Location"] == location)]

        # 設置日期索引
        tem_avg = tem_avg.set_index("Start_time")
        tem_min = tem_min.set_index("Start_time")
        tem_max = tem_max.set_index("Start_time")
        tem_max_feel = tem_max_feel.set_index("Start_time")
        tem_min_feel = tem_min_feel.set_index("Start_time")

        # 確保數據中沒有重複的時間點
        tem_avg = tem_avg[~tem_avg.index.duplicated(keep="first")]
        tem_min = tem_min[~tem_min.index.duplicated(keep="first")]
        tem_max = tem_max[~tem_max.index.duplicated(keep="first")]
        tem_max_feel = tem_max_feel[~tem_max_feel.index.duplicated(keep="first")]
        tem_min_feel = tem_min_feel[~tem_min_feel.index.duplicated(keep="first")]
        
        # 將數據合併到一個 DataFrame 中
        temperature_df = pd.DataFrame(
            {
                "Start_time": tem_avg.index,
                "Maximum Temperature": tem_max["ElementValue"].values,
                "Minimum Temperature": tem_min["ElementValue"].values,
                "Average Temperature": tem_avg["ElementValue"].values,
                "Maximum Feel Temperature": tem_max_feel["ElementValue"].values,
                "Minimum Feel Temperature": tem_min_feel["ElementValue"].values,
            }
        )

        # 檢查數據中是否有缺失值，並將其移除
        temperature_df.dropna(inplace=True)
        
        # 使用 Plotly Express 繪製折線圖
        fig = px.line(
            temperature_df,
            x="Start_time",
            y=["Maximum Feel Temperature","Maximum Temperature","Minimum Feel Temperature", "Average Temperature", "Minimum Temperature"]
            )
        # 設置圖表樣式
        fig.update_layout(
            title={
                "text": f"{location}🌡️",
                "x": 0.5,
                "y": 0.95,
                "xanchor": "center",
                "yanchor": "top",
            },
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
        )
        
        # 在 Streamlit 上顯示圖表
        st.plotly_chart(fig)


    