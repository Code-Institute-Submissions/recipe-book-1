import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId




app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipes'
app.config["MONGO_URI"] = 'mongodb://marcus:rugby4me@ds221003.mlab.com:21003/recipes'



mongo = PyMongo(app)




@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", recipes=mongo.db.the_recipes.find())
    
    
@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html',
    categories=mongo.db.categories.find())
    
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes =  mongo.db.the_recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe =  mongo.db.the_recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('editrecipe.html', recipe=the_recipe, categories=all_categories)
    
@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.the_recipes
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe_name'),
        'category_name':request.form.get('category_name'),
        'ingredients': request.form.get('ingredients'),
        'method': request.form.get('method')
    })
    return redirect(url_for('get_recipes'))
    
    
    
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.the_recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))

@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
    categories=mongo.db.categories.find())

@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form['category_name']})
    return redirect(url_for('get_categories'))

@app.route('/delete_category/<category_id>')  
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for("get_categories"))
    
@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories
    category_doc = {'category_name': request.form['category_name']}
    categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))
    

@app.route('/new_category')
def new_category():
    return render_template('addcategory.html')
    


@app.route('/')        
@app.route('/index', methods=['GET', 'POST'])
def index():
    search_term = []
    if request.method == 'POST':
        search_term = request.form['recipe_name']
    return render_template('index.html', the_recipe=mongo.db.the_recipes.find_one({"recipe_name": search_term}))
       
@app.route('/category_search', methods=['GET', 'POST'])
def category_search():
    search_term = []
    if request.method == 'POST':
        search_term = request.form['category_name']
    return render_template('category_search.html', the_recipe=mongo.db.the_recipes.find_one({"category_name": search_term}))
 

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
