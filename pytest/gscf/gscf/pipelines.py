# -*- coding: utf-8 -*-

# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class GscfPipeline(object):
    def process_item(self, item, spider):
        return item

#PipeLine示例
# import sqlite3
# from os import path
# from scrapy.core import signals
# from scrapy.xlib.pydispatch import dispatcher
# class SQLiteStorePipeline(object):
#     filename = 'data.sqlite'
#     def __init__(self):
#         self.conn = None
#         dispatcher.connect(self.initialize, signals.engine_started)
#         dispatcher.connect(self.finalize, signals.engine_stopped)
#     def process_item(self, domain, item):
#         self.conn.execute('insert into blog values(?,?,?)', (item.url, item.raw, unicode(domain)))
#         return item
#     def initialize(self):
#         if path.exists(self.filename):
#             self.conn = sqlite3.connect(self.filename)
#         else: self.conn = self.create_table(self.filename)
#     def finalize(self):
#         if self.conn is not None:
#             self.conn.commit()
#             self.conn.close()
#             self.conn = None
#     def create_table(self, filename):
#         conn = sqlite3.connect(filename)
#         conn.execute("""create table blog (url text primary key, raw text, domain text)""")
#         conn.commit()
#         return conn