from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from pickle import dumps, loads
import uuid
from datetime import date
from calendar import monthrange

expenses = Blueprint('expenses', __name__)
    
class Expense:
    def __init__(self, name, amount, date, category):
        self.name = name
        self.amount = amount
        self.date = date
        self.category = category
        self.id = uuid.uuid4()
    
class ExpensesList:
    def __init__(self):
        self.expenses = []
        
    def addExpense(self, expense):
        self.expenses.append(expense)
        
    def getExpense(self, id):
        for expense in self.expenses:
            if str(expense.id) == str(id):
                return expense
        return None    
    
    def getIndexOfExpense(self, id):
        for index, expense in enumerate(self.expenses):
            if str(expense.id) == str(id):
                return index
        return None
    
    def deleteExpense(self, id):
        index = self.getIndexOfExpense(id)
        if index != None:
            self.expenses.pop(index)
            return True
        return False

@expenses.route('/addExpense')
@login_required
def addExpense():
    today = date.today()
    
    return render_template('addExpense.html', date=today)
    
@expenses.route('/addExpense', methods=['POST'])
@login_required
def addExpense_post():
    # get data from form        
    name = request.form.get('name')
    amount = request.form.get('amount')
    date = request.form.get('date')
    category = request.form.get('category')
    
    # check non-null fields
    if len(name) == 0  or len(date) == 0 or len(category) == 0:
        flash('Please fill all the fields.')
        return redirect(url_for('expenses.addExpense'))
    elif amount.isnumeric() == False:
        flash('Please provide a number for the expense amount.')
        return redirect(url_for('expenses.addExpense'))
    
    # create expense object
    expense = Expense(name, amount, date, category)
    
    # init expenses list if it doesn't exist
    if current_user.expenses == None:
        current_user.expenses = dumps(ExpensesList())
    
    # add expense to expenses list after unpickling
    expenses_unpickled = loads(current_user.expenses)
    expenses_unpickled.addExpense(expense)
    expenses_pickled = dumps(expenses_unpickled)
    
    # update user's expenses
    current_user.expenses = expenses_pickled
    current_user.save()
    # redirect to profile page
    return redirect(url_for('main.profile'))

@expenses.route('/updateExpense/<id>', methods=['POST', 'GET'])
@login_required
def updateExpense(id):
    expenses_list = loads(current_user.expenses)

    expense = expenses_list.getExpense(id)
    
    if expense == None:
        return redirect(url_for('main.profile'))
    
    if request.method == 'POST':
        expense.name = request.form['name']
        expense.amount = request.form['amount']
        expense.date = request.form['date']
        expense.category = request.form['category']
        
        current_user.expenses = dumps(expenses_list)
        current_user.save()
        return redirect(url_for('main.profile'))        
    else :
        return render_template('updateExpense.html', expense_to_update=expense)
        

@expenses.route('/deleteExpense/<id>', methods=['GET'])
@login_required
def deleteExpense(id):
    expenses_list = loads(current_user.expenses)
    expenses_list.deleteExpense(id)
    
    current_user.expenses = dumps(expenses_list)
    current_user.save()

    return redirect(url_for('main.profile'))

@expenses.route('/yearlyExpenses')
@login_required
def yearlyExpenses():
    expenses_list = loads(current_user.expenses).expenses
    
    expenses_map = {}
    expenses_map["January"] = []
    expenses_map["February"] = []
    expenses_map["March"] = []
    expenses_map["April"] = []
    expenses_map["May"] = []
    expenses_map["June"] = []
    expenses_map["July"] = []
    expenses_map["August"] = []
    expenses_map["September"] = []
    expenses_map["October"] = []
    expenses_map["November"] = []
    expenses_map["December"] = []
        
    current_year = date.today().strftime("%Y")    
    
    for expense in expenses_list:
        # if expense is from this year
        if expense.date.split('-')[0] == date.today().strftime("%Y"):
            # add expense to the corresponding month
            expenses_map[getMonth(expense.date.split('-')[1])].append(expense)
    
    # calculate monthly sums
    monthly_sums = []
    for month in expenses_map:
        sum = 0
        for expense in expenses_map[month]:
            expense_int = int(expense.amount.split()[0])
            sum += int(expense_int)
        monthly_sums.append(sum)
     
     
    months_list = list(expenses_map.keys())        
                
    return render_template('yearlyExpenses.html', labels=months_list, values=monthly_sums, year=current_year)

@expenses.route('/monthlyExpenses')
@login_required
def monthlyExpenses():
    # get current month in format "xx"
    current_month = date.today().strftime("%m")

    # get number of days in current month    
    num_days = monthrange(int(date.today().strftime("%Y")), int(current_month))[1]
    
    # get list of days in current month
    days = [day for day in range(1, int(num_days) + 1)]
    
    
    # get expenses from current month
    expenses_list = loads(current_user.expenses).expenses

    # create list of expenses amounts for each day
    expenses_amounts = [0 for i in range(1, int(num_days) + 1)]
    
    
    # for each expense
    for expense in expenses_list:
        # if expense is from this month
        if int(expense.date.split('-')[1]) == int(current_month):
            if int(expense.date.split('-')[2]) in days:
                # add expense amount to the corresponding day
                expenses_amounts[int(expense.date.split('-')[2]) - 1] += int(expense.amount.split()[0])

    return render_template('monthlyExpenses.html', labels=days, values=expenses_amounts, month=getMonth(current_month))

@expenses.route('/monthlyExpenses/<month>')
@login_required
def monthlyExpenses_other(month):
    # get current month in format "xx"
    current_month = getMonthDigit(month)

    # get number of days in current month    
    num_days = monthrange(int(date.today().strftime("%Y")), int(current_month))[1]
    
    # get list of days in current month
    days = [day for day in range(1, int(num_days) + 1)]
    
    
    # get expenses from current month
    expenses_list = loads(current_user.expenses).expenses

    # create list of expenses amounts for each day
    expenses_amounts = [0 for i in range(1, int(num_days) + 1)]
    
    # for each expense
    for expense in expenses_list:
        # if expense is from this month
        if int(expense.date.split('-')[1]) == int(current_month):
            if int(expense.date.split('-')[2]) in days:
                # add expense amount to the corresponding day
                expenses_amounts[int(expense.date.split('-')[2]) - 1] += int(expense.amount.split()[0])

    return render_template('monthlyExpenses.html', labels=days, values=expenses_amounts, month=month)

def getMonth(month):
    switcher = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December"
    }
    return switcher.get(month, "Invalid month")
    
    
def getMonthDigit(month):
    switcher = {
        "January": "01",
        "February": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12"
    }
    return switcher.get(month, "Invalid month")
    