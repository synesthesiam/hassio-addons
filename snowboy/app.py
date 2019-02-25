import os
import json
from uuid import uuid4

from flask import Flask, request, send_file, render_template, safe_join

app = Flask('mycroft-precise', template_folder='.')
app.secret_key = str(uuid4())

config_path = os.environ.get('CONFIG_PATH', '/data/options.json')
models_dir = os.environ.get('MODEL_PATH', '/share/snowboy')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'delete' in request.form:
            model_name = request.form['model']
            model_path = safe_join(models_dir, model_name)
            if os.path.exists(model_path):
                os.unlink(model_path)
        elif 'file' in request.files:
            file = request.files['file']
            model_name = file.filename
            model_path = safe_join(models_dir, model_name)
            os.makedirs(models_dir, exist_ok=True)
            file.save(model_path)

    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    models = []
    if os.path.exists(models_dir):
        for model_name in os.listdir(models_dir):
            models.append(os.path.join(models_dir, model_name))

    return render_template('index.html', config=config, models=models)
