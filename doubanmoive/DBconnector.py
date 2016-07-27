# coding: utf-8
__author__ = 'PrlNcE'
# coding: utf-8

import MySQLdb

def addItem(item,sql,s):
    if len(item[s]) != 0:
        temp = item[s][0].replace('\'','\\\'')
        sql = sql + ',\'' + temp +'\''
    else:
        sql += ',\'\''
    return sql

def addItemWithList(item,sql,s):
    if len(item[s]) != 0:
        sql = sql + ',\''
        for i in xrange(len(item[s])):
            temp = item[s][i].replace('\'','\\\'')
            sql = sql + temp + '/'
        sql += '\''
    else:
        sql += ',\'\''
    return sql

def getID():
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='movies_kg',port=3306,charset='utf8')
        cur=conn.cursor()

        sql = 'select uuid from movie_info_douban'

        #
        res = cur.execute(sql)
        res = cur.fetchall()
        return res

        # #for i in res:
        # #    print i[0],i[1]
        #
        #
        # cur.close()
        # conn.close()
        # return res
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def insert(item):
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='movies_kg',port=3306,charset='utf8')
        cur=conn.cursor()

        print item['name'][0]

        sql = u'insert into movie_info_douban (' \
              u'uuid,url,year,' \
              u'name,director,screenwriter,' \
              u'actors,type,region,' \
              u'language,release_date,' \
              u'length,alias,imdb_link,score,' \
              u'num_of_reviewers,' \
              u'num_of_five_stars,' \
              u'num_of_four_stars,' \
              u'num_of_three_stars,' \
              u'num_of_two_stars,' \
              u'num_of_one_stars,' \
              u'num_of_people_seen,' \
              u'num_of_people_want_to_see,' \
              u'common_tags,' \
              u'num_of_short_reviews,' \
              u'num_of_long_reviews )' \
              u' values (\'' + str(item['uuid'][0]) +'\''

        sql = addItem(item,sql,'url')
        sql = addItemWithList(item,sql,'year')
        sql = addItem(item,sql,'name')
        sql = addItemWithList(item,sql,'director')
        sql = addItemWithList(item,sql,'screenwriter')
        sql = addItemWithList(item,sql,'actors')

        sql = addItemWithList(item,sql,'type')
        sql = addItem(item,sql,'region')
        sql = addItem(item,sql,'language')
        sql = addItem(item,sql,'release_date')
        sql = addItem(item,sql,'length')
        sql = addItem(item,sql,'alias')
        sql = addItem(item,sql,'imdb_link')
        sql = addItem(item,sql,'score')
        sql = addItem(item,sql,'num_of_reviewers')
        sql = addItem(item,sql,'num_of_five_stars')
        sql = addItem(item,sql,'num_of_four_stars')
        sql = addItem(item,sql,'num_of_three_stars')
        sql = addItem(item,sql,'num_of_two_stars')
        sql = addItem(item,sql,'num_of_one_stars')
        sql = addItem(item,sql,'num_of_people_seen')
        sql = addItem(item,sql,'num_of_people_want_to_see')
        sql = addItemWithList(item,sql,'common_tags')
        sql = addItem(item,sql,'num_of_short_reviews')
        sql = addItem(item,sql,'num_of_long_reviews')


        sql += ')'

        # return 0
        try:
            print sql
            # 执行sql语句
            cur.execute(sql)
            print 'DONE!!!!!!!'
            # 提交到数据库执行
            conn.commit()
        except:
            print 'OOOOOOPSSSSS'
            # Rollback in case there is any error
            conn.rollback()

        #
        #
        # res = cur.execute(sql)
        # # res = cur.fetchall()
        # #for i in res:
        # #    print i[0],i[1]
        #
        #
        # cur.close()
        # conn.close()
        # return res
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])