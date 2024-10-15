from os import getenv

from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, ForeignKey, Float)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import (
    sessionmaker, declarative_base, relationship, scoped_session)


USERNAME = getenv('DB_USERNAME')
ADDRESS = getenv('DB_ADDRESS')
PASSWORD = getenv('DB_PASSWORD')
PORT = getenv('DB_PORT')
DB_NAME = getenv('DB_NAME')

Base = declarative_base()

engine = create_engine(
    f'mysql+pymysql://{USERNAME}:{PASSWORD}@{ADDRESS}:{PORT}/{DB_NAME}')

SessionFactory = sessionmaker(bind=engine)

session = scoped_session(SessionFactory)

# Define the models


class Universities(Base):
    __tablename__ = 'universities'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    year = Column(String(50), nullable=False)
    total_post_utme = Column(Integer, nullable=True)
    post_utme_passmark = Column(Integer, nullable=True)
    olevel_subjects = Column(Integer, nullable=True)
    uni_class = Column(String(50), nullable=True)
    require_olevel = Column(Boolean, default=False, nullable=True)
    utme_postutme = Column(Boolean, default=False, nullable=True)
    utme_postutme_olevel = Column(Boolean, default=False, nullable=True)
    utme_olevel = Column(Boolean, default=False, nullable=True)
    sitting = Column(Boolean, default=False)
    aggr_method = Column(String(255), nullable=True)

    about_uni = relationship(
        "About", back_populates="universities", cascade="all, delete-orphan")

    ui_courses = relationship("UiCourses", back_populates="universities")
    unilag_courses = relationship(
        "UnilagCourses", back_populates="universities")
    unn_courses = relationship("UnnCourses", back_populates="universities")

    oau_courses = relationship("OauCourses", back_populates="universities")
    abu_courses = relationship("AbuCourses", back_populates="universities")
    unilorin_courses = relationship(
        "UnilorinCourses", back_populates="universities")

    futa_courses = relationship("FutaCourses", back_populates="universities")
    unizik_courses = relationship(
        "UnizikCourses", back_populates="universities")
    uniben_courses = relationship(
        "UnibenCourses", back_populates="universities")
    fuoye_courses = relationship("FuoyeCourses", back_populates="universities")


class About(Base):
    __tablename__ = 'about_universities'

    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey(
        'universities.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)
    established = Column(Integer, nullable=False)
    description = Column(String(2000), nullable=False)

    universities = relationship("Universities", back_populates="about_uni")


class BaseUniCourses(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    faculty = Column(String(50), nullable=False)
    aggregate = Column(Float, nullable=False)

    @declared_attr
    def university_id(cls):
        return Column(Integer, ForeignKey('universities.id'), nullable=False)


class UiCourses(BaseUniCourses):
    __tablename__ = 'ui_courses'
    universities = relationship("Universities", back_populates="ui_courses")


class UnilagCourses(BaseUniCourses):
    __tablename__ = 'unilag_courses'
    universities = relationship(
        "Universities", back_populates="unilag_courses")


class UnnCourses(BaseUniCourses):
    __tablename__ = 'unn_courses'
    universities = relationship("Universities", back_populates="unn_courses")


class OauCourses(BaseUniCourses):
    __tablename__ = 'oau_courses'
    universities = relationship("Universities", back_populates="oau_courses")


class AbuCourses(BaseUniCourses):
    __tablename__ = 'abu_courses'
    universities = relationship("Universities", back_populates="abu_courses")


class UnilorinCourses(BaseUniCourses):
    __tablename__ = 'unilorin_courses'
    universities = relationship(
        "Universities", back_populates="unilorin_courses")


class FutaCourses(BaseUniCourses):
    __tablename__ = 'futa_courses'
    universities = relationship("Universities", back_populates="futa_courses")


class UnizikCourses(BaseUniCourses):
    __tablename__ = 'unizik_courses'
    universities = relationship(
        "Universities", back_populates="unizik_courses")


class UnibenCourses(BaseUniCourses):
    __tablename__ = 'uniben_courses'
    universities = relationship(
        "Universities", back_populates="uniben_courses")


class FuoyeCourses(BaseUniCourses):
    __tablename__ = 'fuoye_courses'
    universities = relationship("Universities", back_populates="fuoye_courses")


# # Create the tables
# if __name__ == '__main__':
#     try:
#         # Creates all tables based on the Base models
#         Base.metadata.create_all(engine)
#         print("Tables created successfully!")
#     except Exception as e:
#         print(f"Error creating tables: {e}")

# session = Session()

# try:
#     # Your query/operation here
#     session.commit()  # Commit the transaction if successful
# except Exception as e:
#     # Rollback the transaction if there is any error
#     session.rollback()
#     print(f"Error: {e}")
# finally:
#     session.close()  # Always close the session when done
