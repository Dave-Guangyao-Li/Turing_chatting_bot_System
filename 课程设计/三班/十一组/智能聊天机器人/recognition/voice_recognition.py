# 1. 导入aip包
# 2. 设置应用信息
# 3. 从文件中获取语音进行识别

from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '16658701'
API_KEY = 'F0dDiurOpIuciHnWolWMyECr'
SECRET_KEY = 'CzIkN48GcYqTws5u9SUqda8EvXenZHkX'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)  # 创建一个AipSpeech类的对象


# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:  # 打开文件流，读取内容
        return fp.read()


# 识别本地文件，将此功能整体封装成一个函数
def recognise_local_record(filepath):
    result = client.asr(get_file_content(filepath), 'wav', 16000, {'dev_pid': 1536})
    return result
