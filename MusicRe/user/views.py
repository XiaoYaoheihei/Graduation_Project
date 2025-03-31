from django.http import JsonResponse

from user.models import User, UserTag, UserSim, UserBrowse
from playlist.models import PlayList
import time

# 获取用户全部信息表
def getAllUsers(request):
    # 传入tag和page参数
    tag = request.GET.get("tag")
    page_id = int(request.GET.get("page"))
    print("tag: %s, page_id: %s", tag, page_id)
    
    res = list()
    if tag == "all":
        # 获取全部用户信息
        user_info = User.objects.all().order_by("-u_id")
        # 拼接用户信息
        for one in user_info[(page_id - 1) * 30: page_id * 30]:
            res.append({
                "u_id": one.u_id,
                "u_name": one.u_name,
                "u_img_url": one.u_img_url
            })
    else:
        # 获取指定标签用户信息
        user_ids = UserTag.objects.filter(tag=tag).values("user_id").order_by("user_id")
        for uid in user_ids[(page_id - 1) * 30: page_id * 30]:
            one = User.objects.get(u_id=uid["user_id"])
            res.append({
                "u_id": one.u_id,
                "u_name": one.u_name,
                "u_img_url": one.u_img_url
            })
    
    return {
        "code": 1,
        "data": {
            "total": len(res),
            "sings": res,
            "tags": getAllUserTags()
        }
    }
    
# 获取所有用户标签
def getAllUserTags():
    tags = set()
    for one in UserTag.objects.all().values("tag").distinct():
        tags.add(one["tag"])
    return list(tags)

# 获取单个用户信息
def getOneUser(request):
    u_id = request.GET.get("id")
    one = User.objects.get(u_id=u_id)
    writeUserBrowse(user_name=request.GET.get("username"), click_id=u_id, click_cate="5", user_click_time=getLocalTime(), desc="查看用户")
    return JsonResponse({
        "code": 1,
        "data": [
            {
                "u_id": one.u_id,
                "u_name": one.u_name,
                "u_birthday":one.u_birthday,
                "u_gender":one.u_gender,
                "u_province":one.u_province,
                "u_city":one.u_city,
                "u_tags":one.u_tags,
                "u_img_url": one.u_img_url,
                "u_sign":one.u_sign,
                "u_rec": getOneUserSimRec(u_id),
                "u_playlist":getUserCreatePL(u_id)
            }
        ]
    })
    
# 获取单个用户的相似度推荐信息
def getOneUserSimRec(user_id):
    result = list()
    sim_users = UserSim.objects.filter(user_id=user_id).order_by("-sim").values("sim_user_id")[:10]
    for user in sim_users:
        one = User.objects.filter(u_id= user["sim_user_id"])[0]
        result.append({
            "id": one.u_id,
            "name": one.u_name,
            "img_url": one.u_img_url,
            "cate": "5"
        })
    return result

# 获取用户创建的歌单
def getUserCreatePL(user_id):
    pls = PlayList.objects.filter(pl_creator__u_id=user_id)
    result = list()
    for one in pls:
        result.append(
            {
                "pl_id": one.pl_id,
                "pl_name":  one.pl_name,
                "pl_creator": one.pl_creator.u_name,
                "pl_create_time": one.pl_create_time,
                "pl_img_url": one.pl_img_url,
                "pl_desc":  one.pl_desc
            }
        )
    return result

# 记录用户浏览信息
def writeUserBrowse(user_name = "", click_id = "", click_cate = "", user_click_time = "", desc = ""):
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