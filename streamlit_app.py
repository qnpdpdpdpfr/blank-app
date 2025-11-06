import streamlit as st
import pandas as pd
import numpy as np

# 제목
st.title("📈 지역별 탄산수 매출 (임의 데이터)")

# 더미 데이터 생성
np.random.seed(42)
regions = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종"]
months = [f"{i}월" for i in range(1, 13)]
data = {region: np.random.randint(100, 1000, size=12) for region in regions}
df = pd.DataFrame(data, index=months)

# 사이드바 설정
st.sidebar.header("⚙️ 설정")
selected_region = st.sidebar.selectbox("지역 선택", regions)
chart_type = st.sidebar.radio("차트 종류 선택", ["라인 차트", "막대 차트"])

# 본문
st.subheader(f"📍 {selected_region}의 월별 탄산수 매출 현황")

if chart_type == "라인 차트":
    st.line_chart(df[selected_region])
else:
    st.bar_chart(df[selected_region])

# 지역별 평균 비교
st.subheader("📊 지역별 평균 탄산수 매출 비교")
st.bar_chart(df.mean())

# 통계 요약
st.subheader("📋 통계 요약")
summary = df.describe().T
st.dataframe(summary)
