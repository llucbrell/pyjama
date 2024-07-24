from flask import Flask
from routes.config import config_bp
from routes.general import general_bp
from routes.samplers import samplers_bp
from routes.jam_test import jam_test_bp
from routes.device import device_bp
from routes.themes import theme_bp

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'samplers/soundfonts'


app.register_blueprint(general_bp)
app.register_blueprint(config_bp)
app.register_blueprint(samplers_bp)
app.register_blueprint(jam_test_bp)
app.register_blueprint(device_bp)  # Registra el nuevo blueprint
app.register_blueprint(theme_bp)  # Registra el nuevo blueprint

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
