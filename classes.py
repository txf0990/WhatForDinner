#!/usr/bin/end python
# -*- encoding: utf-8 -*-
import sqlite3

class Database(object):
    'This is the database'
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS receipes (dish_id integer PRIMARY KEY AUTOINCREMENT, dish_name text, components text)")
        self.c.execute("CREATE TABLE IF NOT EXISTS materials (material_id integer PRIMARY KEY AUTOINCREMENT, material_name text)")
        self.c.execute("CREATE TABLE IF NOT EXISTS fridges (user_id integer PRIMARY KEY AUTOINCREMENT, stock text)")
        self.c.execute("CREATE TABLE IF NOT EXISTS users (user_id integer PRIMARY KEY AUTOINCREMENT, user_name text UNIQUE, password text)")
        self.c.execute("CREATE TABLE IF NOT EXISTS user_receipes (user_id integer, user_receipes text)")
        self.conn.commit()

    '''def insertUser(self):
        self.c.execute("INSERT INTO fridges (stock) Values(?)", ('',))
        self.conn.commit()'''

    def insertReceipeEntry(self, dish_name, materials):
        materials_text = ""
        for item in materials:
            self.c.execute("INSERT INTO materials (material_name) SELECT ? WHERE NOT EXISTS(SELECT 1 FROM materials WHERE material_name=?)",(UTF8_to_Unicode(item), UTF8_to_Unicode(item)))
            materials_text = materials_text + item + " "
        materials_text = materials_text[:-1]
        self.c.execute("INSERT INTO receipes (dish_name, components) Values(?,?)", (UTF8_to_Unicode(dish_name), UTF8_to_Unicode(materials_text)))
        cursor_object = self.c.execute("SELECT * FROM receipes WHERE dish_id=last_insert_rowid()");
        list_cursor_object = list(cursor_object)
        self.conn.commit()
        return list_cursor_object[0][0] # return a int.
            
    def deleteReceipeEntry(self, dish_id):
        self.c.execute("DELETE FROM receipes WHERE dish_id=?",(dish_id,))
        self.conn.commit()

    def deliverReceipe(self):
        cursor_object = self.c.execute("SELECT * FROM receipes")
        list_cursor_object = list(cursor_object)    # list_cursor_object is a list of tuple, like: [(1, u'HongShaoRou', u'ZhuRou Tang BaJiao'), (3, u'XiHongShiChaoJiDan', u'XiHongShi JiDan Tang'), (4, u'TangCuPaiGu', u'PaiGu Tang Cu')]
        #list_cursor_object = map(lambda (a, b, c):(a, Unicode_to_UTF8(b), Unicode_to_UTF8(c)),
        #        list_cursor_object)
        return list_cursor_object
########
    #  联合查询
    def insertMyReceipeEntry(self, user_id, dish_name, materials):
        last_insert_id = self.insertReceipeEntry(dish_name, materials)
        cursor_object = self.c.execute("SELECT * FROM user_receipes WHERE user_id=?",(user_id,))
        list_cursor_object = list(cursor_object)        # [(1,'1 2 3')]
        receipe_list_text = list_cursor_object[0][1]
        receipe_list = receipe_list_text.split(' ')     # ['1','2','3']
        if not str(last_insert_id) in receipe_list:
            receipe_list_text = receipe_list_text + ' ' + str(last_insert_id)
            self.c.execute("UPDATE user_receipes SET user_receipes=? WHERE user_id=?", (receipe_list_text, user_id))    
            self.conn.commit()
    
    def deleteMyReceipeEntry(self, user_id, dish_id):
        cursor_object = self.c.execute("SELECT * FROM user_receipes WHERE user_id=?",(user_id,))
        list_cursor_object = list(cursor_object)        # [(1,'1 2 3')]
        receipe_list = list_cursor_object[0][1].split(' ')  #['1','2','3']
        receipe_list.remove(str(dish_id))
        receipe_list_text = ' '.join(receipe_list)
        self.c.execute("UPDATE user_receipes SET user_receipes=? WHERE user_id=?", (receipe_list_text, user_id))
        self.conn.commit()

    def deliverMyReceipe(self, user_id):
        cursor_object = self.c.execute("SELECT * FROM user_receipes WHERE user_id=?", (user_id,))
        list_cursor_object = list(cursor_object)    # a list of receipes to show: [(1,'1 2 3')] user_id, user_receipes
        list_cursor_object = list_cursor_object[0][1].split(' ')        # ['1','2','3']
        receipes_to_show = []
        for dish_id in list_cursor_object:
            temp_object = self.c.execute("SELECT * FROM receipes WHERE dish_id=?", (int(dish_id),))
            list_temp_object = list(temp_object)        # [(1,'西红柿炒鸡蛋','西红柿 鸡蛋')]
            if len(list_temp_object) != 0:
                temp_tuple = list_temp_object[0]
                receipes_to_show.append(temp_tuple)
        return receipes_to_show               # I want to return a list of tuple.

#######


    def insertToFridge(self, user_id, stock):  # stock must not exist in fridge
        cursor_object = self.c.execute("SELECT stock FROM fridges WHERE user_id=?", (user_id,))
        list_cursor_object = list(cursor_object)  # list_cursor_object is a list of tuple, like: [(u'TuDou XiHongShi HuangGua',)]
        stock_text = list_cursor_object[0][0]       
        # stock_text is what i already have in text
        # stock is a list that i wish to add.
        stock_text = stock_text.split(' ')
        # now, stock_text is also a list.
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

    def verifyPassword(self, user_name, password):
        cursor_object = self.c.execute("SELECT * FROM users WHERE user_name=?", (user_name,))
        list_cursor_object = list(cursor_object)
        if len(list_cursor_object) == 0:
            return -1
        if (list_cursor_object[0][2] != password):
            return -1
        return list_cursor_object[0][0]

def UTF8_to_Unicode(s):
    return s.decode('utf8')
def Unicode_to_UTF8(s):
    return s.encode('utf8')
