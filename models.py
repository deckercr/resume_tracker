from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(50), nullable=False, default='Applied')
    company = db.Column(db.String(200), nullable=False)
    position = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), default='')
    url = db.Column(db.String(500), default='')
    job_id = db.Column(db.String(100), default='')
    salary = db.Column(db.String(100), default='')
    contact = db.Column(db.String(200), default='')
    notes = db.Column(db.Text, default='')

    job_description = db.relationship(
        'JobDescription',
        backref='application',
        uselist=False,
        cascade='all, delete-orphan',
    )


class JobDescription(db.Model):
    __tablename__ = 'job_descriptions'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(
        db.Integer, db.ForeignKey('applications.id'), nullable=False, unique=True
    )
    company = db.Column(db.String(200), nullable=False)
    position = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False, default='')
