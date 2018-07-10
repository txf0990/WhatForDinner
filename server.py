#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from classes import Database

filename = 'test.db'

def UTF8_to_Unicode(s):
    return s.decode('utf8')
def Unicode_to_UTF8(s):
    return s.encode('utf8')

app = Flask(__name__)

@app.route('/')
def home():
    return 'This is the home page'

@app.route('/hello')
def welcome():
    return 'Hello!'

@app.route('/hello/<username>')
def hello_sb(username):
    return 'Hello, %s!' % username

@app.route('/receipes')
def receipes():
    database = Database(filename)
    receipes = database.deliverReceipe()
    return render_template('receipes.html', receipes=receipes)

@app.route('/receipes/insert', methods=['GET', 'POST'])
def receipes_insert():
    database = Database(filename)
    if request.method == 'POST':
        content = request.form['content']
        if content == '':
            return redirect(url_for('receipes'))
        content = Unicode_to_UTF8(content)
        content = content.split(' ')
        dish_name = content[0]
        content.remove(dish_name)
        components = content
        database.insertReceipeEntry(dish_name, components)
    return redirect(url_for('receipes'))

@app.route('/receipes/delete', methods=['GET', 'POST'])
def receipes_delete():
    database = Database(filename)
    database.deleteReceipeEntry(request.args['id'])
    return redirect(url_for('receipes'))

@app.route('/fridges')
def fridges():
    database = Database(filename)
    user_id = 1
    fridges = database.deliverFridge(user_id)
    fridges = fridges[0][1].split(' ')
    # now fridges is a list of stock
    return render_template('fridges.html', fridges=fridges)

@app.route('/fridges/insert', methods=['GET','POST'])
def fridges_insert():
    database = Database(filename)
    user_id = 1
    if request.method == 'POST':
        add_stock_text = request.form['content']
        if add_stock_text == '':
            return redirect(url_for('fridges'))
        add_stock_text = Unicode_to_UTF8(add_stock_text)
        add_stock_text = add_stock_text.split(' ')
        database.insertToFridge(user_id, add_stock_text)
    return redirect(url_for('fridges'))

@app.route('/fridges/delete', methods=['GET','POST'])
def fridges_delete():
    database = Database(filename)
    user_id = 1
    material = request.args['name']
    print 'calling deleteFromFridge({},{})'.format(user_id, [material])
    database.deleteFromFridge(user_id, [material])
    return redirect(url_for('fridges'))

@app.route('/result', methods=['GET','POST'])
def result():
    database = Database(filename)
    user_id = 1
    receipes = database.deliverReceipe()
    fridge = database.deliverFridge(user_id)
    fridge = fridge[0][1]
    fridge = fridge.split(' ')
    # fridge is a list of what you have-unicode
    # receipes is a list of tuple 
    receipe_list = list(receipes)
    result_list = []
    for one_receipe in receipes:
        dish_num = one_receipe[0]
        dish_name = one_receipe[1]
        still_need = one_receipe[2].split(' ') #components is a list of materials.
        what_i_have = []
        for item in fridge:
            if item in still_need:
                still_need.remove(item)
                what_i_have.append(item)
        this_entry = []
        this_entry.append(dish_num)
        this_entry.append(dish_name)
        this_entry.append(what_i_have)
        this_entry.append(still_need)
        this_entry.append(len(still_need))
        result_list.append(this_entry)

    sorted_result = []
    while len(result_list) != 0:
        min = 10000
        to_delete = 0
        for line in result_list:
            if line[4] < min:
                min = line[4]
                to_delete = line
        sorted_result.append(to_delete)
        result_list.remove(to_delete)
    # soted_result is a list:
    # [dish_num, dish_name, list(what_i_have), list(material still needed), item number still needed]
    return render_template('result.html', data=sorted_result)




if __name__ == '__main__':
    app.run()
