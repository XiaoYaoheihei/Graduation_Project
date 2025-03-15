import math

class UserCF:
  def __init__(self):
    self.user_score = self.initUserScore()
    self.user_sim = self.caculateUserSimilarity()

  '''初始化用户评分数据'''
  def initUserScore(self) -> dict:
    user_score_dict = {"A": {"a": 3.0, "b": 4.0, "c": 0.0, "d": 3.5, "e": 0.0},
                       "B": {"a": 4.0, "b": 0.0, "c": 4.5, "d": 0.0, "e": 3.5},
                       "C": {"a": 0.0, "b": 3.5, "c": 0.0, "d": 0.0, "e": 3.0},
                       "D": {"a": 0.0, "b": 4.0, "c": 0.0, "d": 3.5, "e": 3.0}}
    return user_score_dict
  
  '''计算用户之间的相似度，暴力解法，采用的是遍历每一个用户进行计算'''
  def caculateUserSimilarity(self) -> dict:
    W = dict()
    for user in self.user_score.keys():
      W.setdefault(user, {})
      for user_next in self.user_score.keys():
        if user_next == user:
          continue
        user_set = self.caculateVector(user)
        user_next_set = self.caculateVector(user_next)
        # 余弦相似度
        dot_product = float(len(user_set & user_next_set))
        modular_product = math.sqrt(len(user_set) * len(user_next_set))
        if modular_product == 0:
          W[user][user_next] = 0
        else:
          W[user][user_next] = dot_product / modular_product 

    return W
  
  '''
    计算用户的向量
    抽象成[1,1,0]的表达形式
    '''
  def caculateVector(self, user_id) -> set:
    user_vector = set()
    user_ratings = self.user_score.get(user_id, {})
    for item in user_ratings.keys():
      if user_ratings[item] > 0:
        user_vector.add(item)
    print(user_id, user_vector)
    return user_vector
  
  ''' 预测用户对item的评分'''
  def preUserItemScore(self, userA, item):
    score = 0.0
    for user in self.user_sim[userA].keys():
      if user != userA:
        score += self.user_sim[userA][user] * self.user_score[user][item]
    return score
  
  ''' 为用户推荐物品'''
  def recommend(self, user): 
    user_item_score_dict = dict()
    for item in self.user_score[user].keys():
      # 计算user未评分item的可能评分
      if self.user_score[user][item] <= 0:
        user_item_score_dict[item] = self.preUserItemScore(user, item)
    return user_item_score_dict

if __name__ == "__main__":
  ub = UserCF()
  print(ub.user_sim)
  print(ub.recommend("C"))
  
