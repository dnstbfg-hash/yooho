
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import List, Tuple

st.set_page_config(page_title="Country MBTI Viewer", layout="wide")

@st.cache_data
def load_data(path: str = "countriesMBTI_16types.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def interp_rgb(c1: Tuple[int, int, int], c2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    return '#%02x%02x%02x' % rgb


def make_colors(values: List[float]) -> List[str]:
    n = len(values)
    if n == 0:
        return []

    sorted_idx = np.argsort(values)[::-1]
    colors = [None] * n

    red_hex = '#ff4136'
    top_idx = sorted_idx[0]
    colors[top_idx] = red_hex

    dark_blue = (0, 102, 204)
    light_blue = (206, 232, 255)

    others = sorted_idx[1:]
    m = len(others)

    if m > 0:
        for pos, idx in enumerate(others):
            t = pos / max(1, m - 1)
            rgb = interp_rgb(dark_blue, light_blue, t)
            colors[idx] = rgb_to_hex(rgb)

    for i, c in enumerate(colors):
        if c is None:
            colors[i] = '#0066cc'

    return colors


st.title("🌍 Country MBTI Proportions — Interactive Explorer")
st.markdown("선택한 국가의 MBTI 16종 분포를 인터랙티브하게 보여줍니다.")

with st.spinner("데이터 로딩 중..."):
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("데이터 파일이 없습니다. 'countriesMBTI_16types.csv'를 업로드하세요.")
        st.stop()

countries = df['Country'].tolist()

col1, col2 = st.columns([1, 3])

with col1:
    country = st.selectbox("국가 선택", countries, index=0)
    show_raw = st.checkbox("원시 데이터 보기", value=False)

with col2:
    row = df[df['Country'] == country].squeeze()
    mbti = row.drop(labels=['Country'])
    mbti_sorted = mbti.sort_values(ascending=False)

    labels = mbti_sorted.index.tolist()
    values = mbti_sorted.values.tolist()
    colors = make_colors(values)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=labels,
            y=values,
            marker_color=colors,
            text=[f"{v * 100:.2f}%" for v in values],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>비율: %{y:.4f}<extra></extra>',
        )
    )

    fig.update_layout(
        title=f"{country} — MBTI 분포",
        xaxis_title="MBTI Type",
        yaxis_title="Proportion (0-1)",
        template="plotly_white",
        margin=dict(l=40, r=20, t=60, b=40),
        height=520,
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Top 3 MBTI**")
    st.write(mbti_sorted.head(3).to_frame(name='Proportion'))

if show_raw:
    st.subheader("선택 국가 원시 데이터 (전치)")
    st.dataframe(mbti_sorted.to_frame(name='Proportion'))

st.markdown('---')
st.caption("CSV 파일을 앱 디렉토리에 포함해야 합니다.")
