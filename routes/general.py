from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from database import session, Configuration
import mido

general_bp = Blueprint('general', __name__)



@general_bp.route('/')
def index():
    return render_template('index.html')

@general_bp.route('/about')
def about():
    return render_template('about.html')

# Manejador de error 404
@general_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
