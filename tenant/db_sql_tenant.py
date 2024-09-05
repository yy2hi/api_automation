import pyodbc
def result_tenant_sql():
        try:
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

                # USER_ID
                sql_USER_ID = "SELECT ID FROM USER_INFO WHERE LOGIN_ID='yjs'"
                result_sql_USER_ID = curs.execute(sql_USER_ID).fetchall()
                global result_USER_ID
                result_USER_ID = int(result_sql_USER_ID[0][0])
                #print("result_USER_ID", result_USER_ID)
                # sql_USER_ID = "SELECT ID FROM USER_INFO WHERE LOGIN_ID='yhi'"
                # result_sql_USER_ID = curs.execute(sql_USER_ID).fetchall()
                # if result_sql_USER_ID:
                #         global result_USER_ID
                #         result_USER_ID = int(result_sql_USER_ID[0][0])
                #         print("result_USER_ID:", result_USER_ID)
                # else:
                #         print("No result for USER_ID")
                
                # TENANT_ID
                sql_TENANT_ID = "SELECT TENANT_ID FROM TENANT WHERE OWNER_ID=%d;" %result_USER_ID
                # sql_TENANT_ID = "SELECT TENANT_ID FROM USERS WHERE USER_ID=2048;"
                result_sql_TENANT_ID = curs.execute(sql_TENANT_ID).fetchall()
                global result_TENANT_ID
                result_TENANT_ID = int(result_sql_TENANT_ID[0][0])
                # print("result_TENANT_ID", result_TENANT_ID)

                # # PROJECT_ID - 프로젝트 이름을 변경해주세요
                # sql_PROJECT_ID = "SELECT PROJECT_ID FROM PROJECT WHERE NAME='net_auto24';"
                # result_sql_PROJECT_ID = curs.execute(sql_PROJECT_ID).fetchall()
                # global result_PROJECT_ID
                # result_PROJECT_ID = int(result_sql_PROJECT_ID[0][0])

                # BlkDevDomain ID
                sql_BlkDevDomain = "select ID from STORAGE_BLOCK_DEVICE_DOMAIN;"
                result_sql_BlkDevDomain = curs.execute(sql_BlkDevDomain).fetchall()
                global result_BlkDevDomain
                result_BlkDevDomain = int(result_sql_BlkDevDomain[0][0])

                
                # 연결 닫기
                conn.close()

        except Exception as ex:
            print(f"An error occurred: {ex}")
            pass

#result_tenant_sql()

