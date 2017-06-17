from django.db import models
from django.contrib.auth.models import User
import numpy as np


class Wine(models.Model):
    name = models.CharField(max_length=200)
    #price = models.FloatField()
    
    def average_rating(self):
        all_ratings = list(map(lambda x: x.rating, self.review_set.all()))
        return np.mean(all_ratings)
        
    def __string__(self):
        return self.name


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    wine = models.ForeignKey(Wine)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)


class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])


class Bought(models.Model):
    user_name = models.CharField(max_length=100)
    wine = models.ForeignKey(Wine)
    pub_date = models.DateTimeField('date bought')



class FinalBuy(models.Model):
    user_name=models.CharField(max_length=100)
    tranno=models.IntegerField(default=0)
    wine=models.ForeignKey(Wine)
    buy_date=models.DateTimeField('date bought')