from flask import Flask, render_template_string
from flask_cdn import CDN

app = Flask(__name__)
app.config['CDN_DOMAIN'] = 'nyud.net'
app.config['CDN_TIMESTAMP'] = False
CDN(app)


@app.route('/')
def index():
    template_str = """{{ url_for('static', filename="logo.png") }}"""
    return render_template_string(template_str)

if __name__ == '__main__':
    app.run(port = 8080, debug=True)