from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from database import session, Configuration
import mido

config_bp = Blueprint('config', __name__)

@config_bp.route('/')
def index():
    return redirect(url_for('config.config'))

@config_bp.route('/config')
def config():
    configurations = session.query(Configuration).all()
    active_config = session.query(Configuration).filter_by(active=True).first()
    midi_ports = mido.get_input_names()
    return render_template('config.html', configurations=configurations, active_config=active_config, midi_ports=midi_ports)

@config_bp.route('/add_config', methods=['POST'])
def add_config():
    data = request.form
    name = data.get('name')
    port = data.get('port')
    new_config = Configuration(name=name, port=port, active=False)
    session.add(new_config)
    session.commit()
    return redirect(url_for('config.config'))

@config_bp.route('/edit_config/<int:config_id>', methods=['POST'])
def edit_config(config_id):
    config = session.query(Configuration).filter_by(id=config_id).first()
    data = request.form
    config.name = data.get('name')
    config.port = data.get('port')
    session.commit()
    return redirect(url_for('config.config'))

@config_bp.route('/delete_config/<int:config_id>')
def delete_config(config_id):
    config = session.query(Configuration).filter_by(id=config_id).first()
    session.delete(config)
    session.commit()
    return redirect(url_for('config.config'))

@config_bp.route('/activate_config/<int:config_id>')
def activate_config(config_id):
    session.query(Configuration).update({Configuration.active: False})
    config = session.query(Configuration).filter_by(id=config_id).first()
    config.active = True
    session.commit()
    return redirect(url_for('config.config'))
