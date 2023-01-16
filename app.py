from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World!"