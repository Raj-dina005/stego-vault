import os
from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
from config import Config
from stego.embed import embed_file
from stego.extract import extract_file

app = Flask(__name__)
app.config.from_object(Config)

# ── Helpers ────────────────────────────────────────────────────────────────

def allowed_video(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_VIDEO_EXTENSIONS']

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_FILE_EXTENSIONS']

def ensure_folders():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# ── Routes ─────────────────────────────────────────────────────────────────

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/app')
def index():
    return render_template('index.html')


@app.route('/embed', methods=['POST'])
def embed():
    ensure_folders()

    # Validate inputs
    if 'video' not in request.files or 'secret' not in request.files:
        return jsonify({'success': False, 'error': 'Missing video or secret file!'}), 400

    video_file = request.files['video']
    secret_file = request.files['secret']
    password = request.form.get('password', '').strip()

    if not password:
        return jsonify({'success': False, 'error': 'Password is required!'}), 400

    if video_file.filename == '' or secret_file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected!'}), 400

    if not allowed_video(video_file.filename):
        return jsonify({'success': False, 'error': 'Invalid video format! Allowed: mp4, avi, mkv'}), 400

    if not allowed_file(secret_file.filename):
        return jsonify({'success': False, 'error': 'Invalid secret file format!'}), 400

    # Save uploaded files
    video_filename = secure_filename(video_file.filename)
    secret_filename = secure_filename(secret_file.filename)

    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    secret_path = os.path.join(app.config['UPLOAD_FOLDER'], secret_filename)

    video_file.save(video_path)
    secret_file.save(secret_path)

    # Output path
    output_filename = 'stego_' + video_filename
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    try:
        result = embed_file(video_path, secret_path, password, output_path)
        return jsonify({
            'success': True,
            'message': 'File successfully hidden in video!',
            'download_url': f'/download/{output_filename}',
            'original_hash': result['original_hash'],
            'secret_filename': result['secret_filename'],
            'output_size': result['output_size']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        # Cleanup uploaded files
        if os.path.exists(video_path): os.remove(video_path)
        if os.path.exists(secret_path): os.remove(secret_path)


@app.route('/extract', methods=['POST'])
def extract():
    ensure_folders()

    if 'video' not in request.files:
        return jsonify({'success': False, 'error': 'Missing stego video!'}), 400

    video_file = request.files['video']
    password = request.form.get('password', '').strip()

    if not password:
        return jsonify({'success': False, 'error': 'Password is required!'}), 400

    if not allowed_video(video_file.filename):
        return jsonify({'success': False, 'error': 'Invalid video format!'}), 400

    video_filename = secure_filename(video_file.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    video_file.save(video_path)

    try:
        result = extract_file(video_path, password, app.config['OUTPUT_FOLDER'])
        extracted_filename = os.path.basename(result['output_path'])
        return jsonify({
            'success': True,
            'message': 'File successfully extracted!',
            'download_url': f'/download/{extracted_filename}',
            'original_filename': result['original_filename'],
            'file_size': result['file_size'],
            'integrity_verified': result['integrity_verified']
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if os.path.exists(video_path): os.remove(video_path)


@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))
    if not os.path.exists(file_path):
        return jsonify({'success': False, 'error': 'File not found!'}), 404
    return send_file(file_path, as_attachment=True)


# ── Run ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=port
    )