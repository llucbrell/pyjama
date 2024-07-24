from flask import Blueprint, request, jsonify, render_template, redirect, url_for, current_app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import Base, Instrument, ParamSong

# Configuración de la base de datos
engine = create_engine('sqlite:///pyjama_data.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

instrument_bp = Blueprint('instrument', __name__)

@instrument_bp.route('/instruments', methods=['GET'])
def list_instruments():
    instruments = session.query(Instrument).all()
    return render_template('list_instruments.html', instruments=instruments)

@instrument_bp.route('/instruments/save', methods=['POST'])
def save_instrument():
    data = request.get_json()
    name = data.get('name')
    instrument_type = data.get('instrument_type', 'soundfont')
    source = data.get('source')
    preset = data.get('preset')

    if not name or not instrument_type or not source or preset is None:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    instrument = Instrument(name=name, instrument_type=instrument_type, source=source, preset=preset)
    session.add(instrument)
    session.commit()
    return jsonify({"status": "success", "message": "Instrument saved successfully"}), 200

@instrument_bp.route('/instruments/delete/<int:instrument_id>', methods=['POST'])
def delete_instrument(instrument_id):
    instrument = session.query(Instrument).get(instrument_id)
    if instrument:
        session.delete(instrument)
        session.commit()
        return jsonify({"status": "success", "message": "Instrument deleted successfully"}), 200
    return jsonify({"status": "error", "message": "Instrument not found"}), 404
