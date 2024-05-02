import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 파일 핸들러 설정
file_handler = logging.FileHandler('./logger.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)

# 포매터 설정
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 로거에 파일 핸들러 추가
logger.addHandler(file_handler)

def Getloger():
    return logger

