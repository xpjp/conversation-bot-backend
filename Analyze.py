#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import MeCab
import string

class Analyze(object):
    """docstring for Analyze"""
    def __init__(self):
        super(Analyze, self).__init__()
        self.taggerdump = MeCab.Tagger("-Odump")
        self.taggerwakati = MeCab.Tagger("-Owakati")
        self.dictionary_info = None
        print ("***Hello Analyze!***")

    # デストラクタ
    def __del__(self):
        print ("***Bye Analyze!***")

    def get_version(self):
        return ("Mecab Version:" + str(MeCab.VERSION))

    def parse_sentence(self,sentence):
        try:
            self.taggerwakati.parse('')
            node = self.taggerdump.parseToNode(sentence)
            array = []
            while node:
                print(node.surface + '\t' + node.feature)
                array.append((node.surface, node.feature))
                node = node.next
            return array
        except RuntimeError as e:
            print ("RuntimeError:", e);

    def parse_wakati_sentence(self,sentence):
        try:
            self.taggerwakati.parse('')
            node = self.taggerwakati.parseToNode(sentence)
            array = []
            while node:
                print(node.surface + '\t' + node.feature)
                array.append((node.surface, node.feature))
                node = node.next
            return array
        except RuntimeError as e:
            print ("RuntimeError:", e);

# sentence = "すもももももももものうち"
# analyze = Analyze()
# print (analyze.get_version())
# analyze.parse_sentence(sentence)



# try:
#     t = MeCab.Tagger (" ".join(sys.argv))
#     print t.parse(sentence)
#     m = t.parseToNode(sentence)
#     while m:
# 	print m.surface, "\t", m.feature
# 	m = m.next
#     print "EOS"
#     lattice = MeCab.Lattice()
#     t.parse(lattice)
#     lattice.set_sentence(sentence)
#     len = lattice.size()
#     for i in range(len + 1):
#         b = lattice.begin_nodes(i)
#         e = lattice.end_nodes(i)
#         while b:
#             print "B[%d] %s\t%s" % (i, b.surface, b.feature)
#             b = b.bnext
#         while e:
#             print "E[%d] %s\t%s" % (i, e.surface, e.feature)
#             e = e.bnext
#     print "EOS";
#
#     d = t.dictionary_info()
#     while d:
#         print "filename: %s" % d.filename
#         print "charset: %s" %  d.charset
#         print "size: %d" %  d.size
#         print "type: %d" %  d.type
#         print "lsize: %d" %  d.lsize
#         print "rsize: %d" %  d.rsize
#         print "version: %d" %  d.version
#         d = d.next
#
# except RuntimeError, e:
#     print "RuntimeError:", e;
