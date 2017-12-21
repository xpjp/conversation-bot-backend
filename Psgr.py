#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2

class Psgr(object):
    """docstring for Psgr"""
    # コンストラクタ
    def __init__(self):
        super(Psgr, self).__init__()
        self.__connection = psycopg2.connect("host=localhost port=5432 dbname=text_analyze user=ryo password=3tfif2DJZEW64W3bsL9Z8af8qAoEM9cUGbzChcraVqvJzAZ6ca")
        self.cur = self.__connection.cursor()
        # print self.__connection.get_backend_pid()
        print "***Hello Psgr!***"

    # デストラクタ
    def __del__(self):
        self.cur.close()
        self.__connection.close()
        print "***Bye Psgr!***"

    def getCur(self):
        return self.cur

    def dbCommit(self):
        self.__connection.commit()

    def showTable(self,table):
        self.cur.execute('select * from ' + table + ';')
        for row in self.cur:
            print(row)

    def lastrowid(self):
        return self.cur.fetchone()[0]

    def getParseData(self,value):
        sentence_word_array = []
        sentence_word_dic = {}
        command = """SELECT s.sentence_id , s.sentence, w.word, w.part_of_speech, w.part_of_speech_detail1 \
        FROM sentences s INNER JOIN sentence_word sw \
        ON sw.sentence_id = s.sentence_id \
        INNER JOIN words w \
        ON  sw.word_id = w.word_id WHERE s.sentence_id = %s;"""
        self.cur.execute(command,value)
        for (i,row) in enumerate(self.cur):
            sentence_word_dic['sentence_id'] = row[0]
            sentence_word_dic['sentence'] = row[1]
            sentence_word_dic['word'] = row[2]
            sentence_word_dic['part_of_speech'] = row[3]
            sentence_word_dic['part_of_speech_detail1'] = row[4]
            sentence_word_array.append(sentence_word_dic)
            print row[0]
            print row[1]
            print row[2]
            print row[3]
            print row[4]
        # print sentence_word_array
        return sentence_word_array

    def execute(self,command,values):
        return self.cur.execute(command,values)

    def begin(self):
        self.cur.execute('begin')

    def commit(self):
        self.cur.execute('commit')
        self.dbCommit()

    def rollback(self):
        self.cur.execute('rollback')








# psgr = Psgr()
# cur = psgr.getCur()
#
# cur.execute("select * from users")
# for row in cur:
#     print(row)
#
# psgr.dbCommit()

# cur.execute("insert into users (name,score,team) values('sato',9.2,'red')")
# cur.execute("select * from users")
# for row in cur:
#     print(row)
#
# print "\n"



# cur.execute("update users set score=5.0 where id=9")
# cur.execute("select * from users")
# for row in cur:
#     print(row)


# cur.execute("delete from users where id=9")
# cur.execute("select * from users")
# for row in cur:
#     print(row)
