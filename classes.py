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
        self.conn.commit()

    def insertUser(self):
        self.c.execute("INSERT INTO fridges (stock) Values(?)", ('',))
        self.conn.commit()

    def insertReceipeEntry(self, dish_name, materials):
        materials_text = ""
        for item in materials:
            self.c.execute("INSERT INTO materials (material_name) SELECT ? WHERE NOT EXISTS(SELECT 1 FROM materials WHERE material_name=?)",(UTF8_to_Unicode(item), UTF8_to_Unicode(item)))
            materials_text = materials_text + item + " "
        materials_text = materials_text[:-1]
        self.c.execute("INSERT INTO receipes (dish_name, components) Values(?,?)", (UTF8_to_Unicode(dish_name), UTF8_to_Unicode(materials_text)))
        self.conn.commit()
            
    def deleteReceipeEntry(self, dish_id):
        self.c.execute("DELETE FROM receipes WHERE dish_id=?",(dish_id,))
        self.conn.commit()

    def insertToFridge(self, user_id, stock):  # stock must not exist in fridge
        cursor_object = self.c.execute("SELECT stock FROM fridges WHERE user_id=?", (user_id,))
        list_cursor_object = list(cursor_object)  # list_cursor_object is a list of tuple, like: [(u'TuDou XiHongShi HuangGua',)]
        stock_text = list_cursor_object[0][0]
        stock_text = Unicode_to_UTF8(stock_text) + " " + ' '.join(stock)
        self.c.execute("UPDATE fridges SET stock=? WHERE user_id=?", (UTF8_to_Unicode(stock_text), user_id))
        self.conn.commit()

    def deleteFromFridge(self, user_id, delete_list):   # item in delete_list must exist in fridge
        cursor_object = self.c.execute("SELECT stock FROM fridges WHERE user_id=?", (user_id,))
        list_cursor_object = list(cursor_object)  # list_cursor_object is a list of tuple, like: [(u'TuDou XiHongShi HuangGua',)]
        stock_text = list_cursor_object[0][0]
        stock_list = stock_text.split(' ')
        for item in delete_list:
            stock_list.remove(UTF8_to_Unicode(item))
        stock_text = ' '.join(stock_list)
        self.c.execute("UPDATE fridges SET stock=? WHERE user_id=?", (stock_text, user_id))
        self.conn.commit()
    
    def deliverReceipe(self):
        cursor_object = self.c.execute("SELECT * FROM receipes")
        list_cursor_object = list(cursor_object)    # list_cursor_object is a list of tuple, like: [(1, u'HongShaoRou', u'ZhuRou Tang BaJiao'), (3, u'XiHongShiChaoJiDan', u'XiHongShi JiDan Tang'), (4, u'TangCuPaiGu', u'PaiGu Tang Cu')]
        #list_cursor_object = map(lambda (a, b, c):(a, Unicode_to_UTF8(b), Unicode_to_UTF8(c)),
        #        list_cursor_object)
        return list_cursor_object
    
    def deliverFridge(self, user_id):
        cursor_object = self.c.execute("SELECT * FROM fridges WHERE user_id=?", (user_id,))
        list_cursor_object = list(cursor_object)    # list_cursor_object is a list of tuple
        #list_cursor_object = map(lambda (a, b):(a, Unicode_to_UTF8(b)),
        #        list_cursor_object)
        return list_cursor_object

def UTF8_to_Unicode(s):
    return s.decode('utf8')
def Unicode_to_UTF8(s):
    return s.encode('utf8')
