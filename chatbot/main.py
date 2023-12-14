from flask import Blueprint,render_template
from flask_login import login_required, current_user
from . import db
from .models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/chatbot')
@login_required
def chatbot():
    return render_template('chatbox.html', name=current_user.email)

@main.route('/admin')
@login_required
def admin():
    if current_user.usertype=='admin':         
        users = User.query
        return render_template('admin.html', users=users)
    else:
        return render_template('chatbox.html', name=current_user.email) 
