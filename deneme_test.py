from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Parameters, Base
import datetime
import models
import numpy as np




engine = create_engine('sqlite:///parameters_database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
parameters_list = models.get_parameters(session)
id_list=[]

for parameter in parameters_list:
    id_list.append(parameter.id)

parameter_last = models.get_parameter(session, id_list[-1])
print("id:{} P:{} D:{}".format(parameter_last.id, parameter_last.raw_measured_power, parameter_last.date))

raw_data = np.fromstring(parameter_last.raw_measured_power, dtype=float, sep=',')

print(raw_data)