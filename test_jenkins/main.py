import argparse
from admin.admin_operations import admin
from tenant.tenant_operations import tenant

def main():
    # 명령줄 옵션으로 기본값 설정
    parser = argparse.ArgumentParser(description="Execute admin or tenant operations based on user type.")
    parser.add_argument("--version", default=None, help="TCP IaaS version")
    parser.add_argument("--user_type", default=None, choices=["admin", "tenant"], help="User type (admin/tenant)")
    parser.add_argument("--project_name", default=None, help="Project name (required if user_type is tenant)")
    parser.add_argument("--network_name", default=None, help="Network name (required if user_type is tenant)")
    parser.add_argument("--subnet_name", default=None, help="Subnet name (required if user_type is tenant)")
    parser.add_argument("--vm_name", default=None, help="VM name (required if user_type is tenant)")

    args = parser.parse_args()

    # input()과 명령줄 인수 병합
    version = args.version or input("Enter the TCP IaaS version: ")
    user_type = args.user_type or input("Enter user type (admin/tenant): ").lower()

    if user_type == 'admin':
        admin(version)
    elif user_type == 'tenant':
        project_name = args.project_name or input("Enter project name: ")
        network_name = args.network_name or input("Enter network name: ")
        subnet_name = args.subnet_name or input("Enter subnet name: ")
        vm_name = args.vm_name or input("Enter vm name: ")
        tenant(version, project_name, network_name, subnet_name, vm_name)
    else:
        print("Invalid user type. Please enter 'admin' or 'tenant'")

if __name__ == "__main__":
    main()

