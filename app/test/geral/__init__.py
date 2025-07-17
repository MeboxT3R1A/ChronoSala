from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.db import db

geral_bp = Blueprint('geral_bp', __name__)