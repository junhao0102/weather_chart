# 台北市天氣溫度可視化應用

這是一個使用Streamlit構建的台北市天氣溫度可視化應用。用戶可以查看未來三天的各種溫度種類曲線圖，以及特定區域的天氣情況。

## 功能

- 顯示未來三天各種溫度種類曲線圖
- 查詢特定台北市區域的溫度情況
- 展示台北市各區溫度概況

## 流程

1.  `requests` 從中央氣象局獲取天氣數據
2.  `matplotlib` 繪製溫度曲線圖
3.  `streamlit` 顯示應用界面和圖表


## 使用
安裝相依python套件  
```
pip install -r requirements.txt
```
啟動應用
```
streamlit run app.py
``` 


