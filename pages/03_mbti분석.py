# app.py
country = st.selectbox('국가 선택', countries, index=0)
st.write('선택된 국가:', country)
show_raw = st.checkbox('원시 데이터 보기 (전치 형태)', value=False)


with col2:
# 선택 국가의 행 가져오기
row = df[df['Country'] == country].squeeze()
# drop Country
mbti = row.drop(labels=['Country'])
# 정렬 (내림차순)
mbti_sorted = mbti.sort_values(ascending=False)


labels = mbti_sorted.index.tolist()
values = mbti_sorted.values.tolist()


colors = make_colors(values)


fig = go.Figure()
fig.add_trace(go.Bar(
x=labels,
y=values,
marker_color=colors,
text=[f"{v*100:.2f}%" for v in values],
textposition='auto',
hovertemplate='<b>%{x}</b><br>비율: %{y:.4f} (총의 %)<extra></extra>',
))


fig.update_layout(
title=f"{country} — MBTI 분포",
xaxis_title='MBTI Type',
yaxis_title='Proportion (0-1)',
yaxis=dict(tickformat='.2f'),
template='plotly_white',
margin=dict(l=40, r=20, t=60, b=40),
height=520
)


st.plotly_chart(fig, use_container_width=True)


# 상위 3개 요약
top3 = mbti_sorted.head(3)
st.markdown("**Top 3 MBTI**")
st.write(top3.to_frame(name='Proportion'))


if show_raw:
st.subheader('원시 데이터 (선택 국가, 전치)')
st.dataframe(mbti_sorted.to_frame(name='Proportion'))


st.markdown('---')
st.caption('Note: 이 앱은 `countriesMBTI_16types.csv` 파일을 로컬에서 로드합니다. Streamlit Cloud에 배포 시 해당 CSV 파일을 함께 업로드하세요.')
