from flask import Blueprint, render_template, request, abort, Markup, jsonify, current_app, send_from_directory
from flask_login import current_user
from bs4 import BeautifulSoup
import os
from werkzeug.utils import secure_filename

bp = Blueprint('home', __name__)

current_directory = os.path.dirname(os.path.abspath(__file__))
template_directory = os.path.join(current_directory, 'templates')


@bp.route('/')
def homepage():
    return render_template('home.html', new_user=request.args.get("new"))


@bp.route('/save-home', methods=['POST'])
def save_home():
    if not current_user.is_authenticated or current_user.role != "admin":
        abort(401)

    try:
        home_nl_location = os.path.join(template_directory, 'home_content_nl.html')
        f = open(home_nl_location, 'w')
        soup = BeautifulSoup(request.form['homepagedataNL'], "html.parser")
        f.write(soup.prettify())
        f.close()

        home_en_location = os.path.join(template_directory, 'home_content_en.html')
        f = open(home_en_location, 'w')
        soup = BeautifulSoup(request.form['homepagedataEN'], "html.parser")
        f.write(soup.prettify())
        f.close()

        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return jsonify({'success': True, 'exception': e}), 400, {'ContentType': 'application/json'}


@bp.route('/home-editor')
def home_editor():
    return render_template('home_editor.html')


@bp.route('/get-home-data')
def get_home_data():
    data_nl = render_template('home_content_nl.html')
    data_nl = Markup(data_nl.replace('\n', ''))
    data_en = render_template('home_content_en.html')
    data_en = Markup(data_en.replace('\n', ''))

    home_directory = os.path.join(current_app.config['file-storage'], 'home')
    return jsonify({"nl": data_nl, "en": data_en, "documents": os.listdir(home_directory)})


@bp.route('/get-document/<string:name>')
def get_document(name):
    if secure_filename(name):
        home_directory = os.path.join(current_app.config['file-storage'], 'home')
        return send_from_directory(home_directory, name)
    return jsonify({'success': False}), 400, {'ContentType': 'application/json'}


@bp.route('/save-document', methods=['POST'])
def save_document():
    if current_user.role != "admin":
        abort(401)

    if 'file' not in request.files:
        return jsonify({'success': False}), 400, {'ContentType': 'application/json'}

    file = request.files['file']

    if file.filename == '':
        return jsonify({'success': False}), 400, {'ContentType': 'application/json'}

    filename = secure_filename(file.filename)
    upload_dir = os.path.join(current_app.config['file-storage'], 'home')

    if not os.path.isdir(upload_dir):
        os.mkdir(upload_dir)

    # Make sure no files get overwritten
    while filename in os.listdir(upload_dir):
        filename = "1" + filename

    file.save(os.path.join(upload_dir, filename))

    return jsonify({'success': True, 'file_location': filename}), 200, {
        'ContentType': 'application/json'}


@bp.route('/remove-document/<string:name>', methods=['POST'])
def remove_document(name):
    name = secure_filename(name)
    home_directory = os.path.join(current_app.config['file-storage'], 'home')
    os.remove(os.path.join(home_directory, name))
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}

