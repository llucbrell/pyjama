import time
import fluidsynth

def play_note_with_soundfont(soundfont_path, midi_note=60, velocity=100, duration=1):
    try:
        # Inicializar FluidSynth con ALSA
        fs = fluidsynth.Synth()
        fs.start(driver='alsa')  # Usa ALSA como backend

        # Cargar el SoundFont
        sfid = fs.sfload(soundfont_path)
        if sfid == -1:
            print("Error al cargar el SoundFont.")
            return
        
        fs.program_select(0, sfid, 0, 0)
        
        # Ajustar el volumen del canal
        fs.cc(0, 7, 100)  # Control Change para el volumen del canal (CC7)
        
        # Reproducir la nota MIDI
        fs.noteon(0, midi_note, velocity)
        time.sleep(duration)
        fs.noteoff(0, midi_note)
    
    except Exception as e:
        print(f"Se produjo un error: {e}")
    
    finally:
        # Finalizar FluidSynth
        fs.delete()

if __name__ == "__main__":
    # Ruta al archivo SoundFont
    soundfont_path = "samplers/soundfonts/Roland_64VoicePiano.sf2"
    
    # Configuración de la nota MIDI
    midi_note = 60      # Nota C4
    velocity = 100      # Velocidad de la nota
    duration = 1        # Duración en segundos
    
    # Reproducir la nota
    play_note_with_soundfont(soundfont_path, midi_note, velocity, duration)
