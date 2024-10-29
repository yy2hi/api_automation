from common.db_sql import conn_db, admin_sql
from common.logger import setup_logger
from common.utils import create_json_file, process_api_request
from common.config import BASE_DIR
import os

def admin(version):
    base_dir = os.path.join(BASE_DIR, version, 'admin')
    os.makedirs(base_dir, exist_ok=True)
    
    logger = setup_logger('admin_automation', version, 'admin')

    total_num_files = 0
    success_num_files = 0
    fail_num_files = 0
    
    try:
        # Host OS Group creation
        host_os_group_data = {
            "header": {
                "targetServiceName": "host-os-service/com.tmax.tmaxcloud.hom.compute.os.CreateHostOSGroup",
                "messageType": "REQUEST"
            },
            "body": {
                "GROUP_NAME": "test",
                "TYPE": "test", 
                "DESCRIPTION": "test"
            }
        }
        
        file_path = create_json_file("CreateHostOSGroup.json", host_os_group_data, base_dir)
        total_num_files += 1
        
        if process_api_request(file_path, logger):
            success_num_files += 1
        else:
            fail_num_files += 1

        # 나머지 admin 작업들도 비슷한 패턴으로 구현
        # ...

    except Exception as e:
        logger.error(f"Admin automation error: {str(e)}")
        
    finally:
        logger.info(f"Total files: {total_num_files}")
        logger.info(f"Successful files: {success_num_files}")
        logger.info(f"Failed files: {fail_num_files}")