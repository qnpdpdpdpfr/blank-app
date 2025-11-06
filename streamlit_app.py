import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.font_manager as fm

# --------------------------
# 한글 폰트 설치 (Streamlit Cloud용)
# --------------------------
if not os.path.exists("/usr/share/fonts/truetype/nanum/NanumGothic.ttf"):
    os.system("apt-get update -qq")
    os.system("apt-get install -qq fonts-nanum")
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

# --------------------------
# 대시보드 기본 설정
# --------------------------
st.set_page_config(page_title="탄산수 매출 대시보드", layout="wide")
st.title("🥤 탄산수 매출 대시보드")
st.caption("전국 월별 매출 추이, 지역별 분석, 지도 시각화를 포함한 종합 대시보드")

# --------------------------
# 예시 데이터 생성
# --------------------------
np.random.seed(42)
regions = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "제주"]
months = [f"{m}월" for m in range(1, 13)]

data = []
for r in regions:
    sales = np.random.randint(800, 2500, size=12)
    profit = np.random.randint(100, 800, size=12)
    for i, m in enumerate(months):
        data.append([r, m, sales[i], profit[i]])

df = pd.DataFrame(data, columns=["지역", "월", "매출", "이익"])

# --------------------------
# 전국 월별 매출 분석
# --------------------------
st.header("📈 전국 월별 탄산수 매출 추이")

monthly_sales = df.groupby("월")["매출"].sum().reset_index()
fig, ax = plt.subplots()
ax.plot(monthly_sales["월"], monthly_sales["매출"], marker="o", color="#36A2EB", linewidth=2)
ax.fill_between(monthly_sales["월"], monthly_sales["매출"], color="#9BD0F5", alpha=0.3)
ax.set_title("전국 월별 매출 추이", fontsize=14)
ax.set_xlabel("월")
ax.set_ylabel("매출액 (단위: 천원)")
st.pyplot(fig)

# --------------------------
# 지역별 매출 비교
# --------------------------
st.header("🏙️ 지역별 매출 비교")

region_sales = df.groupby("지역")["매출"].sum().reset_index()
fig2, ax2 = plt.subplots()
bars = ax2.bar(region_sales["지역"], region_sales["매출"], color=plt.cm.rainbow(np.linspace(0, 1, len(region_sales))))
ax2.set_title("지역별 연간 매출", fontsize=14)
ax2.set_ylabel("매출액 (단위: 천원)")
st.pyplot(fig2)

# --------------------------
# 이익률 분석
# --------------------------
st.header("💰 지역별 이익률 (%)")

region_profit = df.groupby("지역")[["매출", "이익"]].sum().reset_index()
region_profit["이익률"] = (region_profit["이익"] / region_profit["매출"] * 100).round(2)
styled = region_profit.style.background_gradient(cmap="plasma")
st.dataframe(styled, use_container_width=True)

# --------------------------
# 지도 시각화
# --------------------------
st.header("🗺️ 주요 판매 지역 지도")

location_data = {
    "서울": [37.5665, 126.9780],
    "부산": [35.1796, 129.0756],
    "대구": [35.8714, 128.6014],
    "인천": [37.4563, 126.7052],
    "광주": [35.1595, 126.8526],
    "대전": [36.3504, 127.3845],
    "울산": [35.5384, 129.3114],
    "제주": [33.4996, 126.5312]
}

map_df = pd.DataFrame({
    "지역": list(location_data.keys()),
    "lat": [v[0] for v in location_data.values()],
    "lon": [v[1] for v in location_data.values()],
    "매출": region_sales["매출"]
})

st.map(map_df, zoom=6)

# --------------------------
# 전체 데이터 미리보기
# --------------------------
st.header("📊 원본 데이터 미리보기")
st.dataframe(df)
