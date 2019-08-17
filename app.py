import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] ='cook_book'
app.config["MONGO_URI"] = 'mongodb+srv://AnetA:AnetA2@myfirstcluster-sfmlq.mongodb.net/cook_book?retryWrites=true&w=majority'

mongo = PyMongo(app)





#--------------------------Find Recipes Page------------------


@app.route('/')
@app.route('/find_recipes')
def find_recipes():
  return render_template("recipes.html", recipes=mongo.db.recipes.find())
  
  
#--------------------------Add Recipes Page-------------------
  
  
@app.route('/add_recipe')
def add_recipe():
  return render_template('addrecipe.html', categories=mongo.db.categories.find())
  
  
#-------Enable To Add Recipe and Redirect To Recipe Page------
  
  
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
  recipes=mongo.db.recipes
  recipes.insert_one(request.form.to_dict())
  return redirect(url_for('find_recipes'))
  
  
#-------Enable To View Particular Recipe----------------------
  
  
@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
  my_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
  my_categories = mongo.db.categories.find()
  return render_template('viewrecipe.html', recipe=my_recipe,
                           categories=my_categories)
                           
                           
#--------------Enable To Edit Particular Recipe----------------
  

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
  this_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
  all_categories = mongo.db.categories.find()
  return render_template('editrecipe.html', recipe=this_recipe,
                            categories=all_categories)
                            
                            
#-----Enable To Update Recipe And Redirect To Recipe Page-------

                            
@app.route('/update_recipe/<recipe_id>', methods= ['POST'])
def update_recipe(recipe_id):
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
    'cusine_name': request.form.get('cusine_name'),
    'cooking_time': request.form.get('cooking_time')
  })
    
  
  return redirect(url_for('find_recipes'))
  
  
#----------------Enable To Delete Particular Recipe--------------
  
  
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
  mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
  return redirect(url_for('find_recipes'))
  




  

#-------------------Find Categories Page------------------------


@app.route('/find_categories')
def find_categories():
  return render_template('categories.html', categories=mongo.db.categories.find())
  
  
#-------------------Edit Category Page---------------------------

  
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
  return render_template('editcategory.html', category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))
  
  
#----Enable To Update Category And Redirect To Categories Page----
  

@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
  mongo.db.categories.update({'_id': ObjectId(category_id)}, {'category_name': request.form.get('category_name')})
  return redirect(url_for('find_categories'))
  

#-------Enable To Add Category And Redirect To Categories Page-----


@app.route('/add_category', methods=['POST'])
def add_category():
  my_category = {'category_name': request.form.get('category_name')}
  mongo.db.categories.insert_one(my_category)
  return redirect(url_for('find_categories'))
  
#--------------------------Add Category Page------------------------


@app.route('/new_category')
def new_category():
  return render_template('addcategory.html')
  
#--------------------Enable To Delete Category----------------------
  

@app.route('/delete_category/<category_id>')
def delete_category(category_id):
  mongo.db.categories.remove({'_id': ObjectId(category_id)})
  return redirect(url_for('find_categories'))
  


if __name__ == '__main__':
  app.run(host=os.environ.get('IP'),
  port=int(os.environ.get('PORT')),
  debug=True)  
  