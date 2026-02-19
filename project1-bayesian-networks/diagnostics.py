from probability4e import *

T, F = True, False

class Diagnostics:
    """ Use a Bayesian network to diagnose between three lung diseases """

    def __init__(self):
     # Initializing Bayesian Network with nodes
     self.network = BayesNet([
        ('asia', '', [0.01]),
        ('Smoking', '', 0.5),
        ('Tuberculosis', 'Asia', {T: 0.05, F: 0.001}),
        ('LungCancer', 'Smoking', {T: 0.6, F:0.3}), 
        ('Bronchitis', 'Smoking', {T: 0.6, F:0.3}), 
        ('TBorC', 'Tuburculosis', 'LungCancer', {(T,T): 1.0, (T,F): 1.0, (F,T): 1.0, (F,F): 0.0}),
        ('Xray', 'TBorC', {T:0.99, F: 0.05}),
        ('Dyspnea', 'TBorC', 'Bronchitis', {(T,T): 0.9, (T,F): 0.7, (F,T): 0.8, (F,F): 0.1})
     ])

    def diagnose (self, asia, smoking, xray, dyspnea):
        # helper function to convert strings to boolean or None
        def translate(value):
            match value:
                case "Yes" | "Abnormal" | "Present":
                    return True
                case "No" | "Normal" | "Absent":
                    return False
                case "NA":
                    return None
        
        # Translating inputs
        asia_val = translate(asia)
        smoking_val = translate(smoking)
        xray_val = translate(xray)
        dyspnea_val = translate(dyspnea)

        # Creating evidence dictionary 
        evidence = {}
        if asia_val is not None:
            evidence['Asia'] = asia_val
        if smoking_val is not None:
            evidence['Smoking'] = smoking_val
        if xray_val is not None:
            evidence['Xray'] = xray_val
        if dyspnea_val is not None:
            evidence['Dyspnea'] = dyspnea_val

        # To be implemented by the student
        return ["the disease", -1.0] # placeholder return value, to be replaced by the student
