from application import app,db
from flask import render_template,request, json, Response, redirect, flash, url_for, session
import random
from datetime import datetime