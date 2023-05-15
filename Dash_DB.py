# 라이브러리 불러오기
import pandas as pd
import cx_Oracle
import os
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# DB Data 불러오기
os.environ['PATH'] = "C:/oraclexe/instantclient_21_10" + ";" + os.environ['PATH']

dsn = cx_Oracle.makedsn('localhost', 1521, 'xe') #makedsn(호스트이름, 포트, 서비스이름)
conn = cx_Oracle.connect('hr','hr', dsn)  #connect(사용자 이름, 비밀번호, dsn)
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT JOB_ID, SALARY\
               from (SELECT JOB_ID, SALARY FROM HR.EMPLOYEES)\
               group by JOB_ID, SALARY")
                
result = cursor.fetchall()
df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
# print(df)
groups = df['JOB_ID'].unique()

# Dash로 대시보드 만들기

# 앱 초기화
app = Dash(__name__)

# 레이아웃 정의
app.layout = html.Div(children = [
    html.H1(  # H1: 헤더와 같은 가장 큰 문자를 작성할 때 사용
        children = 'A회사 직원연봉',
        style = {'textAlign': 'center'}
    ),
    html.H4(  # H4: 숫자가 클수록 문자의 크기가 작아짐
        children = 'JOB_ID별 직원연봉',
    ),
    dcc.Dropdown(
        id = 'group',
        options = groups,
        value = groups[0]
    ),
    dcc.Graph(
        id = 'graph',
    ),
], style = {'width': '90%', 'margin': 'auto'})

# 콜백 정의
@app.callback(
    Output(component_id = 'graph', component_property = 'figure'),
    Input(component_id = 'group', component_property = 'value'),
)

def update_graph(group):
    
    # 사용자가 선택한 시군구가 포함된 데이터를 필터링
    selected_data = df.loc[df['JOB_ID'] == group]
    
    # boxplot 그래프 생성
    fig = px.scatter(selected_data, x = 'JOB_ID', y = 'SALARY')
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
