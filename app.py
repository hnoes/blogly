"""Blogly application."""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, connect_db


app = Flask(__name__)

# Database configuration.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable modification tracking
app.config['SQLALCHEMY_ECHO'] = True # Enable SQL echo for debugging

# Initialize SQLAlchemy and Debug Toolbar
db.init_app(app)
toolbar = DebugToolbarExtension(app)

# Initialize database connection
connect_db(app)

# Route for the homepage
@app.route('/')
def index():
    return redirect('/users')
    return render_template('base.html') # Display base template

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        image_url = request.form['image_url']

        new_user = User(first_name=first_name, last_name=last_name, email=email, image_url = image_url)
        db.session.add(new_user)
        db.session.commit()

        flash(f'User {first_name} {last_name} added successfully!', 'success')


    return render_template('new_user.html')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id) 

    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        user.image_url = request.form['image_url']

        db.session.commit()

        flash(f'User {user.first_name} {user.last_name} updated successfully!', 'success')
        return redirect(f'/users/{user.id}')

    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f'User {user.first_name} {user.last_name} deleted successfully!', 'success')
    return redirect('/users')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables within the app context

    app.run(debug=True) # Run the app in debug mode 