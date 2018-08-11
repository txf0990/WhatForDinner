#!/usr/bin/end python
# -*- encoding: utf-8 -*-
import sqlite3

import string
import random
import re
class Database(object):
    'This is the database'
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS recipes (dish_id integer PRIMARY KEY AUTOINCREMENT, dish_name text, components text)")
        self.c.execute("CREATE TABLE IF NOT EXISTS materials (material_id integer PRIMARY KEY AUTOINCREMENT, material_name text)")
        self.c.execute("CREATE TABLE IF NOT EXISTS fridges (user_id integer PRIMARY KEY AUTOINCREMENT, stock text)")
        self.c.execute("CREATE TABLE IF NOT EXISTS users (user_id integer PRIMARY KEY AUTOINCREMENT, user_name text UNIQUE, password text)")
        self.c.execute("CREATE TABLE IF NOT EXISTS user_recipes (user_id integer, user_recipes text)")
        self.c.execute("CREATE TABLE IF NOT EXISTS user_verify (verification_code text PRIMARY KEY, user_id integer UNIQUE)")
        self.conn.commit()

    def insertUser(self, user_name, user_email, password, password1):
        cursor_object1 = self.c.execute('SELECT * FROM users WHERE user_name=?', (user_name,))
        list_cursor_object1 = list(cursor_object1)
        cursor_object2 = self.c.execute('SELECT * FROM users WHERE user_email=?', (user_email,))
        list_cursor_object2 = list(cursor_object2)
        status = 0
        if len(list_cursor_object1) != 0 and len(list_cursor_object2) != 0:
            return -1  # existed user
        elif len(list_cursor_object1) != 0 and len(list_cursor_object2) == 0:
            return -2  # existed username
        elif len(list_cursor_object1) == 0 and len(list_cursor_object2) != 0:
            return -3  # existed email
        elif password != password1:
            return -6   # passwords don't match
        else:
            self.c.execute('INSERT INTO users(user_name,user_email,password,user_group) Values(?,?,?,?)',(user_name, user_email,md5(password+'chidiansha'),1,))  #  user_group=1 是已经验证邮箱的用户。user_group=2是刚注册还未验证邮箱的用户
            cursor_object = self.c.execute('SELECT * from users WHERE user_name=?',(user_name,))
            list_cursor_object = list(cursor_object)    # it is a list of tuple
            user_id = list_cursor_object[0][0]
            self.c.execute("INSERT INTO user_recipes Values(?,'1')",(user_id,))
            self.c.execute("INSERT INTO fridges Values(?,'')",(user_id,))
            verification_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))
            self.c.execute('INSERT INTO user_verify Values(?,?)', (verification_code, user_id,))
            # print verification_code
            self.conn.commit()
            return user_id
    
    def verifyEmail(self, verification_code):
        cursor_object = self.c.execute('SELECT * from user_verify WHERE verification_code=?',(verification_code,))
        list_cursor_object = list(cursor_object)
        if len(list_cursor_object) == 0:
            return -1       # the verification code is a fake one. do nothing and give an alert.
        user_id = list_cursor_object[0][1]
        self.c.execute('UPDATE users SET user_group=1 WHERE user_id=?',(user_id,))
        self.c.execute('DELETE FROM user_verify WHERE verification_code=?',(verification_code,))
        self.conn.commit()
        return user_id 

    def findUserGroup(self, user_id):
        cursor_object = self.c.execute('SELECT user_group FROM users WHERE user_id=?', (user_id,))
        list_cursor_object = list(cursor_object)
        group = list_cursor_object[0][0]
        return group

    def findUserName(self, user_id):
        cursor_object = self.c.execute('SELECT user_name FROM users WHERE user_id=?', (user_id,))
        list_cursor_object = list(cursor_object)
        name = list_cursor_object[0][0]
        return name
    
    def findUserProfile(self, user_id):
        cursor_object = self.c.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        list_cursor_object = list(cursor_object)
        result = []
        result.append(list_cursor_object[0][1])
        result.append(list_cursor_object[0][2])
        cursor_object = self.c.execute('SELECT * FROM user_recipes WHERE user_id=?', (user_id,))
        list_cursor_object = list(cursor_object)
        result.append(len(list_cursor_object[0][1].split(' ')))
        return result        # user_name, user_email, recipe number.

    def insertRecipeEntry(self, dish_name, materials):
        materials.sort()
        materials_text = ""
        for item in materials:
            self.c.execute("INSERT INTO materials (material_name) SELECT ? WHERE NOT EXISTS(SELECT 1 FROM materials WHERE material_name=?)",(UTF8_to_Unicode(item), UTF8_to_Unicode(item)))
            materials_text = materials_text + item + " "
        materials_text = materials_text[:-1]
        # first, check if this recipe already exists.
        cursor_object = self.c.execute("SELECT * FROM recipes WHERE components=?",(UTF8_to_Unicode(materials_text),))
        list_cursor_object = list(cursor_object)
        if len(list_cursor_object) != 0:
            for item in list_cursor_object:
                if item[1] == UTF8_to_Unicode(dish_name) and item[2] == UTF8_to_Unicode(materials_text):
                    self.conn.commit()
                    return item[0]

        self.c.execute("INSERT INTO recipes (dish_name, components) Values(?,?)", (UTF8_to_Unicode(dish_name), UTF8_to_Unicode(materials_text)))
        cursor_object = self.c.execute("SELECT * FROM recipes WHERE dish_id=last_insert_rowid()");
        list_cursor_object = list(cursor_object)
        self.conn.commit()
        return list_cursor_object[0][0] # return a int.
        
            
    def deleteRecipeEntry(self, dish_id):
        self.c.execute("DELETE FROM recipes WHERE dish_id=?",(dish_id,))
        self.conn.commit()

    def deliverRecipe(self):
        cursor_object = self.c.execute("SELECT * FROM recipes")
        list_cursor_object = list(cursor_object)    # list_cursor_object is a list of tuple, like: [(1, u'HongShaoRou', u'ZhuRou Tang BaJiao'), (3, u'XiHongShiChaoJiDan', u'XiHongShi JiDan Tang'), (4, u'TangCuPaiGu', u'PaiGu Tang Cu')]
        #list_cursor_object = map(lambda (a, b, c):(a, Unicode_to_UTF8(b), Unicode_to_UTF8(c)),
        #        list_cursor_object)
        return list_cursor_object
########
    #  联合查询
    def insertMyRecipeEntry(self, user_id, dish_name, materials):
        last_insert_id = self.insertRecipeEntry(dish_name, materials)
        print last_insert_id
        cursor_object = self.c.execute("SELECT * FROM user_recipes WHERE user_id=?",(user_id,))
        list_cursor_object = list(cursor_object)        # [(1,'1 2 3')]
        recipe_list = []
        recipe_list_text = ''
        if len(list_cursor_object) != 0:
            recipe_list_text = list_cursor_object[0][1]
            recipe_list = recipe_list_text.split(' ')     # ['1','2','3']
        if not str(last_insert_id) in recipe_list:
            recipe_list_text = recipe_list_text + ' ' + str(last_insert_id)
            self.c.execute("UPDATE user_recipes SET user_recipes=? WHERE user_id=?", (recipe_list_text, user_id))    
            self.conn.commit()
    
    def copyToMyRecipe(self, user_id, dish_id):
        cursor_object = self.c.execute('SELECT * FROM user_recipes WHERE user_id=?',(user_id,))
        list_cursor_object = list(cursor_object)
        recipe_list = list_cursor_object[0][1].split(' ')
        if not dish_id in recipe_list:
            recipe_list.append(dish_id)
            recipe_text = ' '.join(recipe_list)
            self.c.execute('UPDATE user_recipes SET user_recipes=? WHERE user_id=?',(recipe_text, user_id,))
            self.conn.commit()


    def deleteMyRecipeEntry(self, user_id, dish_id):
        cursor_object = self.c.execute("SELECT * FROM user_recipes WHERE user_id=?",(user_id,))
        list_cursor_object = list(cursor_object)        # [(1,'1 2 3')]
        recipe_list = list_cursor_object[0][1].split(' ')  #['1','2','3']
        recipe_list.remove(str(dish_id))
        recipe_list_text = ' '.join(recipe_list)
        self.c.execute("UPDATE user_recipes SET user_recipes=? WHERE user_id=?", (recipe_list_text, user_id))
        self.conn.commit()

    def deliverMyRecipe(self, user_id):
        cursor_object = self.c.execute("SELECT * FROM user_recipes WHERE user_id=?", (user_id,))
        list_cursor_object = list(cursor_object)    # a list of recipes to show: [(1,'1 2 3')] user_id, user_recipes
        recipes_to_show = []
        if len(list_cursor_object) != 0:
            list_cursor_object = list_cursor_object[0][1].split(' ')        # ['1','2','3']
            if len(list_cursor_object) != 0:
                for dish_id in list_cursor_object:
                    if dish_id == '':
                        continue
                    temp_object = self.c.execute("SELECT * FROM recipes WHERE dish_id=?", (int(dish_id),))
                    list_temp_object = list(temp_object)        # [(1,'西红柿炒鸡蛋','西红柿 鸡蛋')]
                    if len(list_temp_object) != 0:
                        temp_tuple = list_temp_object[0]
                        recipes_to_show.append(temp_tuple)
        return recipes_to_show               # I want to return a list of tuple.

#######


    def insertToFridge(self, user_id, stock):  # stock must not exist in fridge
        cursor_object = self.c.execute("SELECT stock FROM fridges WHERE user_id=?", (user_id,))
        list_cursor_object = list(cursor_object)  # list_cursor_object is a list of tuple, like: [(u'TuDou XiHongShi HuangGua',)]
        stock_text = ''
        if len(list_cursor_object) != 0:
            stock_text = list_cursor_object[0][0]       
        # stock_text is what i already have in text
        # stock is a list that i wish to add.
        stock_text = stock_text.split(' ')
        for item in stock_text:
            if item == '':
                stock_text.remove(item)
        for item in stock:
            if item == '':
                stock.remove(item)
        # now, stock_text is also a list.
        # there is no '' in either list.
        for item in stock_text:
            if item in stock:
                stock.remove(item)
        stock_text = ' '.join(stock_text)
        stock = ' '.join(stock)
        stock_text = stock_text + " " + stock

        self.c.execute("UPDATE fridges SET stock=? WHERE user_id=?", (stock_text, user_id))
        self.conn.commit()

    def deleteFromFridge(self, user_id, delete_list):   # item in delete_list must exist in fridge
        cursor_object = self.c.execute("SELECT stock FROM fridges WHERE user_id=?", (user_id,))
        list_cursor_object = list(cursor_object)  # list_cursor_object is a list of tuple, like: [(u'TuDou XiHongShi HuangGua',)]
        stock_text = list_cursor_object[0][0]
        stock_list = stock_text.split(' ')
        for item in delete_list:
            stock_list.remove(item)
        stock_text = ' '.join(stock_list)
        self.c.execute("UPDATE fridges SET stock=? WHERE user_id=?", (stock_text, user_id))
        self.conn.commit()
    
    def deliverFridge(self, user_id):
        cursor_object = self.c.execute("SELECT * FROM fridges WHERE user_id=?", (user_id,))
        list_cursor_object = list(cursor_object)    # list_cursor_object is a list of tuple
        #list_cursor_object = map(lambda (a, b):(a, Unicode_to_UTF8(b)),
        #        list_cursor_object)
        return list_cursor_object

    def verifyPassword_user_name(self, user_name, password):
        cursor_object = self.c.execute("SELECT * FROM users WHERE user_name=?", (user_name,))
        list_cursor_object = list(cursor_object)
        if len(list_cursor_object) == 0:   # user does not exist.
            return -1
        if (list_cursor_object[0][3] != password):  # password mismatch
            return -2
        return list_cursor_object[0][0]         # return the user_id

    def verifyPassword_user_email(self, user_email, password):
        cursor_object = self.c.execute("SELECT * FROM users WHERE user_email=?", (user_email,))
        list_cursor_object = list(cursor_object)
        if len(list_cursor_object) == 0:   # user does not exist.
            return -1
        if (list_cursor_object[0][3] != password):  # password mismatch
            return -2
        return list_cursor_object[0][0]         # return the user_id
    
    def clearRecipe(self, user_id):
        self.c.execute("UPDATE user_recipes SET user_recipes='' WHERE user_id=?",(user_id,))
        self.conn.commit()

    def clearFridge(self, user_id):
        self.c.execute("UPDATE fridges SET stock='' WHERE user_id=?",(user_id,))
        self.conn.commit()


def UTF8_to_Unicode(s):
    return s.decode('utf8')
def Unicode_to_UTF8(s):
    return s.encode('utf8')
def ifValidUsername(user_name):
    char_list = list(user_name)
    if '@' in char_list:
        return false
    else:
        return true
def md5(str):
    import hashlib
    m = hashlib.md5()   
    m.update(str)
    return m.hexdigest()

