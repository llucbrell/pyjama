from flask import Blueprint, request, render_template, redirect, url_for, flash
from database import session, Theme, Instrument, ParamSong

song_instruments_bp = Blueprint('song_instruments', __name__)

@song_instruments_bp.route('/themes')
def list_themes():
    themes = session.query(Theme).all()
    return render_template('list_themes.html', themes=themes)

@song_instruments_bp.route('/themes/<int:theme_id>/instruments', methods=['GET', 'POST'])
def manage_instruments(theme_id):
    theme = session.query(Theme).get(theme_id)
    instruments = session.query(Instrument).all()
    related_instruments = session.query(ParamSong).filter_by(theme_id=theme_id).all()

    if request.method == 'POST':
        selected_instruments = request.form.getlist('instruments')
        for instrument_id in selected_instruments:
            param_song = ParamSong(params='default_params', instrument_id=instrument_id, theme_id=theme_id)
            session.add(param_song)
        session.commit()
        flash('Instruments added to the theme successfully.')
        return redirect(url_for('song_instruments.manage_instruments', theme_id=theme_id))

    return render_template('manage_instruments.html', theme=theme, instruments=instruments, related_instruments=related_instruments)

@song_instruments_bp.route('/themes/<int:theme_id>/instruments/remove/<int:param_id>', methods=['POST'])
def remove_instrument(theme_id, param_id):
    param_song = session.query(ParamSong).get(param_id)
    session.delete(param_song)
    session.commit()
    flash('Instrument removed from the theme successfully.')
    return redirect(url_for('song_instruments.manage_instruments', theme_id=theme_id))
