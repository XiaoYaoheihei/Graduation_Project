from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from index.indexTag import GetRecTags
from user.models import User, UserBrowse
from user.views import all as allUsers, writeBrowse, getLocalTime
from song.models import Song
from sing.models import Sing
from playlist.models import PlayList

# 用户选择登录
def login(request):
    if request.method == "GET":
        # 首先获取30条随机数据
        try:
            users = list(User.objects.order_by("?").values("u_id", "u_name")[:30])
            songs = list(Song.objects.order_by("?").values("song_id", "song_name")[:30])
            sings = list(Sing.objects.order_by("?").values("sing_id", "sing_name")[:20])
        except Exception as e:
            return JsonResponse({"code": 0, "error": "数据库查询失败"}, status=500)
        
        return JsonResponse({
            "code": 1,
            "data": {
                "users": {u["u_id"]: u["u_name"] for u in users},
                "songs": {s["song_id"]: s["song_name"] for s in songs},
                "sings": {si["sing_id"]: si["sing_name"] for si in sings}
            }
        })
    else:
        # 验证用户输入
        username = request.POST.get("username")
        if not username:
            return JsonResponse({"code": 0, "error": "用户名不能为空"}, status=400)
        
        # 记录用户点击信息，暂时先不支持
        # try:
        #     writeBrowse(user_name = username, user_click_time = getLocalTime(), desc = "登录系统")
        # except Exception as e:
        #     return JsonResponse({"code": 0, "error": "记录日志失败"}, status=500)
        
        # 用户的选择信息存储到Session
        request.session["username"] = username
        request.session["sings"] = request.POST.getlist("sings")
        request.session["songs"] = request.POST.getlist("songs")
        
        return JsonResponse({
            "code": 1,
            "data": {
                "username": username,
                "songs": request.session["songs"],
                "sings": request.session["sings"]
            }
        })

# 首页
def home(request):
    cate = request.GET.get("cateid")
    if "username" not in request.session.keys():  # 如果用户未登陆
        return JsonResponse({"code":0, "data":{}})
    
    if cate == "1":     # 为你推荐导航栏
        result = GetRecTags(request, request.GET.get("base_click"))
        return JsonResponse(result)
    # elif cate == "2":   # 歌单
    #     return JsonResponse( allPlayList(request) )
    # elif cate == "3":   # 歌曲
    #     return JsonResponse( allSongs(request) )
    # elif cate == "4":   # 歌手
    #     return JsonResponse( allSings(request) )
    # elif cate == "5":   # 用户
    #     return JsonResponse( allUsers(request) )
    # elif cate == "6":  # 排行榜
    #     return JsonResponse( rankResult(request) )
    # elif cate == "7":  # 我的足迹
    #     return JsonResponse( myBrowse(request) )
    

# 歌单、歌曲、歌手、用户 四个模块的推荐部分
def rec(request):
    return HttpResponse("Hello, world. You're at the polls index.")



# 下面三个不重要，先不重点考虑
# 切换用户
def switchUser(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# 获取导航栏
def getCates(reuqest):
    return HttpResponse("Hello, world. You're at the polls index.")

# 我的足迹（此功能暂定）
def myBrowse(request):
    return HttpResponse("Hello, world. You're at the polls index.")


