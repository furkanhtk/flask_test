import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def process_start():

    veri3 = "Measurement Started"

    return jsonify({'test3': veri3})

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value))
    idx2=np.sort(idx)
    x1 = np.where(idx == idx2[0])
    x2 = np.where(idx == idx2[1])
    return array[x1],x1,array[x2],x2


def beamwidth(results):
    data=np.array(results)
    maximum_db=np.amax(data)
    print(data.size)
    x = np.linspace(0, 361, 361)
    x2 = np.linspace(0, 2*np.pi, 361)
    xvals = np.linspace(0, 361, 1000)
    xvals2 = np.linspace(0, 2*np.pi, 1000)
    yinterp = np.interp(xvals, x, data)
    half_power1,halfpower_ind1,half_power2,halfpower_ind2=find_nearest(yinterp, (maximum_db - 3))
    beamwidth_value = abs(xvals[halfpower_ind1]-xvals[halfpower_ind2])
    beamwidth_angle1 = xvals[halfpower_ind1]
    beamwidth_angle2 = xvals[halfpower_ind2]
    return beamwidth_value, half_power1,beamwidth_angle1,half_power2,beamwidth_angle2

def bandwidth_6dB(results):
    data=np.array(results)
    maximum_db = np.amax(data)
    x = np.linspace(0, 361, 361)
    x2 = np.linspace(0, 2 * np.pi, 361)
    xvals = np.linspace(0, 361, 1000)
    xvals2 = np.linspace(0, 2 * np.pi, 1000)
    yinterp = np.interp(xvals, x, data)
    bandwidth_power1, bandwidth_ind1, bandwidth_power2, bandwidth_ind2 = find_nearest(yinterp, (maximum_db - 6))
    bandwidth_6dB_value = abs(xvals[bandwidth_ind1] - xvals[bandwidth_ind2])
    bandwidth_angle1 = xvals[bandwidth_ind1]
    bandwidth_angle2 = xvals[bandwidth_ind2]
    return bandwidth_6dB_value, bandwidth_power1, bandwidth_angle1, bandwidth_power2, bandwidth_angle2






def gain_calculator(frequency, input_power, gref, distance,results):
    data = np.array(results)
    Pr = np.sum(data)
    wavelength = 1/frequency
    gain = (Pr*pow(4*np.pi*distance, 2))/(input_power*gref*pow(wavelength, 2))
    return gain


def directivity(beamwidth_angle1,beamwidth_angle2):
    kraus=41.253/(beamwidth_angle1*beamwidth_angle2)
    tai_pereira=22.181/(pow(beamwidth_angle1,2)*pow(beamwidth_angle2,2))
    return kraus, tai_pereira



def total_calculation(results,frequency,input_power,gref,distance):
    print("calculatin total inside")
    beamwidth_value, half_power1,beamwidth_angle1,half_power2,beamwidth_angle2=beamwidth(results)
    print("calculating beamwidth")
    bandwidth_6dB_value, bandwidth_power1, bandwidth_angle1, bandwidth_power2, bandwidth_angle2=bandwidth_6dB(results)
    print("Bandwidth")
    gain=gain_calculator(frequency, input_power, gref, distance,results)
    kraus, tai_pereira=directivity(beamwidth_angle1, beamwidth_angle2)


    beamwidth_value = float(beamwidth_value[0])
    bandwidth_6dB_value = float(bandwidth_6dB_value[0])
    kraus = float(kraus[0])
    tai_pereira = float(tai_pereira[0])
    print("Calculating finished")



    return beamwidth_value, bandwidth_6dB_value, gain, kraus, tai_pereira



if __name__ == "__main__":
    calibrate_cn0150()


