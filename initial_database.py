#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sqlite3
filename = 'chidiansha.db'
conn = sqlite3.connect(filename)
c = conn.cursor()
c.execute("CREATE TABLE users (user_id integer PRIMARY KEY, user_name text UNIQUE, user_email text UNIQUE, password text, user_group integer)")
c.execute("INSERT INTO users VALUES(0,'admin','admin@gmail.com','02c6524a4588768a39f5ee6a3d2d52ea', 0)")
c.execute("INSERT INTO users VALUES(1,'Guest','','', 1)")

c.execute("CREATE TABLE fridges (user_id integer PRIMARY KEY AUTOINCREMENT, stock text)")
c.execute("insert into fridges values(0,'')")
c.execute("insert into fridges values(1,'')")

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

c.execute("CREATE TABLE recipes (dish_id integer PRIMARY KEY AUTOINCREMENT, dish_name text, components text)")
c.execute("insert into recipes values(1,'西红柿炒鸡蛋','西红柿 鸡蛋')")
c.execute("insert into recipes values(2,'黄瓜炒鸡蛋','鸡蛋 黄瓜')")
c.execute("insert into recipes values(3,'酱茄子','茄子 豆瓣酱')")
c.execute("insert into recipes values(4,'红烧肉','八角 猪肉 糖')")
c.execute("insert into recipes values(5,'西红柿炒鸡蛋','西红柿 鸡蛋 糖')")
c.execute("insert into recipes values(6,'牛肉丸子菠菜汤','牛肉 菠菜 黑胡椒')")

c.execute("CREATE TABLE user_recipes (user_id integer UNIQUE, user_recipes text)")
c.execute("insert into user_recipes values(0,'')")
c.execute("insert into user_recipes values(1,'')")

c.execute("CREATE TABLE user_verify (verification_code text PRIMARY KEY, user_id integer UNIQUE)")

conn.commit()
