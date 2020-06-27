from application import app
from flask import render_template,request, json, Response, redirect, flash, url_for, session
import random
from datetime import datetime


@app.route("/")
@app.route("/login", methods=['POST'])
def login():
    return render_template("login.html")
