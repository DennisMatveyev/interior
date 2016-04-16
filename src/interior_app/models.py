# coding: utf-8
from __future__ import unicode_literals
from django.db import models


class Sort(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Тип объекта:")

    def __unicode__(self):
        return self.name

class PortfolioObject(models.Model):
    sort = models.ForeignKey(Sort, null=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    draft = models.ImageField(upload_to='drafts', null=True, blank=True)
           
    def __unicode__(self):
        return self.address

class Photo(models.Model):
    portfolio = models.ForeignKey(PortfolioObject, null=True, blank=True)
    photo = models.ImageField(upload_to='photos', null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    pub_date = models.DateField()
    category = models.ForeignKey(Category)
    tag = models.ManyToManyField(Tag)
    
    class Meta:
        ordering = ['-pub_date']
           
    def __unicode__(self):
        return self.title

    def onephoto(self):
        onephoto = self.articlephoto_set.all()[0]
        return onephoto

class ArticlePhoto(models.Model):
    article = models.ForeignKey(Article, null=True, blank=True)
    article_photo = models.ImageField(upload_to='article_photo', null=True, blank=True)

class Subscriber(models.Model):
    email = models.EmailField('', max_length=100, null=True, blank=True)
    
    def __unicode__(self):
        return self.email

class Feedback(models.Model):
    text = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    photo = models.ImageField(upload_to='photos', null=True, blank=True)

