import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] ='cook_book'
app.config["MONGO_URI"] = 'mongodb+srv://AnetA:AnetA2@myfirstcluster-sfmlq.mongodb.net/cook_book?retryWrites=true&w=majority'

mongo = PyMongo(app)




@app.route('/')
@app.route('/get_recipes')
def get_recipes():
  return render_template("recipes.html", recipes=mongo.db.recipes.find())
  
  
@app.route('/add_recipe')
def add_recipe():
  return render_template('addrecipe.html', categories=mongo.db.categories.find())
  
  
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
  recipes=mongo.db.recipes
  recipes.insert_one(request.form.to_dict())
  return redirect(url_for('get_recipes'))
  
  
@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
  the_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
  all_categories = mongo.db.categories.find()
  return render_template('viewrecipe.html', recipe=the_recipe,
                           categories=all_categories)
  

  


    
if __name__ == '__main__':
  app.run(host=os.environ.get('IP'),
  port=int(os.environ.get('PORT')),
  debug=True)  
  