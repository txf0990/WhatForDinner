#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sqlite3
filename = 'test.db'
conn = sqlite3.connect(filename)
c = conn.cursor()
c.execute("CREATE TABLE users (user_id integer PRIMARY KEY, user_name text UNIQUE, user_email text UNIQUE, password text, user_group integer)")
c.execute("INSERT INTO users VALUES(0,'admin','admin@gmail.com','310223c97def9d998a17702ef57361cc', 0)")
c.execute("INSERT INTO users VALUES(1,'111','111@gmail.com','613b701eaee1312b847955200c269110', 1)")
c.execute("INSERT INTO users VALUES(2,'222','222@gmail.com','b681d89adf904bb658bc502abf06b566', 1)")
c.execute("INSERT INTO users VALUES(3,'333','333@gmail.com','b681d89adf904bb658bc502abf06b566', 2)")
c.execute("INSERT INTO users VALUES(4,'444','444@gmail.com','82f21d72f80b11a63b1a9d9e588403ee', 2)")
c.execute("INSERT INTO users VALUES(9988,'Guest','','', 1)")

c.execute("CREATE TABLE fridges (user_id integer PRIMARY KEY AUTOINCREMENT, stock text)")
c.execute("insert into fridges values(0,'')")
c.execute("insert into fridges values(1,'西红柿 黄瓜 牛肉 糖')")
c.execute("insert into fridges values(2,'八角 猪肉 茄子')")
c.execute("insert into fridges values(3,'牛肉 菠菜 糖 西红柿')")
c.execute("insert into fridges values(4,'西红柿 鸡蛋 茄子 豆瓣酱')")
c.execute("insert into fridges values(9988,'')")

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
c.execute("insert into receipes values(2,'黄瓜炒鸡蛋','鸡蛋 黄瓜')")
c.execute("insert into receipes values(3,'酱茄子','茄子 豆瓣酱')")
c.execute("insert into receipes values(4,'红烧肉','八角 猪肉 糖')")
c.execute("insert into receipes values(5,'西红柿炒鸡蛋','糖 西红柿 鸡蛋')")
c.execute("insert into receipes values(6,'牛肉丸子菠菜汤','牛肉 菠菜 黑胡椒')")

c.execute("CREATE TABLE user_receipes (user_id integer UNIQUE, user_receipes text)")
c.execute("insert into user_receipes values(0,'')")
c.execute("insert into user_receipes values(1,'1 2 3')")
c.execute("insert into user_receipes values(2,'2 3 4')")
c.execute("insert into user_receipes values(3,'3 4 5')")
c.execute("insert into user_receipes values(4,'4 5 6')")
c.execute("insert into user_receipes values(9988,'')")

c.execute("CREATE TABLE user_verify (verification_code text PRIMARY KEY, user_id integer UNIQUE)")

conn.commit()
