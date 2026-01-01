from flask import Flask, render_template, request, jsonify
import subprocess
import json
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/inspect', methods=['POST'])
def inspect_image():
    image_url = request.form.get('image_url')
    os_type = request.form.get('os_type')
    architecture = request.form.get('architecture')

    if not image_url:
        return jsonify({'error': 'Image URL is required'}), 400

    # Construct the skopeo command
    command = ['skopeo', 'inspect', '--raw'] # Start with base command

    # Add OS and Architecture overrides if provided
    # Skopeo inspect supports --override-os and --override-arch
    # However, to effectively use them with docker:// transport, we might need to be careful
    # But based on `skopeo inspect --help`, these flags exist.
    
    cmd_args = ['skopeo', 'inspect']
    
    if os_type:
        cmd_args.extend(['--override-os', os_type])
    
    if architecture:
        cmd_args.extend(['--override-arch', architecture])
        
    # Ensure the image url has the docker:// prefix if not present (assuming docker transport for simplicity, or let user provide it)
    # The prompt example "quay.io/pittar/petclinic:latest" suggests no prefix, so we should probably add docker://
    if not "://" in image_url:
        full_image_url = f"docker://{image_url}"
    else:
        full_image_url = image_url

    cmd_args.append(full_image_url)

    app.logger.info(f"Executing command: {' '.join(cmd_args)}")

    try:
        result = subprocess.run(cmd_args, capture_output=True, text=True, check=True)
        # Parse the JSON output from skopeo
        skopeo_data = json.loads(result.stdout)
        return jsonify(skopeo_data)
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Skopeo error: {e.stderr}")
        return jsonify({'error': f"Failed to inspect image: {e.stderr}"}), 500
    except json.JSONDecodeError:
         app.logger.error(f"Failed to parse skopeo output: {result.stdout}")
         return jsonify({'error': "Failed to parse skopeo output"}), 500
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
