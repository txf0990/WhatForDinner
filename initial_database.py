#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sqlite3
filename = 'test.db'
conn = sqlite3.connect(filename)
c = conn.cursor()
c.execute("CREATE TABLE users (user_id integer PRIMARY KEY, user_name text UNIQUE, password text)")
c.execute("INSERT INTO users VALUES(1,'hello','123321')")
c.execute("INSERT INTO users VALUES(2,'world','456654')")
c.execute("INSERT INTO users VALUES(3,'happy','789987')")
c.execute("INSERT INTO users VALUES(4,'day','000000')")

c.execute("CREATE TABLE fridges (user_id integer PRIMARY KEY AUTOINCREMENT, stock text)")
c.execute("insert into fridges values(1,'西红柿 黄瓜 牛肉 糖')")
c.execute("insert into fridges values(2,'八角 猪肉 茄子')")
c.execute("insert into fridges values(3,'牛肉 菠菜 糖 西红柿')")
c.execute("insert into fridges values(4,'西红柿 鸡蛋 茄子 豆瓣酱')")

c.execute("CREATE TABLE materials (material_id integer PRIMARY KEY AUTOINCREMENT, material_name text)")
c.execute("insert into materials (material_name) values('西红柿')")
c.execute("insert into materials (material_name) values('黄瓜')")
c.execute("insert into materials (material_name) values('豆瓣酱')")
c.execute("insert into materials (material_name) values('茄子')")
c.execute("insert into materials (material_name) values('猪肉')")
c.execute("insert into materials (material_name) values('糖')")
c.execute("insert into materials (material_name) values('八角')")
c.execute("insert into materials (material_name) values('牛肉')")
c.execute("insert into materials (material_name) values('菠菜')")
c.execute("insert into materials (material_name) values('鸡蛋')")
c.execute("insert into materials (material_name) values('黑胡椒')")

c.execute("CREATE TABLE receipes (dish_id integer PRIMARY KEY AUTOINCREMENT, dish_name text, components text)")
c.execute("insert into receipes values(1,'西红柿炒鸡蛋','西红柿 鸡蛋')")
c.execute("insert into receipes values(2,'黄瓜炒鸡蛋','黄瓜 鸡蛋')")
c.execute("insert into receipes values(3,'酱茄子','豆瓣酱 茄子')")
c.execute("insert into receipes values(4,'红烧肉','猪肉 糖 八角')")
c.execute("insert into receipes values(5,'西红柿炒鸡蛋','西红柿 鸡蛋 糖')")
c.execute("insert into receipes values(6,'牛肉丸子菠菜汤','牛肉 菠菜 黑胡椒')")

c.execute("CREATE TABLE user_receipes (user_id integer UNIQUE, user_receipes text)")
c.execute("insert into user_receipes values(1,'1 2 3')")
c.execute("insert into user_receipes values(2,'2 3 4')")
c.execute("insert into user_receipes values(3,'3 4 5')")
c.execute("insert into user_receipes values(4,'4 5 6')")

conn.commit()
