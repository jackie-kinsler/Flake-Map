"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
from datetime import datetime 

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefine = StrictUndefined


# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """Render root page of website"""

    return render_template('homepage.html', today = datetime.date(datetime.now()))

@app.route('/log-in')
def log_in():
    email = request.args.get('email')
    password = request.args.get('password')

    if crud.get_password_by_email(email) == password: 
        flash('Logged In!')
        session['user_id'] = crud.get_user_id_by_email(email)
        print(session)
        return redirect('/')
    else:
        flash('Log-in Failed')
        return redirect('/')
    
@app.route('/users', methods = ['POST'])
def create_account():
    """Create a new user"""

    email = request.form.get('email')
    password = request.form.get('password')

    if crud.get_user_by_email(email):
        flash('That email is already assigned to a registered account.')

    else: 
        crud.create_user(email, password)
        flash('User successfully registered')
    
    return redirect('/')

    
@app.route('/trails')
def trail_page():
    """Show a trail page that has a list of trails and a map"""


    return render_template('trailpage.html')

@app.route('/filtered-trails')
def filtered_trail(): 
    """Return a list of trails filtered on distance"""
    
    min_dist = request.args.get('min_dist')
    max_dist = request.args.get('max_dist')
    print(min_dist + " " + max_dist)
    
    trails = crud.trails_by_distance(min_dist, max_dist)

    trail_list = []

    for trail in trails: 
         trail_list.append({'trail_name' : trail.name,
                            'trail_url' : trail.url, 
                            'trail_distance' : trail.length,
                            'trail_location' : trail.location,

                           })


    return jsonify(trail_list)

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
