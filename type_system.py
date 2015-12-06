#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Program:
# Description: implement a type system
# Author: Eric He(hcc1009@gmail.com)
# CREATE: [2015-12-06 Sun 20:44]
# LAST MODIFIED:
'''
using descriptors to enforce constrains on the values that assigned to certain attributes
'''

class Descriptor:
    def __init__(self,name=None,**kargs):
        self.name = name
        for key,value in kargs.items():
            setattr(self,key,value)

    def __set__(self, instance, value):
        instance.__dict__[self.name]=value

class Typed(Descriptor):
    expected_type = type(None)

    def __set__(self,instance,value):
        if not isinstance(value,self.expected_type):
            raise TypeError('Expected '+str(self.expected_type))
        super().__set__(instance,value)

class Unsigned(Descriptor):
    def __set__(self,instance,value):
        if value < 0:
            raise ValueError('Expected >=0')
        super().__set__(instance,value)

class MaxSized(Descriptor):
    def __init__(self,name=None,**kargs):
        if 'size' not in kargs:
            raise TypeError('missing size option')
        super.__init__(name,**kargs)

    def __set__(self,instance,value):
        if len(value)>=self.size:
            raise ValueError('size should less than' + str(self.size))
        super().__set__(instance,value)

class Integer(Typed):
    expected_type = int

class UnsignedInteger(Integer,Unsigned):
    pass

class Float(Typed):
    expected_type = float

class UnsignedFloat(Float,Unsigned):
    pass

class String(Typed):
    expected_type = str

class SizedString(String,MaxSized):
    pass

# No.1 of ways to use. Directly claim these attributes as class variables
class Stock:
    name = SizedString('name',size = 8)
    shares = UnsignedInteger('shares')
    price = UnsignedFloat('price')
    def __init__(self,name,shares,price):
        self.name = name
        self.shares = shares
        self.price = price

# No.2 of ways to use. class decorator

def check_attr(**kargs):
    def decorate(cls):
        for key, value in kargs.items():
            if isinstance(value,Descriptor):
                value.name = key
                setattr(cls,key,value)
            else:
                setattr(cls,key,value(key))
        return cls
    return decorate

@check_attr(name = SizedString(size=8),
            shares = UnsignedInteger,
            price = UnsignedFloat)
class Stock1:
    def __init__(self,name,shares,price):
        self.name = name
        self.shares = shares
        self.price = price

# NO.3 of ways to use. metaclass
class checkedmeta(type):
    def __new__(cls,clsname,bases,methods):
        for key,value in methods.items():
            if isinstance(value,Descriptor):
                value.name = key
        return type.__new__(cls,clsname, bases,methods)

class Stock3(metaclass = checkedmeta):
    name = SizedString(size=8)
    shares = UnsignedInteger()
    price = UnsignedFloat()
    def __init__(self,name,shares,price):
        self.name = name
        self.shares = shares
        self.price = price
