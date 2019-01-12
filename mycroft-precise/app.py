import os
import json
from uuid import uuid4

from flask import Flask, request, send_file, render_template

app = Flask('mycroft-precise', template_folder='.')
app.secret_key = str(uuid4())

config_path = os.environ.get('CONFIG_PATH', '/data/options.json')
model_path = os.environ.get('MODEL_PATH', '/models')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'delete' in request.form:
            model_name = request.form['model']
            os.unlink(os.path.join(model_path, model_name))
        elif 'file' in request.files:
            file = request.files['file']
            model_name = file.filename
            file.save(os.path.join(model_path, model_name))

    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    models = []
    if os.path.exists(model_path):
        for model_name in os.listdir(model_path):
            models.append(os.path.join(model_path, model_name))

    return render_template('index.html', config=config, models=models)
