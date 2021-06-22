from datetime import datetime
from flask import *
from database import Base,Parameters
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import plotly.express as px
import plotly
import numpy as np
import models

status = "Calibration cable started"
print(status)
engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
models.add_parameter(session, "0.5 Ghz", "10",10, 10, 10, "form_antenna_type","Measurement")
results = np.genfromtxt("dipole_pattern.csv", delimiter=',')

x = np.fromstring(results, dtype=float)
raw_data = np.array(results)
print("x:{}".format(x))
raw_data2 = np.array(results)
print("raw_data2:{}".format(raw_data2))


print("--------------------------")
str1 = ""
for ele in results:
    str1 += str(ele) + ","
results_str = str1
print("resutlt_str:{}".format(results_str))
print("type result_str:{}".format(type(results_str)))
raw_data = np.fromstring(results_str, dtype=float, sep=',')
print("raw_data:{}".format(raw_data))
theta = np.arange(0, 361, 1)
fig = px.line_polar(r=raw_data, theta=theta, start_angle=0)
fig.show()