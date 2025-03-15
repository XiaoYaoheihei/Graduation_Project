import json
import os

class UserSim:
	def __init__(self, cache_path = "./data/user_sim.json"):
		self.cache_path = cache_path
		self.user_tags = self.load_user_tags()  # {user_id: tag_set}
		self.similarity_matrix = self.calculate_similarity()

	def load_user_tags(self) -> dict:
		user_tags = dict()
		# UserTag 是数据库模型，包含 user_id 和 tag 字段
		for record in UserTag.objects.all():
			user_tags[record.user_id].add(record.tag)
		return user_tags
	
	"""计算杰卡德相似度系数"""
	def jaccard_similarity(self, tags1, tags2) -> float:
		intersection = len(tags1 & tags2)
		union = len(tags1 | tags2)
		if union:
			return intersection / union
		else:
			return 0.0
	
	"""计算用户相似度矩阵（优先使用缓存）"""
	def calculate_similarity(self) -> dict:
		# 尝试加载缓存
		if os.path.exists(self.cache_path):
			with open(self.cache_path, "r", encoding="utf-8") as f:
				return json.load(f)

		similarity_dict = dict()

		# 优化：预处理所有用户标签（避免循环内重复查询）
		all_users = list(self.user_tags.keys())
        
		for idx, user1 in enumerate(all_users, 1):
			current_tags = self.user_tags[user1]
			similarity_list = []

			for user2 in all_users:
				if user1 == user2:
						continue  # 跳过自身
				
				sim = self.jaccard_similarity(current_tags, self.user_tags[user2])
				
				# 严格筛选条件：仅保留相似度>0.8的
				if sim > 0.8:
					similarity_list.append((user2, sim))

			# 按相似度排序并取Top20
			similarity_list.sort(key=lambda x: -x[1])
			# 将排序之后的列表数据转化为字典
			similarity_dict[user1] = {}
			for user_id, sim in similarity_list[:20]:
				similarity_dict[user1][user_id] = sim

			# 进度打印
			print(f"Processed {idx}/{len(all_users)} users: {user1}")

			# 保存缓存
			with open(self.cache_path, "w", encoding="utf-8") as f:
				json.dump(similarity_dict, f)
			
		return similarity_dict

	'''将计算出的相似度转成导入mysql的格式'''
	def transform(self):
		fd = open("./data/user_sim.txt", "a", encoding="utf-8")
		for user1 in self.similarity_matrix.keys():
			for user2 in self.similarity_matrix[user1].keys():
				fd.write(user1 + "," + user2 + "," + str(self.similarity_matrix[user1][user2]) + "\n")
		fd.close()
		print("Over!")

if __name__ == "__main__":
	user = UserSim()
	user.transform()