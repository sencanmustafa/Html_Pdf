# -*- coding:utf-8 -*-
import blog
from blog import HtmlForm
class User_db:
    def __init__(self,username,password):
        self.username = username
        self.password = password

naseef = User_db("naseef","naseef")

def validate(username,password):
    if naseef.password.split()==password.split() and naseef.username.split()==username.split():
        return True


class Html:
    def __init__(self,text1,text2):
        self.text1 = text1
        self.text2 = text2




