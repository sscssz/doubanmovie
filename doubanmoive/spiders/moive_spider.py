# -*- coding: utf-8 -*-

__author__ = 'PrlNcE'
# coding: utf-8

# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from doubanmoive.items import DoubanmoiveItem


from scrapy.spiders import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
# from tutorial.items import TutorialItem
import re

import MySQLdb

def getID():
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='movies_kg',port=3306,charset='utf8')
        cur=conn.cursor()

        sql = 'select uuid from movie_info_douban'

        #
        res = cur.execute(sql)
        res = cur.fetchall()
        return res
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

class DoubanmoiveSpider(CrawlSpider):
    print 'main_called\n\n'
    name="doubanmoive"
    allowed_domains=["movie.douban.com"]
    # start_urls=["http://movie.douban.com/top250"]

    start_urls = []

    #
    # file_object = open('id.txt','r')
    #
    # for line in file_object:
    #     start_urls.append(line)
    #
    # print '!!!!!!',len(start_urls)
    #
    # for url in start_urls:
    #     yield make_requests_from_url(url)


    # start_urls=["https://movie.douban.com/subject/3707070/",
    #             "https://movie.douban.com/subject/1292792/"]
    # rules=[
    #     # Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/top250\?start=\d+.*'))),
    #     Rule(SgmlLinkExtractor(allow=(r'https://movie.douban.com/subject/\d+/')),callback="parse_item"),
    #
    #     # Rule(linkextractors.LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+'))),
    #     ]

    def start_requests(self):
        file_object = open('id.txt','r')

        done = getID()
        print len(done),type(done)
        done_list = []
        for i in done:
            # print i[0]
            done_list += str(i[0]),

        done_list = set(done_list)
        # for i in done_list:
        #     print i,type(i)

        try:
            url_head = "https://movie.douban.com/subject/"
            count = 0
            for line in file_object:
                # print line[:-1]
                line = line[:-1]
                # if count <= 10:
                #     print line,line,type(line)
                count += 1
                if line not in done_list:
                    self.start_urls.append(url_head + line)

            print '!!!!!!',len(self.start_urls)

            # return
            for url in self.start_urls:
                # print url
                yield self.make_requests_from_url(url)

        finally:
            file_object.close()
            #years_object.close()


    def parse(self, response):
        # print 'parse_Called\n\n'
        sel=Selector(response)
        hxs = HtmlXPathSelector(response)


        item=DoubanmoiveItem()
        item['uuid'] = [response.url.split('/')[-2]]
        item['url'] = [response.url]
        item['name']=sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['director']=sel.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
        item['screenwriter'] = sel.xpath('//*[@id="info"]/span[2]/span[2]/a/text()').extract()
        item['actors']= sel.xpath('//a[@rel="v:starring"]/text()').extract()
        item['type']= sel.xpath('//span[@property="v:genre"]/text()').extract()
        # item['region'] = sel.xpath('//*[@id="info"]/text()[9]').extract()##
        # item['language'] = sel.xpath('//*[@id="info"]/text()').extract()##
        item['release_date'] = sel.xpath('//*[@id="info"]/span[11]/text()').extract()##
        item['length'] = sel.xpath('//*[@id="info"]/span[13]/text()').extract()##
        # item['alias'] = sel.xpath()
        item['imdb_link'] = sel.xpath('//*[@id="info"]/a/text()').extract()
        item['score']=sel.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract()

        item['num_of_reviewers'] = sel.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()').extract()
        item['num_of_five_stars'] = sel.xpath('//*[@id="interest_sectl"]/div[1]/span[2]/text()').extract()
        item['num_of_four_stars'] = sel.xpath('//*[@id="interest_sectl"]/div[1]/span[4]/text()').extract()
        item['num_of_three_stars'] = sel.xpath('//*[@id="interest_sectl"]/div[1]/span[6]/text()').extract()
        item['num_of_two_stars'] = sel.xpath('//*[@id="interest_sectl"]/div[1]/span[8]/text()').extract()
        item['num_of_one_stars'] = sel.xpath('//*[@id="interest_sectl"]/div[1]/span[10]/text()').extract()

        item['num_of_people_seen'] = sel.xpath('//*[@id="subject-others-interests"]/div/a[1]/text()').extract()
        item['num_of_people_want_to_see'] = sel.xpath('//*[@id="subject-others-interests"]/div/a[2]/text()').extract()
        item['num_of_short_reviews'] = sel.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/text()').extract()
        item['num_of_long_reviews'] = sel.xpath('//*[@id="review_section"]/div[1]/h2/span/a/text()').extract()

        item['year']=sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')


        item['num_of_people_seen'] = [''.join(re.findall(r"[0-9]",str(''.join(item['num_of_people_seen']))))]
        item['num_of_people_want_to_see'] = [''.join(re.findall(r"[0-9]",str(''.join(item['num_of_people_want_to_see']))))]
        item['num_of_short_reviews'] = [''.join(re.findall(r"[0-9]",str(''.join(item['num_of_short_reviews']))))]
        item['num_of_long_reviews'] = [''.join(re.findall(r"[0-9]",str(''.join(item['num_of_long_reviews']))))]
        # item['common_tags']=sel.xpath('//*[@id="content"]/div/div[2]/div[5]/div/a/text()').extract()
        # if len(item['common_tags']) == 0:
        item['common_tags']=sel.xpath('//*[@class="tags-body"]/a/text()').extract()

        # item['region'] = sel.xpath()



        movie_detail = hxs.xpath('//*[@id="info"]').extract()

        #电影详情信息字符串
        movie_detail = ''.join(movie_detail).strip()
        movie_detail = movie_detail.replace(' ','')


        #获得国家
        temp = u'制片国家/地区:</span>'
        temp.decode('utf8')
        # print temp
        # print type(movie_detail)
        try:
            reg_idx = movie_detail.index(temp) + len(temp)
            movie_detail = movie_detail[reg_idx:]
            reg_end = movie_detail.index('<br>')
            reg = movie_detail[:reg_end]
            # print type(reg)
            item['region'] = [reg]
            # print item['region']
        except:
            item['region'] = ''

        #获得语言
        try:
            temp = u'语言:</span>'
            temp.decode('utf8')
            lang_idx = movie_detail.index(temp) + len(temp)
            movie_detail = movie_detail[lang_idx:]
            lang_end = movie_detail.index('<br>')
            lang = movie_detail[:lang_end]
            item['language'] = [lang]
        except:
            item['language'] = ''


        #获得别名
        try:
            temp = u'又名:</span>'
            temp.decode('utf8')
            lang_idx = movie_detail.index(temp) + len(temp)
            movie_detail = movie_detail[lang_idx:]
            lang_end = movie_detail.index('<br>')
            lang = movie_detail[:lang_end]
            item['alias'] = [lang]
        except:
            item['alias'] = ''



        # print type(item['actors'])
        # for i in item['actors']:
        #     print i
        # for i in xrange(len(item['language'])):
        #     print i,item['language'][i]
        # print item['region']
        # print item['language']
        # print item['alias']
        # print item['imdb_link'][0]

        return item

    def parse_item(self,response):
        print 'parse_Called\n\n'
        sel=Selector(response)
        item=DoubanmoiveItem()
        item['uuid'] = response.url.split('/')[-1]
        item['url'] = response.url
        item['name']=sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['director']=sel.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
        item['screenwriter'] = sel.xpath('//*[@id="info"]/span[2]/span[2]/a/text()').extract()
        item['actors']= sel.xpath('//a[@rel="v:starring"]/text()').extract()
        item['type']= sel.xpath('//span[@property="v:genre"]/text()').extract()
        item['region'] = sel.xpath('//*[@id="info"]/span[8]/text()').extract()##
        item['language'] = sel.xpath('//*[@id="info"]/span[9]/text()').extract()##
        item['release_date'] = sel.xpath('//*[@id="info"]/span[11]/content/text()').extract()##




        item['year']=sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['score']=sel.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract()
        # item['actor']= sel.xpath('//a[@rel="v:starring"]/text()').extract()

        print type(item['actors'])
        for i in item['actors']:
            print i

        return item