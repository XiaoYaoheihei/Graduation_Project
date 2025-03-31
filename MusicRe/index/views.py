from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from tagrec.views import GetRecTags
from playlist.models import PlayList
from playlist.views import getAllPlayList
from song.models import Song
from song.views import getAllSongs
from sing.models import Sing
from sing.views import getAllSings
from user.models import User
from user.views import getAllUsers, writeUserBrowse, getLocalTime
from rec.views import rec_sim_playlist, rec_sim_song, rec_sim_sing, rec_sim_user

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
        
        # 记录用户浏览信息
        writeUserBrowse(user_name = username, user_click_time = getLocalTime(), desc = "登录系统")
        
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
    elif cate == "2":   # 歌单导航栏
        return JsonResponse( getAllPlayList(request) )
    elif cate == "3":   # 歌曲导航栏
        return JsonResponse( getAllSongs(request) )
    elif cate == "4":   # 歌导航栏
        return JsonResponse( getAllSings(request) )
    elif cate == "5":   # 用户导航栏
        return JsonResponse( getAllUsers(request) )
    # elif cate == "6":  # 排行榜
    #     return JsonResponse( rankResult(request) )
    # elif cate == "7":  # 我的足迹
    #     return JsonResponse( myBrowse(request) )
    

# 歌单、歌曲、歌手、用户 四个模块根据相似度推荐
def rec(request):
    cate = request.GET.get("cateid")
    if "username" not in request.session.keys():
        return JsonResponse({"code": 0, "data": {}})

    if cate == "2":  # 推荐歌单信息
        result = rec_sim_playlist(request)
        return JsonResponse( result )
    elif cate == "3": # 推荐歌曲
        result = rec_sim_song(request)
        return JsonResponse( result )
    elif cate == "4": # 推荐歌手
        result = rec_sim_sing(request)
        return JsonResponse(result)
    elif cate == "5": # 推荐用户
        result = rec_sim_user(request)
        return JsonResponse(result)
    else:  # 其他
        return JsonResponse({"code": 1, "data": {}})



# 下面三个不重要，先不重点考虑
# 切换用户
def switchUser(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# 获取导航栏
def getCates(reuqest):
    return HttpResponse("Hello, world. You're at the polls index.")

# 我的足迹（此功能先不着急）
def myBrowse(request):
    return HttpResponse("Hello, world. You're at the polls index.")


