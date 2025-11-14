# app.py
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
st.caption("CSV 파일을 앱 디렉토리에 포함해야 합니다.")
