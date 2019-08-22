import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "cookbook321"

app.config["MONGO_DBNAME"] ='cook_book'
app.config["MONGO_URI"] = 'mongodb+srv://AnetA:AnetA2@myfirstcluster-sfmlq.mongodb.net/cook_book?retryWrites=true&w=majority'

mongo = PyMongo(app)


                


#-------------RECIPES-------------

@app.route('/')
@app.route('/find_recipes')
def find_recipes():
        """Find Recipe Page"""
        return render_template("recipes.html", recipes=mongo.db.recipes.find(), categories=mongo.db.categories.find())

  
@app.route('/add_recipe')
def add_recipe():
        """Add Recipe Page"""
        all_categories = mongo.db.categories.find()
        all_cusines = mongo.db.cusines.find()
        return render_template('add_recipe.html', categories=all_categories, cusines=all_cusines)

  
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
        """Enable To Add Recipe And Redirect To Recipe Page"""
        recipes=mongo.db.recipes
        recipes.insert_one(request.form.to_dict())
        return redirect(url_for('find_recipes'))

  
@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
        """Enable To View Particular Recipe"""
        my_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        return render_template('view_recipe.html', recipe=my_recipe)

  
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
        """Enable To Edit Particular Recipe"""
        this_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        all_categories = mongo.db.categories.find()
        all_cusines = mongo.db.cusines.find()
        return render_template('edit_recipe.html', recipe=this_recipe,
                            categories=all_categories, cusines=all_cusines)
                            

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
        'cusine_name': request.form.get('cusine_name'),
        'cooking_time': request.form.get('cooking_time')
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
  






  
#-------Cusines---------

@app.route('/find_cusines')
def find_cusines():
        """Cusines Page"""
        return render_template('cusines.html', cusines=mongo.db.cusines.find())


@app.route('/edit_cusine/<cusine_id>')
def edit_cusine(cusine_id):
        """Enable Edit Cusine Page"""
        return render_template('edit_cusine.html', cusine=mongo.db.cusines.find_one({'_id': ObjectId(cusine_id)}))


@app.route('/add_cusine')
def add_cusine():
        """Add Cusine Page"""
        return render_template('add_cusine.html')


@app.route('/new_cusine', methods=['POST'])
def new_cusine():
        """Enable To Add New Cusine And Redirect To Cusines Page"""
        my_cusine = {'cusine_name': request.form.get('cusine_name')}
        mongo.db.cusines.insert_one(my_cusine)
        return redirect(url_for('find_cusines'))


@app.route('/update_cusine/<cusine_id>', methods=['POST'])
def update_cusine(cusine_id):
        """Enable To Update Cusine And Redirect To Cusines Page""" 
        mongo.db.cusines.update({'_id': ObjectId(cusine_id)}, {'cusine_name': request.form.get('cusine_name')})
        return redirect(url_for('find_cusines'))


@app.route('/delete_cusine/<cusine_id>')
def delete_cusine(cusine_id):
        """Enable To Delete Cusine And Redirect To Cusines Page"""
        mongo.db.cusines.remove({'_id': ObjectId(cusine_id)})
        return redirect(url_for('find_cusines'))



if __name__ == '__main__':
        app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)  
  

        