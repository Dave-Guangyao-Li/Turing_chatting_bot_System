# encoding: utf-8
# 调用对应的应用打开指定路径下的文件
# import os
#
#
# def play_file(filepath):
#     os.system('start ' + filepath)
# -*-coding:utf-8-*-
# 引入模块
# from pyaudio import *
# import wave
from playsound import playsound

# 不用弹出音乐播放软件的窗口而在后台直接播放音频的方法，利用playsound模块中的方法
def play_audio(filepath):
    playsound(filepath)
    print('语音播放结束！')
    '''
    这是在后台直接播放wav格式的音频文件的方法。但是因为进行语音合成之后转换mp3再转换为wav的尝试失败，因此不能用
    只能播放wav格式的音频，如果尝试播放其他类型的文件会提示文件头没有RIFF的ID，无法播放
    # chunk = 1024  # 指定WAV文件的大小
    # wf = wave.open(r'D:/MyProgramFiles/PycharmWorkspace/课程设计/三班/十一组/智能聊天机器人/resource/test_file.wav', 'rb')  # 打开WAV文件
    # p = PyAudio()  # 初始化PyAudio模块
    #
    # # 打开一个数据流对象，解码而成的帧将直接通过它播放出来，我们就能听到声音啦
    # stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
    #                 rate=wf.getframerate(), output=True)
    #
    # data = wf.readframes(chunk)  # 读取第一帧数据
    # print(data)  # 以文本形式打印出第一帧数据，实际上是转义之后的十六进制字符串
    #
    # # 播放音频，并使用while循环继续读取并播放后面的帧数
    # # 结束的标志为wave模块读到了空的帧
    # while data != b'':
    #     stream.write(data)  # 将帧写入数据流对象中，以此播放之
    #     data = wf.readframes(chunk)  # 继续读取后面的帧
    #
    # stream.stop_stream()  # 停止数据流
    # stream.close()  # 关闭数据流
    # p.terminate()  # 关闭 PyAudio
    # print('语音播放结束！')
    '''
