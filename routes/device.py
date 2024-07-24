from flask import Blueprint, render_template, request, jsonify, current_app
import os
import fluidsynth
import mido
from sf2utils.sf2parse import Sf2File
from database import session, Configuration, Sampler

device_bp = Blueprint('device', __name__)

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

@device_bp.route('/device')
def device():
    global midi_input
    active_config = session.query(Configuration).filter_by(active=True).first()
    sampler_id = request.args.get('sampler_id')
    preset = request.args.get('preset', type=int)
    sampler = session.query(Sampler).filter_by(id=sampler_id).first()

    if not active_config:
        return "No active configuration found.", 400
    
    sffilepath = os.path.join(UPLOAD_FOLDER, sampler.filename)
    initialize_synth(sffilepath, preset)

    try:
        midi_input = mido.open_input(active_config.port)
        midi_input.callback = handle_midi_message
        current_app.logger.debug(f"Connected to MIDI port: {active_config.port}")
    except Exception as e:
        return f"Failed to connect to MIDI port: {e}", 500

    return render_template('device.html', config=active_config, sampler=sampler, preset=preset)

