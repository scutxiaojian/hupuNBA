# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class HupunbaPipeline(object):
#     def process_item(self, item, spider):
#         return item


import json
import codecs
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


class JsonWithEncodingHupuPipeline(object):
    def __init__(self):
        self.file = codecs.open('hupu.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.decode("unicode_escape"))
        return item

    def spider_closed(self, spider):
        self.file.close()


class MySQLStoreHupuPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._conditional_insert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    def _conditional_insert(self, conn, item, spider):
        conn.execute("""
                select * from hupunba where name = %s
        """, (item['name']))
        ret = conn.fetchone()
        for t in item['rank']:
            if t != '':
                if ret:
                    conn.execute("""
                        update hupunba set rank=%s, name=%s, team=%s, point=%s, fgs=%s, threefgs=%s, freethrowfgs=%s, matchnumber=%s, time=%s where name = %s
                    """, (item['rank'], item['name'], item['team'], item['point'], item['fgs'], item['threefgs'], item['freethrowfgs'], item['matchnumber'], item['time'], item['name']))

                else:
                    conn.execute("""
                        insert into hupunba(rank, name, team, point, fgs, threefgs, freethrowfgs, matchnumber, time)
                        values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (item['rank'], item['name'], item['team'], item['point'], item['fgs'], item['threefgs'], item['freethrowfgs'], item['matchnumber'], item['time']))


    def _handle_error(self, failue, item, spider):
        print failue