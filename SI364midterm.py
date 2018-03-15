###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
import os
from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import sys; print(sys.version)
## https://stackoverflow.com/questions/21122540/input-error-nameerror-name-is-not-defined


## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

## All app.config values database URI.
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/kessen364midterm"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard to guess string from si364'

## Statements for db setup (and manager setup if using Manager)

manager = Manager(app)
db = SQLAlchemy(app) 
migrate = Migrate(app, db) 
manager.add_command('db', MigrateCommand) 


######################################
######## HELPER FXNS (If any) ########
######################################




##################
##### MODELS #####
##################
## 2 db.Models required 

class bitcoin(db.Model):
    __tablename__ = "bitcoin"
    id = db.Column(db.Integer, primary_key=True)
    bitcoin = db.Column(db.String(64))
    #username = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "{} | ID: {})".format(self.bitcoin,self.id)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    #display_name = db.Column(db.String(124)) 


    def __repr__(self):
        return "{} | ID: {})".format(self.username,self.id)

###################
###### FORMS ######
###################

class bitcoinForm(FlaskForm):
    bitcoin = StringField("Which bitcoin are you interested in?", validators=[Required(), Length(min=1, max=64)])
    username = StringField('What is your name?', validators=[Required(), Length(min=1, max=24)])
    #email = StringField('Enter your email (must include an @'), validators=[Required(@)]
    submit = SubmitField('Submit')

    def validate_bitcoin(self, field):
        if (len(field.data) < 1) and (len(field.data) > 64):
            raise ValidationError("Please keep your Tweet between 1 and 280 characters long!")
'''
    def validate_username(self, field):
        if field.data.has('@'):
            raise ValidationError("Please do not add the @ in the username")
        if (len(field.data) < 1) and (len(field.data) > 64):
            raise ValidationError("Username field must be between 1 and 64 characters long.")
'''

#######################
###### VIEW FXNS ######
#######################
## Homepage 

@app.route('/')
def index():
    num_bitcoin = len(bitcoin.query.all())
    return render_template('home.html', num_bitcoin=num_bitcoin)


@app.route('/form', methods = ['GET', 'POST'])
def enter_info():
    form = bitcoinForm()
    if form.validate_on_submit():
        #Get the form data in variables
        bitcoin_name = form.bitcoin.data
        username = form.username.data
        #email = form.email.data
        possible_bitcoin = bitcoin.query.filter_by(bitcoin=bitcoin_name).first()
        possible_user = User.query.filter_by(username=username).first()
        if possible_user is None: 
            user_obj = User(username=username)
            db.session.add(user_obj)
            db.session.commit()
        possible_user_id = User.query.filter_by(username=username).first().id 
        
        if possible_bitcoin is None:
            BT = bitcoin(bitcoin=bitcoin_name, user_id=possible_user_id)
            db.session.add(BT)
            db.session.commit()
        return redirect(url_for('enter_info'))
        flash('Your information has been added!')
    return render_template('index.html', form=form)


###########################
## Error handling routes ##
###########################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



## Code to run the application...

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
if __name__ == "__main__":
    db.create_all()
    app.run(use_reloader=True,debug=True)
