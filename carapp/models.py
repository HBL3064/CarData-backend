from django.db import models

# Create your models here.
class CarData(models.Model):
    series_id = models.IntegerField(primary_key=True)
    series_name = models.CharField(max_length=255,default="",verbose_name='名称')
    image = models.CharField(max_length=255,default="",verbose_name='图片地址')
    car_rank = models.IntegerField(default="",verbose_name='排名')
    car_count = models.IntegerField(default=0,verbose_name='销量')
    min_price = models.FloatField(default=0,verbose_name='最低价格')
    max_price = models.FloatField(default=0,verbose_name='最高价格')
    brand_name = models.CharField(max_length=255,default="",verbose_name='品牌名称')
    level = models.CharField(max_length=255,default="",verbose_name='等级')
    fuel_forml = models.CharField(max_length=255,default="",verbose_name='能源类型')
    market_time = models.CharField(max_length=255,default="",verbose_name='上市时间')
    crate_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        db_table = 'car_data'