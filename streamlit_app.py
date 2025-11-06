import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(page_title="🥤 탄산수 매출 대시보드", page_icon="🥤", layout="wide")

# -----------------------------
# 더미 데이터 생성 (지역별·월별)
# -----------------------------
np.random.seed(42)
regions = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종"]
months = [f"{i}월" for i in range(1, 13)]

rows = []
for region in regions:
    base = np.random.randint(600, 1400)
    for m_idx, month in enumerate(months, start=1):
        sales = base + np.random.randint(-250, 350) + int(100 * np.sin(m_idx))  # 약간 계절성 느낌
        sales = max(sales, 0)
        profit = int(sales * np.random.uniform(0.18, 0.36))
        customers = np.random.randint(60, 350)
        rows.append({"지역": region, "월": month, "매출": sales, "이익": profit, "고객 수": customers})

df = pd.DataFrame(rows)

# 월 순서 보장
month_order = months

# -----------------------------
# 사이드바 (필터)
# -----------------------------
st.sidebar.header("⚙️ 필터")
selected_regions = st.sidebar.multiselect("지역 선택 (여러개 선택 가능)", options=regions, default=regions[:3])
show_table = st.sidebar.checkbox("데이터표 보기", value=True)
chart_variant = st.sidebar.selectbox("그래프 스타일 선택", ["라인/막대/영역 혼합", "간단 라인 차트"])

# -----------------------------
# 헤더 / 설명
# -----------------------------
st.title("🥤 탄산수 매출 대시보드")
st.markdown("지역별 매출과 전국 단위의 월별 매출(총합/증감률 등)을 함께 보여주는 예시 대시보드입니다.")

# -----------------------------
# 필터 적용 데이터
# -----------------------------
filtered = df[df["지역"].isin(selected_regions)].copy()

# -----------------------------
# 상단 KPI
# -----------------------------
total_sales = int(filtered["매출"].sum())
avg_profit = int(filtered["이익"].mean())
total_customers = int(filtered["고객 수"].sum())

k1, k2, k3 = st.columns(3)
k1.metric("총 매출액 (선택한 지역)", f"{total_sales:,} 원")
k2.metric("평균 이익 (선택한 지역)", f"{avg_profit:,} 원")
k3.metric("총 고객 수 (선택한 지역)", f"{total_customers:,} 명")

st.markdown("---")

# -----------------------------
# A. 지역별 월별 매출 (다양한 시각화)
# -----------------------------
st.subheader("🏙️ 선택 지역의 월별 매출 (지역별 비교)")

pivot_region = filtered.pivot_table(index="월", columns="지역", values="매출", aggfunc="sum").reindex(month_order)

colA, colB = st.columns([2,1])

with colA:
    st.markdown("**1) 라인 차트 — 지역별 월별 추이**")
    if chart_variant == "간단 라인 차트":
        st.line_chart(pivot_region)
    else:
        st.line_chart(pivot_region)  # Streamlit 내장 라인 차트 (여러 지역 겹침)

    st.markdown("**2) 막대 차트 — 동일 데이터(월별 합)를 지역별로 비교**")
    # 월별 합을 한 번에 보여주기: 선택된 지역들의 총합을 막대그래프로
    month_total_selected = pivot_region.sum(axis=1)
    st.bar_chart(month_total_selected)

with colB:
    st.markdown("**3) 지역별 요약 테이블**")
    region_summary = filtered.groupby("지역").agg({
        "매출": ["sum", "mean"],
        "이익": "sum",
        "고객 수": "sum"
    })
    # 컬럼 평탄화
    region_summary.columns = ["_".join(col).strip() for col in region_summary.columns.values]
    st.dataframe(region_summary.sort_values("매출_sum", ascending=False).round(0))

st.markdown("---")

# -----------------------------
# B. 전국 월별 매출 분석 (요청하신 내용)
# -----------------------------
st.subheader("📅 전국 월별 매출 분석 (전국 단위)")

# 전국 월별 총합 (항상 전체 df 기준)
monthly_totals = df.groupby("월")["매출"].sum().reindex(month_order).reset_index()
monthly_totals.rename(columns={"매출": "전국_매출"}, inplace=True)

# 전월 대비 증감률(%) 계산
monthly_totals["증감률(%)"] = monthly_totals["전국_매출"].pct_change().fillna(0) * 100
monthly_totals["증감률(%)"] = monthly_totals["증감률(%)"].round(1)

# 누적매출
monthly_totals["누적매출"] = monthly_totals["전국_매출"].cumsum()

mcol1, mcol2 = st.columns(2)
with mcol1:
    st.markdown("**1) 전국 월별 총매출 (라인)**")
    st.line_chart(monthly_totals.set_index("월")["전국_매출"])

with mcol2:
    st.markdown("**2) 전월 대비 증감률(%)**")
    st.bar_chart(monthly_totals.set_index("월")["증감률(%)"])

st.markdown("**3) 누적 매출(연간 누적)**")
st.area_chart(monthly_totals.set_index("월")["누적매출"])

st.markdown("**월별 매출 요약 표**")
st.dataframe(monthly_totals.style.format({"전국_매출": "{:,.0f}", "증감률(%)":"{:.1f}", "누적매출":"{:,.0f}"}))

st.markdown("---")

# -----------------------------
# C. 히트맵(테이블 색상 강조) — 월별·지역별 패턴
# -----------------------------
st.subheader("🔥 월별·지역별 매출 패턴 (색상 강조 테이블)")

heat = df.pivot_table(index="월", columns="지역", values="매출", aggfunc="sum").reindex(month_order)
# pandas Styler를 사용해 색상 그라데이션을 줌 (Streamlit에서 렌더링 가능)
styled = heat.style.background_gradient(axis=None, cmap="Blues").format("{:,.0f}")
st.dataframe(styled)

st.markdown("---")

# -----------------------------
# D. 간단한 상관/추세 요약
# -----------------------------
st.subheader("🔎 간단 인사이트")
# 월별 최고/최저
best_month = monthly_totals.loc[monthly_totals["전국_매출"].idxmax(), "월"]
worst_month = monthly_totals.loc[monthly_totals["전국_매출"].idxmin(), "월"]
st.write(f"- 연중 **매출 최고 월**: {best_month}")
st.write(f"- 연중 **매출 최저 월**: {worst_month}")
st.write(f"- {best_month}의 전국 매출: {int(monthly_totals['전국_매출'].max()):,} 원")

# -----------------------------
# E. 원하면 보여줄 추가 자료
# -----------------------------
if show_table:
    st.markdown("### 📋 원본 데이터 샘플 (정렬됨)")
    st.dataframe(df.sort_values(["지역", "월"]).reset_index(drop=True))

st.markdown("---")
st.caption("© 2025 탄산수 매출 대시보드 (간단모드) — 외부 시각화 라이브러리 불필요")
import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(page_title="🥤 탄산수 매출 대시보드", page_icon="🥤", layout="wide")

# -----------------------------
# 더미 데이터 생성 (지역별·월별)
# -----------------------------
np.random.seed(42)
regions = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종"]
months = [f"{i}월" for i in range(1, 13)]

rows = []
for region in regions:
    base = np.random.randint(600, 1400)
    for m_idx, month in enumerate(months, start=1):
        sales = base + np.random.randint(-250, 350) + int(100 * np.sin(m_idx))  # 약간 계절성 느낌
        sales = max(sales, 0)
        profit = int(sales * np.random.uniform(0.18, 0.36))
        customers = np.random.randint(60, 350)
        rows.append({"지역": region, "월": month, "매출": sales, "이익": profit, "고객 수": customers})

df = pd.DataFrame(rows)

# 월 순서 보장
month_order = months

# -----------------------------
# 사이드바 (필터)
# -----------------------------
st.sidebar.header("⚙️ 필터")
selected_regions = st.sidebar.multiselect("지역 선택 (여러개 선택 가능)", options=regions, default=regions[:3])
show_table = st.sidebar.checkbox("데이터표 보기", value=True)
chart_variant = st.sidebar.selectbox("그래프 스타일 선택", ["라인/막대/영역 혼합", "간단 라인 차트"])

# -----------------------------
# 헤더 / 설명
# -----------------------------
st.title("🥤 탄산수 매출 대시보드")
st.markdown("지역별 매출과 전국 단위의 월별 매출(총합/증감률 등)을 함께 보여주는 예시 대시보드입니다.")

# -----------------------------
# 필터 적용 데이터
# -----------------------------
filtered = df[df["지역"].isin(selected_regions)].copy()

# -----------------------------
# 상단 KPI
# -----------------------------
total_sales = int(filtered["매출"].sum())
avg_profit = int(filtered["이익"].mean())
total_customers = int(filtered["고객 수"].sum())

k1, k2, k3 = st.columns(3)
k1.metric("총 매출액 (선택한 지역)", f"{total_sales:,} 원")
k2.metric("평균 이익 (선택한 지역)", f"{avg_profit:,} 원")
k3.metric("총 고객 수 (선택한 지역)", f"{total_customers:,} 명")

st.markdown("---")

# -----------------------------
# A. 지역별 월별 매출 (다양한 시각화)
# -----------------------------
st.subheader("🏙️ 선택 지역의 월별 매출 (지역별 비교)")

pivot_region = filtered.pivot_table(index="월", columns="지역", values="매출", aggfunc="sum").reindex(month_order)

colA, colB = st.columns([2,1])

with colA:
    st.markdown("**1) 라인 차트 — 지역별 월별 추이**")
    if chart_variant == "간단 라인 차트":
        st.line_chart(pivot_region)
    else:
        st.line_chart(pivot_region)  # Streamlit 내장 라인 차트 (여러 지역 겹침)

    st.markdown("**2) 막대 차트 — 동일 데이터(월별 합)를 지역별로 비교**")
    # 월별 합을 한 번에 보여주기: 선택된 지역들의 총합을 막대그래프로
    month_total_selected = pivot_region.sum(axis=1)
    st.bar_chart(month_total_selected)

with colB:
    st.markdown("**3) 지역별 요약 테이블**")
    region_summary = filtered.groupby("지역").agg({
        "매출": ["sum", "mean"],
        "이익": "sum",
        "고객 수": "sum"
    })
    # 컬럼 평탄화
    region_summary.columns = ["_".join(col).strip() for col in region_summary.columns.values]
    st.dataframe(region_summary.sort_values("매출_sum", ascending=False).round(0))

st.markdown("---")

# -----------------------------
# B. 전국 월별 매출 분석 (요청하신 내용)
# -----------------------------
st.subheader("📅 전국 월별 매출 분석 (전국 단위)")

# 전국 월별 총합 (항상 전체 df 기준)
monthly_totals = df.groupby("월")["매출"].sum().reindex(month_order).reset_index()
monthly_totals.rename(columns={"매출": "전국_매출"}, inplace=True)

# 전월 대비 증감률(%) 계산
monthly_totals["증감률(%)"] = monthly_totals["전국_매출"].pct_change().fillna(0) * 100
monthly_totals["증감률(%)"] = monthly_totals["증감률(%)"].round(1)

# 누적매출
monthly_totals["누적매출"] = monthly_totals["전국_매출"].cumsum()

mcol1, mcol2 = st.columns(2)
with mcol1:
    st.markdown("**1) 전국 월별 총매출 (라인)**")
    st.line_chart(monthly_totals.set_index("월")["전국_매출"])

with mcol2:
    st.markdown("**2) 전월 대비 증감률(%)**")
    st.bar_chart(monthly_totals.set_index("월")["증감률(%)"])

st.markdown("**3) 누적 매출(연간 누적)**")
st.area_chart(monthly_totals.set_index("월")["누적매출"])

st.markdown("**월별 매출 요약 표**")
st.dataframe(monthly_totals.style.format({"전국_매출": "{:,.0f}", "증감률(%)":"{:.1f}", "누적매출":"{:,.0f}"}))

st.markdown("---")

# -----------------------------
# C. 히트맵(테이블 색상 강조) — 월별·지역별 패턴
# -----------------------------
st.subheader("🔥 월별·지역별 매출 패턴 (색상 강조 테이블)")

heat = df.pivot_table(index="월", columns="지역", values="매출", aggfunc="sum").reindex(month_order)
# pandas Styler를 사용해 색상 그라데이션을 줌 (Streamlit에서 렌더링 가능)
styled = heat.style.background_gradient(axis=None, cmap="Blues").format("{:,.0f}")
st.dataframe(styled)

st.markdown("---")

# -----------------------------
# D. 간단한 상관/추세 요약
# -----------------------------
st.subheader("🔎 간단 인사이트")
# 월별 최고/최저
best_month = monthly_totals.loc[monthly_totals["전국_매출"].idxmax(), "월"]
worst_month = monthly_totals.loc[monthly_totals["전국_매출"].idxmin(), "월"]
st.write(f"- 연중 **매출 최고 월**: {best_month}")
st.write(f"- 연중 **매출 최저 월**: {worst_month}")
st.write(f"- {best_month}의 전국 매출: {int(monthly_totals['전국_매출'].max()):,} 원")

# -----------------------------
# E. 원하면 보여줄 추가 자료
# -----------------------------
if show_table:
    st.markdown("### 📋 원본 데이터 샘플 (정렬됨)")
    st.dataframe(df.sort_values(["지역", "월"]).reset_index(drop=True))

st.markdown("---")
st.caption("© 2025 탄산수 매출 대시보드 (간단모드) — 외부 시각화 라이브러리 불필요")
