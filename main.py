from flask import Blueprint, render_template, redirect, url_for, request, Flask
from flask_login import login_required, current_user
from pickle import dumps, loads
from .expenses import ExpensesList
from . import create_app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    if current_user.expenses == None:
        current_user.expenses = dumps(ExpensesList())
        current_user.save()
    
    expenses_unpickled = loads(current_user.expenses)
    expenses_unpickled_list = expenses_unpickled.expenses
    return render_template('profile.html', name=current_user.name, expensesList=expenses_unpickled_list)