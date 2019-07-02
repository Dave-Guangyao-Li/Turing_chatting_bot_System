# -*- coding: utf-8 -*-
from tkinter import *
import time
import 三班.十一组.智能聊天机器人.record.records as rTools
import 三班.十一组.智能聊天机器人.recognition.voice_recognition as sTools
from 三班.十一组.智能聊天机器人.resource.generate_time_string import get_time_string
import 三班.十一组.智能聊天机器人.check.check as cTools
import 三班.十一组.智能聊天机器人.synthesis.speech_synthesis as syTools
import 三班.十一组.智能聊天机器人.resource.play as play
from os.path import join as path_join

# 可能用到的常量
# 存储所有音频文件的路径
RECORDS_FILE_PATH = r'D:/MyProgramFiles/PycharmWorkspace/课程设计/三班/十一组/智能聊天机器人/resource/'
# 图灵机器人的回复生成的MP3的格式音频文件名
ROBOT_RESPONSE_FILE_NAME = 'robotResponse_file'
# 用户的录音wav文件的文件名
USERS_RECORDS_FILE_NAME = 'usersRecords_file'
# 图灵机器人的API_KEY
API_KEY = '20e3b5d7bf4249cf872fedde5349ffe9'


# 发送按钮事件
def sendMsg():  # 发送消息
    global text
    text = txtMsg.get('0.0', END)  # 获取文本框内容
    # 在聊天内容上方加一行 显示发送人及发送时间
    strMsg = '我:' + time.strftime("%Y-%m-%d %H:%M:%S",
                                  time.localtime()) + '\n '
    txtMsgList.insert(END, strMsg, 'redcolor')
    txtMsgList.insert(END, txtMsg.get('0.0', END))
    txtMsg.delete('0.0', END)
    # 1. 触发调用图灵机器人接口,将文字传入图灵机器人
    global bot_response  # <- here
    bot_response = cTools.turing_bot(0, API_KEY, text_input=text) + '\n'
    # 文字传入图灵机器人时，触发机器人回话。图灵机器人根据传入的文字，展示结果
    robot_insertMsg()
    # 拼接生成机器人回复的音频文件的路径
    robot_response__file_path = path_join(RECORDS_FILE_PATH, get_time_string() + ROBOT_RESPONSE_FILE_NAME + '.mp3')
    # 把机器人的回复转换成语音,语音合成方法返回值是二进制文件流
    syTools.speech_synthesis(robot_response__file_path, bot_response)  # 调用语音合成方法
    # 把转化好的wav格式的语音在后台进行播放
    # strMsg = 'robot11:' + time.strftime("%Y-%m-%d %H:%M:%S",
    #                                     time.localtime()) + '\n '
    # txtMsgList.insert(END, strMsg, 'bluecolor')
    # robMsg = "现在来听一下机器人的回复吧~" + '\n '
    # txtMsgList.insert(END, robMsg)
    play.play_audio(robot_response__file_path)


def cancelMsg():  # 取消消息
    txtMsg.delete('0.0', END)


def sendMsgEvent(event):  # 发送消息事件
    if event.keysym == "Up":  # 用方向键↑键启动消息事件，发送消息
        sendMsg()


def human_insertMsg():
    strMsg = '我:' + time.strftime("%Y-%m-%d %H:%M:%S",
                                  time.localtime()) + '\n '
    txtMsgList.insert(END, strMsg, 'redcolor')
    txtMsgList.insert(END, result_text_string)


def robot_insertMsg():
    strMsg = '十一组的bot:' + time.strftime("%Y-%m-%d %H:%M:%S",
                                        time.localtime()) + '\n '
    txtMsgList.insert(END, strMsg, 'greencolor')
    txtMsgList.insert(END, bot_response)


def start():
    strMsg = '十一组的bot:' + time.strftime("%Y-%m-%d %H:%M:%S",
                                        time.localtime()) + '\n '
    txtMsgList.insert(END, strMsg, 'greencolor')
    robMsg = '快来跟我聊天吧。您可以选择发送文字、录音，或者一张图片的URL跟我交互~ ' + '\n'
    txtMsgList.insert(END, robMsg)


def record():
    # 拼接生成用户录音文件的路径
    users_records_file_path = path_join(RECORDS_FILE_PATH, get_time_string() + USERS_RECORDS_FILE_NAME + '.wav')
    # 1.录音
    # 2.存储到本地——resource
    rTools.record(4, users_records_file_path)
    # 3.取出音频进行解析：解析成中文
    r = sTools.recognise_local_record(users_records_file_path)
    global result_text_string  # <- here
    result_text_string = r['result'][0] + '\n'
    # 4.打印解析出来的结果
    human_insertMsg()
    # 5. 语音转化成文字后，触发调用图灵机器人接口,将转化好的文字传入图灵机器人
    global bot_response  # <- here
    bot_response = cTools.turing_bot(0, API_KEY, text_input=result_text_string) + '\n'
    # 6. 文字传入图灵机器人时，触发机器人回话。图灵机器人根据传入的文字，展示结果
    robot_insertMsg()
    # 7. 拼接生成机器人回复的音频文件的路径
    robot_response__file_path = path_join(RECORDS_FILE_PATH, get_time_string() + ROBOT_RESPONSE_FILE_NAME + '.mp3')
    # 8. 把机器人的回复转换成语音,语音合成方法返回值是二进制文件流
    syTools.speech_synthesis(robot_response__file_path, bot_response)  # 调用语音合成方法
    # 9. 把转化好的wav格式的语音在后台进行播放
    # strMsg = 'robot11:' + time.strftime("%Y-%m-%d %H:%M:%S",
    #                                     time.localtime()) + '\n '
    # txtMsgList.insert(END, strMsg, 'bluecolor')
    # robMsg = "现在来听一下机器人的回复吧~"+'\n'
    # txtMsgList.insert(END, robMsg)
    play.play_audio(robot_response__file_path)


def photo():
    global purl
    purl = txtMsg.get('0.0', END)  # 获取文本框内容
    strMsg = '我:' + time.strftime("%Y-%m-%d %H:%M:%S",
                                  time.localtime()) + '\n '
    txtMsgList.insert(END, strMsg, 'redcolor')
    txtMsgList.insert(END, txtMsg.get('0.0', END))
    txtMsg.delete('0.0', END)
    # 1. 触发调用图灵机器人接口,将图片url传入图灵机器人
    global bot_response  # <- here
    bot_response = cTools.turing_bot(1, API_KEY, image_url=purl) + '\n '
    # 2. 文字传入图灵机器人时，触发机器人回话。图灵机器人根据传入的文字，展示结果
    robot_insertMsg()
    # 3. 拼接生成机器人回复的音频文件的路径
    robot_response__file_path = path_join(RECORDS_FILE_PATH, get_time_string() + ROBOT_RESPONSE_FILE_NAME + '.mp3')
    # 8. 把机器人的回复转换成语音,语音合成方法返回值是二进制文件流
    syTools.speech_synthesis(robot_response__file_path, bot_response)  # 调用语音合成方法
    # 9. 把转化好的wav格式的语音在后台进行播放
    # strMsg = 'robot11:' + time.strftime("%Y-%m-%d %H:%M:%S",
    #                                     time.localtime()) + '\n '
    # txtMsgList.insert(END, strMsg, 'bluecolor')
    # robMsg = "现在来听一下机器人的回复吧~" + '\n '
    # txtMsgList.insert(END, robMsg)
    play.play_audio(robot_response__file_path)


# 创建窗口
t = Tk()
t.title('与十一组的bot聊天中...')
# 创建frame容器
frmLT = Frame(width=500, height=320, bg='white')
frmLC = Frame(width=500, height=150, bg='white')
frmLB = Frame(width=500, height=30)
frmRT = Frame(width=500, height=500)
# 创建控件
txtMsgList = Text(frmLT)
txtMsgList.tag_config('greencolor', foreground='#008C00')  # 创建绿色的tag
txtMsgList.tag_config('redcolor', foreground='#FF0000')  # 创建红色的tag
txtMsg = Text(frmLC)
txtMsg.bind("<KeyPress-Up>", sendMsgEvent)

btnStart = Button(frmLB, text='开 始', width=8, command=lambda: start())
btnSend = Button(frmLB, text='发 送', width=8, command=sendMsg)
btnCancel = Button(frmLB, text='取 消', width=8, command=cancelMsg)
btnRecord = Button(frmLB, text='录 音', width=8, command=lambda: record())
btnPhoto = Button(frmLB, text='图 片', width=8, command=lambda: photo())

picture = r"D:/MyProgramFiles/PycharmWorkspace/课程设计/三班/十一组/智能聊天机器人/picture/timg000.gif"
imgInfo = PhotoImage(file=picture)
lblImage = Label(frmRT, image=imgInfo)
lblImage.image = imgInfo

# 窗口布局，使用grid设置各个容器位置
frmLT.grid(row=0, column=0, columnspan=2, padx=1, pady=3)
frmLC.grid(row=1, column=0, columnspan=2, padx=1, pady=3)
frmLB.grid(row=2, column=0, columnspan=2)
frmRT.grid(row=0, column=2, rowspan=3, padx=2, pady=3)
# 固定大小
frmLT.grid_propagate(0)
frmLC.grid_propagate(0)
frmLB.grid_propagate(0)
frmRT.grid_propagate(0)
# 把元素填充进frame
btnStart.grid(row=2, column=0)
btnSend.grid(row=2, column=1)
btnCancel.grid(row=2, column=2)
btnRecord.grid(row=2, column=3)
btnPhoto.grid(row=2, column=4)
lblImage.grid()
txtMsgList.grid()
txtMsg.grid()
# 主事件循环
t.mainloop()
