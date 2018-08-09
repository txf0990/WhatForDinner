#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
import re
import sqlite3
from classes import Database

filename = 'test.db'

def UTF8_to_Unicode(s):
    return s.decode('utf8')
def Unicode_to_UTF8(s):
    return s.encode('utf8')
def ifValidEmail(email):
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
        return True
    return False
def md5(str):
    import hashlib
    m = hashlib.md5()   
    m.update(str)
    return m.hexdigest()

app = Flask(__name__)

@app.route('/changelanguage/ce')
def change_language_ce():
    session['language'] = 'ENG'
    return redirect(url_for('recipes'))

@app.route('/changelanguage/ec')
def change_language_ec():
    session['language'] = 'CHN'
    return redirect(url_for('recipes'))

@app.route('/')
def index():
    if not 'language' in session:
        session['language'] = 'CHN'
    if 'user_id' in session:
        return redirect(url_for('recipes'))
    else:
        session['user_id'] = 9988
    return redirect(url_for('recipes'))

@app.route('/loginname', methods=['GET', 'POST'])
def login_name():
    status = 0
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = md5(request.form['password'] + 'chidiansha')
        database = Database(filename)
        user_id = database.verifyPassword_user_name(user_name, password)
        if user_id == -1:       # user does not exist
            status = -1
        elif user_id == -2:     # mismatch password
            status = -2
        elif user_id == 0:
            session['user_id'] = user_id
            return redirect(url_for('admin'))
        else:                # 判断用户名密码是否匹配
            session['user_id'] = user_id
            return redirect(url_for('result'))
    return render_template('login_name.html', status=status, user_id=session['user_id'], language=session['language'])
    
@app.route('/loginemail', methods=['GET', 'POST'])
def login_email():
    status = 0
    if request.method == 'POST':
        user_email = request.form['user_email']
        password = request.form['password']
        database = Database(filename)
        user_id = database.verifyPassword_user_email(user_email, password)
        if user_id == -1:       # user does not exist
            status = -1
        elif user_id == -2:     # mismatch password
            status = -2
        elif user_id == 0:
            session['user_id'] = user_id
            return redirect(url_for('admin'))
        else:                # 判断用户名密码是否匹配
            session['user_id'] = user_id
            return redirect(url_for('result'))
    return render_template('login_email.html', status=status, language=session['language'])

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    status = 0
    if request.method == 'POST':
        user_name = request.form['user_name']
        if not user_name.isalnum():
            return render_template('register.html', status=-4, language=session['language'], user_name=user_name)
        user_email = request.form['user_email']
        # 检查是否合法邮件地址
        if not ifValidEmail(user_email):
            return render_template('register.html', status=-5, language=session['language'], user_name=user_name)

        password = request.form['password']
        database = Database(filename)
        status = database.insertUser(user_name, user_email, password)
        if status != 0 and status != -1 and status != -2 and status != -3 and status != -4 and status != -5:
            session['user_id'] = status
            return redirect(url_for('result'))

    return render_template('register.html', status=status, language=session['language'], user_name='Guest')

@app.route('/verify/<verification_code>')
def verify(verification_code):
    database = Database(filename)
    status = database.verifyEmail(verification_code)
    if status == -1:
        return '错误的激活链接'
    else:
        session['user_id'] = status
        return redirect(url_for('result'))

@app.route('/debug')
def debug():
    user_id = session['user_id']
    database = Database(filename)
    user_group = database.findUserGroup(user_id)
    user_name = database.findUserName(user_id)
    return render_template('debug.html', user_id=user_id, user_group=user_group, user_name=user_name, language=session['language'])

@app.route('/profile')
def profile():
    user_id = session['user_id']
    database = Database(filename)
    user_profile = database.findUserProfile(user_id)
    user_name = database.findUserName(user_id)
    return render_template('profile.html', user_id=user_id, user_profile=user_profile, user_name=user_name, language=session['language'])

@app.route('/hello')
def welcome():
    return 'Hello, %s' % session['user_id']

@app.route('/hello/<username>')
def hello_sb(username):
    return 'Hello, %s!' % username

@app.route('/recipes')
def recipes():
    print session['language']
    if 'user_id' in session:
        user_id = session['user_id']
        database = Database(filename)
        user_name = database.findUserName(user_id)
        recipes = database.deliverRecipe()
        return render_template('recipes.html', user_id=session['user_id'], recipes=recipes, user_name=user_name, language=session['language'])
    return render_template('login_name.html', language=session['language'])

@app.route('/myrecipes')
def my_recipes():
    if 'user_id' in session:
        user_id = session['user_id']
        database = Database(filename)
        user_name = database.findUserName(user_id)
        user_group = database.findUserGroup(user_id)
        if user_group == 2:
            return "您必须先验证邮箱才能使用功能"
        recipes = database.deliverMyRecipe(user_id)
        return render_template('my_recipes.html', user_id=session['user_id'], recipes=recipes, user_name=user_name, language=session['language'])
    return render_template('login_name.html', language=session['language'])

@app.route('/recipes/insert', methods=['GET', 'POST'])
def recipes_insert():
    database = Database(filename)
    if request.method == 'POST':
        content = request.form['content']
        if content == '':
            return redirect(url_for('recipes'))
        content = Unicode_to_UTF8(content)
        content = content.split(' ')
        dish_name = content[0]
        content.remove(dish_name)
        components = content
        database.insertRecipeEntry(dish_name, components)
    return redirect(url_for('recipes'))

@app.route('/myrecipes/insert', methods=['GET', 'POST'])
def my_recipes_insert():
    database = Database(filename)
    user_id = session['user_id']
    if request.method == 'POST':
        content = request.form['content']
        if content == '':
            return redirect(url_for('my_recipes'))
        content = Unicode_to_UTF8(content)
        content = content.split(' ')
        dish_name = content[0]
        content.remove(dish_name)
        components = content
        database.insertMyRecipeEntry(user_id, dish_name, components)
    return redirect(url_for('my_recipes'))

@app.route('/myrecipes/copy', methods=['GET', 'POST'])
def my_recipes_copy():
    database = Database(filename)
    user_id = session['user_id']
    dish_id = request.args['id']
    database.copyToMyRecipe(user_id, dish_id)
    return redirect(url_for('recipes'))

@app.route('/recipes/delete', methods=['GET', 'POST'])
def recipes_delete():
    database = Database(filename)
    database.deleteRecipeEntry(request.args['id'])
    return redirect(url_for('recipes'))

@app.route('/myrecipes/delete', methods=['GET', 'POST'])
def my_recipes_delete():
    user_id = session['user_id']
    database = Database(filename)
    database.deleteMyRecipeEntry(user_id, request.args['id'])
    return redirect(url_for('my_recipes'))

@app.route('/myrecipes/clear')
def my_recipes_clear():
    user_id = session['user_id']
    database = Database(filename)
    database.clearRecipe(user_id)
    return redirect(url_for('my_recipes'))

@app.route('/fridges')
def fridges():
    if 'user_id' in session:
        database = Database(filename)
        user_id = session['user_id']
        user_name = database.findUserName(user_id)
        user_group = database.findUserGroup(user_id)
        if user_group == 2:
            return "您必须先验证邮箱才能使用功能"
        #user_id = 1
        fridges = database.deliverFridge(user_id)
        if len(fridges) != 0:
            fridges = fridges[0][1].split(' ')
        # now fridges is a list of stock
        return render_template('fridges.html', user_id=session['user_id'], fridges=fridges, user_name=user_name, language=session['language'])
    return render_template('login_name.html', language=session['language'])

@app.route('/fridges/insert', methods=['GET','POST'])
def fridges_insert():
    database = Database(filename)
    user_id = session['user_id']
    #user_id = 1
    # user_fridge is a list of what is already in fridge
    if request.method == 'POST':
        add_stock_text = request.form['content']
        if add_stock_text == '':
            return redirect(url_for('fridges'))
        add_stock_text = add_stock_text.split(' ')
        database.insertToFridge(user_id, add_stock_text)
    return redirect(url_for('fridges'))

@app.route('/fridges/delete', methods=['GET','POST'])
def fridges_delete():
    database = Database(filename)
    user_id = session['user_id']
    #user_id = 1
    material = request.args['name']
    #print 'calling deleteFromFridge({},{})'.format(user_id, [material])
    database.deleteFromFridge(user_id, [material])
    return redirect(url_for('fridges'))

@app.route('/fridges/clear')
def fridges_clear():
    user_id = session['user_id']
    database = Database(filename)
    database.clearFridge(user_id)
    return redirect(url_for('fridges'))

@app.route('/result', methods=['GET','POST'])
def result():
    if 'user_id' in session:
        database = Database(filename)
        user_id = session['user_id']
        user_name = database.findUserName(user_id)
        #user_id = 1
        recipes = database.deliverMyRecipe(user_id)
        fridge = database.deliverFridge(user_id)
        if len(fridge) != 0:
            fridge = fridge[0][1]
            fridge = fridge.split(' ')
        # fridge is a list of what you have-unicode
        # recipes is a list of tuple 
        recipe_list = list(recipes)
        result_list = []
        for one_recipe in recipes:
            dish_num = one_recipe[0]
            dish_name = one_recipe[1]
            still_need = one_recipe[2].split(' ') #components is a list of materials.
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
        return render_template('result.html', user_id=session['user_id'], data=sorted_result, user_name=user_name, language=session['language'])
    return render_template('login_name.html', language=session['language'])

#######
# admin
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not 'user_id' in session:
        return redirect(url_for('login_name'))
    if session['user_id'] != 0:
        return "You don't have the access!"
    return redirect(url_for('recipes'))
            
@app.route('/admin/myrecipes', methods=['GET', 'POST'])
def admin_my_recipes():
    if not 'user_id' in session:
        return redirect(url_for('login_name'))
    if session['user_id'] != 0:
        return "You don't have the access!"
    user_id = request.args['user_id']
    recipes = []
    if request.method == 'POST':
        user_id = request.form['next_user_id']
    database = Database(filename)
    recipes = database.deliverMyRecipe(user_id)
    return render_template('admin_my_recipes.html', user_id=user_id, recipes=recipes)

@app.route('/admin/myrecipes/insert', methods=['GET', 'POST'])
def admin_my_recipes_insert():
    if not 'user_id' in session:
        return redirect(url_for('login_name'))
    if session['user_id'] != 0:
        return "You don't have the access!"
    user_id = 0
    if request.method == 'POST':
        user_id = request.form['current_user_id']
        database = Database(filename)
        content = request.form['content']
        if content == '':
            return redirect(url_for('admin_my_recipes', user_id=user_id))
        content = Unicode_to_UTF8(content)
        content = content.split(' ')
        dish_name = content[0]
        content.remove(dish_name)
        components = content
        database.insertMyRecipeEntry(user_id, dish_name, components)
    return redirect(url_for('admin_my_recipes',user_id=user_id))

@app.route('/admin/myrecipes/delete', methods=['GET', 'POST'])
def admin_my_recipes_delete():
    if not 'user_id' in session:
        return redirect(url_for('login_name'))
    if session['user_id'] != 0:
        return "You don't have the access!"
    user_id = request.args['current_user_id']
    database = Database(filename)
    database.deleteMyRecipeEntry(user_id, request.args['id'])
    return redirect(url_for('admin_my_recipes', user_id=user_id))

@app.route('/admin/fridges', methods=['GET','POST'])
def admin_fridges():
    if not 'user_id' in session:
        return redirect(url_for('login_name'))
    if session['user_id'] != 0:
        return "You don't have the access!"
    user_id = request.args['user_id']
    if request.method == 'POST':
        user_id = request.form['next_user_id']
    database = Database(filename)
    fridges = database.deliverFridge(user_id)
    if len(fridges) != 0:
        fridges = fridges[0][1].split(' ')
    # now fridges is a list of stock
    return render_template('admin_fridges.html', user_id=user_id, fridges=fridges)

@app.route('/admin/fridges/insert', methods=['GET','POST'])
def admin_fridges_insert():
    if not 'user_id' in session:
        return redirect(url_for('login_name'))
    if session['user_id'] != 0:
        return "You don't have the access!"
    user_id = 0
    if request.method == 'POST':
        user_id = request.form['current_user_id']
        database = Database(filename)
# user_fridge is a list of what is already in fridge
        add_stock_text = request.form['content']
        if add_stock_text == '':
            return redirect(url_for('admin_fridges', user_id=user_id))
        add_stock_text = add_stock_text.split(' ')
        database.insertToFridge(user_id, add_stock_text)
    return redirect(url_for('admin_fridges', user_id=user_id))

@app.route('/admin/fridges/delete', methods=['GET','POST'])
def admin_fridges_delete():
    if not 'user_id' in session:
        return redirect(url_for('login_name'))
    if session['user_id'] != 0:
        return "You don't have the access!"
    user_id = request.args['current_user_id']
    database = Database(filename)
    #user_id = 1
    material = request.args['name']
    #print 'calling deleteFromFridge({},{})'.format(user_id, [material])
    database.deleteFromFridge(user_id, [material])
    return redirect(url_for('admin_fridges', user_id=user_id))

@app.route('/admin/statistics')
def admin_statistics():
    if not 'user_id' in session:
        return redirect(url_for('login_name'))
    if session['user_id'] != 0:
        return "You don't have the access!"
    database = Database(filename)
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    num_recipes = c.execute('select count(*) from recipes')
    num_recipes = num_recipes.fetchone()[0]
    num_users = c.execute('select count(*) from users')
    num_users = num_users.fetchone()[0]
    return render_template('admin_statistics.html', num_users=num_users, num_recipes=num_recipes)

@app.route('/admin/userlist')
def admin_user_list():
    if not 'user_id' in session:
        return redirect(url_for('login_name'))
    if session['user_id'] != 0:
        return "You don't have the access!"
    database = Database(filename)
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    users = c.execute('SELECT * FROM users')    # users is a cursor object
    users = list(users)     # users is a list of tuple, like [(0,'admin','admin@gmail.com'),(1,'111','111@gmail.com'),(2,'222','222@gmail.com')]
    return render_template('admin_user_list.html', users=users)


app.secret_key = '\ng\xaa!\x01\xd8\xd2%Ftz}m\xf0\xa1\xe6\xdf\xe8I\x8a\xb8\x80\xb6\x90'



if __name__ == '__main__':
    app.run()
