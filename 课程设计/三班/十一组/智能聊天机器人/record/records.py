import pyaudio
import wave

# 定义音频采样的一些相关常量
# 采样率（每秒截取多少个样本，声音截取的密度）
RATE = 8000
# 采样管道数（有几个管道同时采样）
CHANNEL = 2
# 量化位数（bit）
FORMAT = pyaudio.paInt16


# 模块 1.内置模块 2. 自定义模块 3. 第三方模块

# 封装一个函数，seconds:录音的时长 filename:录好音之后的文件名（路径）
def record(seconds, filename):
    # 录音时长
    SECONDS = seconds
    # 创建音频对象
    p = pyaudio.PyAudio()
    # 开启数据流
    stream = p.open(rate=RATE, channels=CHANNEL, format=FORMAT, input=True)
    # 创建数据仓库
    frames = []
    # 打印提示语句
    print("开始录音，您还有" + str(SECONDS) + "秒的时间")
    # 开始录音
    data = stream.read(RATE * SECONDS)
    # 存储数据
    frames.append(data)
    # 停止录音
    stream.stop_stream()
    # 释放资源
    stream.close()
    # 关闭会话（音频对象）
    p.terminate()
    print("录音结束")

    # 将录好的的音频数据存储到本地文件中（wav）
    wf = wave.open(filename, 'wb')
    # 设置管道数量
    wf.setnchannels(CHANNEL)
    # 设置采样率
    wf.setframerate(RATE)
    # 设置量化位数
    wf.setsampwidth(p.get_sample_size(FORMAT))
    # 将数据存储起来
    wf.writeframes(b''.join(frames))  # frames是数据
    # 关闭资源
    wf.close()
    return filename
