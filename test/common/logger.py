import os
import logging
from .config import BASE_DIR

def setup_logger(name, version, log_type):
    # 로그 디렉토리 생성
    log_dir = os.path.join(BASE_DIR, version)
    os.makedirs(log_dir, exist_ok=True)
        
    log_file = os.path.join(log_dir, f'{log_type}_output.log')
    
    # 로거 설정
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # 기존 핸들러 제거
    if logger.handlers:
        logger.handlers = []
    
    # 파일 핸들러 설정
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setLevel(logging.INFO)
    
    # 포맷터 설정
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger