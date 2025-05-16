"""
    歌单导航栏的歌单推荐模块
    基于内容的推荐算法 构建用户的歌单推荐
    1、构建用户偏好矩阵(用户->标签的偏好)
    2、构建歌单的特征信息矩阵
"""

import json
import os
import re
import numpy as np

class RecPlaylist:
    def __init__(self):
        self.file = "../tosql/data/pl_mess_all.txt"
        self.tags_list = []  # 所有标签列表
        self.tag_to_index = {}  # 标签到索引的映射
        self.user_tags_count_dict = {}  # 用户对标签的计数字典
        self.playlist_tags_dict = {}  # 歌单与标签的映射
        self.user_playlist_dict = {}  # 用户创建的歌单列表
        
        self.load_data()
        self.tag_to_index = {tag: idx for idx, tag in enumerate(self.tags_list)}
        
        self.playlist_feature_matrix = self.create_playlist_feature_matrix()
        self.user_feature_prefer_matrix = self.create_user_feature_prefer_matrix()
        self.user_playlist_prefer_dict = self.calculation_user_prefer()


    def load_data(self):
        """加载数据并构建基础结构"""
        with open(self.file, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(" |=| ")
                playlist_id, user_id, tags_str = parts[0], parts[1], parts[10]
                
                # 使用正则表达式提取标签列表
                tags = re.findall(r"'(.*?)'", tags_str)
                
                # 更新用户歌单字典
                self.user_playlist_dict.setdefault(user_id, []).append(playlist_id)
                
                # 更新用户标签计数字典和歌单标签列表
                user_tags = self.user_tags_count_dict.setdefault(user_id, {})
                playlist_tags = self.playlist_tags_dict.setdefault(playlist_id, [])
                
                for tag in tags:
                    if tag not in self.tags_list:
                        self.tags_list.append(tag)
                    
                    # 更新用户标签计数
                    user_tags[tag] = user_tags.get(tag, 0) + 1
                    
                    # 更新歌单标签列表
                    playlist_tags.append(tag)
        
        print("数据加载完成！标签、用户计数、歌单标签统计已构建")


    def create_playlist_feature_matrix(self):
        """构建歌单特征矩阵（二进制特征向量）"""
        feature_matrix = {}
        tags_len = len(self.tags_list)
        
        for playlist_id, tags in self.playlist_tags_dict.items():
            feature = [0] * tags_len
            for tag in tags:
                idx = self.tag_to_index[tag]
                feature[idx] = 1
            feature_matrix[playlist_id] = feature
        
        print("歌单特征矩阵构建完成")
        return feature_matrix


    def create_user_feature_prefer_matrix(self):
        """构建用户偏好矩阵（基于标签使用频率）"""
        user_preference = {}
        tags_len = len(self.tags_list)
        
        for user_id, tag_counts in self.user_tags_count_dict.items():
            total = sum(tag_counts.values())
            count = len(tag_counts)
            u_avg = total / count if count else 0
            
            feature = [0] * tags_len
            for tag, cnt in tag_counts.items():
                idx = self.tag_to_index[tag]
                feature[idx] = cnt - u_avg + 1  # 避免偏好为零
            
            user_preference[user_id] = feature
        
        print("用户偏好矩阵构建完成")
        return user_preference


    def calculation_user_prefer(self):
        """计算用户对歌单的偏好并保存结果"""
        if os.path.exists("./data/user_playlist_prefer.json"):
            print("加载已有的偏好数据...")
            return json.load(open("./data/user_playlist_prefer.json", "r", encoding="utf-8"))
        
        user_prefer = {}
        
        for user_id, user_vec in self.user_feature_prefer_matrix.items():
            user_prefer[user_id] = {}
            user_array = np.array(user_vec)
            user_playlists = self.user_playlist_dict.get(user_id, [])
            
            for playlist_id, pl_vec in self.playlist_feature_matrix.items():
                if playlist_id in user_playlists:
                    continue  # 跳过用户已创建的歌单
                
                pl_array = np.array(pl_vec)
                score = np.dot(user_array, pl_array)
                
                if score > 0:
                    user_prefer[user_id][playlist_id] = score
        
        # 保存结果
        with open("./data/user_playlist_prefer.json", "w", encoding="utf-8") as f:
            json.dump(user_prefer, f)
        
        print("用户歌单偏好计算完成并已保存")
        return user_prefer


    # 将用户对歌单的偏好写入文件，保存每个用户的top 100
    def wrtie_to_file(self):
        fw = open("./data/user_playlist_prefer.txt", "a", encoding="utf-8")
        for user_id in self.user_playlist_prefer_dict.keys():
            sorted_user_prefer = sorted(self.user_playlist_prefer_dict[user_id].items(), key = lambda one: one[1], reverse= True)
            for one in sorted_user_prefer[:100]:
                fw.write(user_id + "," + one[0] + "," + str(one[1]) + "\n")
        fw.close()
        
if __name__ == "__main__":
    rec_playlist = RecPlaylist()
    rec_playlist.wrtie_to_file()