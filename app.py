from flask import Flask
from routes.config import config_bp
from routes.samplers import samplers_bp
from routes.jam_test import jam_test_bp

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'samplers/soundfonts'

app.register_blueprint(config_bp)
app.register_blueprint(samplers_bp)
app.register_blueprint(jam_test_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
