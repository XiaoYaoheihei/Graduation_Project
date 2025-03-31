from django.http import JsonResponse

from song.models import Song, SongLysic, SongTag, SongSim
from sing.models import Sing
from user.views import writeUserBrowse, getLocalTime

# 获取全部歌曲信息
def getAllSongs(request):
    # 传入tag和page参数
    tag = request.GET.get("tag")
    page_id = int(request.GET.get("page"))
    print("tag: %s, page_id: %s", tag, page_id)
    
    res = list()
    if tag == "all":
        # 获取全部歌曲信息
        song_info = Song.objects.all().values("song_id","song_name","song_publish_time").order_by("-song_publish_time")
        # 分页获取信息
        for one in song_info[(page_id-1) * 30: page_id * 30]:
            res.append({
                "song_id": one["song_id"],
                "song_name": one["song_name"],
                "song_publish_time": one["song_publish_time"]
            })
    else:
        # 获取指定标签的全部歌曲信息
        song_tags_list = SongTag.objects.filter(tag=tag).values("song_id").order_by("song_id")
        song_ids = [song["song_id"] for song in song_tags_list[(page_id-1) * 30: page_id * 30]]
        songs_list = Song.objects.filter(song_id__in=song_ids).values("song_id","song_name","song_publish_time")
        for one in songs_list:
            res.append({
                "song_id": one["song_id"],
                "song_name": one["song_name"],
                "song_publish_time": one["song_publish_time"]
            })
    return {
        "code": 1,
        "data": {
            "total": len(song_tags_list),
            "songs": res,
            "tags": getAllSongTags()
        }
    }
    
# 获取全部歌曲信息的标签信息
def getAllSongTags():
    tags = set()
    for one in SongTag.objects.all().values("tag").distinct():
        tags.add(one["tag"])
    return list(tags)

# 获取单个歌曲的信息
def getOneSong(request):
    song_id = request.GET.get("id")
    song = Song.objects.filter(song_id=song_id)[0]
    
    s_name = list()
    if "#" in song.song_sing_id:
        for s_one in song.song_sing_id.split("#"):
            s_name.append(Sing.objects.filter(sing_id=s_one)[0].sing_name)
    else:
        s_name.append(Sing.objects.filter(sing_id=song.song_sing_id)[0].sing_name)
    song_lysic = SongLysic.objects.filter(song_id=song_id)[0]
    writeUserBrowse(user_name=request.GET.get("username"), click_id=song_id, click_cate="3", user_click_time=getLocalTime(), desc="查看歌曲")
    return JsonResponse({
        "code":1,
        "data":[
            {
                "song_id": song.song_id,
                "song_name": song.song_name,
                "song_playlist": song.song_pl_id,
                "song_publish_time": song.song_publish_time,
                "song_sing":" / ".join(s_name),
                "song_total_comments": song.song_total_comments,
                "song_hot_comments": song.song_hot_comments,
                "song_url":song.song_url,
                "song_lysic": song_lysic.song_lysic,
                "song_rec": getOneSimRecBased(song_id)
            }
        ]
    })
    
# 获取单个歌曲的相似度推荐信息
def getOneSimRecBased(song_id):
    result = list()
    songs = SongSim.objects.filter(song_id=song_id).order_by("-sim").values("sim_song_id")[:10]
    for song in songs:
        one = Song.objects.filter(song_id=song["sim_song_id"])[0]
        result.append({
            "id": one.song_id,
            "name": one.song_name,
            "publish_time": one.song_publish_time,
            "url": one.song_url,
            "cate": "3"

        })
    return result