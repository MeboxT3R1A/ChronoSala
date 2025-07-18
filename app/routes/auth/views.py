# app/routes/auth/views.py
from flask import render_template, request, redirect, url_for, flash
from app.db import get_db
from . import login_bp 

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')