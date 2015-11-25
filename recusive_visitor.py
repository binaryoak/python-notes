#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Program:
# Description: representation of mathematical expressions
# Author: Eric He(hcc1009@gmail.com)
# CREATE: [2015-11-25 Wed 16:44]
# LAST MODIFIED:
'''
visitor pattern, used to process or navigate through a complicated data structure consisting of many different kinds of objects, each of which needs to be handled in a different way. Benefit is to decouple the manipulations of a complicated data structure from the data structure ieself
'''
class Node:
    pass

class Unaryop(Node):
    def __init__(self, operand):
        self.operand = operand

class BinaryOp(Node):
    def __init__(self,left,right):
        self.left = left
        self.right = right

class Add(BinaryOp):
    pass

class Sub(BinaryOp):
    pass

class Mul(BinaryOp):
    pass

class Div(BinaryOp):
    pass

class Negate(Unaryop):
    pass

class Number(Node):
    def __init__(self,value):
        self.value = value

class NodeVisitor:
    def visit(self, Node):
        methname = 'visit_'+type(Node).__name__
        meth= getattr(self,methname,None)
        if meth is None:
            meth = self.generic_visit()
        return meth(Node)

    def generic_visit(self,Node):
        raise RuntimeError('No {} method'.format('visit_'+type(Node).__name__))

class Evaluator(NodeVisitor):
    def visit_Number(self, node):
        return node.value

    def visit_Add(self, node):
        return self.visit(node.left)+self.visit(node.right)

    def visit_Sub(self, node):
        return self.visit(node.left)-self.visit(node.right)

    def visit_Mul(self, node):
        return self.visit(node.left)*self.visit(node.right)

    def visit_Div(self, node):
        return self.visit(node.left)/self.visit(node.right)

    def visit_Negate(self, node):
        return -node.operand

if __name__=='__main__':
    t1 = Add(Number(2),Number(5))
    t2 = Mul(Number(7),t1)
    t3 = Div(Number(4),t2)
    t4 = Sub(t3,Number(9))

    e = Evaluator()
    print(e.visit(t4))
