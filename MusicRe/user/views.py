import time
from django.shortcuts import render


def wirteBrowse(user_name = "", click_id = "", click_cate = "", user_click_time = "", desc = ""):
    if "12797496" in click_id: click_id = "12797496"
    UserBrowse(user_name=user_name,
               click_id=click_id,
               click_cate=click_cate,
               user_click_time = user_click_time,
               desc=desc).save()
    print("用户【 %s 】的行为记录【 %s 】写入数据库" % (user_name, desc))

# 获取当前格式化的系统时间
def getLocalTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())