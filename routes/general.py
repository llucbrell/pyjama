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

