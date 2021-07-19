import PyPNS
import matplotlib.pyplot as plt
import numpy as np
from time import monotonic

# ---------------------------------------------------------------------------
# --------------------------------- DEFINITION ------------------------------
# ---------------------------------------------------------------------------

# ----------------------------- simulation params ---------------------------

tStop=50
dt=0.0025

# ----------------------------- axon params ---------------------------

# diameters enlarged for quicker execution
myelinatedParameters = {'fiberD': {'distName': 'normal', 'params': (1.7, 0.4)}}
unmyelinatedParameters = {'fiberD': {'distName': 'normal', 'params': (1.0, 0.2)}}

segmentLengthAxon = 15
rdc = 0.2 # random direction component

# ----------------------------- bundle params -------------------------------

# set length of bundle and number of axons
bundleLength = 40000
nAxons = 5

# bundle guide
bundleGuide = PyPNS.createGeometry.get_bundle_guide_straight(bundleLength, segmentLengthAxon)

# ------------------------ intracellular stimulation params -----------------

# parameters of signals for stimulation
rectangularSignalParamsIntra = {'amplitude': 50., #50,  # Pulse amplitude (mA)
                                'frequency': 20.,  # Frequency of the pulse (kHz)
                                'dutyCycle': 0.5,  # Percentage stimulus is ON for one period (t_ON = duty_cyle*1/f)
                                'stimDur': 0.05,  # Stimulus duration (ms)
                                'waveform': 'MONOPHASIC',  # Type of waveform either "MONOPHASIC" or "BIPHASIC" symmetric
                                'delay': 0.,  # ms
                                # 'invert': True,
                                # 'timeRes': timeRes,
                                }

intraParameters = {'stimulusSignal': PyPNS.signalGeneration.rectangular(**rectangularSignalParamsIntra)}

# ------------------------- extracellular stimulation params -----------------

rectangularSignalParamsExtra = {'amplitude': 3000, # Pulse amplitude (nA)
                                'frequency': 1,  # Frequency of the pulse (kHz)
                                'dutyCycle': 0.5, # Percentage stimulus is ON for one period (t_ON = duty_cyle*1/f)
                                'stimDur': 1.,  # Stimulus duration (ms)
                                'waveform': 'MONOPHASIC', # Type of waveform either "MONOPHASIC" or "BIPHASIC" symmetric
                                'delay': 0.,  # ms
                                # 'invert': True,
                                # 'timeRes': timeRes,
                                }

elecPosStim = PyPNS.createGeometry.circular_electrode(bundleGuide, positionAlongBundle=12500, radius=235,
                                                     numberOfPoles=2, poleDistance=1000)
extPotMechStim = PyPNS.Extracellular.precomputedFEM(bundleGuide) # , 'oil190Inner50Endoneurium')

extraParameters = {'stimulusSignal': PyPNS.signalGeneration.rectangular(**rectangularSignalParamsExtra),
                   'electrodePositions': elecPosStim,
                   'extPotMech': extPotMechStim}

# ----------------------------- recording params -------------------------------

recordingParametersNew = {'bundleGuide': bundleGuide,
                          'radius': 220,
                          'positionAlongBundle': bundleLength*0.5,
                          'numberOfPoles': 1,
                          'poleDistance': 1000,
                          }

electrodePoints = PyPNS.createGeometry.circular_electrode(**recordingParametersNew)

extracellularMechs = []
extracellularMechs.append(PyPNS.Extracellular.homogeneous(sigma=1))
extracellularMechs.append(PyPNS.Extracellular.precomputedFEM(bundleGuide))
extracellularMechs.append(PyPNS.Extracellular.analytic(bundleGuide))

# ------------------------------------------------------------------------------
# --------------------------- PyPNS object instantiation  -----------------------
# ------------------------------------------------------------------------------

# set all properties of the bundle
bundleParameters = {'radius': 180,  #um Radius of the bundle (match carefully to extracellular mechanism)
                    'randomDirectionComponent': rdc,
                    'bundleGuide': bundleGuide,

                    'numberOfAxons': nAxons,  # Number of axons in the bundle
                    'pMyel': 1.,  # Percentage of myelinated fiber type A
                    'pUnmyel': 0.,  # Percentage of unmyelinated fiber type C
                    'paramsMyel': myelinatedParameters,  # parameters for fiber type A
                    'paramsUnmyel': unmyelinatedParameters,  # parameters for fiber type C

                    'tStop': tStop,
                    'timeRes': dt,

                    # 'saveI':True,
                    'saveV': False,

                    # 'numberOfSavedSegments': 50,  # number of segments of which the membrane potential is saved to disk
                    }

# create the bundle with all properties of axons
bundle = PyPNS.Bundle(**bundleParameters)

# spiking through a single electrical stimulation
bundle.add_excitation_mechanism(PyPNS.StimIntra(**intraParameters))
bundle.add_excitation_mechanism(PyPNS.StimField(**extraParameters))

# add recording electrodes. One for each extracellular medium
for extracellularMech in extracellularMechs:
    bundle.add_recording_mechanism(PyPNS.RecordingMechanism(electrodePoints, extracellularMech))

# ------------------------------------------------------------------------------
# -------------------------------- PyPNS calculation  ---------------------------
# ------------------------------------------------------------------------------

startTime = monotonic()
# run the simulation
bundle.simulate()
endTime = monotonic()
print(f"Time to run: {endTime - startTime} s")

PyPNS.save_bundle(bundle)
print('bundle saved.')

# ------------------------------------------------------------------------------
# -------------------------------- Result Plotting  ----------------------------
# ------------------------------------------------------------------------------
plt.figure()
for i in range(len(bundle.recordingMechanisms)):
    t, SFAPs = bundle.get_SFAPs_from_file(i)
    plt.plot(t, SFAPs, label='recordingMechanism_%i'%i)
plt.legend()
plt.xlabel('time (ms)')
plt.ylabel('voltage (mV)')
plt.show()

bundle = None