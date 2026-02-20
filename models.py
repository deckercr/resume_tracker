import os
from datetime import date, datetime

from sqlalchemy import create_engine, String, Text, Integer, Date, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

DB_PATH = os.environ.get('JOB_TRACKER_DB', os.path.join(os.path.abspath(os.path.dirname(__file__)), 'job_tracker.db'))
engine = create_engine(f'sqlite:///{DB_PATH}')


class Base(DeclarativeBase):
    pass


class Resume(Base):
    __tablename__ = 'resumes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    original_format: Mapped[str] = mapped_column(String(10), nullable=False)
    pdf_data: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    docx_data: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    applications: Mapped[list['Application']] = relationship(back_populates='resume')


class Application(Base):
    __tablename__ = 'applications'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default='Applied')
    company: Mapped[str] = mapped_column(String(200), nullable=False)
    position: Mapped[str] = mapped_column(String(200), nullable=False)
    location: Mapped[str] = mapped_column(String(200), default='')
    url: Mapped[str] = mapped_column(String(500), default='')
    job_id: Mapped[str] = mapped_column(String(100), default='')
    salary: Mapped[str] = mapped_column(String(100), default='')
    contact: Mapped[str] = mapped_column(String(200), default='')
    notes: Mapped[str] = mapped_column(Text, default='')
    resume_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('resumes.id'), nullable=True)

    job_description: Mapped['JobDescription'] = relationship(
        back_populates='application',
        uselist=False,
        cascade='all, delete-orphan',
    )
    resume: Mapped['Resume | None'] = relationship(back_populates='applications')


class JobDescription(Base):
    __tablename__ = 'job_descriptions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('applications.id'), nullable=False, unique=True
    )
    company: Mapped[str] = mapped_column(String(200), nullable=False)
    position: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default='')

    application: Mapped['Application'] = relationship(back_populates='job_description')


def init_db():
    Base.metadata.create_all(engine)
