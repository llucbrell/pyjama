from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from database import session, Sampler

samplers_bp = Blueprint('samplers', __name__)

UPLOAD_FOLDER = 'samplers/soundfonts'
ALLOWED_EXTENSIONS = {'sf2'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@samplers_bp.route('/samplers')
def samplers():
    samplers = session.query(Sampler).all()
    return render_template('samplers.html', samplers=samplers)

@samplers_bp.route('/add_sampler', methods=['POST'])
def add_sampler():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        name = request.form.get('name')
        new_sampler = Sampler(name=name, filename=filename)
        session.add(new_sampler)
        session.commit()
        return redirect(url_for('samplers.samplers'))

@samplers_bp.route('/edit_sampler/<int:sampler_id>', methods=['POST'])
def edit_sampler(sampler_id):
    sampler = session.query(Sampler).filter_by(id=sampler_id).first()
    data = request.form
    sampler.name = data.get('name')
    session.commit()
    return redirect(url_for('samplers.samplers'))

@samplers_bp.route('/delete_sampler/<int:sampler_id>')
def delete_sampler(sampler_id):
    sampler = session.query(Sampler).filter_by(id=sampler_id).first()
    os.remove(os.path.join(UPLOAD_FOLDER, sampler.filename))
    session.delete(sampler)
    session.commit()
    return redirect(url_for('samplers.samplers'))
