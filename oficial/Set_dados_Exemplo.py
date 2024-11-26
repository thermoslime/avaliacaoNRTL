from oficial.NRTL import *


############## CASO 1 ###############

# Caso 1: Inconsistente
caso_1_inconsistente = {
    "temperatura" : "298.15",

    "nome_1": "Benzeno",
    "nome_2": "Ciclohexano",
    "nome_3": "DMSO",

    "MM_1": "78.11",
    "MM_2": "84.16",
    "MM_3": "78.14",

    "A12": "12763.4",
    "A13": "9587.29",
    "A21": "24786.4",
    "A23": "24220.8",
    "A31": "-168.807",
    "A32": "11347.3",

    "Alfa12": "0.4248",
    "Alfa13": "0.3458",
    "Alfa23": "0.3750",
}

# Caso 1: Consistente
caso_1_consistente = {
    "temperatura" : "298.15",

    "nome_1": "Benzeno",
    "nome_2": "Ciclohexano",
    "nome_3": "DMSO",

    "MM_1": "78.11",
    "MM_2": "84.16",
    "MM_3": "78.14",

    "A12": "-674.127",
    "A13": "1050.97",
    "A21": "727.532",
    "A23": "13545.2",
    "A31": "697.021",
    "A32": "4016.58",

    "Alfa12": "0.2",
    "Alfa13": "0.2",
    "Alfa23": "0.2",
}

# Fração Mássica da fase rica em DMSO. Retirado do artigo
fracao_massica_caso_1_extrato = np.array([
    [0.036, 0.042, 0.922],
    [0.053, 0.046, 0.901],
    [0.080, 0.056, 0.864],
    [0.102, 0.058, 0.84],
    [0.121, 0.060, 0.819],
    [0.144, 0.066, 0.79],
    [0.161, 0.069, 0.77],
    [0.188, 0.079, 0.733],
    [0.228, 0.089, 0.683]
    ])

# Fração Mássica da fase rica em cyclohexane
fracao_massica_caso_1_rafinado = np.array([
    [0.055, 0.942, 0.0030],
    [0.083, 0.914, 0.0030],
    [0.116, 0.879, 0.0050],
    [0.142, 0.853, 0.0050],
    [0.179, 0.816, 0.0050],
    [0.200, 0.788, 0.0120],
    [0.246, 0.741, 0.0130],
    [0.259, 0.719, 0.0220],
    [0.290, 0.673, 0.0370]
])

# Massa molar dos componentes. Obtidos de: https://pubchem.ncbi.nlm.nih.gov/
# A massa molar é a mesma, do consistente e inconsistente
massa_molar_caso_1 = np.array([float(caso_1_consistente["MM_1"]), float(caso_1_consistente["MM_2"]), float(caso_1_consistente["MM_3"])])


# Frações molares, na ordem: [benzene (1), cyclohexane (2), DMSO(3)]
frac_molar_1_extrato = FracaoMolar(fracao_massica_caso_1_extrato, massa_molar_caso_1)

frac_molar_1_rafinado = FracaoMolar(fracao_massica_caso_1_rafinado, massa_molar_caso_1)



############## CASO 2 ###############
# Ordem usada: [n-hexane (1), benzene (2), sulfolane(3)]

# Caso 2: Inconsistente
caso_2_inconsistente = {
    "temperatura" : "298.15",
    "nome_1": "n-hexano",
    "nome_2": "Benzeno",
    "nome_3": "Sulfolano",

    "MM_1": "86.18",
    "MM_2": "78.11",
    "MM_3": "120.17",

    "A12": "22761.7",
    "A13": "19822.8",
    "A21": "8478.03",
    "A23": "8194.48",
    "A31": "13937.4",
    "A32": "1774.24",

    "Alfa12": "0.44505",
    "Alfa13": "0.42441",
    "Alfa23": "0.49549",
}

# Caso 2: Consistente
caso_2_consistente = {
    "temperatura" : "298.15",

    "nome_1": "n-hexano",
    "nome_2": "Benzeno",
    "nome_3": "Sulfolano",

    "MM_1": "86.18",
    "MM_2": "78.11",
    "MM_3": "120.17",

    "A12": "-166.878",
    "A13": "6495.50",
    "A21": "531.517",
    "A23": "860.391",
    "A31": "7615.40",
    "A32": "492.417",

    "Alfa12": "0.73115",
    "Alfa13": "0.10680",
    "Alfa23": "0.99993",
}

# Fração Mássica da fase rica em  Sulfolane.
fracao_massica_caso_2_extrato = np.array([
    [0.015, 0.06, 0.925],
    [0.023, 0.166, 0.811],
    [0.03, 0.264, 0.706],
    [0.034, 0.308,	0.657],
    [0.043, 0.361,	0.595],
    [0.047, 0.41, 0.543],
    [0.074, 0.475, 0.451],
    [0.106, 0.545, 0.348],
    [0.117, 0.556, 0.327],
    [0.14, 0.572 ,0.288]
    ])

# Fração Mássica da fase rica em  n-Hexane
fracao_massica_caso_2_rafinado = np.array([
    [0.924,	0.073,	0.003],
    [0.771,	0.223,	0.006],
    [0.657,	0.327,	0.016],
    [0.596,	0.392,	0.012],
    [0.535,	0.451,	0.014],
    [0.471,	0.499,	0.03],
    [0.392,	0.55,	0.057],
    [0.307,	0.601,	0.092],
    [0.283,	0.603,	0.114],
    [0.252,	0.609,	0.14]
])

# Massa molar dos componentes. Obtidos de: https://pubchem.ncbi.nlm.nih.gov/
massa_molar_caso_2 = np.array([float(caso_2_consistente["MM_1"]), float(caso_2_consistente["MM_2"]), float(caso_2_consistente["MM_3"])])

# Frações molares, na ordem: [benzene (1), cyclohexane (2), DMSO(3)]
fracao_molar_caso_2_extrato = FracaoMolar(fracao_massica_caso_2_extrato, massa_molar_caso_2)

fracao_molar_caso_2_rafinado = FracaoMolar(fracao_massica_caso_2_rafinado, massa_molar_caso_2)



