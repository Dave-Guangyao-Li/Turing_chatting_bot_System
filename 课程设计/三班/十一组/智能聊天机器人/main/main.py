# encoding: utf-8
#顶层文件：用于调用其他所有的文件
# 主业务流程，在控制台执行软件的主要流程

import 三班.十一组.智能聊天机器人.record.records as rTOOLS
import 三班.十一组.智能聊天机器人.recognition.voice_recognition as recTools
import 三班.十一组.智能聊天机器人.synthesis.speech_synthesis as synTools
import 三班.十一组.智能聊天机器人.check.check as botTools
import 三班.十一组.智能聊天机器人.resource.play as play
import 三班.十一组.智能聊天机器人.resource.generate_time_string as timeTools
from os.path import join as path_join

# 可能用到的常量
# 要发送的图片的URL
IMG_URL='https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1562321181&di=0978be38fd3a2c9386c8e1035fb86790&imgtype=jpg&er=1&src=http%3A%2F%2Fpic15.nipic.com%2F20110703%2F7727434_193100046150_2.jpg'
# 存储所有音频文件的路径
RECORDS_FILE_PATH = r'D:/MyProgramFiles/PycharmWorkspace/课程设计/三班/十一组/智能聊天机器人/resource/'
# 图灵机器人的回复生成的MP3的格式音频文件名
ROBOT_RESPONSE = 'robotResponse_file'
# 用户的录音wav文件的文件名
USERS_RECORDS = 'usersRecords_file'
# 图灵机器人的API_KEY
API_KEY = '20e3b5d7bf4249cf872fedde5349ffe9'


print('欢迎来到智能机器人聊天系统~')
choose_continue = 1
while choose_continue:
    type_num_input = int(input('请选择输入方式：0 为录音输入，1 为图片URL输入，2为文字输入：'))
    # 输入
    if type_num_input == 0:
        print("现在请说一段话吧，之后您的语音会被自动存储并解析成文字：")
        # 拼接生成用户录音文件的路径
        users_records_file_path = path_join(RECORDS_FILE_PATH, timeTools.get_time_string() + USERS_RECORDS + '.wav')
        # 录音
        # 存储到本地——存到resource文件夹下
        rTOOLS.record(4, users_records_file_path)
        # 取出音频进行解析,解析成中文
        print("开始解析录音...")
        r = recTools.recognise_local_record(users_records_file_path)
        print('录音文字解析完毕！')
        # 储存解析出来的文字
        result_text_string = r['result'][0]
        # 打印解析出来的结果
        print('我说：' + result_text_string)
        # 语音转化成文字后，触发调用图灵机器人接口,将转化好的文字传入图灵机器人
        bot_response = botTools.turing_bot(type_num_input, API_KEY, text_input=result_text_string)
        # 文字传入图灵机器人时，触发机器人回话。图灵机器人根据传入的文字，展示结果
        print('机器人的回答：' + bot_response)
        # 拼接生成机器人回复的音频文件的路径
        robot_response__file_path = path_join(RECORDS_FILE_PATH, timeTools.get_time_string() + ROBOT_RESPONSE + '.mp3')
        # 把机器人的回复转换成语音,语音合成方法返回值是二进制文件流
        synTools.speech_synthesis(robot_response__file_path, bot_response)  # 调用语音合成方法
        # 把转化好的wav格式的语音在后台进行播放
        print("机器人正在说话...")
        play.play_audio(robot_response__file_path)
    elif type_num_input == 1:
        image_url_string = input('请您发送一个图片的URL给机器人吧:\n')
        # 调用图灵机器人接口,将图片的url传入图灵机器人
        bot_response = botTools.turing_bot(type_num_input, API_KEY, image_url=image_url_string)
        # 文字传入图灵机器人时，触发机器人回话。图灵机器人根据传入的文字，展示结果
        print('机器人的回答：' + bot_response)
        # 拼接生成机器人回复的音频文件的路径
        robot_response__file_path = path_join(RECORDS_FILE_PATH, timeTools.get_time_string() + ROBOT_RESPONSE + '.mp3')
        # 把机器人的回复转换成语音,语音合成方法返回值是二进制文件流
        synTools.speech_synthesis(robot_response__file_path, bot_response)  # 调用语音合成方法
        # 把转化好的wav格式的语音在后台进行播放
        print("机器人正在说话...")
        play.play_audio(robot_response__file_path)
    elif type_num_input == 2:
        result_text_string = input("请打字输入一段文字：")
        # 打印结果至窗口界面
        print('我说：' + result_text_string)
        # 调用图灵机器人接口,将文字传入图灵机器人
        bot_response = botTools.turing_bot(apikey=API_KEY, type_num=0, text_input=result_text_string)
        # 文字传入图灵机器人时，触发机器人回话。图灵机器人根据传入的文字，展示结果
        print('机器人的回答：' + bot_response)
        # 拼接生成机器人回复的音频文件的路径
        robot_response__file_path = path_join(RECORDS_FILE_PATH, timeTools.get_time_string() + ROBOT_RESPONSE + '.mp3')
        # 把机器人的回复转换成语音,语音合成方法返回值是二进制文件流
        synTools.speech_synthesis(robot_response__file_path, bot_response)  # 调用语音合成方法
        # 把转化好的wav格式的语音在后台进行播放
        print("机器人正在说话...")
        play.play_audio(robot_response__file_path)
    else:
        print("输入有误，请输入0（录音）或1（图片URL）或2（文字输入）！")
    choose_continue = int(input("是否要继续聊天，请输入数字进行选择：1：继续  0：退出："))
