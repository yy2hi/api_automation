import os
import json
import db_sql_admin
import subprocess
import re
import time

def admin_sapgo_result(base_direc,file_path, success_num_files, fail_num_files):
    command = "java -jar /home/sasctl/sasctl-1.9.1.jar 172.31.5.7:38080 apply -f "
    command += file_path
    output = subprocess.getoutput(command)
    #print("output: ", repr(output))

    cleaned_output = re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]', '', output)
    cleaned_output = "\n".join(cleaned_output.split("\n")[1:])
    #print("cleand_output: ", cleaned_output)

    try:
        json_data = json.loads(cleaned_output)
        print("Parsed JSON data:", json_data)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
        fail_num_files += 1
        print("result: fail")
        with open(f'{base_direc}output.txt', 'a') as file:
            print("JSON decode error:", e, file=file)
            print("result: fail", file=file)
            print("-" * 80, file=file)

    # response_value = json_data['response_of']
    # print("response_of: ", response_value)
    filename = os.path.basename(file_path)
    file_without_extension = os.path.splitext(filename)[0]
    print("service name: ", file_without_extension)
    with open(f'{base_direc}output.txt', 'a') as file:
        print("service name: ", file_without_extension, file=file)

    status_value = json_data['status']
    print("status value: ", status_value)
    with open(f'{base_direc}output.txt', 'a') as file:
        print("status value: ", status_value, file=file)

    if status_value == -1:
        fail_num_files += 1
        print("result: fail")
        print("-" * 80)
        with open(f'{base_direc}output.txt', 'a') as file:
            print("result: fail", file=file)
            print("-"* 80, file=file)

    elif status_value == 1:
        success_num_files += 1
        print("result: success")
        print("-" * 80)
        with open(f'{base_direc}output.txt', 'a') as file:
            print("result: success", file=file)
            print("-"* 80, file=file)

    time.sleep(2)

    return success_num_files, fail_num_files