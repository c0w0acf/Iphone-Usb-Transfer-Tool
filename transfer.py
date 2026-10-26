from flask import Flask, request
import os
import socket
import zipfile

app = Flask(__name__)
UPLOAD_DIR = "transferred_photos"

os.makedirs(UPLOAD_DIR, exist_ok=True)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>iPhone Zip Folder Transfer</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; text-align: center; padding: 40px 20px; background: #f2f2f7; color: #1c1c1e; }
        .card { background: white; max-width: 500px; margin: 0 auto; padding: 30px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        input[type=file] { margin: 20px 0; padding: 12px; font-size: 16px; border: 2px dashed #007aff; border-radius: 8px; width: 100%; box-sizing: border-box; background: #f9f9f9; }
        input[type=submit] { background: #007aff; color: white; border: none; padding: 14px 28px; font-size: 16px; font-weight: bold; border-radius: 10px; cursor: pointer; width: 100%; }
        input[type=submit]:active { background: #0056b3; }
        h1 { font-size: 24px; margin-bottom: 10px; }
        .instructions { text-align: left; background: #f2f2f7; padding: 15px; border-radius: 8px; font-size: 14px; color: #333; margin-bottom: 20px; }
        .instructions ol { margin: 0; padding-left: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>iPhone Folder Transfer</h1>
        
        <div class="instructions">
            <b>How to send folders from iPhone:</b>
            <ol>
                <li>Open the iPhone <b>Files</b> app.</li>
                <li>Long-press the folder you want to send and tap <b>Compress</b>.</li>
                <li>Select the new <code>.zip</code> file below and hit Upload!</li>
            </ol>
        </div>

        <form method="post" enctype="multipart/form-data">
            <input type="file" name="zipfile" accept=".zip"><br>
            <input type="submit" value="Upload & Extract to PC">
        </form>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('zipfile')
        if file and file.filename.endswith('.zip'):
            filepath = os.path.join(UPLOAD_DIR, file.filename)
            file.save(filepath)
            
            # Automatically extract the zip folder
            extract_folder_name = os.path.splitext(file.filename)[0]
            extract_path = os.path.join(UPLOAD_DIR, extract_folder_name)
            os.makedirs(extract_path, exist_ok=True)
            
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            
            # Clean up the zip file after extraction
            os.remove(filepath)
            
            return f"""
            <!DOCTYPE html>
            <html>
            <head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
            <body style="font-family: -apple-system; text-align: center; padding: 60px 20px; background: #f2f2f7;">
                <div style="background: white; max-width: 400px; margin: 0 auto; padding: 30px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    <h2 style="color: #34c759; margin-top: 0;">Extracted Successfully!</h2>
                    <p style="font-size: 15px;">Your folder was saved and unpacked in your PC's <b>transferred_photos</b> directory.</p>
                    <a href="/" style="display: inline-block; margin-top: 15px; color: #007aff; text-decoration: none; font-size: 16px; font-weight: bold;">Upload Another</a>
                </div>
            </body>
            </html>
            """
    return HTML_PAGE

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == '__main__':
    ip = get_local_ip()
    print("=" * 60)
    print(f"🚀 Zip Transfer Server is running!")
    print(f"📱 Open Safari on your iPhone and go to:")
    print(f"   http://{ip}:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000)