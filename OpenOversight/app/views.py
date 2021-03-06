import os
from flask import (render_template, request, redirect, url_for,
                  send_from_directory, flash, session)
from werkzeug import secure_filename
from app import app

from utils import allowed_file, grab_officers, grab_officer_faces
from forms import FindOfficerForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/find', methods=['GET', 'POST'])
def get_officer():
    form = FindOfficerForm()
    if form.validate_on_submit():
        #  flash('[DEBUG] Forms validate correctly')
        return redirect(url_for('get_gallery'), code=307)
    return render_template('input_find_officer.html', form=form)


@app.route('/gallery', methods=['GET', 'POST'])
def get_gallery():
    form_values = request.form

    officers = grab_officers(form_values)
    officer_ids = [officer.Officer.id for officer in officers]
    officer_images = grab_officer_faces(officer_ids)

    return render_template('gallery.html', officers=officers, form=form_values,
                           officer_images=officer_images)


@app.route('/complaint', methods=['GET', 'POST'])
def submit_complaint():
    return render_template('complaint.html',
                           officer_first_name=request.args.get('officer_first_name'),
                           officer_last_name=request.args.get('officer_last_name'),
                           officer_middle_initial=request.args.get('officer_middle_name'),
                           officer_star=request.args.get('officer_star'),
                           officer_image=request.args.get('officer_image'))


@app.route('/submit')
def submit_data():
    return render_template('submit.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UNLABELLED_UPLOADS'], filename))
        return redirect(url_for('show_upload',
                                filename=filename))


@app.route('/show_upload/<filename>')
def show_upload(filename):
    #return send_from_directory('../'+config.UNLABELLED_UPLOADS,
    #                           filename)
    return 'Successfully uploaded: {}'.format(filename)


@app.route('/label')
def label_data():
    return render_template('label_data.html')


@app.route('/about')
def about_oo():
    return render_template('about.html')


@app.route('/contact')
def contact_oo():
    return render_template('contact.html')

@app.route('/privacy')
def privacy_oo():
    return render_template('privacy.html')
