# -*- coding:utf-8 -*-

class User_db:
    def __init__(self,username,password):
        self.username = username
        self.password = password

naseef = User_db("naseef","naseef")

def validate(username,password):
    if naseef.password.split()==password.split() and naseef.username.split()==username.split():
        return True
    else:
        return False
list = []






