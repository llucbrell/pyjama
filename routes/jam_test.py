from flask import Blueprint, render_template, request, jsonify, current_app
import os
import fluidsynth
import mido
from database import session, Sampler, Configuration

jam_test_bp = Blueprint('jam_test', __name__)

synth = None
sffilepath = None
midi_input = None
soundfont_path = "samplers/soundfonts/Strings.sf2"

UPLOAD_FOLDER = 'samplers/soundfonts'

def initialize_synth():
    global synth, sffilepath
    if synth is None:
        synth = fluidsynth.Synth()
        synth.start(driver='alsa')  # Usa ALSA como backend
        print(sffilepath)
        sfid = synth.sfload(sffilepath)
        synth.program_select(0, sfid, 0, 0)
        synth.cc(0, 7, 100)
        current_app.logger.debug("Synth initialized")
        current_app.logger.debug(sffilepath)

@jam_test_bp.route('/jam_test/<int:sampler_id>')
def jam_test(sampler_id):
    global synth, midi_input, sffilepath
    sampler = session.query(Sampler).filter_by(id=sampler_id).first()
    sffilepath = os.path.join(UPLOAD_FOLDER, sampler.filename)
    print(sffilepath)
    current_app.logger.debug(f"File SoundFont: {sampler.filename}")
    sffilepath = os.path.join(UPLOAD_FOLDER, sampler.filename)
    active_config = session.query(Configuration).filter_by(active=True).first()
    initialize_synth()
    midi_ports = mido.get_input_names()
    message = None
    if active_config:
        try:
            if midi_input is None:
                midi_input = mido.open_input(active_config.port)
            current_app.logger.debug(f"Loading SoundFont: {sampler.filename}")
            sfid = synth.sfload(sffilepath, update_midi_preset=True)
            if sfid == -1:
                raise Exception("Failed to load SoundFont")
            current_app.logger.debug("SoundFont loaded successfully")
        except Exception as e:
            message = str(e)
            current_app.logger.error(f"Error initializing synth or loading SoundFont: {e}")
    else:
        message = "No active configuration found"
        current_app.logger.error(message)
    return render_template('jam_test.html', sampler=sampler, midi_ports=midi_ports, message=message)

@jam_test_bp.route('/send_note', methods=['POST'])
def send_note():
    current_app.logger.debug("SEND_NOTE")
    global synth
    data = request.get_json()
    if not data or 'note' not in data or 'action' not in data:
        error_response = jsonify({"status": "error", "message": "Invalid request"})
        current_app.logger.error(f"Invalid request: {error_response.get_data(as_text=True)}")
        return error_response, 400

    note = int(data['note'])
    action = data['action']
    try:
        if synth is None:
            initialize_synth()  # Asegúrate de que el sintetizador esté inicializado
        if action == 'note_on':
            current_app.logger.debug(f"Note on: {note}")
            synth.noteon(0, note, 100)
        elif action == 'note_off':
            current_app.logger.debug(f"Note off: {note}")
            synth.noteoff(0, note)
        success_response = jsonify({"status": "success", "note": note, "action": action})
        current_app.logger.debug(success_response.get_data(as_text=True))
        return success_response
    except Exception as e:
        error_response = jsonify({"status": "error", "message": str(e)})
        current_app.logger.error(f"Error processing note: {error_response.get_data(as_text=True)}")
        return error_response, 500
