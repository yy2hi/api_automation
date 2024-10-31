from common.logger import setup_logger
from common.utils import create_json_file, process_api_request
from common.config import BASE_DIR
from common.db_sql import conn_db, tenant_sql
import common.db_sql
import os

def tenant(version, project_name, network_name, subnet_name, vm_name):
    base_dir = os.path.join(BASE_DIR, version, 'tenant')
    os.makedirs(base_dir, exist_ok=True)
    
    logger = setup_logger('tenant_automation', version, 'tenant')

    total_num_files = 0
    success_num_files = 0
    fail_num_files = 0

    tenant_sql()
    try:
        # 프로젝트 생성
        CreateProjectWithQuotaService = {
            "header": {
                "messageType": "REQUEST",
                "targetServiceName": "inframaster-compute/com.tmax.tmaxcloud.inframaster.compute.master.service.project.CreateProjectWithQuotaService"
            },
            "body": {
                "name": project_name,
                "tenant_id": common.db_sql.result_TENANT_ID,
                "description": "JSON",
                "vcpu_limit": 100,
                "vmem_limit": 20480,
                "disk_limit": 90737418240
            }
        }
        tenant_sql()

        file_path = create_json_file("CreateProjectWithQuotaService.json", CreateProjectWithQuotaService, base_dir)
        total_num_files += 1
        
        if process_api_request(file_path, logger):
            success_num_files += 1
        else:
            fail_num_files += 1

        # PROJECT_ID 추출
        conn, curs = conn_db()
        sql_PROJECT_ID = f"SELECT PROJECT_ID FROM PROJECT WHERE NAME='{project_name}'"
        result_sql_PROJECT_ID = curs.execute(sql_PROJECT_ID).fetchall()
        PROJECT_ID = int(result_sql_PROJECT_ID[0][0])
        conn.close()

        # 네트워크 생성 (bvt)
        CreateNetworkService = {
            "header": {
                "targetServiceName": "network/com.tmax.tmaxcloud.network.master.net.overlay.CreateNetworkService",
                "messageType": "REQUEST",
                "contentType": "TEXT"
            },
            "body": {
                "tenant_id": common.db_sql.result_TENANT_ID,
                "project_id": PROJECT_ID,
                "cidr": "10.0.0.0/16",
                "description": "test_network",
                "name": network_name
            }
        }
        tenant_sql()

        file_path = create_json_file("CreateNetworkService.json", CreateNetworkService, base_dir)
        total_num_files += 1
        
        if process_api_request(file_path, logger):
            success_num_files += 1
        else:
            fail_num_files += 1

        # NETWORK_ID 추출
        conn, curs = conn_db()
        sql_NETWORK_ID = f"SELECT NETWORK_ID FROM NETWORK WHERE NAME='{network_name}'"
        result_sql_NETWORK_ID = curs.execute(sql_NETWORK_ID).fetchall()
        NETWORK_ID = int(result_sql_NETWORK_ID[0][0])
        conn.close()

        # 서브넷 생성 (bvt)
        CreateSubnetService = {
            "header": {
                "targetServiceName": "network/com.tmax.tmaxcloud.network.master.subnet.overlay.CreateSubnetService",
                "requestId": 1,
                "messageType": "REQUEST",
                "contentType": "TEXT"
            },
            "body": {
                "project_id" : PROJECT_ID,
                "tenant_id" : common.db_sql.result_TENANT_ID,
                "network_id" : NETWORK_ID,
                "name" : subnet_name,
                "description" : "test_subnet",
                "cidr" : "10.0.1.0/24",
                "dns_server" : "8.8.8.8"
            }
        }
        tenant_sql()

        file_path = create_json_file("CreateSubnetService.json", CreateSubnetService, base_dir)
        total_num_files += 1
        
        if process_api_request(file_path, logger):
            success_num_files += 1
        else:
            fail_num_files += 1

        # SUBNET_ID 추출
        conn, curs = conn_db()
        sql_SUBNET_ID = f"SELECT SUBNET_ID FROM SUBNET WHERE NAME='{subnet_name}'"
        result_sql_SUBNET_ID = curs.execute(sql_SUBNET_ID).fetchall()
        SUBNET_ID = int(result_sql_SUBNET_ID[0][0])
        conn.close()

    except Exception as e:
        logger.error(f"Tenant automation error: {str(e)}")
        
    finally:
        logger.info(f"Total files: {total_num_files}")
        logger.info(f"Successful files: {success_num_files}") 
        logger.info(f"Failed files: {fail_num_files}")