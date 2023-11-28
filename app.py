# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
db = SQLAlchemy(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary)

# This function ensures the application context is created
# before running any commands
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        image_file = request.files['image']
        if image_file:
            image_data = base64.b64encode(image_file.read())
            new_image = Image(data=image_data)
            db.session.add(new_image)
            db.session.commit()
            return 'Image uploaded successfully!'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)