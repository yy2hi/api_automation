import os
import json
import subprocess
import re
from .config import API_ENDPOINT, SASCTL_JAR_PATH

def create_json_file(file_name, data, base_dir):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)
        
    file_path = os.path.join(base_dir, file_name)
    
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        
    return file_path

def process_api_request(file_path, logger):
    command = f"java -jar {SASCTL_JAR_PATH} {API_ENDPOINT} apply -f {file_path}"
    output = subprocess.getoutput(command)
    
    cleaned_output = re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]', '', output)
    cleaned_output = "\n".join(cleaned_output.split("\n")[1:])
    
    try:
        json_data = json.loads(cleaned_output)
        status = json_data.get('status')
        
        if status == 1 or status == '1' or status == 0 or status == '0':
            logger.info(f"Success: {file_path}")
            return True
        else:
            logger.error(f"Failed: {file_path}")
            return False
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        return False