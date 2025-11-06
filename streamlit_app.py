import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="탄산수 매출 대시보드", layout="wide")

st.title("🥤 탄산수 매출 대시보드")
st.markdown("### 전국 및 지역별 탄산수 매출 분석")

# 데이터 생성
np.random.seed(42)
regions = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"]
months = pd.date_range("2025-01-01", "2025-12-01", freq="MS").strftime("%Y-%m").tolist()

data = []
for region in regions:
    for month in months:
        data.append({
            "지역": region,
            "월": month,
            "매출액": np.random.randint(500, 5000)
        })
df = pd.DataFrame(data)

# 월별 전국 매출
monthly_sales = df.groupby("월")["매출액"].sum().reset_index()
fig1 = px.line(monthly_sales, x="월", y="매출액", title="전국 월별 매출 추이", markers=True)
st.plotly_chart(fig1, use_container_width=True)

# 지역별 매출
region_sales = df.groupby("지역")["매출액"].sum().reset_index()
fig2 = px.bar(region_sales, x="지역", y="매출액", title="지역별 총 매출", color="매출액", color_continuous_scale=px.colors.sequential.Rainbow)
st.plotly_chart(fig2, use_container_width=True)

# 지도
coords = {
    "서울": [37.5665, 126.9780], "부산": [35.1796, 129.0756], "대구": [35.8714, 128.6014],
    "인천": [37.4563, 126.7052], "광주": [35.1595, 126.8526], "대전": [36.3504, 127.3845],
    "울산": [35.5384, 129.3114], "경기": [37.4138, 127.5183], "강원": [37.8228, 128.1555],
    "충북": [36.8, 127.7], "충남": [36.5184, 126.8], "전북": [35.7175, 127.153], "전남": [34.816, 126.463],
    "경북": [36.4919, 128.8889], "경남": [35.4606, 128.2132], "제주": [33.4996, 126.5312]
}
map_df = pd.DataFrame([
    {"지역": r, "위도": coords[r][0], "경도": coords[r][1], "매출액": region_sales.loc[region_sales["지역"] == r, "매출액"].values[0]}
    for r in regions
])

fig3 = px.scatter_mapbox(
    map_df, lat="위도", lon="경도", size="매출액", color="매출액",
    color_continuous_scale=px.colors.sequential.Turbo,
    hover_name="지역", zoom=5, height=500
)
fig3.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig3, use_container_width=True)
