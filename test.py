from geopy.geocoders import Nominatim

# 初始化 Nominatim 物件
geolocator = Nominatim(user_agent="geoapiExercises")


# 獲取地點名稱
location = "Taipei 101"

# 獲取地點的經緯度座標
location = geolocator.geocode(location)

# 獲取經緯度座標
latitude = location.latitude
longitude = location.longitude

# 輸入特定的經緯度座標
latitude = 25.0330
longitude = 121.5654

# 進行反向地理編碼，獲取地址資訊
location = geolocator.reverse((latitude, longitude))

# 獲取地址資訊
address = location.address
print("該位置位於：", address)
