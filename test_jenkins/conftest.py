# conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption("--version", action="store", default="1.0", help="TCP IaaS 버전")
    parser.addoption("--project_name", action="store", default="test_project", help="Project Name")
    parser.addoption("--network_name", action="store", default="test_network", help="Network Name")
    parser.addoption("--subnet_name", action="store", default="test_subnet", help="Subnet Name")
    parser.addoption("--vm_name", action="store", default="test_vm", help="VM Name")

@pytest.fixture
def tenant_params(request):
    return {
        "version": request.config.getoption("--version"),
        "project_name": request.config.getoption("--project_name"),
        "network_name": request.config.getoption("--network_name"),
        "subnet_name": request.config.getoption("--subnet_name"),
        "vm_name": request.config.getoption("--vm_name")
    }
