from django.db import models

class SingTag(models.Model):
    sing_id = models.CharField(blank=False, max_length=64, verbose_name="歌手ID")
    tag = models.CharField(blank=True, max_length=64, verbose_name="歌手标签")

    def __str__(self):
        return self.sing_id

    class Meta:
        db_table = 'SingTag'
        verbose_name_plural = "歌手标签"
