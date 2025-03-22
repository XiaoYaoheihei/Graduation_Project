from sing.models import SingTag
from song.models import SongTag
from user.models import UserClicks
from playlist.models import PlayListToSongs, PlayListToTag
from django.db.models import Count

"""
    为你推荐导航栏，这里的标签推荐基于：
    1、用户进入系统时的选择
    2、用户在站内产生的点击行为
    3、热门标签进行补数
"""

# 返回歌单、歌手、歌曲的Tags
def GetRecTags(request, base_click):
    sings = request.session["sings"].split(",")
    songs = request.session["songs"].split(",")
    # 分别获取歌手、歌曲、歌单Tags
    sings_tags = getSingsRecTags(sings, base_click)
    songs_tags, playlist_tags = getSongsAndPlaylistRecTags(songs, base_click)
    return {
        "code": 1,
        "data": {
            "playlist": {"cateid": 2, "tags": list(playlist_tags)},
            "song": {"cateid": 3, "tags": list(songs_tags)},
            "sing": {"cateid": 4, "tags": list(sings_tags)},
        }
    }
    
def getSingsRecTags(sings, base_click):
    sings_tags = []
    # 用户有点击记录，根据历史的点击记录和当前点击的歌手id获取标签
    if base_click == 1:
        # 根据用户历史点击记录查询歌手标签
        clickIds = list(UserClicks.objects.filter(click_cate="4").values("click_id"))
        if len(clickIds) != 0:
            singBatchQuery(clickIds, sings_tags)
        if len(sings) != 0:
            singBatchQuery(sings, sings_tags)
    else:
        if len(sings) != 0:
            singBatchQuery(sings, sings_tags)
    
    sings_tags = supplement_tags(sings_tags, model = SingTag, tag_field = "tag", target_count = 15)

    return sings_tags

# 歌手批量查询
def singBatchQuery(singIds, singsTags):
    singTags = SingTag.objects.filter(sing_id__in=singIds).values("sing_id", "tag")
            
    # 完成数据去重
    processed_sings = {}
    for entry in singTags:
        singId = entry["sing_id"]
        tag = entry["tag"]
        if singId not in processed_sings:
            processed_sings[singId] = tag
            singsTags.append(tag)

# 歌曲，歌单批量查询
def collectSongAndPlaylistTags(songIds):
    songTags = list(SongTag.objects.filter(song_id__in=songIds).values_list("tag", flat=True))
    playlist_ids = PlayListToSongs.objects.filter(song_id__in=songIds).values_list("pl_id", flat=True)
    playlistTags = list(PlayListToTag.objects.filter(pl_id__in=playlist_ids).values_list("tag", flat=True))
    
    def deduplicate(tags):
        result = []
        seen = set()
        for t in tags:
            if t not in seen:
                seen.add(t)
                result.append(t)
        return result
    
    return deduplicate(songTags), deduplicate(playlistTags)

# 获得歌曲、歌单标签推荐
def getSongsAndPlaylistRecTags(songs, base_click):
    songs_tags = []
    playlist_tags = []
    # 用户有点击记录，根据历史的点击记录和当前点击的歌曲id获取对应标签
    if base_click == 1:
        click_ids = list(UserClicks.objects.filter(click_cate="3").values("click_id"))
        if len(click_ids) != 0:
            click_song_tags, click_pl_tags = collectSongAndPlaylistTags(click_ids)
            songs_tags.extend(click_song_tags)
            playlist_tags.extend(click_pl_tags)
        if len(songs) != 0:
            choose_song_tags, choose_pl_tags = collectSongAndPlaylistTags(songs)
            songs_tags.extend(choose_song_tags)
            playlist_tags.extend(choose_pl_tags)
    else:
        if len(songs) != 0:
            choose_song_tags, choose_pl_tags = collectSongAndPlaylistTags(songs)
            songs_tags.extend(choose_song_tags)
            playlist_tags.extend(choose_pl_tags)
    
    # 如果tag数量不够拿hot数据来补充
    songs_tags = supplement_tags(songs_tags, model = SongTag, tag_field = "tag", target_count = 15)
    playlist_tags = supplement_tags(playlist_tags, model = PlayListToTag, tag_field = "tag", target_count = 15)
    
    return songs_tags, playlist_tags

# 标签补充函数
def supplement_tags(tags_list, model, tag_field="tag", target_count=15):
    needed = max(0, target_count - len(tags_list))
    if needed <= 0:
        return tags_list  # 已满足数量要求，无需补充
    
    # 使用数据库聚合统计标签热度
    hot_tags = (
        model.objects
        .values(tag_field)
        .annotate(count=Count(tag_field))
        .order_by("-count", f"-{tag_field}")  # 按热度排序，相同热度按字段名排序
        .values_list(tag_field, flat=True)
    )
    
    # 将已有标签转为集合，快速判断是否存在
    existing_tags = set(tags_list)
    
    # 补充热门标签
    for tag in hot_tags:
        if tag not in existing_tags and needed > 0:
            tags_list.append(tag)
            needed -= 1
        if needed == 0:
            break
    
    return tags_list