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
selected_regions = st.sidebar.multiselect("지역 선택", regions, default=["서울", "부산", "대구"])
show_table = st.sidebar.checkbox("데이터표 보기", True)

filtered_df = df[df["지역"].isin(selected_regions)]

# -----------------------------
# 메인 타이틀
# -----------------------------
st.title("🥤 탄산수 매출 대시보드")
st.markdown("##### 2025년 전국 탄산수 판매 데이터를 기반으로 한 시각화 대시보드")

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
# 1️⃣ 전국 월별 탄산수 매출 분석
# -----------------------------
st.subheader("📅 전국 월별 탄산수 매출 추이")

# 월별 총합 계산
monthly_sales = df.groupby("월")["매출"].sum().reset_index()

# 증감률 계산
monthly_sales["증감률(%)"] = monthly_sales["매출"].pct_change() * 100
monthly_sales["증감률(%)"] = monthly_sales["증감률(%)"].fillna(0).round(1)

# 라인 차트 (Plotly)
fig1 = px.line(
    monthly_sales,
    x="월",
    y="매출",
    markers=True,
    text="증감률(%)",
    title="전국 월별 총 매출 추이 (증감률 포함)",
)
fig1.update_traces(textposition="top center")
st.plotly_chart(fig1, use_container_width=True)

# 증감률 강조
st.markdown("#### 📊 월별 매출 증감률")
fig2 = px.bar(
    monthly_sales,
    x="월",
    y="증감률(%)",
    color="증감률(%)",
    color_continuous_scale="RdYlGn",
    title="전월 대비 매출 증감률",
)
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# 2️⃣ 선택 지역별 월별 매출 비교
# -----------------------------
st.subheader("🏙️ 선택 지역 월별 매출 비교")
region_sales = filtered_df.pivot_table(index="월", columns="지역", values="매출", aggfunc="sum").reset_index()
fig3 = px.line(region_sales, x="월", y=selected_regions, markers=True, title="선택 지역별 월별 매출 비교")
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# 3️⃣ 전국 매출 분포 (히트맵)
# -----------------------------
st.subheader("🔥 월별·지역별 매출 히트맵")
heat_data = df.pivot_table(index="월", columns="지역", values="매출", aggfunc="sum")
fig4 = px.imshow(
    heat_data,
    text_auto=True,
    color_continuous_scale="Blues",
    title="월별·지역별 매출 분포 (단위: 원)"
)
st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# 데이터 표 보기
# -----------------------------
if show_table:
    st.markdown("### 📋 상세 데이터")
    st.dataframe(filtered_df.sort_values(by=["지역", "월"]).reset_index(drop=True))

# -----------------------------
# 푸터
# -----------------------------
st.markdown("---")
st.caption("© 2025 탄산수 매출 분석 | Streamlit + Plotly Dashboard Example")
