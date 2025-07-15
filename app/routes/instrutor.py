from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import conectar

instrutor = Blueprint('instrutor', __name__)

@instrutor.route('/')
def painel():
    return render_template('instrutor.html')
