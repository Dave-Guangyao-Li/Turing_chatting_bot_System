# encoding: utf-8
# 图灵机器人接口
import requests
import json

API_URL = "http://openapi.tuling123.com/openapi/api/v2"

# 函数,用来获得图灵机器人回复字符串
def turing_bot(type_num, apikey, text_input='', image_url=''):
    # 请求字符串
    req = {
        "reqType": type_num,
        "perception":
            {
                "inputText":
                    {
                        "text": text_input
                    },
                "inputImage":
                    {  # 图片信息，后跟参数信息为url地址，string类型
                        "url": image_url
                    },
                "selfInfo":
                    {
                        "location":
                            {
                                "city": "晋中",
                                "province": "山西",
                                "street": "大学街"
                            }
                    }
            },

        "userInfo":
            {
                "apiKey": apikey,
                "userId": "DaveyLgy"
            }
    }
    # 利用request的post方法获取请求参数字符串
    res = requests.post(url=API_URL, json=req)
    # 调用json模块的loads方法将json串先转化为字典，才能利用下标、键拿到字典的值，res存储返回的结果
    res = json.loads(res.text)
    # 用下标和对应的键取出结果字典中对应位置的的机器人回复的字符串
    results_text = res['results'][0]['values']['text']
    # 返回结果字符串
    return results_text

