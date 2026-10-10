from flask import Flask, request, render_template_string, send_file
import yt_dlp
import os
import glob

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Music Hub 🎵</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial;background:#111;color:#fff;text-align:center;padding:20px}
input{width:95%;padding:15px;border-radius:10px;border:none;margin:10px;font-size:16px}
button{padding:15px 30px;background:#1DB954;color:#fff;border:none;border-radius:10px;font-size:18px;font-weight:bold}
.box{background:#222;padding:20px;border-radius:15px;margin-top:20px;word-break:break-all}
a{color:#1DB954}
</style>
</head>
<body>
<h1>🎵 Music Hub Bot</h1>
<p>Paste YouTube / TikTok / Instagram link</p>
<form method="post">
<input name="url" placeholder="https://youtube.com/watch?v=..." required>
<br><button type="submit">Download Music</button>
</form>
{% if msg %}<div class="box">{{msg|safe}}</div>{% endif %}
<p style="margin-top:30px;color:#888">Your own music downloader - No Telegram needed!</p>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def home():
    msg = ""
    if request.method == "POST":
        url = request.form.get("url")
        try:
            for f in glob.glob("/tmp/*"):
                try: os.remove(f)
                except: pass
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '/tmp/%(title)s.%(ext)s',
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                files = glob.glob("/tmp/*")
                if files:
                    fname = files[0]
                    just_name = os.path.basename(fname)
                    msg = f"✅ <b>{info.get('title','Music')}</b><br><br><a href='/download?f={just_name}' style='font-size:22px'>⬇️ TAP HERE TO SAVE</a>"
                else:
                    msg = "Downloaded but file not found"
        except Exception as e:
            msg = f"❌ Error: {str(e)[:300]}"
    return render_template_string(HTML, msg=msg)

@app.route("/download")
def download():
    f = request.args.get("f")
    path = f"/tmp/{f}"
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "File expired, please download again"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
