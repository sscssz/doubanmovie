# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import DBconnector

reload(sys)
sys.setdefaultencoding( "utf-8" )

class DoubanmoivePipeline(object):
    def process_item(self, item, spider):

        # print item['name']

        DBconnector.insert(item)

        # print 'pipeline_called\n\n\n'
        #
        # #print item['name']
        # res = ''
        # res += item['name'][0]
        #
        # # for i in item['name']:
        # #     print i
        # #     res += i
        # #     #print filename
        # #     #print response
        # filename = 'names.txt'
        # open(filename, 'a').write(res + '\n')

        return item
