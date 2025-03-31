from django.http import JsonResponse

from playlist.models import PlayList, PlayListToTag, PlayListToSongs
from song.models import Song
from sing.models import Sing
from user.views import writeUserBrowse, getLocalTime


# 获取所有歌单信息
def getAllPlayList(request):
    # 接口传入的tag、page参数
    tag = request.GET.get("tag")
    page_id = int(request.GET.get("page"))
    print("tag : %s, page_id: %s" % (tag,page_id))
    if page_id < 1:
        return {"code": 0, "msg": "页码无效"}
    
    if tag == "all":
        play_lists = PlayList.objects.all().order_by("-pl_create_time")
    else:
        play_lists = PlayList.objects.filter(pl_tags__contains=tag).order_by("-pl_create_time")
    total = len(play_lists)
    res = list()
    # 分页处理数据
    for one in play_lists[(page_id-1) * 30: page_id * 30]:
        res.append({
            "pl_id": one.pl_id,
            "pl_creator": one.pl_creator.u_name,
            "pl_name": one.pl_name,
            "pl_img_url": one.pl_img_url
        })
    return {
        "code": 1,
        "data": {
            "total": total,
            "playlist": res,
            "tags": getAllPlayListTags()
        }
        }

# 获取所有歌单标签
def getAllPlayListTags():
    tags = set()
    for one in PlayListToTag.objects.all().values("tag"):
        tags.add(one["tag"])
    return list(tags)


# 获取单个歌单信息
def getOnePlayList(request):
    playlist_id = request.GET.get("id")
    # 记录浏览信息
    writeUserBrowse(user_name=request.GET.get("username"), click_id=playlist_id, click_cate="2", user_click_time=getLocalTime(), desc="查看歌单")
    one = PlayList.objects.filter(pl_id=playlist_id)[0]
    return JsonResponse({
        "code":1,
        "data":[
            {
                "pl_id":one.pl_id,
                "pl_creator": one.pl_creator.u_name,
                "pl_name": one.pl_name,
                "pl_create_time": one.pl_create_time,
                "pl_update_time": one.pl_update_time,
                "pl_songs_num": one.pl_songs_num,
                "pl_listen_num": one.pl_listen_num,
                "pl_share_num": one.pl_share_num,
                "pl_comment_num": one.pl_comment_num,
                "pl_follow_num": one.pl_follow_num,
                "pl_tags": one.pl_tags,
                "pl_img_url": one.pl_img_url,
                "pl_desc": one.pl_desc,
                "pl_rec": getRecBasedOne(playlist_id),
                "pl_songs": getIncludeSong(playlist_id)
            }
        ]
    })

# 根据歌单ID获取其他具有相同或部分相同标签的歌单
def getRecBasedOne(playlist_id):
    pl_tags = PlayList.objects.filter(pl_id=playlist_id).values("pl_tags").first()["pl_tags"]
    pl_tags_list = pl_tags.replace(" ","").split(",")
    print(pl_tags_list)
    
    # 查询所有标签相等的歌单，并排除自身
    base_results = list(PlayList.objects.filter(
        pl_tags=pl_tags
    ).exclude(pl_id=playlist_id))
    # 扩展匹配标签记录
    if len(results) < 10:
        # 预先收集所有可能的候选歌单并去重
        candidates = PlayList.objects.filter(pl_tags__icontains__in=pl_tags_list).exclude(pl_id=playlist_id)
        results = list(base_results) + list(candidates)
        unique_results = list({pl.pl_id: pl for pl in results}.values())
        results = unique_results[:10]
    else:
        results = list(base_results)[:10]
    # print(results)
    # 拼接返回结果
    rec_pl_list = list()
    for one in results:
        rec_pl_list.append({
            "id": one.pl_id,
            "name": one.pl_name,
            "creator": one.pl_creator.u_name,
            "img_url": one.pl_img_url,
            "cate": "2"
        })
    return rec_pl_list

# 根据歌单ID获取该歌单包含的所有歌曲信息
def getIncludeSong(pl_id):
    result = list()
    song_ids = PlayListToSongs.objects.filter(pl_id=pl_id).values_list("song_id", flat=True)
    if not song_ids:
        return []
     
    # 批量查询歌曲和歌手（减少数据库访问）
    songs = Song.objects.filter(song_id__in=song_ids).select_related('song_sing_id')
    song_sing_ids = set()
    for song in songs:
        if "#" in song.song_sing_id:
            song_sing_ids.update(song.song_sing_id.split("#"))
        else:
            song_sing_ids.add(song.song_sing_id)
    
    # 批量查询歌手
    singers = {s.sing_id: s.sing_name for s in Sing.objects.filter(sing_id__in=song_sing_ids)}
    
    # 构建结果
    result = []
    for song in songs:
        sing_ids = song.song_sing_id.split("#") if "#" in song.song_sing_id else [song.song_sing_id]
        sing_names = []
        for sid in sing_ids:
            if sid in singers:
                sing_names.append(singers[sid])
        # 合并歌手名（去除空值）
        song_sing_name = ", ".join([name for name in sing_names if name])
        
        result.append({
            "song_id": song.song_id,
            "song_name": song.song_name,
            "song_sing_name": song_sing_name or "",
            "song_url": song.song_url
        })
    return result