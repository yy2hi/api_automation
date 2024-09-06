import os
import json
import db_sql_admin
import sapgo_result

def create_json_file(file_name, data, total_num_files):
    # 해당 디렉토리에 json 저장
    base_direc = f'/home/sapgo/bvt/admin/{version}/'

    # 디렉토리가 없으면 생성
    if not os.path.exists(base_direc):
        os.makedirs(base_direc, exist_ok=True)
    # else:
    #     print(f"{base_direc} directory is already exists!")

    file_path = os.path.join(base_direc, file_name)

    # 각 키(서비스)에 대해 파일 생성 및 저장
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    total_num_files+=1

    return file_path, total_num_files, base_direc

# Python 딕셔너리를 이용하여 json 파일 생성
def admin():
    base_direc = f'/home/sapgo/bvt/admin/{version}/'
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
    db_sql_admin.result_sql_admin()


    # HOST_OS_GROUP 생성
    CreateHostOSGroup = {
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
    file_path, total_num_files,base_direc= create_json_file("CreateHostOSGroup.json", CreateHostOSGroup, total_num_files)
    success_num_files, fail_num_files = sapgo_result.admin_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_admin.rseult_sql_admin()


    # HOST OS GROUP MEMBER 생성
    CreateHostOSGroupMember= {
        "header": {
            "targetServiceName": "host-os-service/com.tmax.tmaxcloud.hom.compute.dx_service.CreateHostOSGroupMember",
            "messageType": "REQUEST"
        },
        "body": {
            "os_group_id": db_sql_admin.result_OS_GROUP_ID,
            "host_os_id": db_sql_admin.result_HOM_HOST_OS_ID
        }
    }
    file_path, total_num_files,base_direc = create_json_file("CreateHostOSGroupMember.json", CreateHostOSGroupMember, total_num_files)
    success_num_files, fail_num_files = sapgo_result.admin_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_admin.rseult_sql_admin()

    # # master8
    # CreateHostInterface = {
    #     "header": {
    #         "targetServiceName": "network/com.tmax.tmaxcloud.network.master.CreateHostInterface",
    #         "requestId": 1,
    #         "messageType": "REQUEST",
    #         "contentType": "TEXT"
    #     },
    #     "body":{
    #       "HOSTNAME": "master8"
    #     }
    # }
    # file_path, total_num_files, base_direc= create_json_file("CreateHostInterface.json", CreateHostInterface, total_num_files)
    # success_num_files, fail_num_files = sapgo_result.admin_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    # db_sql_admin.result_sql_admin()

    # # master9
    # CreateHostInterface = {
    #     "header": {
    #         "targetServiceName": "network/com.tmax.tmaxcloud.network.master.CreateHostInterface",
    #         "requestId": 1,
    #         "messageType": "REQUEST",
    #         "contentType": "TEXT"
    #     },
    #     "body":{
    #       "HOSTNAME": "master9"
    #     }
    # }
    # file_path, total_num_files, base_direc= create_json_file("CreateHostInterface.json", CreateHostInterface, total_num_files)
    # success_num_files, fail_num_files = sapgo_result.admin_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    # db_sql_admin.result_sql_admin()

    # # compute17
    # CreateHostInterface = {
    #     "header": {
    #         "targetServiceName": "network/com.tmax.tmaxcloud.network.master.CreateHostInterface",
    #         "requestId": 1,
    #         "messageType": "REQUEST",
    #         "contentType": "TEXT"
    #     },
    #     "body":{
    #       "HOSTNAME": "compute17"
    #     }
    # }
    # file_path, total_num_files, base_direc= create_json_file("CreateHostInterface.json", CreateHostInterface, total_num_files)
    # success_num_files, fail_num_files = sapgo_result.admin_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    # db_sql_admin.result_sql_admin()

    # # compute18
    # CreateHostInterface = {
    #     "header": {
    #         "targetServiceName": "network/com.tmax.tmaxcloud.network.master.CreateHostInterface",
    #         "requestId": 1,
    #         "messageType": "REQUEST",
    #         "contentType": "TEXT"
    #     },
    #     "body":{
    #       "HOSTNAME": "compute18"
    #     }
    # }
    # file_path, total_num_files, base_direc= create_json_file("CreateHostInterface.json", CreateHostInterface, total_num_files)
    # success_num_files, fail_num_files = sapgo_result.admin_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    # db_sql_admin.result_sql_admin()


    # compute17 용도 지정 (bvt)
    CreateHostInterfaceUsage  = {
        "header": {
            "targetServiceName": "network/com.tmax.tmaxcloud.network.master.networkinterface.CreateHostInterfaceUsage",
            "requestId": 1,
            "messageType": "REQUEST",
            "contentType": "TEXT"
        },
        "body": {
                "osId":db_sql_admin.result_HOST_OS_ID,
                "interfaceName":"enp2s0",
                "ifUsage":["control","ceph_front","internal"]
        }
    }

    file_path, total_num_files, base_direc= create_json_file("CreateHostInterfaceUsage.json", CreateHostInterfaceUsage, total_num_files)
    success_num_files, fail_num_files = sapgo_result.admin_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_admin.result_sql_admin()


    # compute17 CreateComputeHostService 생성 (bvt)
    CreateComputeHostService = {
       "header": {
            "targetServiceName": "inframaster-compute/com.tmax.tmaxcloud.inframaster.compute.master.service.compute.host.CreateComputeHostService",
            "messageType": "REQUEST"
        },
        "body": {
            "host_os_id" : db_sql_admin.result_COM_HOST_OS_ID,
            "host_os_group_id" : 2,
            "memory_overcommit_ratio" : "2.0",
            "memory_limit_ratio" : "1",
            "interface_usage" : [{"name" : "enp2s0" , "usage" : "internal"}, {"name" : "enp2s0" , "usage" : "control"},
            {"name" : "enp2s0", "usage" : "ceph-front", "ip" : "172.21.5.17", "dns" : "8.8.8.8", "gateway" : "172.21.5.1", "netmask" : 24}]
        }
    }

    file_path, total_num_files, base_direc= create_json_file("CreateComputeHostService.json", CreateComputeHostService, total_num_files)
    success_num_files, fail_num_files = sapgo_result.admin_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_admin.result_sql_admin()


    # master9 네트워크 노드 등록 (bvt)
    SettingNetworkHostService  = {
        "header": {
            "targetServiceName": "network/com.tmax.tmaxcloud.network.master.etc.SettingNetworkHostService",
            "messageType": "REQUEST"
        },
        "body": {
            "osId":db_sql_admin.result_NET_HOST_OS_ID,
            "interfaceSetting": [                
                    {"interfaceName":  "eno1", "usage": "control", "ip" : "172.21.5.9", "netmask": "255.255.255.0", "gateway": None, "dns":"8.8.8.8"},
                    {"interfaceName":  "eno1", "usage": "internal", "ip" : "175.21.5.9", "netmask": "255.255.255.0", "gateway": None, "dns":None},
                    {"interfaceName":  "eno4", "usage": "data-isp", "ip" : "172.31.5.8", "netmask": "255.255.0.0", "gateway": "172.31.0.2", "dns":"8.8.8.8"},
                    {"interfaceName":  "eno1", "usage": "ceph_front", "ip" : "172.21.5.9", "netmask": "255.255.255.0", "gateway": None, "dns":"8.8.8.8"}
                ]
            }
        }

    file_path, total_num_files, base_direc= create_json_file("SettingNetworkHostService.json", SettingNetworkHostService, total_num_files)
    success_num_files, fail_num_files = sapgo_result.admin_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_admin.result_sql_admin()
 

    # IP POOL 등록 (bvt)
    CreateClusterIppoolService  = {
        "header": {
            "targetServiceName": "network/com.tmax.tmaxcloud.network.master.subnet.underlay.CreateClusterIppoolService",
            "messageType": "REQUEST",
            "contentType": "TEXT"
        },
        "body": {
            "name" : "auto_ipPool",
            "start_ip" : "172.31.5.100",
            "end_ip" : "172.31.5.200",
            "dns_server" : "8.8.8.8",
            "description" : "Public Ippool",
            "type" : "PUBLIC",
            "cidr" : "172.31.0.0/16",
            "gateway_ip" : "172.31.0.2"
        }
    }
    file_path, total_num_files, base_direc= create_json_file("CreateClusterIppoolService.json", CreateClusterIppoolService, total_num_files)
    success_num_files, fail_num_files = sapgo_result.admin_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_admin.result_sql_admin()


    # storage 대시보드 확인
    DashboardStorageClusterInfo = {
    "header": {
        "targetServiceName": "storage/com.tmax.tmaxcloud.storage.master.DashboardStorageClusterInfo",
        "requestId": 1,
        "messageType": "REQUEST",
        "contentType": "TEXT"
        },
        "body": {
        }
    }

    file_path, total_num_files, base_direc= create_json_file("DashboardStorageClusterInfo.json", DashboardStorageClusterInfo, total_num_files)
    success_num_files, fail_num_files = sapgo_result.admin_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_admin.result_sql_admin()


    # OsTypeList 확인
    OsTypeList = {
        "header": {
            "targetServiceName": "storage/com.tmax.tmaxcloud.storage.master.OsTypeList",
            "requestId": 1,
            "messageType": "REQUEST",
            "contentType": "TEXT"
        },
        "body": {
        }
    }

    file_path, total_num_files, base_direc= create_json_file("OsTypeList.json", OsTypeList, total_num_files)
    success_num_files, fail_num_files = sapgo_result.admin_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_admin.result_sql_admin()


    # BlkDevDomainGet 확인
    BlkDevDomainGet = {
    "header": {
        "targetServiceName": "storage/com.tmax.tmaxcloud.storage.master.BlkDevDomainGet",
        "requestId": 1,
        "messageType": "REQUEST",
        "contentType": "TEXT"
    },
    "body": {
        "id": db_sql_admin.result_BlkDevDomain
    }
    }

    file_path, total_num_files, base_direc= create_json_file("BlkDevDomainGet.json", BlkDevDomainGet, total_num_files)
    success_num_files, fail_num_files = sapgo_result.admin_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_admin.result_sql_admin()


    # FSDomain 확인
    FsDomainGet = {
        "header": {
            "targetServiceName": "storage/com.tmax.tmaxcloud.storage.master.FsDomainGet",
            "requestId": 1,
            "messageType": "REQUEST",
            "contentType": "TEXT"
        },
        "body": {
            "id": db_sql_admin.result_FSDomain_ID
        }
    }

    file_path, total_num_files, base_direc= create_json_file("FsDomainGet.json", FsDomainGet, total_num_files)
    success_num_files, fail_num_files = sapgo_result.admin_sapgo_result(base_direc,file_path, success_num_files, fail_num_files)
    db_sql_admin.result_sql_admin()

    print("total_num_files",total_num_files)
    print("success_num_files",success_num_files)
    print("fail_num_files", fail_num_files)

    with open(f'{base_direc}output.txt', 'a') as file:
        print("total_num_files:", total_num_files, file=file)
        print("success_num_files:", success_num_files, file=file)
        print("fail_num_files:", fail_num_files, file=file)

if __name__=="__main__":
    version = input("typing the tcp iaas version: ")
    admin()

