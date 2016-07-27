# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class DoubanmoiveItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    uuid = Field()#uuid
    name=Field()#电影名
    url = Field()#链接
    year=Field()#上映年份
    score=Field()#豆瓣分数
    director=Field()#导演
    type=Field()#分类
    actors=Field()#演员
    screenwriter = Field()#编剧
    region = Field()#国家和地区
    language = Field()#语言
    release_date = Field()#上映日期
    length = Field()#片长
    alias = Field()#又名
    imdb_link = Field()#imdb链接

    num_of_reviewers = Field()#评价人数
    num_of_five_stars = Field()#五星人数
    num_of_four_stars = Field()#4星人数
    num_of_three_stars = Field()#3星人数
    num_of_two_stars = Field()#2星人数
    num_of_one_stars = Field()#1星人数

    num_of_people_seen = Field()#看过的人数
    num_of_people_want_to_see = Field()#想看的人数
    num_of_long_reviews = Field()#长评论个数
    num_of_short_reviews = Field()#短评论个数
    common_tags = Field()#常用标签




    #pass
