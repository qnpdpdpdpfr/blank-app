import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# 페이지 기본 설정
# -----------------------------
st.set_page_config(page_title="탄산수 매출 현황 대시보드", page_icon="📊", layout="wide")

# -----------------------------
# 더미 데이터 생성
# -----------------------------
np.random.seed(42)
regions = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종"]
months = [f"{i}월" for i in range(1, 13)]

data = []
for region in regions:
    for i, month in enumerate(months, start=1):
        data.append({
            "지역": region,
            "월": month,
            "매출": np.random.randint(500, 2000),
            "고객 수": np.random.randint(100, 1000)
        })

df = pd.DataFrame(data)

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.header("⚙️ 필터 설정")
selected_region = st.sidebar.multiselect("지역 선택", regions, default=["서울"])
chart_type = st.sidebar.radio("차트 유형 선택", ["라인 차트", "막대 차트"])
show_table = st.sidebar.checkbox("데이터 표 보기", value=True)

# -----------------------------
# 데이터 필터링
# -----------------------------
filtered_df = df[df["지역"].isin(selected_region)]

# -----------------------------
# 메인 헤더
# -----------------------------
st.title("📊 전국 지역별 탄산수 매출 현황 대시보드")
st.markdown("### 2025년 기준 가상 데이터")

# -----------------------------
# 상단 KPI 카드
# -----------------------------
total_sales = int(filtered_df["매출"].sum())
avg_sales = int(filtered_df["매출"].mean())
total_customers = int(filtered_df["고객 수"].sum())

col1, col2, col3 = st.columns(3)
col1.metric("총 매출액", f"{total_sales:,} 원")
col2.metric("평균 매출액", f"{avg_sales:,} 원")
col3.metric("총 고객 수", f"{total_customers:,} 명")

st.markdown("---")

# -----------------------------
# 그래프 영역
# -----------------------------
st.subheader("📈 월별 매출 추이")

pivot_sales = filtered_df.pivot_table(index="월", columns="지역", values="매출", aggfunc="sum")

if chart_type == "라인 차트":
    st.line_chart(pivot_sales)
else:
    st.bar_chart(pivot_sales)

st.subheader("👥 월별 고객 수 추이")
pivot_customers = filtered_df.pivot_table(index="월", columns="지역", values="고객 수", aggfunc="sum")
st.line_chart(pivot_customers)

# -----------------------------
# 데이터 테이블
# -----------------------------
if show_table:
    st.markdown("### 📋 세부 데이터")
    st.dataframe(filtered_df.sort_values(by=["지역", "월"]))

# -----------------------------
# 푸터
# -----------------------------
st.markdown("---")
st.caption("© 2025 데이터 예시 | Streamlit으로 제작된 대시보드")
