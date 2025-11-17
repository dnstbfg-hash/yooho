# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from io import StringIO

st.set_page_config(page_title="지하철 TOP10 역 (승+하)", layout="wide")

@st.cache_data
def load_local_or_uploaded(path="/mnt/data/subway.csv"):
    # try common encodings for korean csv
    try:
        df = pd.read_csv(path, encoding="cp949")
        return df
    except Exception:
        try:
            df = pd.read_csv(path, encoding="utf-8")
            return df
        except Exception:
            return None

def load_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return None

    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception:
        try:
            uploaded_file.seek(0)
            text = uploaded_file.read().decode("cp949")
            df = pd.read_csv(StringIO(text))
            return df
        except Exception:
            uploaded_file.seek(0)
            text = uploaded_file.read().decode("utf-8", errors="replace")
            df = pd.read_csv(StringIO(text))
            return df

st.title("🗺️ 지하철 역 Top 10 (선택 날짜·호선) — Plotly Interactive")

# 데이터 로드 시도 (내장 파일 먼저)
df = load_local_or_uploaded()

if df is None:
    st.info("내장 데이터 파일 없음 → CSV 파일을 업로드해주세요. (예: subway.csv)")
    uploaded = st.file_uploader("CSV 파일 업로드", type=["csv"])
    if uploaded:
        df = load_uploaded_file(uploaded)
else:
    st.success("내장 데이터 파일을 불러왔습니다: `/mnt/data/subway.csv`")

if df is None:
    st.stop()

# 표준화: 필요한 컬럼 확인
expected_cols = ["사용일자", "호선명", "역명", "승차총승객수", "하차총승객수"]
missing = [c for c in expected_cols if c not in df.columns]
if missing:
    st.error(f"데이터에 필요한 컬럼이 없습니다: {missing}")
    st.write("현재 CSV 컬럼:", df.columns.tolist())
    st.stop()

# 사용일자 -> datetime 변환
try:
    df["사용일자"] = pd.to_datetime(df["사용일자"].astype(str), format="%Y%m%d")
except Exception:
    df["사용일자"] = pd.to_datetime(df["사용일자"], errors="coerce")

# 2025년 10월 날짜만 필터
available_oct_dates = sorted(
    df.loc[
        (df["사용일자"].dt.year == 2025) & (df["사용일자"].dt.month == 10),
        "사용일자"
    ].dt.date.unique()
)

if len(available_oct_dates) == 0:
    st.error("데이터에 2025년 10월 날짜가 없습니다.")
    st.stop()

col1, col2 = st.columns([1, 2])
with col1:
    sel_date = st.selectbox(
        "🔹 날짜 선택 (2025년 10월)",
        options=available_oct_dates,
        format_func=lambda d: d.strftime("%Y-%m-%d")
    )

with col2:
    lines = sorted(df["호선명"].astype(str).unique())
    sel_line = st.selectbox("🔹 호선 선택", options=lines)

# 필터링
filtered = df[
    (df["사용일자"].dt.date == sel_date) &
    (df["호선명"].astype(str) == sel_line)
].copy()

if filtered.empty:
    st.warning("선택한 날짜 + 호선에 데이터가 없습니다.")
    st.stop()

# 총 승객수 생성
filtered["총승객수"] = (
    filtered["승차총승객수"].fillna(0) +
    filtered["하차총승객수"].fillna(0)
)

# 역별 합계
grouped = (
    filtered.groupby("역명", as_index=False)["총승객수"]
    .sum()
    .sort_values("총승객수", ascending=False)
)

top10 = grouped.head(10).copy()
top10.reset_index(drop=True, inplace=True)

# 색상 생성 함수 (1등 빨강, 나머지 파랑 그라데이션)
def make_colors(n):
    colors = []
    if n >= 1:
        colors.append("rgba(230,0,0,1)")  # red
    base_rgb = (0, 102, 204)
    rest = n - 1
    for i in range(rest):
        alpha = 1.0 - (i * (0.75 / max(rest - 1, 1))) if rest > 1 else 0.6
        r, g, b = base_rgb
        colors.append(f"rgba({r},{g},{b},{alpha:.2f})")
    return colors

colors = make_colors(len(top10))

# Plotly 그래프
fig = px.bar(
    top10,
    x="총승객수",
    y="역명",
    orientation="h",
    text="총승객수",
    labels={"총승객수": "총 승·하차 승객수", "역명": "역명"},
    title=f"{sel_date.strftime('%Y-%m-%d')} — {sel_line} 호선 Top 10 역"
)

fig.update_yaxes(autorange="reversed")

fig.update_traces(
    marker_color=colors,
    textposition="outside",
    hovertemplate="%{y}<br>총승객수: %{x:,}"
)

fig.update_layout(
    margin=dict(l=160, r=40, t=80, b=40),
    xaxis_tickformat=",",
    height=550,
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🔎 Top 10 상세 데이터")
st.dataframe(top10.style.format({"총승객수": "{:,}"}), height=300)

st.markdown("---")
st.caption("개발자 노트: CSV 인코딩은 cp949가 기본이며, utf-8도 자동 처리됩니다.")
