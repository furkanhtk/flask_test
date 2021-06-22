from datetime import datetime
from flask import *
import models
from database import Base,Parameters

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
########################
import plotly.express as px
import numpy as np
import plotly
import string
import control
import calculation


def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=today)


def Measurement_page():
    engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == "GET":
        return render_template("Measurement.html")
    elif request.form.get('Start') == 'Start':
        form_frequency = request.form["frequency"]
        form_power = request.form["power"]
        form_sample_size = request.form["sample_size"]
        form_g_ref = request.form["g_ref"]
        form_distance = request.form["distance"]
        form_antenna_type = request.form["antenna_type"]
        form_mode = request.form["mode"]
        models.add_parameter(session, form_frequency, form_power,form_sample_size, form_g_ref, form_distance, form_antenna_type,form_mode)
        return redirect(url_for("Process_Measurement_page"))


def Calibration_fs_page():
    engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == "GET":
        return render_template("Calibration_fs.html")
    elif request.form.get('Start') == 'Start':
        form_frequency = request.form["frequency"]
        form_power = request.form["power"]
        form_sample_size = request.form["sample_size"]
        form_g_ref = request.form["g_ref"]
        form_distance = request.form["distance"]
        form_antenna_type = request.form["antenna_type"]
        form_mode = request.form["mode"]
        models.add_parameter(session, form_frequency, form_power,form_sample_size, form_g_ref, form_distance, form_antenna_type,form_mode)
        return redirect(url_for("parameters_page"))


def Calibration_cable_page():
    engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == "GET":
        return render_template("Calibration_cable.html")
    elif request.form.get('Start') == 'Start':
        form_frequency = request.form["frequency"]
        form_power = request.form["power"]
        form_sample_size = request.form["sample_size"]
        form_g_ref = request.form["g_ref"]
        form_distance = request.form["distance"]
        form_antenna_type = request.form["antenna_type"]
        form_mode = request.form["mode"]
        models.add_parameter(session, form_frequency, form_power,form_sample_size, form_g_ref, form_distance, form_antenna_type,form_mode)
        return redirect(url_for("parameters_page"))


def parameters_page():
    engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == "GET":
        parameters_list = models.get_parameters(session)
        return render_template("parameters.html", parameters=parameters_list)
    elif request.form.get('Add') == 'Add':
        form_frequency = request.form["frequency"]
        form_power = request.form["power"]
        form_g_ref = request.form["g_ref"]
        form_distance = request.form["distance"]
        form_antenna_type = request.form["antenna_type"]
        form_sample_size = request.form["sample_size"]
        models.add_parameter(session,form_frequency,form_power,form_sample_size,form_g_ref,form_distance,form_antenna_type)
        return redirect(url_for("parameters_page"))
    elif request.form.get('Delete') == 'Delete':
        form_parameter_ids = request.form.getlist("parameter_ids")
        for form_parameter_id in form_parameter_ids:
            models.delete_parameter(session, form_parameter_id)
        return redirect(url_for("parameters_page"))
    else:
        return redirect(url_for("parameters_page"))


def parameter_page(parameter_id):
    parameter = models.get_parameter(session, parameter_id)
    raw_data = np.fromstring(parameter.raw_measured_power, dtype=float, sep=',')
    theta = np.arange(0, 361, 1)
    fig = px.line_polar(r=raw_data, theta=theta, start_angle=0)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    parameter = models.get_parameter(session, parameter_id)
    if parameter is None:
        abort(404)
    return render_template("parameter.html", parameter=parameter,graphJSON=graphJSON)


def Process_Measurement_page():
    status = "Measurement started"
    print(status)
    data_func(status)
    engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    parameters_list = models.get_parameters(session)
    id_list=[]
    for parameter in parameters_list:
        id_list.append(parameter.id)
    parameter=models.get_parameter(session, id_list[-1])
    input_Power=int(parameter.input_Power)
    input_frequency=parse_frequency(parameter.input_Power)
    status = "Parameters received"
    print(status)
    data_func(status)
    results = control.Measurement_Antenna(input_frequency,input_Power, parameter.sample_size)
    status = "Measurement completed, calculations in progress"
    print(status)
    data_func(status)
    beamwidth_value, bandwidth_6dB_value, gain, kraus, tai_pereira = calculation.total_calculation(results,input_frequency,input_Power, parameter.g_ref, parameter.distance)
    beamwidth_value = float(beamwidth_value[0])
    bandwidth_6dB_value = float(bandwidth_6dB_value[0])
    kraus = float(kraus[0])
    tai_pereira = float(tai_pereira[0])
    str1 = ""
    for ele in results:
        str1 += str(ele) + ","
    results_str = str1
    models.add_results(session,id_list[-1],results_str,beamwidth_value, bandwidth_6dB_value, gain, tai_pereira, kraus)
    status = "Measurement complete, calculations complete"
    print(status)
    data_func(status)
    return render_template("Process_Measurement.html")


def parse_frequency(value):
    value = value.lower()
    if "ghz" in value:
        frequency = (float(value.strip(string.ascii_letters)))
        frequency = int(frequency * (10 ** 9))
    elif "mhz" in value:
        frequency = (float(value.strip(string.ascii_letters)))
        frequency = int(frequency * (10 ** 6))
    else:
        frequency = (int(value.strip(string.ascii_letters)))
    return frequency


def data_func(status):
    veri2 = status
    return jsonify({'status_value': veri2})