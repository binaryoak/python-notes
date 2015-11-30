#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Program:
# Description: parse arithmetic expressions.
# Author: Eric He(hcc1009@gmail.com)
# CREATE: [2015-11-30 Mon 17:22]
# LAST MODIFIED:
'''
aimed to parse text with small grammar rules.
'''

#expr :: term {(+|-) term} *
#term :: factor{(*|/)factor} *
#factor :: (expr)| NUM

import re
import collections


#token sepcification
NUM =r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
MINUS = r'(?P<MINUS>-)'
TIMES = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS = r'(?P<WS>\s+)'

pat = re.compile('|'.join([NUM,PLUS,MINUS,TIMES,DIVIDE,LPAREN,RPAREN,WS]))

Token = collections.namedtuple('Token',['type','value'])

def generate_tokens(text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        tok = Token(m.lastgroup, m.group())
        if tok.type != 'WS':
            yield tok


class ExpressionEvaluator:
    '''
    recursive descent parse, each method implement a single grammar rule. ._ac    cept() used to test and accept the current lookahead token, ._expect() use    d to exactly match and discard the next token on the input
    '''

    def parse(self,text):
        self.tokens = generate_tokens(text)
        self.tok = None
        self.nexttok = None
        self._advance()
        return self.expr()

    def _advance(self):
        'advance one token ahead'
        self.tok, self.nexttok = self.nexttok, next(self.tokens,None)

    def _accept(self,toktype):
        'test and consume the next token if it matches toktype'
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        else:
            return False

    def _expect(self,toktype):
        'comsume next token if it matches toktype or raise syntaxerror'
        if not self._accept(toktype):
            raise SyntaxError('Expected '+toktype)

    # grammar rules

    def expr(self):
        "expr :: term {(+|-) term}*"
        exprval = self.term()
        while self._accept('PLUS') or self._accept('MINUS'):
             op = self.tok.type
             right = self.term()
             if op == 'PLUS':
                 exprval += right
             elif op == 'MINUS':
                 exprval -= right

        return exprval

    def term(self):
        "term :: factor{(*|/) factor}*"

        termval = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.tok.type
            right = self.factor()
            if op == 'TIMES':
                termval *= right

            elif op == 'DIVIDE':
                termval /= right

        return termval

    def factor(self):
        "factor :: NUM|(expr)"

        if self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            exprval = self.expr()
            self._expect('RPAREN')
            return exprval
        else:
            raise SyntaxError('Expected number or left parentheses')

if __name__ == '__main__':
    e = ExpressionEvaluator()
    print(e.parse('10*11+(22/2)'))
