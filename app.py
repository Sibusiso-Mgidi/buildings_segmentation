import os
import base64
from flask import Flask,render_template,request,redirect,flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = os.environ['UPLOAD_FOLDER']


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/predict",methods=["GET","POST"])
def predict():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'image' not in request.files:
            flash('No image')
            return redirect(request.url)

        image_file = request.files["image"]

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if image_file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if image_file:
            print()
            sec_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], sec_filename))
            return render_template('predict.html',model_pred_1=1,model_pred_2=1)
            
    return render_template('predict.html',model_pred_1=0,model_pred_2=0)

if __name__ == "__main__":
    app.run(debug=True)
