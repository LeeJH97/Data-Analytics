# 라이브러리 불러오기
import pandas as pd
import cx_Oracle
import os

os.environ['PATH'] = "C:/oraclexe/instantclient_21_10" + ";" + os.environ['PATH']

dsn = cx_Oracle.makedsn('localhost', 1521, 'xe') #makedsn(호스트이름, 포트, 서비스이름)
conn = cx_Oracle.connect('hr','hr', dsn)  #connect(사용자 이름, 비밀번호, dsn)
cursor = conn.cursor()

cursor.execute("SELECT * FROM HR.EMPLOYEES")
result = cursor.fetchall()
df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
print(df)