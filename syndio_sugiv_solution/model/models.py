from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Float, Numeric


Base = declarative_base()

class Employee(Base):
    __tablename__ = "employee"
    employee_id = Column(Integer, primary_key=True)
    employee_job_group = Column(String(50))
    employee_job_level = Column(String(100))
    employee_job_title = Column(String(100))
    employee_gender = Column(String(100))
    employee_race = Column(String(50))
    employee_compensation = Column(Float)
    employee_years_of_experience = Column(Integer)
    employee_time_in_role = Column(Integer)
    employee_city = Column(String(100),ForeignKey('geo.employee_city'))
    employee_company = Column(String(100), ForeignKey('company.company_name'))

class Geo(Base):
    __tablename__ = "geo"
    geo_zone_id = Column(String)
    employee_geo_zone = Column(String(100))
    employee_city = Column(String(100), primary_key=True)
    employee_state = Column(String(10))
    geo_zone_cost_of_living_factor = Column(Float)
    employees = relationship("Employee", backref="same_location_employees")

class Company(Base):
    __tablename__ = "company"
    company_name = Column(String(100), primary_key=True)
    company_headquarters_city = Column(String(100))
    company_headquarters_state = Column(String(10))
    company_sector = Column(String(50))
    employees = relationship("Employee", backref="company_employees")