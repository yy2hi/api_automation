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

def admin_sql():
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

def tenant_sql():
        try:
                conn, curs = conn_db()

                # USER_ID
                sql_USER_ID = "SELECT ID FROM USER_INFO WHERE LOGIN_ID='yhi2'"
                result_sql_USER_ID = curs.execute(sql_USER_ID).fetchall()
                global result_USER_ID
                result_USER_ID = int(result_sql_USER_ID[0][0])
                
                # STORAGE IMAGE_ID (어드민 이미지 ID)
                sql_IMAGE_ID = "SELECT ID FROM STORAGE_PUBLIC_IMAGE;"
                result_sql_IMAGE_ID = curs.execute(sql_IMAGE_ID).fetchall()
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

                # GUEST_MACHINE_ID 추출
                sql_GUEST_MACHINE_ID = "SELECT GUEST_MACHINE_ID FROM GUEST_MACHINE WHERE NAME = 'yjsautovm'"
                result_sql_GUEST_MACHINE_ID = curs.execute(sql_GUEST_MACHINE_ID).fetchall()
                global result_GUEST_MACHINE_ID
                result_GUEST_MACHINE_ID = int(result_sql_GUEST_MACHINE_ID[0][0])

                # 연결 닫기
                conn.close()

        except Exception as ex:
            print(f"An error occurred: {ex}")
            pass

