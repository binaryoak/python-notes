#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Program:
# Description:
# Author: Eric He(hcc1009@gmail.com)
# CREATE: [2015-12-04 Fri 17:47]
# LAST MODIFIED:
'''
messed up a text document, removed all spaces, punctuation and capitalization. Parsing the string in the way that minimize the number of unrecognized sequences of characters.
'''
import sys
class result:
    def __init__(self,inval_num=sys.maxsize,seq):
        self.inval_num = inval_num
        self.seq = seq

    def clone(self):
        return result(self.inval_num,self.seq)

    @staticmethod
    def min(r1,r2):
        if r1 == None:
            return r2
        elif r2 == None:
            return r1
        return r1 if r1.inval_num < r2.inval_num else r2

def parse(start, end, cache):
    # sentence is the string need to be parsed
    if end >= len(sentence) :
        return result(end-start,sentence[start:].upper())

    if start in cache:
        return cache[start].clone()

    cur_word = sentence[start,end+1]

    val_partial = dic.startwith(cur_word)  #implement the trie(dic) separately
    val_exact = val_partial and dic.hasword(cur_word)

    best_exact = parse(end+1,end+1,cache)

    if(val_exact):
        best_exact.seq = cur_word + ""+best_exact.seq
    else:
        best_exact.inval_num += len(cur_word)
        best_exact.seq = cur_word.upper()+""+best_exact.seq

    bestextend = None
    if val_partial:

        bestextend = parse(start,end+1,cache)

    best = result.min(best_exact,bestextend)

    cache[start] = best.clone()

    return best
