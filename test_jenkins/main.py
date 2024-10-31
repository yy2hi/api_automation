from admin.test_admin import admin
from tenant.test_tenant import tenant

if __name__ == "__main__":
    version = input("Enter the TCP IaaS version: ")
    user_type = input("Enter user type (admin/tenant): ")

    if user_type.lower() == 'admin':
        admin(version)
    elif user_type.lower() == 'tenant':
        project_name = input("Enter project name: ")
        network_name = input("Enter network name: ")
        subnet_name = input("Enter subnet name: ")
        vm_name = input("Enter vm name: ")
        tenant(version, project_name, network_name, subnet_name, vm_name)
    else:
        print("Invalid user type. Please enter 'admin' or 'tenant'")