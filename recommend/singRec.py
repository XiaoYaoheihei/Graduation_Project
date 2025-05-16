"""
    歌手导航栏的歌手推荐模块
    基于物品的协同过滤算法 推荐相似歌手
"""

import os
import math
import json

class RecSinger:
    def __init__(self):
        self.playlist_mess_file = "../tosql/data/pl_mess_all.txt"
        self.playlist_singer_mess_file = "../tosql/data/pl_singer_id.txt"
        self.song_mess_file = "../tosql/data/song_mess_all.txt"
        
        self.user_singer_dict, self.singer_list = self.load_data()
        self.singer_sim = self.calculate_singer_similarity()
        self.user_singer_score_dict = self.recommend_singer()


    def load_data(self):
        singer_list = []
        song_singer_dict = {}   # {歌曲：歌手}
        # 歌曲和歌手的对应关系
        for line in open(self.song_mess_file, "r", encoding="utf-8"):
            one_mess_list = line.strip().split(" |+| ")
            song_id, singer_id = one_mess_list[0], one_mess_list[4]
            song_singer_dict[song_id] = singer_id
            for singer in singer_id.split("#"):
                if singer not in singer_list and singer != "0":
                    singer_list.append(singer)
        # print(song_singer_dict)
        print("歌曲和歌手对应关系构建完成！")
        
         # 歌单和歌手对应关系
        playlist_singer_dict = dict()   # {歌单：歌手}
        for line in open(self.playlist_singer_mess_file, "r", encoding="utf-8"):
            # 歌单 \t 歌曲s
            playlist_id, song_ids = line.strip().split("\t")
            playlist_singer_dict.setdefault(playlist_id, list())
            # 多个歌手合作演唱的话，需要拆分添加
            # 单个歌手演唱的话，直接添加
            for song_id in song_ids.split(","):
                if "#" in song_singer_dict[song_id]:
                    for singer_one in song_singer_dict[song_id].split("#"):
                        if singer_one == "0":
                            continue
                        playlist_singer_dict[playlist_id].append(singer_one)
                else:
                    playlist_singer_dict[playlist_id].append(song_singer_dict[song_id])
        # print(playlist_sing_dict)
        print("歌单和歌手对应关系构建完成！")

        # 用户和歌手对应关系
        user_singer_dict = dict()   # {用户：歌手}
        for line in open(self.playlist_mess_file, "r", encoding="utf-8"):
            pl_mess_list = line.strip().split(" |=| ")
            playlist_id, user_id = pl_mess_list[0], pl_mess_list[1]
            user_singer_dict.setdefault(user_id,{})
            for singer_id in playlist_singer_dict[playlist_id]:
                user_singer_dict[user_id].setdefault(singer_id, 0)
                user_singer_dict[user_id][singer_id] += 1
        # print(user_singer_dict)
        print("用户和歌手对应信息统计完毕 ！")

        return user_singer_dict, singer_list


    """计算歌手相似度"""
    def calculate_singer_similarity(self):
        itemSim = dict()
        if os.path.exists("./data/singer_sim_singer.json"):
            itemSim = json.load(open("./data/singer_sim_singer.json", "r", encoding="utf-8"))
            print("歌手相似从文件中加载")
            return itemSim

        item_user_count = dict()  # 得到每个物品有多少用户产生过行为
        count = dict()  # 共现矩阵
        for user, item in self.user_singer_dict.items():
            for i in item.keys():
                item_user_count.setdefault(i, 0)
                if self.user_singer_dict[user][i] > 0.0:
                    item_user_count[i] += 1
                for j in item.keys():
                    count.setdefault(i, {}).setdefault(j, 0)
                    if self.user_singer_dict[user][i] > 0.0 and self.user_singer_dict[user][j] > 0.0 and i != j:
                        count[i][j] += 1
        # 共现矩阵 -> 相似度矩阵
        for i, related_items in count.items():
            itemSim.setdefault(i, dict())
            for j, cuv in related_items.items():
                itemSim[i].setdefault(j, 0)
                itemSim[i][j] = cuv / math.sqrt(item_user_count[i] * item_user_count[j])
        json.dump(itemSim,open("./data/singer_sim_singer.json","w",encoding="utf-8"))
        print("歌手相似计算完毕！")
        return itemSim


    """为每个用户推荐歌手"""
    def recommend_singer(self):
        # 记录用户对歌手的评分
        user_singer_score_dict = dict()
        if os.path.exists("./data/user_singer_prefer.json"):
            user_singer_score_dict = json.load(open("./data/user_singer_prefer.json", "r", encoding="utf-8"))
            print("用户对歌手的偏好从文件加载完毕！")
            return user_singer_score_dict
        
        for user in self.user_singer_dict.keys():
            # print(user)
            user_singer_score_dict.setdefault(user,{})
            # 遍历所有用户未评分歌手
            for singer in self.singer_list:
                if singer in self.user_singer_dict[user].keys():
                    continue
                score = 0.0
                for singer_sim in self.singer_sim[singer].keys():
                    if singer_sim == singer or singer_sim not in self.user_singer_dict[user].keys() or singer_sim not in self.singer_sim[singer].keys():
                        continue
                    score += self.singer_sim[singer][singer_sim] * self.user_singer_dict[user][singer_sim]
                user_singer_score_dict[user][singer] = score
        json.dump(user_singer_score_dict,open("./data/user_singer_prefer.json", "w", encoding="utf-8"))
        print("用户对歌手的偏好计算完成！")
        return user_singer_score_dict
    
    
    # 写入文件
    def write_to_file(self):
        fw = open("./data/user_singer_prefer.txt", "a", encoding="utf-8")
        for user_id in self.user_singer_score_dict.keys():
            sort_user_singer_prefer = sorted(self.user_singer_score_dict[user_id].items(), key = lambda one:one[1], reverse=True)
            for one in sort_user_singer_prefer[:100]:
                fw.write(user_id + "," + one[0] + "," + str(one[1]) +"\n" )
        fw.close()
        print("写入文件完成！")

if __name__ == "__main__":
    rec_sing = RecSinger()
    rec_sing.write_to_file()