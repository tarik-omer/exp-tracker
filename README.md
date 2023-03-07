# Money Rails

## We will keep your expenses on track.

### Description

This project is a web application that you can track your expenses with. You add expenses based on name, category, date and amount. You can edit and delete existent expenses. Charts of monthly and yearly expenses are also available for the user. Requires Signup and Login for usage.

### Languages and technologies

- Python3.9.7 + Flask + Jinja2 -> backend, API, routing, HTML inheritance, HTML for-loops, HTML parameters
- HTML + CSS (Bulma Framework) -> front-end
- SQLAlchemy (SQLite) -> database management
- Flask Login -> authentification management
- Chart.js -> chart generation

See versions and other plugins in 'requirement.txt'.

### Usage

For local running:

- run command: 'source proj/bin/activate' to activate virtual machine

- make install -> installs required packages
- make build -> set required environment variables
- make run -> activates app on 'http://127.0.0.1:5000' (localhost)

For live usage, sign up and join us on [Money Rails - Expense Tracker](http://moneyrails.pythonanywhere.com/).

### Improvements

- Better handling of the database (tables - 1 for Users, 1 for Expenses)
- More features - see months of previous years, see charts based on categories
- Better front-end for mobile devices
