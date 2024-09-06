import os
import json
import db_sql_tenant
import sapgo_result
import pyodbc

def create_json_file(file_name, data, total_num_files):
    # 해당 디렉토리에 json 저장
    base_direc = f'/home/sapgo/bvt/tenant/{version}/'

    # 디렉토리가 없으면 생성
    if not os.path.exists(base_direc):
        os.makedirs(base_direc, exist_ok=True)

    file_path = os.path.join(base_direc, file_name)

    # 각 키(서비스)에 대해 파일 생성 및 저장
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    total_num_files+=1

    return file_path, total_num_files, base_direc

# Python 딕셔너리를 이용하여 json 파일 생성
def tenant(project_name, network_name, subnet_name):
    base_direc = f'/home/sapgo/bvt/tenant/{version}/'
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

    # PROJECT_ID 추출
    conn, curs = db_sql_tenant.conn_db()
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

    # NETWORK_ID 추출
    conn, curs = db_sql_tenant.conn_db()
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

    # SUBNET_ID 추출
    conn, curs = db_sql_tenant.conn_db()
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

    # PUB_ADDR 추출
    conn, curs = db_sql_tenant.conn_db()
    # 가장 최근에 생성된 PUBLIC_IP 추출 쿼리
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

    # SECURITY_GROUP_ID 추출
    conn, curs = db_sql_tenant.conn_db()
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

    # ip 인스턴스 타겟 그룹 생성
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

    # TARGET_GROUP_ID 추출
    conn, curs = db_sql_tenant.conn_db()
    sql_TARGET_GROUP_ID = f"SELECT TARGET_GROUP_ID FROM TARGET_GROUP WHERE NETWORK_ID={NETWORK_ID}"
    result_sql_TARGET_GROUP_ID = curs.execute(sql_TARGET_GROUP_ID).fetchall()
    TARGET_GROUP_ID = int(result_sql_TARGET_GROUP_ID[0][0])
    conn.close()

    # 공인 IP 생성 2
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

    # 상위 공인 IP ID 추출
    conn, curs = db_sql_tenant.conn_db()
    sql_PUB_ADDR = "SELECT PUB_ADDR FROM PUBLIC_IP WHERE CREATED_TIME = (SELECT MAX(CREATED_TIME) FROM PUBLIC_IP)"
    result_sql_PUB_ADDR = curs.execute(sql_PUB_ADDR).fetchall()
    PUB_ADDR = str(result_sql_PUB_ADDR[0][0])
    conn.close()

    # LB 생성 (bvt)
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


    # 빈블록 생성 (bvt)
    BlkDevCreateEmpty = {
        "header": {
            "targetServiceName": "storage/com.tmax.tmaxcloud.storage.master.BlkDevCreateEmpty",
            "requestId": 1,
            "messageType": "REQUEST",
            "contentType": "TEXT"
        },
        "body": {
            "name": "jsonblock",
            "description": "test",
            "tenant_id": db_sql_tenant.result_TENANT_ID,
            "project_id": PROJECT_ID,
            "blk_dev_domain_id": db_sql_tenant.result_BlkDevDomain,
            "size": 1073741824,
            "is_shared": True
        }
    }

    file_path, total_num_files,base_direc= create_json_file("BlkDevCreateEmpty.json", BlkDevCreateEmpty, total_num_files)
    success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_tenant.result_tenant_sql()


    # 파일시스템 생성 (bvt)
    FsCreate = {
        "header": {
            "targetServiceName": "storage/com.tmax.tmaxcloud.storage.master.FsCreate",
            "requestId": 1,
            "messageType": "REQUEST",
            "contentType": "TEXT"
        },
        "body": {
                    "name":"fsjson",
                    "description":"JSON",
                    "project_id":PROJECT_ID,
                    "tenant_id":db_sql_tenant.result_TENANT_ID,
                    "filesystem_domain_id": db_sql_tenant.result_FSDomain_ID,
                    "quota": 10737418240
        }
    }

    
    file_path, total_num_files,base_direc= create_json_file("FsCreate.json", FsCreate, total_num_files)
    success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_tenant.result_tenant_sql()

    # 테넌트 이미지 임포트 (bvt)
    ImgImport_tenant = {
        "header": {
            "targetServiceName": "storage/com.tmax.tmaxcloud.storage.service.image.Import",
            "requestId": 1,
            "messageType": "REQUEST",
            "contentType": "TEXT"
        },
        "body": {
            "visibility": 2,
            "tenant_id": db_sql_tenant.result_TENANT_ID,
            "project_id": "0",
            "image_repository_file_image_id": db_sql_tenant.result_IMAGE_ID,
            "dest_block_device_domain_id": db_sql_tenant.result_BlkDevDomain
        }
    }

    file_path, total_num_files,base_direc= create_json_file("ImgImport_tenant.json", ImgImport_tenant, total_num_files)
    success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_tenant.result_tenant_sql()

    # 프로젝트 이미지 임포트 (bvt) -> 가상 머신에 사용할 ID
    ImgImport_project = {
    "header": {
        "targetServiceName": "storage/com.tmax.tmaxcloud.storage.service.image.Import",
        "requestId": 1,
        "messageType": "REQUEST",
        "contentType": "TEXT"
    },
    "body": {
        "visibility": 3,
        "tenant_id": db_sql_tenant.result_TENANT_ID,
        "project_id": PROJECT_ID,
        "image_repository_file_image_id": db_sql_tenant.result_IMAGE_ID,
        "dest_block_device_domain_id": db_sql_tenant.result_BlkDevDomain
    }
    }

    file_path, total_num_files,base_direc= create_json_file("ImgImport_project.json", ImgImport_project, total_num_files)
    success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_tenant.result_tenant_sql()

    # STORAGE IMAGE_ID 추출
    conn, curs = db_sql_tenant.conn_db()
    sql_IMAGE_ID = f"SELECT ID FROM STORAGE_IMAGE PROJECT_ID='{PROJECT_ID}'"
    result_sql_IMAGE_ID = curs.execute(sql_IMAGE_ID).fetchall()
    IMAGE_ID = int(result_sql_IMAGE_ID[0][0])
    conn.close()

    # 가상머신 생성 (bvt)
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
            "image_id" : IMAGE_ID,
            "blk_dev_domain_id": db_sql_tenant.result_BlkDevDomain,
        }
    }

    file_path, total_num_files,base_direc= create_json_file("CreateGuestMachineService.json", CreateGuestMachineService, total_num_files)
    success_num_files, fail_num_files = sapgo_result.tenant_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_tenant.result_tenant_sql()

    # # GUEST_MACHINE_ID 추출
    # conn, curs = db_sql_tenant.conn_db()
    # sql_GUEST_MACHINE_ID = "select GUEST_MACHINE_ID from guest_machine where name = 'yjsautovm'"
    # result_sql_GUEST_MACHINE_ID = curs.execute(sql_GUEST_MACHINE_ID).fetchall()
    # GUEST_MACHINE_ID = str(result_sql_GUEST_MACHINE_ID[0][0])
    # conn.close()

    # 가상머신 실행 (bvt)
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


