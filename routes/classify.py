from flask import Blueprint,session,request, jsonify, send_from_directory, current_app, render_template
from services.classifyAlex import ImageClassifier
from services.classifyVGG import ImageClassifier2
from werkzeug.utils import secure_filename
import os

from flask import session, redirect, url_for
image_bp = Blueprint('classify', __name__)

ALLOWED_EXTENSIONS = {'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@image_bp.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':

        if 'file' not in request.files:
            return jsonify({'code': -1, 'message': 'No file part', 'data': {}})
        user_id = session['user_id']
        file = request.files['file']
        if file.filename == '':
            return jsonify({'code': -1, 'message': 'No selected file', 'data': {}})

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # Get the selected model from the form
            model_type = request.form.get('model')
            print(f"Selected model type: {model_type}")

            try:
                if model_type == 'alexnet':
                    model_path = "./ai/mushroom_alex_32_0.0001.mod"
                    classifier = ImageClassifier(model_path=model_path)
                elif model_type == 'vgg':
                    model_path = "./ai/mushroom_vgg_64_0.0001.mod"
                    classifier = ImageClassifier2(model_path=model_path)
                else:
                    return jsonify({'code': -1, 'message': 'Invalid model type selected', 'data': {}})

                predicted_class, confidence = classifier.classify_image(file_path, user_id)
                return render_template('mrclassify.html',
                                       predicted_class=predicted_class,
                                       confidence=confidence,
                                       filename=filename)
            except Exception as e:
                return jsonify({'code': -1, 'message': f'Error loading model: {e}', 'data': {}})


@image_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@image_bp.route('/records')
def view_records():
    username = session.get('username')
    if username:
        record_class = globals().get(f'Record_{username}')
        if record_class:
            records = record_class.query.filter_by(user_id=username).all()
            return render_template('test.html', records=records)
    return "No records found."
