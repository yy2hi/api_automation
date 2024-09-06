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

                # host os group id (test)
                sql_OS_GROUP_ID = "SELECT OS_GROUP_ID FROM HOST_OS_GROUP WHERE OS_GROUP_NAME='test';"
                result_sql_OS_GROUP_ID = curs.execute(sql_OS_GROUP_ID).fetchall()
                global result_OS_GROUP_ID
                result_OS_GROUP_ID = int(result_sql_OS_GROUP_ID[0][0])

                # HOST OS GROUP MEMBER 조인 테스트용 ID (server_101)
                sql_HOM_HOST_OS_ID = "SELECT OS_ID FROM HOST_OS WHERE HOSTNAME='server_101';"
                result_sql_HOM_HOST_OS_ID = curs.execute(sql_HOM_HOST_OS_ID).fetchall()
                global result_HOM_HOST_OS_ID
                result_HOM_HOST_OS_ID = int(result_sql_HOM_HOST_OS_ID[0][0])

                # 컴퓨트 노드 HOST_OS_ID (compute17)
                sql_COM_HOST_OS_ID = "SELECT OS_ID FROM HOST_OS WHERE HOSTNAME='compute17';"
                result_sql_COM_HOST_OS_ID = curs.execute(sql_COM_HOST_OS_ID).fetchall()
                global result_COM_HOST_OS_ID
                result_COM_HOST_OS_ID = int(result_sql_COM_HOST_OS_ID[0][0])

                # 네트워크 노드 HOST_OS_ID (master9)
                sql_NET_HOST_OS_ID = "SELECT OS_ID FROM HOST_OS WHERE HOSTNAME='master9';"
                result_sql_NET_HOST_OS_ID = curs.execute(sql_NET_HOST_OS_ID).fetchall()
                global result_NET_HOST_OS_ID
                result_NET_HOST_OS_ID = int(result_sql_NET_HOST_OS_ID[0][0])

                # BlkDevDomain ID
                sql_BlkDevDomain = "select ID from STORAGE_BLOCK_DEVICE_DOMAIN;"
                result_sql_BlkDevDomain = curs.execute(sql_BlkDevDomain).fetchall()
                global result_BlkDevDomain
                result_BlkDevDomain = int(result_sql_BlkDevDomain[0][0])

                # FSDomain_ID
                sql_FSDomain_ID = "select ID from STORAGE_FILESYSTEM_DOMAIN;"
                result_sql_FSDomain_ID = curs.execute(sql_FSDomain_ID).fetchall()
                global result_FSDomain_ID
                result_FSDomain_ID = int(result_sql_FSDomain_ID[0][0])

                # 연결 닫기
                conn.close()

        except Exception as ex:
            #print(f"An error occurred: {ex}")
            pass

