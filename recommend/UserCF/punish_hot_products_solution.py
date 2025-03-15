import math

class UserCF:
  def __init__(self):
    self.user_score = self.initUserScore()
    self.user_sim = self.caculateUserSimilarityBest()

  '''初始化用户评分数据'''
  def initUserScore(self) -> dict:
    user_score_dict = {"A": {"a": 3.0, "b": 4.0, "c": 0.0, "d": 3.5, "e": 0.0},
                       "B": {"a": 4.0, "b": 0.0, "c": 4.5, "d": 0.0, "e": 3.5},
                       "C": {"a": 0.0, "b": 3.5, "c": 0.0, "d": 0.0, "e": 3.0},
                       "D": {"a": 0.0, "b": 4.0, "c": 0.0, "d": 3.5, "e": 3.0}}
    return user_score_dict
  
  '''惩罚商品和倒排表一同优化'''
  def caculateUserSimilarityBest(self):
    # 得到每个item被哪些user评价过
    item_users = dict()
    for user, items in self.user_score.items():
      for item in items.keys():
        item_users.setdefault(item, set())
        if self.user_score[user][item] > 0:
          item_users[item].add(user)
    print(item_users)      
    
    # 构建倒排表和用户活跃度统计
    inverted_list = dict()
    number = dict()
    for item, users in item_users.items():
      for u in users:
        number.setdefault(u, 0)
        number[u] += 1
        inverted_list.setdefault(u, {})
        for v in users:
          inverted_list[u].setdefault(v, 0)
          if u == v:
            continue
          else:
            # 惩罚商品，重新计算权重
            inverted_list[u][v] += 1 / (math.log(1 + len(users)))

    # debug打印倒排表和活跃度
    # for i in inverted_list.keys():
    #   print(i, inverted_list[i])
    # print(number)
    
    # 构建相似度矩阵
    W = dict()
    for u, related_users in inverted_list.items():
      W.setdefault(u, {})
      for v, num in related_users.items():
        W[u].setdefault(v, 0.0)
        if v == u:
          continue
        else:
          W[u][v] = num / math.sqrt(number[u] * number[v])
    
    # debug打印相似度矩阵
    # for i in W.keys():
    #   print(i, W[i])
    
    return W
  
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