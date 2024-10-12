from django.db import  models
#创建模型#
class Topic(models.Model):
    text=models.charField(max_length=200)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.text
