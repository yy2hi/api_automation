import pyodbc

def conn_db():
       # 데이터베이스 설정
        user = 'superiaas'
        passwd = 'superiaas'
        dsn = 'tibero7'

        # 데이터베이스 연결
        conn = pyodbc.connect(f'DSN={dsn};UID={user};PWD={passwd}')
        conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        conn.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-32le')
        conn.setencoding(encoding='utf-8')

        # 커서 생성
        curs = conn.cursor()

        return conn, curs

def result_sql_admin():
        try:
                conn, curs = conn_db()

                # admin 계정 추출 쿼리 실행 후 ADMIN_ID 저장
                sql_ADMIN_ID = "SELECT ID FROM USER_INFO WHERE LOGIN_ID='admin';"
                result_sql_ADMIN_ID = curs.execute(sql_ADMIN_ID).fetchall()
                global result_ADMIN_ID
                result_ADMIN_ID = int(result_sql_ADMIN_ID[0][0])


                # 사용할 host os id 추출 (compute17)
                sql_HOST_OS_ID = "SELECT OS_ID FROM HOST_OS WHERE HOSTNAME='compute17';"
                result_sql_HOST_OS_ID = curs.execute(sql_HOST_OS_ID).fetchall()
                global result_HOST_OS_ID
                result_HOST_OS_ID = int(result_sql_HOST_OS_ID[0][0])


                # 연결 닫기
                conn.close()

        except Exception as ex:
            #print(f"An error occurred: {ex}")
            pass

