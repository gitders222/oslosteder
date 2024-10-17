from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    cuisine_type = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)


@app.route('/')
def home():
    restaurants = Restaurant.query.all()  # Fetch all restaurants from the database
    return render_template('home.html', restaurants=restaurants)

@app.route('/restaurants')
def show_restaurants():
    restaurants = Restaurant.query.all()
    return render_template('steder.html', restaurants=restaurants)


    
@app.route('/restaurants/<int:id>', methods=['GET', 'POST'])
def restaurant_detail(id):
    restaurant = Restaurant.query.get_or_404(id)
    if request.method == 'POST':
        user = request.form['user']
        comment = request.form['comment']
        rating = request.form['rating']
        review = Review(user=user, comment=comment, rating=rating, restaurant_id=id)
        db.session.add(review)
        db.session.commit()
        return redirect(f'/restaurants/{id}')
    reviews = Review.query.filter_by(restaurant_id=id).all()
    return render_template('steder_detalj.html', restaurant=restaurant, reviews=reviews)    

@app.route('/add', methods=['GET', 'POST'])
def add_restaurant():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        cuisine_type = request.form['cuisine_type']
        rating = request.form['rating']
        
        # Create a new Restaurant object
        new_restaurant = Restaurant(name=name, location=location, cuisine_type=cuisine_type, rating=rating)
        
        # Add it to the database and commit
        db.session.add(new_restaurant)
        db.session.commit()
        
        # Redirect to a different route (e.g., the list of restaurants)
        return redirect(url_for('show_restaurants'))
    
    return render_template('add_steder.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
