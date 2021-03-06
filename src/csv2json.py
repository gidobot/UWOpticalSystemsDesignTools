
import numpy as np
import json
import os

def convert(filepath):
    array = np.genfromtxt(filepath, delimiter=',')
    json_dict = {}
    json_dict["quantum_efficiency_wavelengths"] = list(array[:, 0])
    json_dict["quantum_efficiency"] = list(array[:, 1])

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../cfg/imx264_quantumeff_red.json")
    with open(path,'w') as file:
        json.dump(json_dict, file, indent=2)


if __name__=="__main__":
    convert("/home/gidobot/workspace/droplab_tools/uwopticalsystemsdesigntools/test/BFLY-PGE-50S5C/RedChannel.csv")
