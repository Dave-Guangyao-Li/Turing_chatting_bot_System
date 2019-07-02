# 获取当前时间的格式化字符串
from time import strftime, localtime


# 获取当前时间字符串并格式化，作为文件名的一部分
def get_time_string():
    time_now = strftime("%Y-%m-%d-%H_%M_%S_", localtime())
    return time_now