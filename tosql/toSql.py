'''
    把数据写入DB中
'''

import pymysql
import datetime
import time
import re
import os
import json

from MusicRec.mysite.settings import DB_HOST, DB_PORT, DB_USER, DB_PASSWD, DB_NAME
from MusicRec.playlist.models import PlayListToSongs, PlayListToTag, PlayList
from MusicRec.song.models import SongLysic, Song, SongTag
from MusicRec.user.models import User, UserTag
from MusicRec.sing.models import Sing, SingTag

class ToSQL:
    def __init__(self):
        self.db = self.__connect()
        self.cursor = self.db.cursor()

    '''连接MySql数据库'''
    def __connect(self):
        db = pymysql.Connect(DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT, charset='utf8')
        return db
    
    # 13位时间戳转换为时间
    def TransFormTime(self,t1):
        try:
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t1))
        except Exception as e:
            print(t1)
            print("%s, %s " %(t1,e))
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(0))
        return dt

    # 歌曲部分
    """歌曲信息写入DB"""
    def saveSongToSql(self):
        with open("./data/song_mess_all.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.split(" |+| ")
                if len(parts) != 9:
                    print(f"数据格式异常：{line.strip()}")
                    continue  # 或者记录日志并跳过异常行
                (
                    song_id, 
                    song_name, 
                    song_playlist_id, 
                    publish_time, 
                    singer_id, 
                    total_comments, 
                    hot_comments, 
                    song_url
                ) = parts
                
                s = Song(
                    song_id = song_id,
                    song_name = song_name,
                    song_pl_id = song_playlist_id,
                    song_publish_time = self.TransFormTime(int(publish_time)/1000),
                    song_sing_id = singer_id,
                    song_total_comments = total_comments,
                    song_hot_comments = hot_comments,
                    song_url = song_url
                )
                
                try:
                    s.save()
                except Exception as e:
                    print(e)
            print("save song over!")
            
    
    """歌曲标签"""
    def saveSong2TagToSql(self):
        # 找到歌曲所属歌单，歌单对应的标签
        BATCH_SIZE = 1000  # 批量插入的大小
        song_tag_to_save = []
        
        with open("./data/song_tag.txt", "a", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                try:
                    parts = line.strip().split(',')
                    # 基础验证
                    if not parts:
                        print(f"警告：第{i}行数据无效，跳过：{line.strip()}")
                        continue
                    song_id = parts[0].strip()
                    tag = parts[1].strip()
                    song_tag_to_save.append(
                        SongTag(song_id=song_id, tag=tag)
                    )
                    
                    if len(song_tag_to_save) >= BATCH_SIZE:
                        SongTag.objects.bulk_create(song_tag_to_save)
                        song_tag_to_save = []
                        print(f"已处理 {i} 条记录")
                    
                except Exception as e:
                    print(f"错误处理第{i}行：{str(e)}，内容：{line.strip()}")
                    
            if song_tag_to_save:
                SongTag.objects.bulk_create(song_tag_to_save)
                print(f"剩余 {len(song_tag_to_save)} 条记录插入完成")
            
            print(f"歌词标签写入数据库完成！共处理 {i} 条记录")
                    
    
    """歌词信息"""
    def saveSongLysicToSql(self):
        BATCH_SIZE = 1000  # 批量插入的大小
        songs_to_save = []
        
        with open("./data/song_lysic_mess_all.txt", "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                try:
                    parts = line.strip().split("\t")
                    
                    # 基础验证
                    if not parts:
                        print(f"警告：第{i}行数据无效，跳过：{line.strip()}")
                        continue
                    
                    song_id = parts[0].strip()  # 确保ID无空格
                    
                    # 处理歌词内容
                    if len(parts) > 1:
                        lyric = parts[1].strip()
                        lyric = "暂无歌词提供！" if lyric.lower() == "null" else lyric
                    else:
                        lyric = "暂无歌词提供！"
                    
                    # 创建模型对象并批量保存
                    songs_to_save.append(
                        SongLysic(song_id=song_id, song_lysic=lyric)
                    )
                    
                    # 批量插入操作
                    if len(songs_to_save) >= BATCH_SIZE:
                        SongLysic.objects.bulk_create(songs_to_save)
                        songs_to_save = []
                        print(f"已处理 {i} 条记录")
                    
                except Exception as e:
                    print(f"错误处理第{i}行：{str(e)}，内容：{line.strip()}")
            
            # 插入剩余数据
            if songs_to_save:
                SongLysic.objects.bulk_create(songs_to_save)
                print(f"剩余 {len(songs_to_save)} 条记录插入完成")
            
            print(f"歌词信息写入数据库完成！共处理 {i} 条记录")
    
    # 歌手部分
    """歌手信息"""
    def saveSingerToSql(self):
        processed_count = 0
        failed_count = 0
        existing_singers = set()  # 使用集合存储已处理的歌手ID
        
        with open("./data/singer_mess_all.txt", "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                try:
                    parts = line.strip().split(",")
                    
                    # 基础验证
                    if len(parts) != 6:
                        print(f"警告：第{line_num}行数据格式错误，跳过：{line.strip()}")
                        continue
                    
                    singer_id, singer_name, singer_music_num, singer_mv_num, singer_album_num, singer_url = parts
                    
                    # 去重处理
                    if singer_id in existing_singers:
                        continue
                    
                    # 创建模型对象
                    singer = Sing(
                        sing_id=singer_id,
                        sing_name=singer_name,
                        sing_music_num=singer_music_num,
                        sing_mv_num=singer_mv_num,
                        sing_album_num=singer_album_num,
                        sing_url=singer_url
                    )
                    
                    # 保存到数据库
                    try:
                        singer.save()
                        existing_singers.add(singer_id)  # 仅成功保存后才标记为已处理
                        processed_count += 1
                    except Exception as e:
                        print(f"错误：第{line_num}行歌手ID {singer_id} 保存失败，错误：{str(e)}")
                        failed_count += 1
                    
                except Exception as e:
                    print(f"致命错误：处理第{line_num}行时发生异常，错误：{str(e)}，内容：{line.strip()}")
        
        print(f"歌手信息导入完成！共处理 {processed_count + failed_count} 条记录，成功 {processed_count} 条，失败 {failed_count} 条")
    
    """歌手标签"""
    def saveSinger2TagToSql(self):
        BATCH_SIZE = 1000  # 批量插入的大小
        singer_tag_to_save = []
        
        with open("./data/singer_tag.txt", "a", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                try:
                    parts = line.strip().split(',')
                    # 基础验证
                    if not parts:
                        print(f"警告：第{i}行数据无效，跳过：{line.strip()}")
                        continue
                    singer_id = parts[0].strip()
                    tag = parts[1].strip()
                    singer_tag_to_save.append(
                        SingTag(sing_id=singer_id, tag=tag)
                    )
                    
                    if len(singer_tag_to_save) >= BATCH_SIZE:
                        SingTag.objects.bulk_create(singer_tag_to_save)
                        singer_tag_to_save = []
                        print(f"已处理 {i} 条记录")
                    
                except Exception as e:
                    print(f"错误处理第{i}行：{str(e)}，内容：{line.strip()}")
                    
            if singer_tag_to_save:
                SingTag.objects.bulk_create(singer_tag_to_save)
                print(f"剩余 {len(singer_tag_to_save)} 条记录插入完成")
            
            print(f"歌词标签写入数据库完成！共处理 {i} 条记录")
    
    # 用户部分
    """用户信息"""
    def saveUserToSql(self):
        BATCH_SIZE = 1000  # 批量插入大小
        users_to_save = []
        processed_count = 0
        failed_count = 0
        existing_users = set()  # 使用集合存储已处理的用户ID
        
        with open("./data/user_mess_all.txt", "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                try:
                    parts = line.strip().split(" |=| ")
                    
                    # 数据格式验证
                    if len(parts) != 14:
                        print(f"警告：第{line_num}行数据格式错误（字段数不为14），跳过：{line.strip()}")
                        continue
                    
                    (
                        u_id, u_name, u_birthday_str, u_gender_str, u_province, u_city, u_type,
                        u_tags, u_img_url, u_auth_status, u_account_status, u_dj_status,
                        u_vip_type, u_sign
                    ) = parts
                    
                    # 去重处理
                    if u_id in existing_users:
                        continue
                    
                    # 字段清洗与转换
                    try:
                        u_birthday = self.TransFormTime(float(int(u_birthday_str) / 1000))
                    except (ValueError, TypeError):
                        u_birthday = datetime.datetime(1970, 1, 1)  # 默认时间
                        
                    u_gender = int(u_gender_str) if u_gender_str.isdigit() else 0
                    
                    u_sign = u_sign.strip() if u_sign and u_sign != "\n" else "我就是我是颜色不一样的花火！"
                    
                    u_tags = u_tags.replace("[", "").replace("]", "").strip()
                    
                    # 创建用户对象
                    user = User(
                        u_id=u_id,
                        u_name=u_name,
                        u_birthday=u_birthday,
                        u_gender=u_gender,
                        u_province=u_province,
                        u_city=u_city,
                        u_type=u_type,
                        u_tags=u_tags,
                        u_img_url=u_img_url,
                        u_auth_status=u_auth_status,
                        u_account_status=u_account_status,
                        u_dj_status=u_dj_status,
                        u_vip_type=u_vip_type,
                        u_sign=u_sign
                    )
                    
                    # 添加到批量插入列表
                    users_to_save.append(user)
                    existing_users.add(u_id)
                    
                    # 批量插入
                    if len(users_to_save) >= BATCH_SIZE:
                        User.objects.bulk_create(users_to_save)  # 假设使用Django ORM
                        users_to_save = []
                        processed_count += BATCH_SIZE
                        print(f"已处理 {processed_count} 条记录")
                    
                except Exception as e:
                    failed_count += 1
                    print(f"错误：第{line_num}行用户ID {u_id} 处理失败，错误：{str(e)}，内容：{line.strip()}")
        
        # 插入剩余数据
        if users_to_save:
            User.objects.bulk_create(users_to_save)
            processed_count += len(users_to_save)
        
        print(f"用户信息导入完成！共处理 {line_num} 行，成功 {processed_count} 条，失败 {failed_count} 条")
    
    """用户标签"""
    def saveUser2TagToSql(self):
        for one in PlayList.objects.all():
            # print(one)
            for tag in one.pl_tags.split(","):
                UserTag(
                    user_id=one.pl_creator.u_id,
                    tag=tag.replace(" ","")
                ).save()
        print("Over !")
    
    
    # 歌单部分
    """歌单信息"""
    def savePlaylistToSql(self):
        BATCH_SIZE = 1000  # 批量插入大小
        playlists_to_save = []
        processed_count = 0
        failed_count = 0
        
        with open("./data/pl_mess_all.txt", "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                try:
                    parts = line.strip().split(" |=| ")
                    
                    # 数据格式验证
                    if len(parts) != 13:
                        print(f"警告：第{line_num}行数据格式错误（字段数不为13），跳过：{line.strip()}")
                        continue
                    
                    (
                        pl_id, pl_creator, pl_name, pl_create_time_str,
                        pl_update_time_str, pl_songs_num_str, pl_listen_num_str,
                        pl_share_num_str, pl_comment_num_str, pl_follow_num_str,
                        pl_tags_str, pl_img_url, pl_desc
                    ) = parts
                    
                    # 获取用户对象
                    try:
                        user = User.objects.get(u_id=pl_creator)
                    except User.DoesNotExist:
                        print(f"错误：用户ID {pl_creator} 不存在，跳过歌单 {pl_id}")
                        failed_count += 1
                        continue
                    
                    # 时间戳转换
                    try:
                        pl_create_time = self.TransFormTime(int(pl_create_time_str) / 1000)
                        pl_update_time = self.TransFormTime(int(pl_update_time_str) / 1000)
                    except (ValueError, TypeError):
                        print(f"错误：第{line_num}行时间戳转换失败，跳过：{line.strip()}")
                        failed_count += 1
                        continue
                    
                    # 数字字段转换
                    try:
                        pl_songs_num = int(pl_songs_num_str)
                        pl_listen_num = int(pl_listen_num_str)
                        pl_share_num = int(pl_share_num_str)
                        pl_comment_num = int(pl_comment_num_str)
                        pl_follow_num = int(pl_follow_num_str)
                    except ValueError:
                        print(f"错误：第{line_num}行数值字段格式错误，跳过：{line.strip()}")
                        failed_count += 1
                        continue
                    
                    # 清洗标签字段
                    pl_tags = re.sub(r"[\"\[\]\']", "", pl_tags_str.strip())
                    
                    # 创建歌单对象
                    playlist = PlayList(
                        pl_id=pl_id,
                        pl_creator=user,
                        pl_name=pl_name,
                        pl_create_time=pl_create_time,
                        pl_update_time=pl_update_time,
                        pl_songs_num=pl_songs_num,
                        pl_listen_num=pl_listen_num,
                        pl_share_num=pl_share_num,
                        pl_comment_num=pl_comment_num,
                        pl_follow_num=pl_follow_num,
                        pl_tags=pl_tags,
                        pl_img_url=pl_img_url,
                        pl_desc=pl_desc
                    )
                    
                    # 添加到批量插入列表
                    playlists_to_save.append(playlist)
                    
                    # 批量插入
                    if len(playlists_to_save) >= BATCH_SIZE:
                        PlayList.objects.bulk_create(playlists_to_save)  # 假设使用Django ORM
                        playlists_to_save = []
                        processed_count += BATCH_SIZE
                        print(f"已处理 {processed_count} 条记录")
                    
                except Exception as e:
                    failed_count += 1
                    print(f"致命错误：第{line_num}行歌单ID {pl_id} 处理失败，错误：{str(e)}，内容：{line.strip()}")
        
        # 插入剩余数据
        if playlists_to_save:
            PlayList.objects.bulk_create(playlists_to_save)
            processed_count += len(playlists_to_save)
        
        print(f"歌单信息导入完成！共处理 {line_num} 行，成功 {processed_count} 条，失败 {failed_count} 条")
    
    """歌曲所属歌单信息"""
    def savePlaylist2SongToSql(self):
        BATCH_SIZE = 1000  # 批量插入大小
        playlist_songs = []
        processed_count = 0
        failed_count = 0
        
        with open("./data/pl_song_id.txt", "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                try:
                    parts = line.strip().split("\t")
                    
                    # 数据格式验证
                    if len(parts) != 2:
                        print(f"警告：第{line_num}行数据格式错误（字段数不为2），跳过：{line.strip()}")
                        continue
                    
                    pl_id, sids_str = parts
                    sids = sids_str.split(",")
                    
                    for song_id in sids:
                        song_id = song_id.strip()
                        if not song_id:
                            continue  # 跳过空ID
                        
                        # 创建关联对象
                        playlist_song = PlayListToSongs(
                            pl_id=pl_id,
                            song_id=song_id
                        )
                        
                        playlist_songs.append(playlist_song)
                        
                        # 批量插入
                        if len(playlist_songs) >= BATCH_SIZE:
                            PlayListToSongs.objects.bulk_create(playlist_songs)
                            playlist_songs = []
                            processed_count += BATCH_SIZE
                            print(f"已处理 {processed_count} 条记录")
                        
                except Exception as e:
                    failed_count += 1
                    print(f"错误：第{line_num}行处理失败，错误：{str(e)}，内容：{line.strip()}")
        
        # 插入剩余数据
        if playlist_songs:
            PlayListToSongs.objects.bulk_create(playlist_songs)
            processed_count += len(playlist_songs)
        
        print(f"歌单与歌曲关联关系导入完成！共处理 {line_num} 行，成功 {processed_count} 条，失败 {failed_count} 条")

    """歌单标签"""
    def savePlaylist2TagToSql(self):
        BATCH_SIZE = 1000  # 批量插入大小
        playlist_tags = []
        processed_count = 0
        failed_count = 0
        
        with open("./data/pl_mess_all.txt", "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                try:
                    parts = line.strip().split(" |=| ")
                    
                    # 数据格式验证
                    if len(parts) < 11:
                        print(f"警告：第{line_num}行数据格式错误（字段数不足11），跳过：{line.strip()}")
                        continue
                    
                    pl_id = parts[0]
                    tags_str = parts[10]
                    
                    # 清洗标签字段
                    tags_str = re.sub(r"[\[\]']", "", tags_str).strip()
                    tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
                    
                    # 创建关联对象
                    for tag in tags:
                        playlist_tag = PlayListToTag(
                            pl_id=pl_id,
                            tag=tag
                        )
                        playlist_tags.append(playlist_tag)
                        
                        # 批量插入
                        if len(playlist_tags) >= BATCH_SIZE:
                            PlayListToTag.objects.bulk_create(playlist_tags)
                            playlist_tags = []
                            processed_count += BATCH_SIZE
                            print(f"已处理 {processed_count} 条记录")
                        
                except Exception as e:
                    failed_count += 1
                    print(f"错误：第{line_num}行处理失败，错误：{str(e)}，内容：{line.strip()}")
        
        # 插入剩余数据
        if playlist_tags:
            PlayListToTag.objects.bulk_create(playlist_tags)
            processed_count += len(playlist_tags)
        
        print(f"歌单与标签关联关系导入完成！共处理 {line_num} 行，成功 {processed_count} 条，失败 {failed_count} 条")
    
    
    # 推荐部分
    """用户歌单推荐"""
    
    """用户歌曲推荐"""
    
    """用户歌手推荐"""
    
    """用户用户推荐"""
    
if __name__ == "__main__":
    tosql = ToSQL()