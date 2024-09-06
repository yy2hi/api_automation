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

def result_tenant_sql():
        try:
                conn, curs = conn_db()

                # USER_ID
                sql_USER_ID = "SELECT ID FROM USER_INFO WHERE LOGIN_ID='yhi'"
                result_sql_USER_ID = curs.execute(sql_USER_ID).fetchall()
                global result_USER_ID
                result_USER_ID = int(result_sql_USER_ID[0][0])
                
                # STORAGE IMAGE_ID (어드민 이미지 ID)
                sql_IMAGE_ID = "SELECT PROJECT_ID FROM PROJECT WHERE NAME='projectJSON';"
                result_sql_IMAGE_ID = curs.execute(sql_PROJECT_ID).fetchall()
                global result_IMAGE_ID
                result_IMAGE_ID = int(result_sql_IMAGE_ID[0][0])
                # print("result_IMAGE_ID",result_IMAGE_ID)

                # FSDomain_ID
                sql_FSDomain_ID = "SELECT ID FROM STORAGE_FILESYSTEM_DOMAIN;"
                result_sql_FSDomain_ID = curs.execute(sql_FSDomain_ID).fetchall()
                global result_FSDomain_ID
                result_FSDomain_ID = int(result_sql_FSDomain_ID[0][0])

                # BlkDevDomain ID
                sql_BlkDevDomain = "SELECT ID FROM STORAGE_BLOCK_DEVICE_DOMAIN;"
                result_sql_BlkDevDomain = curs.execute(sql_BlkDevDomain).fetchall()
                global result_BlkDevDomain
                result_BlkDevDomain = int(result_sql_BlkDevDomain[0][0])
                # print("result_BlkDevDomain",result_BlkDevDomain)

                # # storage Blk_dev_id
                # sql_BLK_DEV_ID = "SELECT ID FROM STORAGE_BLOCK_DEVICE WHERE DESCRIPTION='*JSON*';"
                # result_sql_BLK_DEV_ID = curs.execute(sql_BLK_DEV_ID).fetchall()
                # global result_BLK_DEV_ID
                # result_BLK_DEV_ID= int(result_BLK_DEV_ID[0][0])

                # TENANT_ID
                sql_TENANT_ID = "SELECT TENANT_ID FROM TENANT WHERE OWNER_ID=%d;" %result_USER_ID
                result_sql_TENANT_ID = curs.execute(sql_TENANT_ID).fetchall()
                global result_TENANT_ID
                result_TENANT_ID = int(result_sql_TENANT_ID[0][0])
                # print("result_TENANT_ID", result_TENANT_ID)

                # 연결 닫기
                conn.close()

        except Exception as ex:
            print(f"An error occurred: {ex}")
            pass

#result_tenant_sql()

