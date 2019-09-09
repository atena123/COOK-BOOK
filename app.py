import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.secret_key =os.environ.get('SECRET_KEY')

app.config["MONGO_DBNAME"] ='COOK-BOOK'
app.config["MONGO_URI"]=os.environ.get('MONGO_URI')

mongo = PyMongo(app)



                


#-------------Registration & Login-------------

@app.route('/')
def index():
        return render_template('index.html')
        
                
@app.route('/login', methods=['POST'])
def login():
        users = mongo.db.users
        login_user = users.find_one({'name': request.form['username']})
        
        if login_user:
                if request.form['pass'] and login_user['password'] == login_user['password']:
                        session['username'] = request.form['username']
                        return redirect(url_for('find_recipes'))
                        
        return redirect(url_for('register'))
        
        
        
@app.route('/register', methods=['POST', 'GET'])
def register():
        if request.method == 'POST':
            users = mongo.db.users
            existing_user = users.find_one({'name': request.form['username']})
            
            if existing_user is None:
                    hashpass = request.form['pass']
                    users.insert({'name': request.form['username'], 'password': hashpass})
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
                    
            return 'Username already exist'
                
        return render_template('register.html')
        
        
        
        
        
        
        
#-------------RECIPES-------------

@app.route('/find_recipes')
def find_recipes():
        """Find Recipe Page"""
        return render_template("recipes.html", recipes=mongo.db.recipes.find(), categories=mongo.db.categories.find())
                
                
@app.route('/add_recipe')
def add_recipe():
        """Add Recipe Page"""
        all_categories = mongo.db.categories.find()
        all_cuisines = mongo.db.cuisines.find()
        return render_template('add_recipe.html', categories=all_categories, cuisines=all_cuisines)
        
        
@app.route('/find_recipes/<category>')
def find_recipes_by_category(category):
        """Find Recipe By Category"""
        return render_template("recipes.html", recipes=mongo.db.recipes.find({"category_name":category}), categories=mongo.db.categories.find())

  
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
        """Enable To Add Recipe And Redirect To Recipe Page"""
        recipes=mongo.db.recipes
        recipes.insert_one(request.form.to_dict())
        return redirect(url_for('find_recipes'))

  
@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
        """Enable To View Particular Recipe"""
        recipes =  mongo.db.recipes
        my_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        return render_template('view_recipe.html', recipe=my_recipe)

  
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
        """Enable To Edit Particular Recipe"""
        this_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        all_categories = mongo.db.categories.find()
        all_cuisines = mongo.db.cuisines.find()
        return render_template('edit_recipe.html', recipe=this_recipe,
                            categories=all_categories, cuisines=all_cuisines)
                            

@app.route('/update_recipe/<recipe_id>', methods= ['POST'])
def update_recipe(recipe_id):
        """Enable To Update Recipe And Redirect To Recipe Page"""
        recipes=mongo.db.recipes
        recipes.update({"_id": ObjectId(recipe_id)},
  
        { 
        'category_name': request.form.get('category_name'),
        'recipe_name': request.form.get('recipe_name'), 
        'recipe_ingredients': request.form.get('recipe_ingredients'),
        'recipe_method': request.form.get('recipe_method'),
        'recipe_description': request.form.get('recipe_description'),
        'preparation_time': request.form.get('preparation_time'),
        'recipe_servings': request.form.get('recipe_servings'),
        'cuisine_name': request.form.get('cuisine_name'),
        'cooking_time': request.form.get('cooking_time'),
        'name': request.form.get('name')
        })
    
        return redirect(url_for('find_recipes'))

  
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
        """Enable To Delete Particular Recipe"""
        mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
        return redirect(url_for('find_recipes'))
  




  


  

#-------CATEGORIES--------

@app.route('/find_categories')
def find_categories():
        """Find Categories Page"""
        return render_template('categories.html', categories=mongo.db.categories.find())


@app.route('/new_category')
def new_category():
        """Add Category Page"""
        return render_template('add_category.html')


@app.route('/add_category', methods=['POST'])
def add_category():
        """Enable To Add Category And Redirect To Categories Page"""
        my_category = {'category_name': request.form.get('category_name')}
        mongo.db.categories.insert_one(my_category)
        return redirect(url_for('find_categories'))


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
        """Edit Category Page"""
        return render_template('edit_category.html', category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))

  
@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
        """Enable To Update Category And Redirect To Cateories Page"""
        mongo.db.categories.update({'_id': ObjectId(category_id)}, {'category_name': request.form.get('category_name')})
        return redirect(url_for('find_categories'))

  
@app.route('/delete_category/<category_id>')
def delete_category(category_id):
        """Enable To Delete Category"""
        mongo.db.categories.remove({'_id': ObjectId(category_id)})
        return redirect(url_for('find_categories'))
  






  
#-------Cuisines---------

@app.route('/find_cuisines')
def find_cuisines():
        """Cuisines Page"""
        return render_template('cuisines.html', cuisines=mongo.db.cuisines.find())


@app.route('/edit_cuisine/<cuisine_id>')
def edit_cuisine(cuisine_id):
        """Enable Edit Cuisine Page"""
        return render_template('edit_cuisine.html', cuisine=mongo.db.cuisines.find_one({'_id': ObjectId(cuisine_id)}))


@app.route('/add_cuisine')
def add_cuisine():
        """Add Cuisine Page"""
        return render_template('add_cuisine.html')


@app.route('/new_cuisine', methods=['POST'])
def new_cuisine():
        """Enable To Add New Cusine And Redirect To Cusines Page"""
        my_cuisine = {'cuisine_name': request.form.get('cuisine_name')}
        mongo.db.cuisines.insert_one(my_cuisine)
        return redirect(url_for('find_cuisines'))


@app.route('/update_cuisine/<cuisine_id>', methods=['POST'])
def update_cuisine(cuisine_id):
        """Enable To Update Cuisine And Redirect To Cuisines Page""" 
        mongo.db.cuisines.update({'_id': ObjectId(cuisine_id)}, {'cuisine_name': request.form.get('cuisine_name')})
        return redirect(url_for('find_cuisines'))


@app.route('/delete_cuisine/<cuisine_id>')
def delete_cuisine(cuisine_id):
        """Enable To Delete Cuisine And Redirect To Cuisines Page"""
        mongo.db.cuisines.remove({'_id': ObjectId(cuisine_id)})
        return redirect(url_for('find_cuisines'))



if __name__ == '__main__':
        app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)  
  

        