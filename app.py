import os
import cv2
import numpy as np
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import insightface
from insightface.app import FaceAnalysis
import traceback

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Initialize face analysis and swapper
face_app = None
face_swapper = None

def init_models():
    """Initialize the face analysis and swapping models"""
    global face_app, face_swapper
    try:
        print("Initializing face analysis model...")
        face_app = FaceAnalysis(name='buffalo_l')
        face_app.prepare(ctx_id=0, det_size=(640, 640))
        
        print("Loading face swapper model...")
        face_swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=True, download_zip=True)
        print("Models initialized successfully!")
    except Exception as e:
        print(f"Error initializing models: {e}")
        traceback.print_exc()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'tif', 'tiff'}

def swap_faces(source_path, target_path, output_path):
    """
    Swap face from source image onto target image
    source_path: path to image with the face you want to use (the player's head)
    target_path: path to image with the body/jersey you want to use
    output_path: where to save the result
    """
    try:
        # Read images
        source_img = cv2.imread(source_path)
        target_img = cv2.imread(target_path)
        
        if source_img is None or target_img is None:
            raise ValueError("Could not read one or both images")
        
        # Detect faces in both images
        source_faces = face_app.get(source_img)
        target_faces = face_app.get(target_img)
        
        if len(source_faces) == 0:
            raise ValueError("No face detected in the source image (player headshot)")
        
        if len(target_faces) == 0:
            raise ValueError("No face detected in the target image (jersey template)")
        
        # Use the first (or largest) face from each image
        source_face = source_faces[0]
        target_face = target_faces[0]
        
        # Perform the face swap
        result = face_swapper.get(target_img, target_face, source_face, paste_back=True)
        
        # Save the result
        cv2.imwrite(output_path, result)
        
        return True, "Face swap completed successfully!"
        
    except Exception as e:
        error_msg = f"Face swap failed: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        return False, error_msg

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/swap', methods=['POST'])
def swap():
    """Handle face swap request"""
    try:
        # Check if files are present
        if 'player_head' not in request.files or 'jersey_template' not in request.files:
            return jsonify({'error': 'Both images are required'}), 400
        
        player_file = request.files['player_head']
        jersey_file = request.files['jersey_template']
        
        # Check if files are selected
        if player_file.filename == '' or jersey_file.filename == '':
            return jsonify({'error': 'No files selected'}), 400
        
        # Validate file types
        if not (allowed_file(player_file.filename) and allowed_file(jersey_file.filename)):
            return jsonify({'error': 'Invalid file type. Use PNG, JPG, or TIF'}), 400
        
        # Save uploaded files
        player_filename = secure_filename(player_file.filename)
        jersey_filename = secure_filename(jersey_file.filename)
        
        player_path = os.path.join(app.config['UPLOAD_FOLDER'], f"player_{player_filename}")
        jersey_path = os.path.join(app.config['UPLOAD_FOLDER'], f"jersey_{jersey_filename}")
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"result_{player_filename}")
        
        player_file.save(player_path)
        jersey_file.save(jersey_path)
        
        # Perform face swap
        success, message = swap_faces(player_path, jersey_path, output_path)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'result_url': f'/result/{os.path.basename(output_path)}'
            })
        else:
            return jsonify({'error': message}), 500
            
    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        return jsonify({'error': error_msg}), 500

@app.route('/result/<filename>')
def get_result(filename):
    """Serve the resulting image"""
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), mimetype='image/jpeg')

if __name__ == '__main__':
    print("Starting Hockey Face Swap application...")
    init_models()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
