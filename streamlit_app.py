# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.font_manager as fm

# ✅ 한글 폰트 깨짐 방지
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우용
plt.rcParams['axes.unicode_minus'] = False

# ---------------------------
# 가상 탄산수 매출 데이터 생성
# ---------------------------
np.random.seed(42)
regions = ['서울', '부산', '대구', '인천', '광주', '대전', '울산']
months = pd.date_range('2025-01-01', periods=12, freq='M')

data = []
for region in regions:
    for month in months:
        sales = np.random.randint(500, 3000)
        profit = sales * np.random.uniform(0.1, 0.25)
        lat = 37 + np.random.uniform(-0.5, 0.5)
        lon = 127 + np.random.uniform(-0.5, 0.5)
        data.append([region, month, sales, profit, lat, lon])

df = pd.DataFrame(data, columns=['지역', '월', '매출액', '이익', '위도', '경도'])

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("🥤 탄산수 매출 대시보드")

# 지역 선택 필터
selected_region = st.selectbox("지역을 선택하세요", ["전체"] + regions)

if selected_region != "전체":
    filtered_df = df[df['지역'] == selected_region]
else:
    filtered_df = df

# ---------------------------
# 그래프 1: 월별 매출 추이
# ---------------------------
st.subheader("📈 월별 매출 추이")
line_fig = px.line(
    filtered_df,
    x="월",
    y="매출액",
    color="지역",
    markers=True,
    title="지역별 월별 매출 변화",
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(line_fig, use_container_width=True)

# ---------------------------
# 그래프 2: 지역별 평균 매출
# ---------------------------
st.subheader("🏙️ 지역별 평균 매출 비교")
avg_sales = df.groupby('지역')['매출액'].mean().reset_index()
bar_fig = px.bar(
    avg_sales,
    x='지역',
    y='매출액',
    color='지역',
    title='지역별 평균 매출액',
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(bar_fig, use_container_width=True)

# ---------------------------
# 그래프 3: 매출 vs 이익
# ---------------------------
st.subheader("💰 매출과 이익의 관계")
scatter_fig = px.scatter(
    filtered_df,
    x="매출액",
    y="이익",
    color="지역",
    size="이익",
    hover_name="지역",
    title="매출과 이익 관계",
    color_discrete_sequence=px.colors.qualitative.Bold
)
st.plotly_chart(scatter_fig, use_container_width=True)

# ---------------------------
# 지도: 지역별 매출 위치 표시
# ---------------------------
st.subheader("🗺️ 지역별 매출 지도")
map_df = filtered_df[['위도', '경도']]
st.map(map_df, zoom=6)

# ---------------------------
# 데이터 테이블
# ---------------------------
st.subheader("📊 상세 데이터")
st.dataframe(filtered_df[['지역', '월', '매출액', '이익']].sort_values('월'))
