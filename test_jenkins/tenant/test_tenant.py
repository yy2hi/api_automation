import pytest
from common.logger import setup_logger
from common.utils import create_json_file, process_api_request
from common.config import BASE_DIR
from common.db_sql import conn_db, tenant_sql
import common.db_sql
import os

@pytest.fixture
def tenant_logger(params):
    # 각 테스트 실행 시마다 로거 설정
    version = params["version"]
    return setup_logger('tenant_automation', version, 'tenant')

def test_tenant_operations(params, tenant_logger):
    base_dir = os.path.join(BASE_DIR, params["version"], 'tenant')
    os.makedirs(base_dir, exist_ok=True)

    # 파일 처리 및 API 요청에 대한 성공/실패 기록
    total_num_files = 0
    success_num_files = 0
    fail_num_files = 0

    # 데이터베이스에서 필요한 값 추출
    tenant_sql()
    try:
        # 프로젝트 생성
        CreateProjectWithQuotaService = {
            "header": {
                "messageType": "REQUEST",
                "targetServiceName": "inframaster-compute/com.tmax.tmaxcloud.inframaster.compute.master.service.project.CreateProjectWithQuotaService"
            },
            "body": {
                "name": params["project_name"],
                "tenant_id": common.db_sql.result_TENANT_ID,
                "description": "JSON",
                "vcpu_limit": 100,
                "vmem_limit": 20480,
                "disk_limit": 90737418240
            }
        }
        file_path = create_json_file("CreateProjectWithQuotaService.json", CreateProjectWithQuotaService, base_dir)
        total_num_files += 1
        
        if process_api_request(file_path, tenant_logger):
            success_num_files += 1
        else:
            fail_num_files += 1
            pytest.fail(f"Failed to create project: {file_path}")

        # PROJECT_ID 추출
        conn, curs = conn_db()
        sql_PROJECT_ID = f"SELECT PROJECT_ID FROM PROJECT WHERE NAME='{params['project_name']}'"
        result_sql_PROJECT_ID = curs.execute(sql_PROJECT_ID).fetchall()
        PROJECT_ID = int(result_sql_PROJECT_ID[0][0])
        conn.close()

        # 네트워크 생성
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
                "name": params["network_name"]
            }
        }
        file_path = create_json_file("CreateNetworkService.json", CreateNetworkService, base_dir)
        total_num_files += 1
        
        if process_api_request(file_path, tenant_logger):
            success_num_files += 1
        else:
            fail_num_files += 1
            pytest.fail(f"Failed to create network: {file_path}")

        # NETWORK_ID 추출
        conn, curs = conn_db()
        sql_NETWORK_ID = f"SELECT NETWORK_ID FROM NETWORK WHERE NAME='{params['network_name']}'"
        result_sql_NETWORK_ID = curs.execute(sql_NETWORK_ID).fetchall()
        NETWORK_ID = int(result_sql_NETWORK_ID[0][0])
        conn.close()

        # 서브넷 생성
        CreateSubnetService = {
            "header": {
                "targetServiceName": "network/com.tmax.tmaxcloud.network.master.subnet.overlay.CreateSubnetService",
                "requestId": 1,
                "messageType": "REQUEST",
                "contentType": "TEXT"
            },
            "body": {
                "project_id": PROJECT_ID,
                "tenant_id": common.db_sql.result_TENANT_ID,
                "network_id": NETWORK_ID,
                "name": params["subnet_name"],
                "description": "test_subnet",
                "cidr": "10.0.1.0/24",
                "dns_server": "8.8.8.8"
            }
        }
        file_path = create_json_file("CreateSubnetService.json", CreateSubnetService, base_dir)
        total_num_files += 1
        
        if process_api_request(file_path, tenant_logger):
            success_num_files += 1
        else:
            fail_num_files += 1
            pytest.fail(f"Failed to create subnet: {file_path}")

        # SUBNET_ID 추출
        conn, curs = conn_db()
        sql_SUBNET_ID = f"SELECT SUBNET_ID FROM SUBNET WHERE NAME='{params['subnet_name']}'"
        result_sql_SUBNET_ID = curs.execute(sql_SUBNET_ID).fetchall()
        SUBNET_ID = int(result_sql_SUBNET_ID[0][0])
        conn.close()

    except Exception as e:
        tenant_logger.error(f"Tenant automation error: {str(e)}")
        pytest.fail(f"Exception occurred during tenant operations: {e}")

    # 테스트 결과 기록
    tenant_logger.info(f"Total files: {total_num_files}")
    tenant_logger.info(f"Successful files: {success_num_files}")
    tenant_logger.info(f"Failed files: {fail_num_files}")

    # 전체 성공 여부를 최종적으로 체크
    assert fail_num_files == 0, "Some tenant operations failed, check logs for details."
