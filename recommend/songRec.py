# -*- coding: utf-8 -*-
"""
    歌曲导航栏中的歌曲推荐模块
    基于用户的协同过滤推荐算法 推荐相似歌曲
"""
import os
import math
import json

class RecSong:
    def __init__(self):
        self.playlist_mess_file = "../tosql/data/pl_mess_all.txt"
        self.playlist_song_mess_file = "../tosql/data/pl_song_id.txt"
        self.song_mess_file = "../tosql/data/song_mess_all.txt"

        self.user_song_dict, self.user_list = self.load_data()
        self.user_sim = self.calculate_user_similarity()
        self.user_song_score_dict = self.recommend_song()

    '''加载数据，计算用户与歌曲的对应关系'''
    def load_data(self):
        user_list = list()
        # 歌单和歌曲对应关系
        playlist_to_song = dict()
        for line in open(self.playlist_song_mess_file, "r", encoding="utf-8"):
            # 歌单 \t 歌曲s
            playlist_id, song_ids = line.strip().split("\t")
            playlist_to_song.setdefault(playlist_id, list())
            for song_id in song_ids.split(","):
                playlist_to_song[playlist_id].append(song_id)

        # print(playlist_to_song)
        print("完成歌单和歌曲对应关系统计!")

        # 用户和歌曲对应关系
        user_to_song = dict()
        for line in open(self.playlist_mess_file, "r", encoding="utf-8"):
            # 歌单id |=| 用户id
            pl_mess_list = line.strip().split(" |=| ")
            playlist_id, user_id = pl_mess_list[0], pl_mess_list[1]
            if user_id not in user_list:
                user_list.append(user_id)
            user_to_song.setdefault(user_id, dict())
            # 用户创建了歌单，歌单中包含有歌曲，用户把一首歌曲信息归档到歌单中时，认为是对歌曲的评分+1
            for song_id in playlist_to_song[playlist_id]:
                user_to_song[user_id].setdefault(song_id, 0)
                user_to_song[user_id][song_id] += 1
        
        # print(user_to_song)
        print("用户和歌曲对应信息统计完毕!")
        return user_to_song, user_list

    '''计算用户之间的相似度，采用惩罚热门商品和优化算法复杂度的算法'''
    def calculate_user_similarity(self):
        # 得到每个item被哪些user评价过
        tags_users = dict()
        for user_id, tags in self.user_song_dict.items():
            for tag in tags.keys():
                tags_users.setdefault(tag,set())
                if self.user_song_dict[user_id][tag] > 0:
                    tags_users[tag].add(user_id)
        # 构建倒排表
        C = dict()
        N = dict()
        for tags, users in tags_users.items():
            for u in users:
                N.setdefault(u,0)
                N[u] += 1
                C.setdefault(u,{})
                for v in users:
                    C[u].setdefault(v, 0)
                    if u == v:
                        continue
                    C[u][v] += 1 / math.log(1+len(users))
        # 构建相似度矩阵
        W = dict()
        for u, related_users in C.items():
            W.setdefault(u,{})
            for v, cuv in related_users.items():
                if u==v:
                    continue
                W[u].setdefault(v, 0.0)
                W[u][v] = cuv / math.sqrt(N[u] * N[v])
        print("用户相似度计算完成！")
        return W

    # 计算用户对歌曲的偏好，全量数据
    def recommend_song(self):
        # 记录用户对歌手的评分
        user_song_score_dict = dict()
        if os.path.exists("./data/user_song_prefer.json"):
            user_song_score_dict = json.load(open("./data/user_song_prefer.json", "r", encoding="utf-8"))
            print("用户对歌手的偏好从文件加载完毕！")
            return user_song_score_dict

        for user in self.user_song_dict.keys():
            print(user)
            user_song_score_dict.setdefault(user, {})
            # 遍历所有用户
            for u in self.user_sim[user].keys():
                if u == user:
                    continue
                for song in self.user_song_dict[u].keys():
                    user_song_score_dict[user].setdefault(song, 0.0)
                    user_song_score_dict[user][song] += self.user_sim[user][u] * self.user_song_dict[u][song]
        json.dump(user_song_score_dict, open("./data/user_song_prefer.json", "w", encoding="utf-8"))
        print("用户对歌曲的偏好计算完成！")
        return user_song_score_dict

    # 对每个用户的歌曲偏好进行排序
    # 将前100首歌曲写入文件
    def write_to_file(self):
        fw = open("./data/user_song_prefer.txt", "a", encoding="utf-8")
        for user in self.user_song_score_dict.keys():
            sort_user_song_prefer = sorted(self.user_song_score_dict[user].items(), key=lambda one:one[1], reverse=True)
            for one in sort_user_song_prefer[:100]:
                fw.write(user + ',' + one[0] + ',' + str(one[1]) + '\n')
        fw.close()
        print("写入文件完成")

if __name__ == "__main__":
    rec_song = RecSong()
    rec_song.write_to_file()