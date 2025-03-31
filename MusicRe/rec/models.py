from django.db import models

# 用户歌单推荐表
class UserPlayListRec(models.Model):
    user = models.CharField(blank=True, max_length=64, verbose_name="用户ID")
    related_pl = models.CharField(blank=True, max_length=64, verbose_name="歌单ID")
    sim = models.FloatField(blank=True,verbose_name="相似度")
    def __str__(self):
        return self.user

    class Meta:
        db_table = "UserPlayListRec"
        verbose_name_plural = "用户歌单推荐"

# 用户歌曲推荐表
class UserSongRec(models.Model):
    user = models.CharField(blank=True, max_length=64, verbose_name="用户ID")
    related_song = models.CharField(blank=True, max_length=64, verbose_name="歌曲ID")
    sim = models.FloatField(blank=True,verbose_name="相似度")
    def __str__(self):
        return self.user

    class Meta:
        db_table = "UserSongRec"
        verbose_name_plural = "用户歌曲推荐"

# 用户歌手推荐表
class UserSingRec(models.Model):
    user = models.CharField(blank=True, max_length=64, verbose_name="用户ID")
    related_sing = models.CharField(blank=True, max_length=64, verbose_name="歌手ID")
    sim = models.FloatField(blank=True,verbose_name="相似度")
    def __str__(self):
        return self.user

    class Meta:
        db_table = "UserSingRec"
        verbose_name_plural = "用户歌手推荐"

# 用户用户推荐表
class UserUserRec(models.Model):
    user = models.CharField(blank=True, max_length=64, verbose_name="用户ID")
    related_user = models.CharField(blank=True, max_length=64, verbose_name="用户ID")
    sim = models.FloatField(blank=True,verbose_name="相似度")
    def __str__(self):
        return self.user

    class Meta:
        db_table = "UserUserRec"
        verbose_name_plural = "用户用户推荐"