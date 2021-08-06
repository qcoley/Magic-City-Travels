from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy

import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRAC_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, nullable = False)
    interest = db.Column(db.String)

    def __init__(self, name, email, interest):
        self.name = name
        self.email = email
        self.interest = interest

    def __repr__(self):
        return f"User('{self.id}')"



# -----------------------------------------------------------------------------

@app.route('/', methods=['POST', 'GET'])
def home():

    # Sign in or create user account. Depending on which button you selected
    # on the home screen. this will direct the user to the new profile page
    # or the sign in page
    if request.method == 'POST':

        # new user page ----------------------------------------
        try:
            new_name = request.form['new_name']
            return render_template('addUser.html')

        except:
            pass


        # sign in page -----------------------------------------
        try:
            returning_name = request.form['returning_name']
            return render_template('sign_in.html')

        except:
            pass

    # Else just stay on the home page -----------------------------------------
    else:
        return render_template('index.html')

    return render_template('index.html')



# create new user with profile info and add to database -----------------------
@app.route('/user', methods=['POST', 'GET'])
def user():

    db.create_all()

    if request.method == 'POST':
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        user_interests = request.form['interests']
        new_user = User(name = user_name, email = user_email, interest = user_interests)

        db.session.add(new_user)
        db.session.commit()

        users = User.query.all()
        return render_template('created.html', users = users)


    else:
        users = User.query.all()
        return render_template('index.html', users = users)


    return render_template('index.html', users = users)


# searches for user in database and if the user exists, it will take you ------
# to your user profile
@app.route("/profile_page", methods=['POST', 'GET'])
def profile_page():

    user_name = request.form['user_name']

    try:
        query = User.query.all()

    except:
        pass

    try:
        for x in query:

            # if user name entered matches name in database -------------------
            if x.name == user_name:
                user = x

                user_info = [user.name, user.interest]

                return render_template('profile_page.html', user = user_info)

            else:
                print("Sorry, that profile does not exist")

    except:
        pass

    return render_template('sign_in.html')


# other app routes for additional pages ---------------------------------------
@app.route("/sign_in", methods=['POST', 'GET'])
def sign_in():
    return render_template('sign_in.html')


@app.route("/baranddrinks", methods=['POST', 'GET'])
def baranddrinks():
    return render_template('baranddrinks.html')


@app.route("/food_favs", methods=['POST', 'GET'])
def food_favs():
    return render_template('food_favs.html')


@app.route("/funandbeyond", methods=['POST', 'GET'])
def funandbeyond():
    return render_template('funandbeyond.html')


@app.route("/index", methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route("/show", methods=['POST', 'GET'])
def show():
    return render_template('show.html')


if __name__ == '__main__':
    app.run(debug=True)
