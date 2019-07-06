# -*- coding: utf-8 -*-
"""
Created on Thur July 4 13:34:10 2019
@author: 李光耀 郭余悦 马瑞鑫
"""
from tkinter import *
import tkinter.messagebox as messagebox
import pickle
import time
import 三班.十一组.智能聊天机器人.record.records as rTools
import 三班.十一组.智能聊天机器人.recognition.voice_recognition as sTools
from 三班.十一组.智能聊天机器人.resource.generate_time_string import get_time_string
import 三班.十一组.智能聊天机器人.check.check as cTools
import 三班.十一组.智能聊天机器人.synthesis.speech_synthesis as syTools
import 三班.十一组.智能聊天机器人.resource.play as play
from os.path import join as path_join
# 全局变量，代表是否显示聊天界面窗口,1代表显示，0代表不显示
global show_chat_window  # 在使用前初次声明
show_chat_window = 0    # 给全局变量赋值,默认先赋值为0，不显示
global usr_name  # 用户名
global usr_pwd  # 用户密码

# 可能用到的常量
# 存储所有音频文件的路径
RECORDS_FILE_PATH = r'D:/MyProgramFiles/PycharmWorkspace/课程设计/三班/十一组/智能聊天机器人/resource/'
# 图灵机器人的回复生成的MP3的格式音频文件名
ROBOT_RESPONSE_FILE_NAME = 'robotResponse_file'
# 用户的录音wav文件的文件名
USERS_RECORDS_FILE_NAME = 'usersRecords_file'
# 图灵机器人的API_KEY
API_KEY = '20e3b5d7bf4249cf872fedde5349ffe9'
# 图片文件的路径
IMAGE_PATH = r'D:/MyProgramFiles/PycharmWorkspace/课程设计/三班/十一组/智能聊天机器人/picture/'
# 存储用户信息的文件路径
USER_INFO_FILE = r'D:/MyProgramFiles/PycharmWorkspace/课程设计/三班/十一组/智能聊天机器人/user/'


# 开始弹出的登录窗口
window_login = Tk()  # 创建开始的登录窗口
window_login.title('欢迎进入智能聊天机器人系统')  # 登录窗口标题
window_login.geometry('450x300')  # 设置窗口大小

# 画布放置图片
backgroud_pic = IMAGE_PATH + 'background_pic.gif'
canvas = Canvas(window_login, height=300, width=500)
imagefile = PhotoImage(file=backgroud_pic)
image = canvas.create_image(0, 0, anchor='nw', image=imagefile)
canvas.pack(side='top')
# 标签 用户名密码
Label(window_login, text='用户名:').place(x=100, y=150)
Label(window_login, text='密码:').place(x=100, y=190)
# 用户名输入框
var_usr_name = StringVar()
entry_usr_name = Entry(window_login, textvariable=var_usr_name)
entry_usr_name.place(x=160, y=150)
# 密码输入框
var_usr_pwd = StringVar()
entry_usr_pwd = Entry(window_login, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=160, y=190)


# 登录函数
def usr_log_in():
    # 输入框获取用户名密码
    global usr_name
    global usr_pwd
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    # 从本地字典获取用户信息，如果没有则新建本地数据库
    try:
        with open(USER_INFO_FILE + 'usr_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        with open(USER_INFO_FILE + 'usr_info.pickle', 'wb') as usr_file:
            usrs_info = {'admin': 'admin'}
            pickle.dump(usrs_info, usr_file, 0)
    # 判断用户名和密码是否匹配
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            messagebox.showinfo(title='welcome',
                                   message='欢迎您：' + usr_name)
            # 登录成功关闭登录框，进入聊天界面
            window_login.destroy()
            global show_chat_window
            show_chat_window = 1
        else:
            messagebox.showerror(message='密码错误')
    # 用户名密码不能为空
    elif usr_name == '' or usr_pwd == '':
        messagebox.showerror(message='用户名或密码为空')
    # 不在数据库中弹出是否注册的框
    else:
        is_signup = messagebox.askyesno('欢迎', '您还没有注册，是否现在注册')
        if is_signup:
            usr_sign_up()


# 注册函数
def usr_sign_up():
    # 确认注册时的相应函数
    def signtowcg():
        # 获取输入框内的内容
        nn = new_name.get()
        np = new_pwd.get()
        npf = new_pwd_confirm.get()

        # 本地加载已有用户信息,如果没有则已有用户信息为空
        try:
            with open(USER_INFO_FILE + 'usr_info.pickle', 'rb') as usr_file:
                exist_usr_info = pickle.load(usr_file)
        except FileNotFoundError:
            exist_usr_info = {}

            # 检查用户名存在、密码为空、密码前后不一致
        if nn in exist_usr_info:
            messagebox.showerror('错误', '用户名已存在')
        elif np == '' or nn == '':
            messagebox.showerror('错误', '用户名或密码为空')
        elif np != npf:
            messagebox.showerror('错误', '密码前后不一致')
        # 注册信息没有问题则将用户名密码写入数据库
        else:
            exist_usr_info[nn] = np
            with open(USER_INFO_FILE + 'usr_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file, 0)
            messagebox.showinfo('欢迎', '注册成功')
            # 注册成功关闭注册框
            window_sign_up.destroy()

    # 新建注册界面
    window_sign_up = Toplevel(window_login)
    window_sign_up.geometry('350x200')
    window_sign_up.title('注册')
    # 用户名变量及标签、输入框
    new_name = StringVar()
    Label(window_sign_up, text='用户名：').place(x=10, y=10)
    Entry(window_sign_up, textvariable=new_name).place(x=150, y=10)
    # 密码变量及标签、输入框
    new_pwd = StringVar()
    Label(window_sign_up, text='请输入密码：').place(x=10, y=50)
    Entry(window_sign_up, textvariable=new_pwd, show='*').place(x=150, y=50)
    # 重复密码变量及标签、输入框
    new_pwd_confirm = StringVar()
    Label(window_sign_up, text='请再次输入密码：').place(x=10, y=90)
    Entry(window_sign_up, textvariable=new_pwd_confirm, show='*').place(x=150, y=90)
    # 确认注册按钮及位置
    bt_confirm_sign_up = Button(window_sign_up, text='确认注册',
                                   command=signtowcg)
    bt_confirm_sign_up.place(x=150, y=130)


# # 退出的函数
# def usr_sign_quit():
#     window_login.destroy()
#     # 代表是否显示聊天界面窗口,1代表显示，0代表不显示
#     global show_chat_window
#     show_chat_window = 0


# 登录 注册按钮
bt_login = Button(window_login, text='登录', command=usr_log_in)
bt_login.place(x=140, y=230)
bt_logup = Button(window_login, text='注册', command=usr_sign_up)
bt_logup.place(x=280, y=230)
# bt_logquit = Button(window_login, text='退出', command=usr_sign_quit)
# bt_logquit.place(x=280, y=230)
# 主循环
window_login.mainloop()


# 聊天窗口部分的函数
# 发送按钮事件对应的函数
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


# # 如果全局变量为0则不会创建录音提示窗口
# if show_record_window:
#     # 建立窗口window
#     window_record = Tk()
#     # 给窗口的可视化起名字
#     window_record.title('录音中...')
#     # 设定窗口的大小(长＊宽)
#     window_record.geometry('400x100')
#     # 在图形界面上设定标签
#     l = Label(window_record, text='正在录音中，持续时间4秒，请说句话吧：', bg='red', font=('Arial,12'), width=100, height=2)
#     # 说明： bg为背景，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
#     # 安置标签
#     l.pack()
#     # 主事件循环
#     window_record.mainloop()


def record():
    # 拼接生成用户录音文件的路径
    users_records_file_path = path_join(RECORDS_FILE_PATH, get_time_string() + USERS_RECORDS_FILE_NAME + '.wav')
    # 录音
    # 存储到本地——resource
    # # 录音的过程中跳出提示正在录音的一个界面
    # global show_record_window
    # show_record_window = 1
    rTools.record(4, users_records_file_path)
    # 录音结束后自动关闭提示录音窗口
    # window_record.destroy()
    # 重新置全局变量为0
    # show_record_window = 0
    # 取出音频进行解析：解析成中文
    # 录音结束后弹出提示框提示录音已结束
    messagebox.showinfo(title='提示', message='录音已结束！')
    r = sTools.recognise_local_record(users_records_file_path)
    global result_text_string  # <- here
    try:
        result_text_string = r['result'][0] + '\n'
    except KeyError as e:
        messagebox.showerror('错误','录音不清晰，识别失败，请重试！')
    # 打印解析出来的结果
    human_insertMsg()
    # 语音转化成文字后，触发调用图灵机器人接口,将转化好的文字传入图灵机器人
    global bot_response  # <- here
    bot_response = cTools.turing_bot(0, API_KEY, text_input=result_text_string) + '\n'
    # 文字传入图灵机器人时，触发机器人回话。图灵机器人根据传入的文字，展示结果
    robot_insertMsg()
    # 拼接生成机器人回复的音频文件的路径
    robot_response__file_path = path_join(RECORDS_FILE_PATH, get_time_string() + ROBOT_RESPONSE_FILE_NAME + '.mp3')
    # 把机器人的回复转换成语音,语音合成方法返回值是二进制文件流
    syTools.speech_synthesis(robot_response__file_path, bot_response)  # 调用语音合成方法
    # 把转化好的wav格式的语音在后台进行播放
    play.play_audio(robot_response__file_path)


if show_chat_window:
    global usr_name
    # 如果全局变量为0则不会创建聊天窗口
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
    labelUser = Label(frmLB, text='当前用户：' + usr_name)
    bot_picture = IMAGE_PATH + 'bot_pic.gif'
    imgInfo = PhotoImage(file=bot_picture)
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
    labelUser.grid(row=2, column=5)
    lblImage.grid()
    txtMsgList.grid()
    txtMsg.grid()
    # 主事件循环
    t.mainloop()
