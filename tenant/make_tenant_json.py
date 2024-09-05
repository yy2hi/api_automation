import os
import json
import db_sql_tenant
import sapgo_result
import pyodbc

def create_json_file(file_name, data, total_num_files):
    # 해당 디렉토리를 만들어서 여기다 저장할 거임
    base_direc = f'/home/yjs/automation/Create/yhi/tenant/{version}/'

    # 디렉토리가 없으면 생성
    if not os.path.exists(base_direc):
        os.makedirs(base_direc, exist_ok=True)
    # else:
    #     print(f"{base_direc} directory is already exists!")

    # base_direc+=file_name
    # file_path=base_direc
    # 경로 조합하기
    file_path = os.path.join(base_direc, file_name)

    # 각 키(서비스)에 대해 파일 생성 및 저장
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    # print("file_path: ",file_path)
    # with open(f'{base_direc}admin_hom_create_output.txt', 'a') as file:
    #     print("files have been saved successfully.", file=file)
    total_num_files+=1

    return file_path, total_num_files, base_direc


# Python 딕셔너리를 이용하여 json 파일 생성
def tenant(project_name, network_name, subnet_name):
    base_direc = f'/home/yjs/automation/Create/yhi/tenant/{version}/'
    if not os.path.exists(base_direc):
        os.makedirs(base_direc, exist_ok=True)

    if os.path.exists(f'{base_direc}output.txt'):
        print("There is existing output.txt file.")
        print("Do you want to remove existing file? y/n")
        answer=input()
        if answer=='y':
            os.remove(f'{base_direc}output.txt')

    total_num_files = 0
    success_num_files = 0
    fail_num_files = 0

    db_sql_tenant.result_tenant_sql()

    # 프로젝트 생성
    CreateProjectWithQuotaService = {
        "header":{
            "messageType" : "REQUEST",
            "targetServiceName": "inframaster-compute/com.tmax.tmaxcloud.inframaster.compute.master.service.project.CreateProjectWithQuotaService"
        },
        "body":{
            "name" : project_name,
            "tenant_id" : "2",
            "description" : "JSON",
            "vcpu_limit" : 100,
            "vmem_limit" : 20480,
            "disk_limit" : 90737418240
            }
        }
        #disk_limit은 byte단위....
    file_path, total_num_files,base_direc= create_json_file("CreateProjectWithQuotaService.json", CreateProjectWithQuotaService, total_num_files)
    success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_tenant.result_tenant_sql()

    # PROJECT_ID
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
            "tenant_id": db_sql_tenant.result_TENANT_ID,
            "project_id": PROJECT_ID,
            "cidr": "10.0.0.0/16",
            "description": "test_network",
            "name": network_name
        }
    }
    file_path, total_num_files, base_direc=create_json_file("CreateNetworkService.json", CreateNetworkService,total_num_files)
    success_num_files, fail_num_files=sapgo_result.tenant_sapgo_result(base_direc, file_path, success_num_files, fail_num_files)
    db_sql_tenant.result_tenant_sql()

    # NETWORK_ID
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
    sql_NETWORK_ID = f"SELECT NETWORK_ID FROM NETWORK WHERE NAME='{network_name}'"
    result_sql_NETWORK_ID = curs.execute(sql_NETWORK_ID).fetchall()
    NETWORK_ID = int(result_sql_NETWORK_ID[0][0])

    conn.close()

    CreateSubnetService = {
            "header": {
                "targetServiceName": "network/com.tmax.tmaxcloud.network.master.subnet.overlay.CreateSubnetService",
                "requestId": 1,
                "messageType": "REQUEST",
                "contentType": "TEXT"
            },
            "body": {
                "project_id" : PROJECT_ID,
                "tenant_id" : db_sql_tenant.result_TENANT_ID,
                "network_id" : NETWORK_ID,
                "name" : subnet_name,
                "description" : "test_subnet",
                "cidr" : "10.0.1.0/24",
                "dns_server" : "8.8.8.8"
            }
    }
    file_path, total_num_files, base_direc = create_json_file("CreateSubnetService.json", CreateSubnetService,total_num_files)
    success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc, file_path, success_num_files, fail_num_files)
    db_sql_tenant.result_tenant_sql()

    # SUBNET_ID
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
    sql_SUBNET_ID = f"SELECT SUBNET_ID FROM SUBNET WHERE NAME='{subnet_name}'"
    result_sql_SUBNET_ID = curs.execute(sql_SUBNET_ID).fetchall()
    SUBNET_ID = int(result_sql_SUBNET_ID[0][0])

    conn.close()

    # CreateVrouterService = {
    #         "header": {
    #             "targetServiceName": "network/com.tmax.tmaxcloud.network.master.vr.gw.CreateVrouterService",
    #             "messageType": "REQUEST",
    #             "contentType": "TEXT"
    #         },
    #         "body": {
    #             "tenant_id": PROJECT_ID,
    #             "project_id": db_sql_tenant.result_TENANT_ID,
    #             "network_id": NETWORK_ID
    #         }
    # }
    # file_path, total_num_files, base_direc = create_json_file("CreateVrouterService.json", CreateVrouterService, total_num_files)
    # success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc, file_path, success_num_files, fail_num_files)
    # db_sql_tenant.result_tenant_sql()

    # ApplyMasqueradingService = {
    #         "header": {
    #             "targetServiceName": "network/com.tmax.tmaxcloud.network.master.masquerading.ApplyMasqueradingService",
    #             "requestId": 1,
    #             "messageType": "REQUEST",
    #             "contentType": "TEXT"
    #         },
    #         "body": {
    #             "tenant_id" : db_sql_tenant.result_TENANT_ID,
    #             "project_id" : PROJECT_ID,
    #             "network_id" : NETWORK_ID,
    #             "subnet_id" :  SUBNET_ID
    #         }
    # }
    # file_path, total_num_files, base_direc = create_json_file("ApplyMasqueradingService.json", ApplyMasqueradingService, total_num_files)
    # success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc, file_path, success_num_files, fail_num_files)
    # db_sql_tenant.result_tenant_sql()

    # 공인 IP 할당 (bvt)
    AllocatePublicIpService = {
            "header": {
                "targetServiceName": "network/com.tmax.tmaxcloud.network.master.subnet.publicip.AllocatePublicIpService",
                "messageType": "REQUEST",
                "contentType": "TEXT"
        },
            "body": {
                "project_id": PROJECT_ID,
                "type": "FREE"
        }
    }
    file_path, total_num_files, base_direc = create_json_file("AllocatePublicIpService.json", AllocatePublicIpService, total_num_files)
    success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc, file_path, success_num_files, fail_num_files)
    db_sql_tenant.result_tenant_sql()

    # PUB_ADDR
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
    sql_PUB_ADDR = "SELECT PUB_ADDR FROM PUBLIC_IP WHERE CREATED_TIME = (SELECT MAX(CREATED_TIME) FROM PUBLIC_IP)"
    result_sql_PUB_ADDR = curs.execute(sql_PUB_ADDR).fetchall()
    PUB_ADDR = str(result_sql_PUB_ADDR[0][0])

    conn.close()

    # 보안그룹 생성 (bvt)
    CreateSecurityGroupService = {
            "header": {
                "targetServiceName": "network/com.tmax.tmaxcloud.network.master.securitygroup.CreateSecurityGroupService",
                "messageType": "REQUEST",
                "contentType": "TEXT"
            },
            "body": {
                "tenant_id" : db_sql_tenant.result_TENANT_ID,
                "project_id" : PROJECT_ID,
                "network_id" : NETWORK_ID,
                "name" : "test_securityGroup",
                "description" : "test"
            }
    }
    file_path, total_num_files, base_direc = create_json_file("CreateSecurityGroupService.json", CreateSecurityGroupService, total_num_files)
    success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc, file_path, success_num_files, fail_num_files)
    db_sql_tenant.result_tenant_sql()

    # SECURITY_GROUP_ID
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
    sql_SECURITY_GROUP_ID = f"SELECT SECURITY_GROUP_ID FROM SECURITY_GROUP WHERE NETWORK_ID={NETWORK_ID}"
    result_sql_SECURITY_GROUP_ID = curs.execute(sql_SECURITY_GROUP_ID).fetchall()
    SECURITY_GROUP_ID = int(result_sql_SECURITY_GROUP_ID[0][0])

    conn.close()

    # ApplyEgressFirewallService = {
    #         "header": {
    #             "targetServiceName": "network/com.tmax.tmaxcloud.network.master.firewall.overlay.ApplyEgressFirewallService",
    #             "requestId": 1,
    #             "messageType": "REQUEST",
    #             "contentType": "TEXT"
    #         },
    #         "body": {
    #             "tenant_id" : db_sql_tenant.result_TENANT_ID,
    #             "project_id" : PROJECT_ID,
    #             "network_id" : NETWORK_ID,
    #             "rules" : [
    #             {
    #                     "rule_number" : 1,
    #                     "src_ip" : None,
    #                     "dst_ip" : None,
    #                     "proto" : "all",
    #                     "src_port" : None,
    #                     "dst_port" : None,
    #                     "action" : "ACCEPT",
    #                     "description": "test"
    #             }
    #             ]
    #         }
    # }
    # file_path, total_num_files, base_direc = create_json_file("ApplyEgressFirewallService.json", ApplyEgressFirewallService, total_num_files)
    # success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc, file_path, success_num_files, fail_num_files)
    # db_sql_tenant.result_tenant_sql()

    # ApplyIngressFirewallService = {
    #         "header": {
    #             "targetServiceName": "network/com.tmax.tmaxcloud.network.master.firewall.overlay.ApplyIngressFirewallService",
    #             "requestId": 1,
    #             "messageType": "REQUEST",
    #             "contentType": "TEXT"
    #         },
    #         "body": {
    #             "tenant_id" : db_sql_tenant.result_TENANT_ID,
    #             "project_id" : PROJECT_ID,
    #             "network_id" : NETWORK_ID,
    #             "rules" : [
    #             {
    #                     "rule_number" : 1,
    #                     "src_ip" : None,
    #                     "dst_ip" : None,
    #                     "proto" : "all",
    #                     "src_port" : None,
    #                     "dst_port" : None,
    #                     "action" : "ACCEPT",
    #                     "description": "test"
    #             }
    #             ]
    #         }
    # }
    # file_path, total_num_files, base_direc = create_json_file("ApplyIngressFirewallService.json", ApplyIngressFirewallService, total_num_files)
    # success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc, file_path, success_num_files, fail_num_files)
    # db_sql_tenant.result_tenant_sql()

    CreateFloatingIpService = {
            "header": {
                "targetServiceName": "network/com.tmax.tmaxcloud.network.master.floatingip.CreateFloatingIpService",
                "messageType": "REQUEST"
            },
            "body": {
                "tenant_id": db_sql_tenant.result_TENANT_ID,
                "project_id": PROJECT_ID,
                "network_id": NETWORK_ID,
                "name": "test_floatingIp",
                "description": "fip description",
                "ip_address": PUB_ADDR
            }
    }
    file_path, total_num_files, base_direc = create_json_file("CreateFloatingIpService.json", CreateFloatingIpService, total_num_files)
    success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc, file_path, success_num_files, fail_num_files)
    db_sql_tenant.result_tenant_sql()

    CreateNaclService = {
            "header": {
                "targetServiceName": "network/com.tmax.tmaxcloud.network.master.nacl.CreateNaclService",
                "messageType": "REQUEST"
            },
            "body": {
                "project_id" : PROJECT_ID,
                "tenant_id" : db_sql_tenant.result_TENANT_ID,
                "name" : "test_nacl",
                "network_id" : NETWORK_ID
                }
    }
    file_path, total_num_files, base_direc = create_json_file("CreateNaclService.json", CreateNaclService, total_num_files)
    success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc, file_path, success_num_files, fail_num_files)
    db_sql_tenant.result_tenant_sql()

    CreateTargetGroupService  = {
        "header": {
            "targetServiceName": "network/com.tmax.tmaxcloud.network.master.targetgroup.CreateTargetGroupService",
            "messageType": "REQUEST"
        },
        "body": {
            "tenant_id": db_sql_tenant.result_TENANT_ID,
            "project_id": PROJECT_ID,
            "network_id": NETWORK_ID,
            "name": "target group name",
            "description": "desc",
            "protocol": "tcp",
            "port": "80",
            "editable": 1,
            "type": "ip",
            "health_protocol": "tcp",
            "health_port": "80",
            "health_threshold": 3,
            "health_interval": 120,
            "create_members": [
                {
                    "guest_interface_id": None,
                    "target_ip": "10.0.0.10",
                    "target_port": "80",
                    "rule_option": None
                },
                {
                    "guest_interface_id": None,
                    "target_ip": "10.0.0.11",
                    "target_port": "81",
                    "rule_option": "11"
                }
            ]
        }
    }

    file_path, total_num_files, base_direc = create_json_file("CreateTargetGroupService.json", CreateTargetGroupService, total_num_files)
    success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc, file_path, success_num_files, fail_num_files)
    db_sql_tenant.result_tenant_sql()

    # TARGET_GROUP_ID (bvt)
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
    sql_TARGET_GROUP_ID = f"SELECT TARGET_GROUP_ID FROM TARGET_GROUP WHERE NETWORK_ID={NETWORK_ID}"
    result_sql_TARGET_GROUP_ID = curs.execute(sql_TARGET_GROUP_ID).fetchall()
    TARGET_GROUP_ID = int(result_sql_TARGET_GROUP_ID[0][0])

    conn.close()


    AllocatePublicIpService = {
                "header": {
                    "targetServiceName": "network/com.tmax.tmaxcloud.network.master.subnet.publicip.AllocatePublicIpService",
                    "messageType": "REQUEST",
                    "contentType": "TEXT"
            },
                "body": {
                    "project_id": PROJECT_ID,
                    "type": "FREE"
            }
    }
    
    file_path, total_num_files, base_direc = create_json_file("AllocatePublicIpService.json", AllocatePublicIpService, total_num_files)
    success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc, file_path, success_num_files, fail_num_files)
    db_sql_tenant.result_tenant_sql()

    # pub_addr
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
    sql_PUB_ADDR = "SELECT PUB_ADDR FROM PUBLIC_IP WHERE CREATED_TIME = (SELECT MAX(CREATED_TIME) FROM PUBLIC_IP)"
    result_sql_PUB_ADDR = curs.execute(sql_PUB_ADDR).fetchall()
    PUB_ADDR = str(result_sql_PUB_ADDR[0][0])

    conn.close()

    CreateLbService = {
        "header": {
            "targetServiceName": "network/com.tmax.tmaxcloud.network.master.loadbalancer.overlay.CreateLbService",
            "messageType": "REQUEST"
        },
        "body": {
            "tenant_id": db_sql_tenant.result_TENANT_ID,
            "project_id": PROJECT_ID,
            "network_id": NETWORK_ID,
            "name": "lb name",
            "description": "lb description",
            "lb_type": "external",
            "lb_ip": None,
            "subnet_id": SUBNET_ID,
            "listeners":[
                {
                "port": 80,
                "protocol": "tcp",
                "algorithm": "weight",
                "description": "description111",
                "target_group_id": TARGET_GROUP_ID
                }
            ]
        }
    }

    file_path, total_num_files, base_direc = create_json_file("CreateLbService.json", CreateLbService, total_num_files)
    success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc, file_path, success_num_files, fail_num_files)
    db_sql_tenant.result_tenant_sql()

    # 가상머신 생성
    CreateGuestMachineService = {
    "header": {
        "targetServiceName": "inframaster-compute/com.tmax.tmaxcloud.inframaster.compute.master.service.compute.vm.CreateGuestMachineService",
        "messageType": "REQUEST"
    },
    "body": {
        "name" : "yjsautovm",
        "tenant_id" : db_sql_tenant.result_TENANT_ID,
        "project_id" : PROJECT_ID,
        "network_id" : NETWORK_ID,
        "vnic_info" : [{"subnet_id" : SUBNET_ID , "security_group_ids" : [SECURITY_GROUP_ID]}],
        "mem_total" : "1024",
        "vcpu_count" : "1",
        "disks" : [],
        "image_id" : "22",
        "blk_dev_domain_id": db_sql_tenant.result_BlkDevDomain,
    }
    }
    file_path, total_num_files,base_direc= create_json_file("CreateGuestMachineService.json", CreateGuestMachineService, total_num_files)
    success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_tenant.result_tenant_sql()

    # guest_machine_id
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
    sql_GUEST_MACHINE_ID = "select GUEST_MACHINE_ID from guest_machine where name = 'yjsautovm'"
    result_sql_GUEST_MACHINE_ID = curs.execute(sql_GUEST_MACHINE_ID).fetchall()
    GUEST_MACHINE_ID = str(result_sql_GUEST_MACHINE_ID[0][0])

    conn.close()

    #  가상머신 실행
    RunGuestMachineService = {
        "header": {
            "targetServiceName": "inframaster-compute/com.tmax.tmaxcloud.inframaster.compute.master.service.compute.vm.RunGuestMachineService",
            "messageType": "REQUEST"
        },
        "body": {
            "guest_machine_id" : GUEST_MACHINE_ID,
            "project_id" : PROJECT_ID
        }
    }

    file_path, total_num_files,base_direc= create_json_file("RunGuestMachineService.json", RunGuestMachineService, total_num_files)
    success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_tenant.result_tenant_sql()


    print("total_num_files: ",total_num_files)
    print("success_num_files: ",success_num_files)
    print("fail_num_files: ", fail_num_files)

    with open(f'{base_direc}output.txt', 'a') as file:
        print("total_num_files: ", total_num_files, file=file)
        print("success_num_files: ", success_num_files, file=file)
        print("fail_num_files: ", fail_num_files, file=file)


if __name__ == "__main__":
    version = input("Enter the TCP IaaS version: ")
    project_name = input("Enter the PROJECT creation name: ")
    network_name = input("Enter the NETWORK name: ")
    subnet_name = input("Enter the SUBNET name: ")
    tenant(project_name, network_name, subnet_name)


