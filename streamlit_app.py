import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="🥤 탄산수 매출 대시보드", page_icon="🥤", layout="wide")

# -----------------------------
# 데이터 생성
# -----------------------------
np.random.seed(42)
regions = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종"]
months = [f"{i}월" for i in range(1, 13)]

rows = []
for region in regions:
    base = np.random.randint(700, 1500)
    for m_idx, month in enumerate(months, start=1):
        sales = base + np.random.randint(-300, 300) + int(80 * np.sin(m_idx))
        sales = max(sales, 0)
        profit = int(sales * np.random.uniform(0.2, 0.4))
        customers = np.random.randint(100, 400)
        rows.append({"지역": region, "월": month, "매출": sales, "이익": profit, "고객 수": customers})

df = pd.DataFrame(rows)

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.header("⚙️ 필터 설정")
selected_regions = st.sidebar.multiselect("지역 선택", options=regions, default=regions[:4])
show_table = st.sidebar.checkbox("데이터 표 보기", value=False)

# -----------------------------
# 헤더
# -----------------------------
st.title("🥤 탄산수 매출 대시보드")
st.markdown("### 지역별 매출 비교와 전국 월별 추이 분석")

# -----------------------------
# 필터 적용
# -----------------------------
filtered = df[df["지역"].isin(selected_regions)]

# -----------------------------
# KPI (요약 지표)
# -----------------------------
total_sales = int(filtered["매출"].sum())
avg_profit = int(filtered["이익"].mean())
total_customers = int(filtered["고객 수"].sum())

col1, col2, col3 = st.columns(3)
col1.metric("총 매출액", f"{total_sales:,} 원")
col2.metric("평균 이익", f"{avg_profit:,} 원")
col3.metric("총 고객 수", f"{total_customers:,} 명")

st.markdown("---")

# -----------------------------
# A. 지역별 월별 매출 추이
# -----------------------------
st.subheader("🏙️ 선택 지역의 월별 매출 추이")

fig1 = px.line(
    filtered,
    x="월",
    y="매출",
    color="지역",
    markers=True,
    title="지역별 월별 매출 (라인 그래프)",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig1.update_layout(height=400, template="simple_white")
st.plotly_chart(fig1, use_container_width=True)

# 막대 그래프 (월별 매출 평균)
region_month_avg = (
    filtered.groupby(["월", "지역"])["매출"].mean().reset_index()
)
fig2 = px.bar(
    region_month_avg,
    x="월",
    y="매출",
    color="지역",
    barmode="group",
    title="지역별 월별 평균 매출 (막대 그래프)",
    color_discrete_sequence=px.colors.qualitative.Bold
)
fig2.update_layout(height=400, template="plotly_white")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# -----------------------------
# B. 전국 월별 매출 분석
# -----------------------------
st.subheader("📅 전국 월별 매출 분석")

monthly_totals = (
    df.groupby("월")["매출"].sum().reindex(months).reset_index()
)
monthly_totals["전월 대비 증감률(%)"] = (
    monthly_totals["매출"].pct_change().fillna(0) * 100
).round(1)
monthly_totals["누적 매출"] = monthly_totals["매출"].cumsum()

# 라인 그래프: 전국 월별 매출
fig3 = px.line(
    monthly_totals,
    x="월",
    y="매출",
    title="전국 월별 총매출 (라인 그래프)",
    markers=True,
    color_discrete_sequence=["#1f77b4"]
)
st.plotly_chart(fig3, use_container_width=True)

# 증감률 막대 그래프
fig4 = px.bar(
    monthly_totals,
    x="월",
    y="전월 대비 증감률(%)",
    title="전월 대비 증감률 (%)",
    color="전월 대비 증감률(%)",
    color_continuous_scale="Bluered"
)
st.plotly_chart(fig4, use_container_width=True)

# 누적 매출 영역 그래프
fig5 = px.area(
    monthly_totals,
    x="월",
    y="누적 매출",
    title="연간 누적 매출 (면적 그래프)",
    color_discrete_sequence=["#66c2a5"]
)
st.plotly_chart(fig5, use_container_width=True)

# -----------------------------
# C. 히트맵 스타일 테이블
# -----------------------------
st.subheader("🔥 월별·지역별 매출 패턴 (히트맵)")

heat = df.pivot_table(index="월", columns="지역", values="매출", aggfunc="sum").reindex(months)
styled = heat.style.background_gradient(cmap="YlGnBu").format("{:,.0f}")
st.dataframe(styled)

# -----------------------------
# D. 데이터 표 (선택)
# -----------------------------
if show_table:
    st.markdown("### 📋 원본 데이터 보기")
    st.dataframe(filtered.sort_values(["지역", "월"]))

st.markdown("---")
st.caption("© 2025 탄산수 매출 대시보드 | Plotly & Streamlit")
