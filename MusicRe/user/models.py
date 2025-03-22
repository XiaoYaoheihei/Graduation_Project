from django.db import models

class UserClicks(models.Model):
	user_name = models.CharField(blank=False, max_length=64, verbose_name="用户名")
	click_id = models.CharField(blank=True, max_length=64, verbose_name="ID")
	click_cate = models.CharField(blank=True, max_length=64, verbose_name="类别")
	user_click_time = models.DateTimeField(blank=True, verbose_name="浏览时间")
	desc = models.CharField(
		blank=True, max_length=1000, verbose_name="备注", default="Are you ready!"
	)

    def __str__(self):
        return self.user_name
 
    class Meta:
        db_table = "UserClick"
        verbose_name_plural = "用户登录时的点击信息"