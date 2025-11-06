import streamlit as st
import pandas as pd
import numpy as np

# 페이지 설정
st.set_page_config(page_title="탄산수 매출 (No Plotly)", page_icon="🥤", layout="wide")

# 더미 데이터 생성
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

# 사이드바
st.sidebar.header("⚙️ 필터 설정")
selected_regions = st.sidebar.multiselect("지역 선택", regions, default=["서울", "부산"])
show_table = st.sidebar.checkbox("데이터표 보기", True)

filtered_df = df[df["지역"].isin(selected_regions)]

# 타이틀 + 설명
st.title("🥤 탄산수 매출 (간단모드)")
st.markdown("##### Plotly 미설치 환경을 위한 대체 버전 — Streamlit 내장 차트만 사용")

# KPI
total_sales = int(filtered_df["매출"].sum())
avg_profit = int(filtered_df["이익"].mean())
total_customers = int(filtered_df["고객 수"].sum())

c1, c2, c3 = st.columns(3)
c1.metric("총 매출액", f"{total_sales:,} 원")
c2.metric("평균 이익", f"{avg_profit:,} 원")
c3.metric("총 고객 수", f"{total_customers:,} 명")
st.markdown("---")

# 1) 월별 매출 추이 (라인)
st.subheader("📈 월별 탄산수 매출 추이")
pivot_sales = filtered_df.pivot_table(index="월", columns="지역", values="매출", aggfunc="sum").reindex(months)
st.line_chart(pivot_sales)

# 2) 지역별 총 매출 (막대)
st.subheader("🏙️ 지역별 탄산수 총 매출 비교")
region_sales = filtered_df.groupby("지역", as_index=False)["매출"].sum().sort_values("매출", ascending=False)
st.bar_chart(region_sales.set_index("지역"))

# 3) 이익 비중 (간단한 막대 비율로 표시 — 파이 대신)
st.subheader("💰 지역별 이익 비중 (막대 비율)")
region_profit = filtered_df.groupby("지역", as_index=False)["이익"].sum().sort_values("이익", ascending=False)
# 이익 비율 컬럼 추가
region_profit["비율(%)"] = (region_profit["이익"] / region_profit["이익"].sum() * 100).round(1)
st.dataframe(region_profit.set_index("지역"))

st.bar_chart(region_profit.set_index("지역")["이익"])

# 4) 매출-이익 관계 (간단 표 형태로 상관성 확인)
st.subheader("📊 매출-이익 요약 (지역별)")
scatter_like = filtered_df.groupby("지역").agg({"매출": "mean", "이익": "mean", "고객 수": "mean"}).round(0)
st.dataframe(scatter_like)

# 5) 히트맵 대신 색상 강조된 테이블(월별·지역별 매출)
st.subheader("🔥 월별·지역별 탄산수 매출 (테이블)")
heat = df.pivot_table(index="월", columns="지역", values="매출", aggfunc="sum").reindex(months)
# 숫자 포맷
st.dataframe(heat.style.format("{:,.0f}"))

# 데이터표 옵션
if show_table:
    st.markdown("### 📋 상세 데이터")
    st.dataframe(filtered_df.sort_values(by=["지역", "월"]).reset_index(drop=True))

st.markdown("---")
st.caption("© 2025 탄산수 매출 예시 (간단모드)")
