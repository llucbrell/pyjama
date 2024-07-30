from flask import Blueprint, render_template, request, jsonify, current_app
import os
import fluidsynth
import mido
from sf2utils.sf2parse import Sf2File
from database import session, Sampler, Configuration

jam_test_bp = Blueprint('jam_test', __name__)

synth = None
sffilepath = None
midi_input = None
UPLOAD_FOLDER = 'samplers/soundfonts'

def initialize_synth():
    global synth
    if synth is None:
        synth = fluidsynth.Synth()
        synth.start(driver='alsa')  # Usa ALSA como backend
        current_app.logger.debug("Synth initialized")


def get_presets(sffilepath):
    presets = []
    try:
        with open(sffilepath, 'rb') as sf2_file:
            sf = Sf2File(sf2_file)
            for preset in sf.presets:
                presets.append((preset.preset, preset.name))
    except Exception as e:
        current_app.logger.error(f"Error loading presets: {e}")
    return presets



@jam_test_bp.route('/jam_test/<int:sampler_id>')
def jam_test(sampler_id):
    global synth, sffilepath
    sampler = session.query(Sampler).filter_by(id=sampler_id).first()
    sffilepath = os.path.join(UPLOAD_FOLDER, sampler.filename)
    current_app.logger.debug(f"File SoundFont: {sampler.filename}")
    initialize_synth()
    
    message = None
    presets = []
    try:
        sfid = synth.sfload(sffilepath, update_midi_preset=True)
        if sfid == -1:
            raise Exception("Failed to load SoundFont")
        
        presets = get_presets(sffilepath)
        current_app.logger.debug(f"Presets loaded: {presets}")
    except Exception as e:
        message = str(e)
        current_app.logger.error(f"Error loading SoundFont or presets: {e}")
        return render_template('jam_test.html', sampler=sampler, presets=[], message=message)

    return render_template('jam_test.html', sampler=sampler, presets=presets, message=None)

@jam_test_bp.route('/send_note', methods=['POST'])
def send_note():
    current_app.logger.debug("SEND_NOTE")
    global synth
    data = request.get_json()
    if not data or 'note' not in data or 'action' not in data or 'preset' not in data:
        error_response = jsonify({"status": "error", "message": "Invalid request"})
        current_app.logger.error(f"Invalid request: {error_response.get_data(as_text=True)}")
        return error_response, 400

    note = int(data['note'])
    action = data['action']
    preset = int(data['preset'])
    try:
        if synth is None:
            initialize_synth()  # Asegúrate de que el sintetizador esté inicializado

        # Cargar solo el preset específico
        sfid = synth.sfload(sffilepath, update_midi_preset=True)
        synth.program_select(0, sfid, 0, preset)

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
