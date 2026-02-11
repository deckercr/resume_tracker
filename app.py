import os
from datetime import date, datetime

from flask import (
    Flask, flash, redirect, render_template, request, send_file, url_for,
)

from export import export_to_excel
from models import Application, JobDescription, db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'job_tracker.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

STATUSES = ['Applied', 'Screening', 'Interview', 'Offer', 'Rejected', 'Withdrawn']


@app.route('/')
def index():
    status_filter = request.args.get('status', '')
    query = Application.query.order_by(Application.date.desc())
    if status_filter:
        query = query.filter_by(status=status_filter)
    applications = query.all()
    return render_template(
        'index.html',
        applications=applications,
        statuses=STATUSES,
        current_status=status_filter,
    )


@app.route('/application/new', methods=['GET', 'POST'])
def new_application():
    if request.method == 'POST':
        app_entry = Application(
            date=datetime.strptime(request.form['date'], '%Y-%m-%d').date()
            if request.form.get('date')
            else date.today(),
            status=request.form.get('status', 'Applied'),
            company=request.form['company'].strip(),
            position=request.form['position'].strip(),
            location=request.form.get('location', '').strip(),
            url=request.form.get('url', '').strip(),
            job_id=request.form.get('job_id', '').strip(),
            salary=request.form.get('salary', '').strip(),
            contact=request.form.get('contact', '').strip(),
            notes=request.form.get('notes', '').strip(),
        )
        db.session.add(app_entry)
        db.session.commit()
        flash('Application added.', 'success')
        return redirect(url_for('index'))
    return render_template(
        'application_form.html',
        application=None,
        statuses=STATUSES,
        today=date.today().strftime('%Y-%m-%d'),
    )


@app.route('/application/<int:id>')
def application_detail(id):
    app_entry = Application.query.get_or_404(id)
    return render_template('application_detail.html', application=app_entry)


@app.route('/application/<int:id>/edit', methods=['GET', 'POST'])
def edit_application(id):
    app_entry = Application.query.get_or_404(id)
    if request.method == 'POST':
        app_entry.date = (
            datetime.strptime(request.form['date'], '%Y-%m-%d').date()
            if request.form.get('date')
            else app_entry.date
        )
        app_entry.status = request.form.get('status', app_entry.status)
        app_entry.company = request.form['company'].strip()
        app_entry.position = request.form['position'].strip()
        app_entry.location = request.form.get('location', '').strip()
        app_entry.url = request.form.get('url', '').strip()
        app_entry.job_id = request.form.get('job_id', '').strip()
        app_entry.salary = request.form.get('salary', '').strip()
        app_entry.contact = request.form.get('contact', '').strip()
        app_entry.notes = request.form.get('notes', '').strip()
        db.session.commit()
        flash('Application updated.', 'success')
        return redirect(url_for('application_detail', id=app_entry.id))
    return render_template(
        'application_form.html',
        application=app_entry,
        statuses=STATUSES,
        today=date.today().strftime('%Y-%m-%d'),
    )


@app.route('/application/<int:id>/delete', methods=['GET', 'POST'])
def delete_application(id):
    app_entry = Application.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(app_entry)
        db.session.commit()
        flash('Application deleted.', 'success')
        return redirect(url_for('index'))
    return render_template('confirm_delete.html', application=app_entry)


@app.route('/application/<int:id>/description', methods=['GET', 'POST'])
def job_description(id):
    app_entry = Application.query.get_or_404(id)
    jd = app_entry.job_description

    if request.method == 'POST':
        desc_text = request.form.get('description', '').strip()
        if jd:
            jd.description = desc_text
            jd.company = app_entry.company
            jd.position = app_entry.position
        else:
            jd = JobDescription(
                application_id=app_entry.id,
                company=app_entry.company,
                position=app_entry.position,
                description=desc_text,
            )
            db.session.add(jd)
        db.session.commit()
        flash('Job description saved.', 'success')
        return redirect(url_for('application_detail', id=app_entry.id))

    return render_template('job_description.html', application=app_entry, jd=jd)


@app.route('/export')
def export():
    applications = Application.query.order_by(Application.date.desc()).all()
    descriptions = JobDescription.query.all()
    filepath = export_to_excel(applications, descriptions)
    return send_file(
        filepath, as_attachment=True, download_name='job_applications.xlsx'
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
