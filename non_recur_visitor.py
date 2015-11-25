#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Program:
# Description:non-recursion version of visitor pattern
# Author: Eric He(hcc1009@gmail.com)
# CREATE: [2015-11-25 Wed 17:20]
# LAST MODIFIED:

'''
non-recursion version of visitor pattern, aiming to avoid the recursion limit of python interpreter. stack and generator used here
'''
import types

class Node:
    pass

class UnaryOp(Node):
    def __init__(self,operand):
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

class Negate(UnaryOp):
    pass

class Number(Node):
    def __init__(self,value):
        self.value = value

class NodeVisitor:
    def visit(self, node):
        stack = [node]
        last_res = None

        while stack:
            try:
                last = stack[-1]
                if isinstance(last, types.GeneratorType):
                    stack.append(last.send(last_res))
                    last_res = None
                elif isinstance(last,Node):
                    stack.append(self._visit(stack.pop()))
                else:
                    last_res = stack.pop()

            except StopIteration:
                stack.pop()
        return last_res


    def _visit(self,Node):
        methname = 'visit_'+type(Node).__name__
        meth = getattr(self,methname,None)

        if meth is None:
            meth = self.generic_visit
        return meth(Node)

    def generic_visit(self,Node):
        raise RuntimeError('No {} method'.format('visit_'+type(Node).__name__))

class Evaluator(NodeVisitor):

    def visit_Number(self, Node):
        return Node.value

    def visit_Add(self,Node):
        yield (yield Node.left)+(yield Node.right)

    def visit_Sub(self, Node):
        yield (yield Node.left)-(yield Node.right)

    def visit_Mul(self, Node):
        yield (yield Node.left)*(yield Node.right)

    def visit_Div(self, Node):
        yield (yield Node.left)/(yield Node.right)

    def visit_Negate(self,Node):
        yield -(yield Node.operand)


if __name__=='__main__':
    a = Number(0)

    for n in range(1,100000):
        a = Add(a, Number(n))

    e = Evaluator()
    print(e.visit(a))
