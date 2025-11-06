import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(page_title="탄산수 매출 대시보드", page_icon="🥤", layout="wide")

# -----------------------------
# 더미 데이터 생성
# -----------------------------
np.random.seed(42)
regions = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종"]
months = [f"{i}월" for i in range(1, 13)]

data = []
for region in regions:
    base = np.random.randint(500, 1500)
    for month in months:
        sales = base + np.random.randint(-200, 300)
        profit = int(sales * np.random.uniform(0.2, 0.35))
        customers = np.random.randint(80, 300)
        data.append({
            "지역": region,
            "월": month,
            "매출": max(sales, 0),
            "이익": profit,
            "고객 수": customers
        })

df = pd.DataFrame(data)

# -----------------------------
# 사이드바 설정
# -----------------------------
st.sidebar.header("⚙️ 필터 설정")
selected_regions = st.sidebar.multiselect("지역 선택", regions, default=["서울", "부산"])
chart_theme = st.sidebar.selectbox("차트 스타일", ["plotly", "streamlit 기본"])
show_table = st.sidebar.checkbox("데이터표 보기", True)

filtered_df = df[df["지역"].isin(selected_regions)]

# -----------------------------
# 메인 타이틀
# -----------------------------
st.title("🥤 탄산수 매출 대시보드")
st.markdown("##### 2025년 전국 탄산수 판매 데이터를 기반으로 한 예시 대시보드입니다.")

# -----------------------------
# KPI 카드
# -----------------------------
total_sales = int(filtered_df["매출"].sum())
avg_profit = int(filtered_df["이익"].mean())
total_customers = int(filtered_df["고객 수"].sum())

col1, col2, col3 = st.columns(3)
col1.metric("총 매출액", f"{total_sales:,} 원")
col2.metric("평균 이익", f"{avg_profit:,} 원")
col3.metric("총 고객 수", f"{total_customers:,} 명")

st.markdown("---")

# -----------------------------
# 시각화 1️⃣ : 월별 매출 추이
# -----------------------------
st.subheader("📈 월별 매출 추이")

if chart_theme == "plotly":
    fig1 = px.line(filtered_df, x="월", y="매출", color="지역", markers=True, title="월별 탄산수 매출 추이")
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.line_chart(filtered_df.pivot(index="월", columns="지역", values="매출"))

# -----------------------------
# 시각화 2️⃣ : 지역별 총 매출 비교 (막대그래프)
# -----------------------------
st.subheader("🏙️ 지역별 총 매출 비교")

region_sales = filtered_df.groupby("지역")["매출"].sum().reset_index()
if chart_theme == "plotly":
    fig2 = px.bar(region_sales, x="지역", y="매출", color="지역", title="지역별 총 매출")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.bar_chart(region_sales.set_index("지역"))

# -----------------------------
# 시각화 3️⃣ : 이익 비중 (파이차트)
# -----------------------------
st.subheader("💰 지역별 이익 비중")

region_profit = filtered_df.groupby("지역")["이익"].sum().reset_index()
fig3 = px.pie(region_profit, names="지역", values="이익", title="지역별 이익 비율")
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# 시각화 4️⃣ : 매출-이익 관계 (산점도)
# -----------------------------
st.subheader("📊 매출과 이익의 관계")

fig4 = px.scatter(filtered_df, x="매출", y="이익", color="지역", size="고객 수",
                  hover_data=["월"], title="매출 대비 이익 관계")
st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# 시각화 5️⃣ : 히트맵 (월별 매출 패턴)
# -----------------------------
st.subheader("🔥 월별·지역별 매출 히트맵")

heatmap_data = df.pivot_table(index="월", columns="지역", values="매출")
fig5 = px.imshow(heatmap_data, text_auto=True, color_continuous_scale="Blues",
                 title="월별·지역별 매출 히트맵")
st.plotly_chart(fig5, use_container_width=True)

# -----------------------------
# 데이터 표
# -----------------------------
if show_table:
    st.markdown("### 📋 상세 데이터")
    st.dataframe(filtered_df.sort_values(by=["지역", "월"]))

st.markdown("---")
st.caption("© 2025 탄산수 매출 분석 | Streamlit + Plotly Dashboard Example")
