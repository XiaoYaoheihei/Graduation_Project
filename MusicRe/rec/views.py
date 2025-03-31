from playlist.models import PlayList
from song.models import Song
from sing.models import Sing
from user.models import User
from rec.models import UserPlayListRec, UserSongRec, UserSingRec, UserUserRec

# 根据用户推荐相似度歌单
def rec_sim_playlist(request):
    user = request.GET.get("username")
    u_id = User.objects.filter(u_name=user)[0].u_id
    rec_all = UserPlayListRec.objects.filter(user=u_id).order_by("-sim")[:12]
    res = list()
    for rec in rec_all:
        one = PlayList.objects.filter(pl_id=rec.related_pl)[0]
        res.append({
            "pl_id": one.pl_id,
            "pl_creator": one.pl_creator.u_name,
            "pl_name": one.pl_name,
            "pl_img_url": one.pl_img_url
        })
    return {
        "code": 1,
        "data": {"recplaylist": res}
    }
    
# 根据用户推荐相似度歌曲
def rec_sim_song(request):
    user = request.GET.get("username")
    u_id = User.objects.filter(u_name=user)[0].u_id
    rec_all = UserSongRec.objects.filter(user=u_id).order_by("-sim")[:12]
    res = list()
    for rec in rec_all:
        one = Song.objects.filter(song_id=rec.related_song)[0]
        res.append({
            "song_id": one.song_id,
            "song_name": one.song_name,
            "song_publish_time": one.song_publish_time,
        })
    return {
        "code": 1,
        "data": {"songs": res}
    }

# 根据用户推荐相似度歌手
def rec_sim_sing(request):
    user = request.GET.get("username")
    id = User.objects.filter(u_name=user)[0].u_id
    rec_all = UserSingRec.objects.filter(user=id).order_by("-sim")[:12]
    res = list()
    for rec in rec_all:
        one = Sing.objects.filter(sing_id=rec.related_sing)[0]
        res.append({
            "sing_id": one.sing_id,
            "sing_name": one.sing_name,
            "sing_url": one.sing_url
        })
    return {
        "code": 1,
        "data": {"sings": res}
    }

# 根据用户推荐相似度用户
def rec_sim_user(request):
    user = request.GET.get("username")
    id = User.objects.filter(u_name=user)[0].u_id
    rec_all = UserUserRec.objects.filter(user=id).order_by("-sim")[:12]
    res = list()
    for rec in rec_all:
        one = User.objects.filter(u_id=rec.related_user)[0]
        res.append({
            "u_id": one.u_id,
            "u_name": one.u_name,
            "u_img_url": one.u_img_url
        })
    return {
        "code": 1,
        "data": {"users": res}
    }