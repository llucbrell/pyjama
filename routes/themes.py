# routes/theme.py
import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import Base, Theme

# Configuración de la base de datos
engine = create_engine('sqlite:///pyjama_data.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

theme_bp = Blueprint('theme', __name__)

# Configuración para las subidas de archivos
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@theme_bp.route('/themes')
def list_themes():
    themes = session.query(Theme).all()
    return render_template('list_themes.html', themes=themes)

@theme_bp.route('/themes/add', methods=['POST'])
def add_theme():
    title = request.form['title']
    new_theme = Theme(title=title)
    session.add(new_theme)
    session.commit()
    return redirect(url_for('theme.list_themes'))

@theme_bp.route('/themes/edit/<int:theme_id>', methods=['GET', 'POST'])
def edit_theme(theme_id):
    theme = session.query(Theme).get(theme_id)
    if request.method == 'POST':
        theme.title = request.form['title']
        theme.author = request.form['author']
        theme.player = request.form['player']
        theme.genre = request.form['genre']
        
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.root_path, UPLOAD_FOLDER, filename))
                theme.image = filename
        
        session.commit()
        return redirect(url_for('theme.list_themes'))
    return render_template('edit_theme.html', theme=theme)

@theme_bp.route('/themes/delete/<int:theme_id>', methods=['POST'])
def delete_theme(theme_id):
    theme = session.query(Theme).get(theme_id)
    session.delete(theme)
    session.commit()
    return redirect(url_for('theme.list_themes'))
