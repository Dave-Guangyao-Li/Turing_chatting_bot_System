# encoding: utf-8

# 进行语音合成并在指定路径生成对应的音频文件
# 1. 导入aip包
# 2. 设置应用信息
# 3. 进行语音合成并在指定路径生成对应的音频文件
from aip import AipSpeech
""" 你的 APPID AK SK """
APP_ID = '16658701'
API_KEY = 'F0dDiurOpIuciHnWolWMyECr'
SECRET_KEY = 'CzIkN48GcYqTws5u9SUqda8EvXenZHkX'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 进行语音合成
def speech_synthesis(FILE_PATH, text_string):
    result = client.synthesis(text_string, 'zh', 1, {'vol': 5})
    # 识别正确返回语音二进制 错误则返回dict，参照错误码
    if not isinstance(result, dict):
        with open(FILE_PATH, 'wb') as f:
            f.write(result)
    return result   # 返回二进制流文件


'''
尝试用pydub模块的audioSegment来把二进制音频文件转换为MP3再转换为wav格式，但是from_mp3方法总是出现莫名的错误，无法解决。
语音合成的结果就是mp3格式的音频，但如果直接把此非wav格式的音频用AudioSegment传入相关参数，并导出为wav格式的话，音频整体会损坏，不能正常播放。
# audiosegment = AudioSegment.from_mp3('BLACKPINK - 뚜두뚜두 (DDU-DU DDU-DU) (Korean Ver.).mp3')
# audiosegment = AudioSegment(data=r, sample_width=pyaudio.get_sample_size(FORMAT), frame_rate=RATE,
#                             channels=CHANNEL)
# audiosegment.export('test.wav', format='wav')
'''