import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. 데이터 로드 및 전처리 함수
@st.cache_data
def load_and_preprocess_data(file_content):
    """주어진 텍스트 파일 내용을 Pandas DataFrame으로 로드하고 전처리합니다."""
    # 데이터 로드 (메모리 내 파일 내용 사용)
    from io import StringIO
    df = pd.read_csv(StringIO(file_content), sep='\t', header=3)
    
    # 필요한 열 선택 및 이름 변경
    columns_map = {
        '동별(2)': '구',
        '소계': '총 화재 건수',
        '전기적요인': '전기적 요인',
        '기계적 요인': '기계적 요인',
        '가스누출(폭발)': '가스 누출(폭발)',
        '화학적 요인': '화학적 요인',
        '교통사고': '교통사고',
        '부주의': '부주의',
        '자연적인 요인': '자연적인 요인',
        '방화명확': '방화 명확',
        '방화의심': '방화 의심',
        '발화요인(기타)': '기타 요인',
        '발화요인(미상)': '미상 요인'
    }
    df = df.rename(columns=columns_map)
    
    # 구별 소계 데이터만 추출 ('소계' 행만 필터링)
    # 구별 소계는 동별(3) 값이 '소계'이고 구 이름이 '합계'가 아닌 행
    df_borough = df[
        (df['동별(3)'] == '소계') & 
        (df['구'] != '소계') & 
        (df['구'] != '종로구') # '종로구'는 첫 소계 다음에 나오므로, '합계' 구 데이터만 포함
    ]
    
    # '합계' 구 데이터가 이미 포함되어 있으므로 '합계' 행을 다시 필터링 (원본 데이터 구조에 따라 달라질 수 있음)
    df_borough = df_borough[df_borough['동별(1)'] == '합계']
    
    # 불필요한 열 제거 및 데이터 정리
    df_borough = df_borough[['구'] + list(columns_map.values())[1:]]
    
    # 데이터 타입 변환: '-'를 0으로 처리하고 정수형으로 변환
    for col in df_borough.columns[1:]:
        df_borough[col] = df_borough[col].replace('-', '0').astype(int)
        
    return df_borough

# 2. Streamlit 앱 구성
def app():
    st.set_page_config(layout="wide")
    st.title("🔥 서울시 2007년 구별 화재 발생 현황")
    st.caption("데이터 출처: seoul a.txt (2007년 동별 화재발생현황)")

    # 파일 내용 변수 (제공된 파일 내용)
    file_content = """
동별(1)	동별(2)	동별(3)	2007	2007	2007	2007	2007	2007	2007	2007	2007	2007	2007	2007
동별(1)	동별(2)	동별(3)	합계	합계	합계	합계	합계	합계	합계	합계	합계	합계	합계	합계
동별(1)	동별(2)	동별(3)	소계	전기적요인	기계적 요인	가스누출(폭발)	화학적 요인	교통사고	부주의	자연적인 요인	방화명확	방화의심	발화요인(기타)	발화요인(미상)
합계	소계	소계	6698	1682	291	32	18	47	3138	3	130	792	90	475
합계	종로구	소계	189	56	9	1	-	1	67	-	6	28	2	19
합계	중구	소계	280	63	20	-	1	1	128	-	22	17	1	27
합계	중구	소공동	11	3	-	-	-	-	8	-	-	-	-	-
... (중략: 전체 데이터가 여기에 포함되어야 함) ...
합계	송파구	소계	446	111	19	3	2	3	239	1	2	56	-	10
합계	강동구	소계	233	66	5	1	-	1	97	-	5	26	-	32
    """
    
    # 실제 파일 내용을 사용하기 위해 제공된 텍스트 전체를 `file_content` 변수에 붙여넣어 사용해야 합니다.
    # 여기서는 데이터의 일부만 포함하고 있습니다. 실제 사용 시에는 전문을 사용하세요.
    
    try:
        df_borough = load_and_preprocess_data(file_content)
    except Exception as e:
        st.error(f"데이터 로드 및 전처리 중 오류가 발생했습니다: {e}")
        st.info("원본 파일의 전체 내용을 코드 내 'file_content' 변수에 붙여넣어주세요.")
        return

    st.header("1. 구별 화재 발생 건수 순위")

    # 1. 총 화재 건수 순위
    df_sorted = df_borough.sort_values(by='총 화재 건수', ascending=False)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("총 화재 건수 Top 5")
        st.dataframe(df_sorted[['구', '총 화재 건수']].head(5).reset_index(drop=True), use_container_width=True)
        
        st.markdown(f"* **최다 발생 구:** **{df_sorted.iloc[0]['구']}** ({df_sorted.iloc[0]['총 화재 건수']}건)")
        st.markdown(f"* **최소 발생 구:** **{df_sorted.iloc[-1]['구']}** ({df_sorted.iloc[-1]['총 화재 건수']}건)")
    
    with col2:
        fig_total = px.bar(
            df_sorted,
            x='구',
            y='총 화재 건수',
            title='구별 총 화재 건수',
            color='총 화재 건수',
            color_continuous_scale=px.colors.sequential.Reds
        )
        st.plotly_chart(fig_total, use_container_width=True)

    st.header("2. 발화 요인별 분석")
    st.markdown("특정 발화 요인을 선택하여 구별 현황을 비교할 수 있습니다.")

    # 2. 발화 요인별 비교
    cause_columns = df_borough.columns[2:].tolist()
    selected_cause = st.selectbox("분석할 발화 요인을 선택하세요:", cause_columns)

    df_cause_sorted = df_borough.sort_values(by=selected_cause, ascending=False)
    
    col3, col4 = st.columns([1, 2])
    
    with col3:
        st.subheader(f"'{selected_cause}' 발생 순위 Top 5")
        st.dataframe(df_cause_sorted[['구', selected_cause]].head(5).reset_index(drop=True), use_container_width=True)
        
        # 전체 합계 계산 (데이터 파일에 '합계' 행이 포함되어 있어 이를 사용하거나 직접 계산)
        total_in_selected_cause = df_borough[selected_cause].sum()
        st.markdown(f"**서울시 전체 '{selected_cause}' 발생:** **{total_in_selected_cause}건**")
    
    with col4:
        fig_cause = px.bar(
            df_cause_sorted,
            x='구',
            y=selected_cause,
            title=f"구별 '{selected_cause}' 발생 현황",
            color=selected_cause,
            color_continuous_scale=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_cause, use_container_width=True)

    st.header("3. 구별 상세 데이터")
    st.dataframe(df_borough, use_container_width=True)

if __name__ == "__main__":
    # Streamlit 앱 실행
    # (주의: 실제 실행을 위해서는 'file_content' 변수에 파일의 전체 내용이 포함되어야 합니다.)
    app()
