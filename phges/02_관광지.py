import streamlit as st
import folium
from streamlit_folium import st_folium

# -------------------------------
# 서울 관광지 Top 10 데이터
# -------------------------------
places = [
    {"name": "경복궁", "lat": 37.579617, "lon": 126.977041,
     "desc": "조선 왕조의 정궁으로 한국의 대표적인 궁궐입니다.",
     "station": "경복궁역 (3호선)"},
    {"name": "남산서울타워", "lat": 37.551169, "lon": 126.988227,
     "desc": "서울 전경을 한눈에 볼 수 있는 대표 전망대입니다.",
     "station": "명동역 (4호선)"},
    {"name": "명동", "lat": 37.563600, "lon": 126.982050,
     "desc": "쇼핑과 먹거리가 가득한 서울의 대표 번화가입니다.",
     "station": "명동역 (4호선)"},
    {"name": "북촌한옥마을", "lat": 37.582604, "lon": 126.983998,
     "desc": "전통 한옥이 잘 보존된 아름다운 마을입니다.",
     "station": "안국역 (3호선)"},
    {"name": "청계천", "lat": 37.569308, "lon": 126.978987,
     "desc": "서울 도심 속 휴식 공간으로 산책 명소입니다.",
     "station": "종각역 (1호선)"},
    {"name": "홍대", "lat": 37.556209, "lon": 126.922829,
     "desc": "젊음과 예술, 자유로운 분위기로 가득한 거리입니다.",
     "station": "홍대입구역 (2호선, 경의중앙선)"},
    {"name": "이태원", "lat": 37.534505, "lon": 126.994634,
     "desc": "다국적 문화가 공존하는 국제적인 거리입니다.",
     "station": "이태원역 (6호선)"},
    {"name": "동대문디자인플라자(DDP)", "lat": 37.566482, "lon": 127.009177,
     "desc": "현대적인 건축물로 패션과 전시의 중심지입니다.",
     "station": "동대문역사문화공원역 (2·4·5호선)"},
    {"name": "서울숲", "lat": 37.544578, "lon": 127.037842,
     "desc": "자연과 도시가 어우러진 대형 공원입니다.",
     "station": "서울숲역 (수인분당선)"},
    {"name": "롯데월드", "lat": 37.511034, "lon": 127.098131,
     "desc": "실내외 놀이시설과 쇼핑몰이 결합된 테마파크입니다.",
     "station": "잠실역 (2호선, 8호선)"}
]

# -------------------------------
# Streamlit 기본 설정
# -------------------------------
st.set_page_config(page_title="서울 관광지 지도", page_icon="🗺️", layout="centered")

st.title("🗺️ 외국인들이 좋아하는 서울의 관광지 Top 10")
st.markdown("""
서울을 찾는 외국인 관광객들이 가장 많이 찾는 명소 TOP 10을  
지도 위에 표시했습니다. 마커를 클릭하면 장소와 가까운 지하철역 정보를 볼 수 있습니다.
""")

# -------------------------------
# Folium 지도 생성 (컬러풀하게)
# -------------------------------
seoul_map = folium.Map(location=[37.5665, 126.9780],
                       zoom_start=12,
                       tiles="OpenStreetMap")

# 관광지 마커 추가 (노란색)
for place in places:
    popup_html = f"""
    <b>{place['name']}</b><br>
    {place['desc']}<br>
    🚇 <b>{place['station']}</b>
    """
    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=popup_html,
        tooltip=place["name"],
        icon=folium.Icon(color="beige", icon_color="yellow", icon="star")
    ).add_to(seoul_map)

# -------------------------------
# Streamlit에 지도 표시 (80% 크기)
# -------------------------------
st_data = st_folium(seoul_map, width=640, height=480)

# -------------------------------
# 관광지 간단 소개
# -------------------------------
st.subheader("📍 관광지 & 지하철역 소개")

for idx, place in enumerate(places, start=1):
    st.markdown(
        f"**{idx}. {place['name']}** — {place['desc']}  \n"
        f"🚇 **가까운 지하철역:** {place['station']}"
    )
