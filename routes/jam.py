from flask import Blueprint, render_template, request, jsonify, current_app
import os
import fluidsynth
import mido
from database import session, Theme, ParamSong, Instrument, Configuration

jam_bp = Blueprint('jam', __name__)

synth = None
midi_input = None
UPLOAD_FOLDER = 'samplers/soundfonts'

def initialize_synth(sffilepath, preset):
    global synth
    if synth is None:
        synth = fluidsynth.Synth()
        synth.start(driver='alsa')  # Usa ALSA como backend
    sfid = synth.sfload(sffilepath, update_midi_preset=True)
    synth.program_select(0, sfid, 0, preset)
    synth.cc(0, 7, 127)  # Set volume to maximum

def handle_midi_message(message):
    global synth
    if message.type == 'note_on':
        synth.noteon(0, message.note, message.velocity)
    elif message.type == 'note_off':
        synth.noteoff(0, message.note)
    elif message.type == 'control_change':
        if message.control == 64:  # Sustain pedal
            synth.cc(0, 64, message.value)

@jam_bp.route('/jam/<int:theme_id>')
def jam(theme_id):
    global midi_input
    theme = session.query(Theme).get(theme_id)
    param_songs = session.query(ParamSong).filter_by(theme_id=theme_id).all()

    active_config = session.query(Configuration).filter_by(active=True).first()
    if not active_config:
        return "No active configuration found.", 400

    # Conectarse al puerto MIDI activo
    try:
        midi_input = mido.open_input(active_config.port)
        midi_input.callback = handle_midi_message
        current_app.logger.debug(f"Connected to MIDI port: {active_config.port}")
    except Exception as e:
        return f"Failed to connect to MIDI port: {e}", 500

    return render_template('jam.html', theme=theme, param_songs=param_songs)

@jam_bp.route('/play_instrument', methods=['POST'])
def play_instrument():
    global synth
    data = request.get_json()
    if not data or 'preset' not in data or 'soundfont' not in data:
        return jsonify({"status": "error", "message": "Invalid request"}), 400

    preset = data['preset']
    soundfont = data['soundfont']

    try:
        sffilepath = os.path.join(UPLOAD_FOLDER, soundfont)
        initialize_synth(sffilepath, preset)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
