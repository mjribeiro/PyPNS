import PyPN
import matplotlib.pyplot as plt
from PyPN.takeTime import *
import numpy as np
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


# import cPickle as pickle
# import os

calculationFlag = True# run simulation or load latest bundle with this parameters (not all taken into account for identification)

upstreamSpikingOn = False
electricalStimulusOn = True

# set simulation paramse
tStop=20
timeRes=0.0025#0.0025

# set length of bundle and number of axons
lengthOfBundle = 4000 # 400000
numberOfAxons = 2

# create a guide the axons will follow
# segmentLengthAxon = 10
# bundleGuide = PyPN.createGeometry.get_bundle_guide_straight(lengthOfBundle, segmentLengthAxon)
# bundleGuide = PyPN.createGeometry.get_bundle_guide_corner(lengthOfBundle, segmentLengthAxon)
# bundleGuide = PyPN.createGeometry.get_bundle_guide_corner(lengthOfBundle, segmentLengthAxon)
# bundleGuide = PyPN.createGeometry.get_bundle_guide_random(lengthOfBundle, segmentLength=200)

# set the diameter distribution or fixed value
# see http://docs.scipy.org/doc/numpy/reference/routines.random.html
# 5.7, 7.3, 8.7, 10., 11.5, 12.8, 14., 15., 16.
myelinatedDiam =  {'distName' : 'uniform', 'params' : (1.5, 4)} # .2 #
unmyelinatedDiam = {'distName' : 'uniform', 'params' : (0.1, 2)} # .2 #



# # definition of the stimulation type of the axon
# stimulusParameters = {  'stimType': "EXTRA", #Stimulation type either "INTRA" or "EXTRA"
#                         'amplitude': 0.015, # 0.005, # 0.016,#0.2,# .0001,#1.5, #0.2, # 0.004, # 10., #  # Pulse amplitude (mA)
#                         'frequency': 20., # Frequency of the pulse (kHz)
#                         'dutyCycle': .5, # 0.05, # Percentage stimulus is ON for one period (t_ON = duty_cyle*1/f)
#                         'stimDur' : 0.05, # Stimulus duration (ms)
#                         'waveform': 'BIPHASIC', # Type of waveform either "MONOPHASIC" or "BIPHASIC" symmetric
#                         'radiusBundle' : 50, #um
#                         # 'tStop' : tStop,
#                         'timeRes' : timeRes,
#                         'delay': 5, # ms
#                         # 'invert': True
# }
#
# # MONO, inv: 0.005
# # BI, inv: 0.015
# # MONO, non-inv: 0.025
# # BI, non-inv: 0.015

# definition of the stimulation type of the axon
cuffParameters = {      'amplitude': 1., # 0.005, # 0.016,#0.2,# .0001,#1.5, #0.2, # 0.004, # 10., #  # Pulse amplitude (mA)
                        'frequency': 20., # Frequency of the pulse (kHz)
                        'dutyCycle': .5, # 0.05, # Percentage stimulus is ON for one period (t_ON = duty_cyle*1/f)
                        'stimDur' : 0.05, # Stimulus duration (ms)
                        'waveform': 'MONOPHASIC', # Type of waveform either "MONOPHASIC" or "BIPHASIC" symmetric
                        'radius' : 50, #um
                        'timeRes' : timeRes,
                        'delay': 5, # ms
                        'invert': True
}

intraParameters = {     'amplitude': 2., # 0.005, # 0.016,#0.2,# .0001,#1.5, #0.2, # 0.004, # 10., #  # Pulse amplitude (mA)
                        'frequency': 20., # Frequency of the pulse (kHz)
                        'dutyCycle': .5, # 0.05, # Percentage stimulus is ON for one period (t_ON = duty_cyle*1/f)
                        'stimDur' : 0.05, # Stimulus duration (ms)
                        'waveform': 'MONOPHASIC', # Type of waveform either "MONOPHASIC" or "BIPHASIC" symmetric
                        'timeRes' : timeRes,
                        'delay': 5, # ms
                        # 'invert': True
}

# # definition of the stimulation type of the axon
# stimulusParameters = {  'delay': 5, # delay (ms)
#                         'stimDur': 0.05, # Stimulus duration (ms)
#                         'amplitude': 1.5 # 0.15 # Pulse amplitude (nA)
# }

# recording parameters of the cuff electrodes
# recordingParameters = { 'numberContactPoints': 8, # Number of points on the circle constituing the cuff electrode
#                         'recordingElecPos': [lengthOfBundle, lengthOfBundle + 50], #um Position of the recording electrode along axon in um, in "BIPOLAR" case the position along axons should be given as a couple [x1,x2]
#                         'numberElecs': 3, # number of electrodes along the bundle
# }
recordingParameters = { 'radius': 200,
                        'numberOfElectrodes': 2,
                        'positionMax': 1.,
                        'numberOfPoles': 2
}

# axon parameters
myelinatedParameters = {'fiberD': myelinatedDiam, # um Axon diameter (5.7, 7.3, 8.7, 10.0, 11.5, 12.8, 14.0, 15.0, 16.0)
}

# axon parameters
unmyelinatedParameters = {'fiberD': unmyelinatedDiam, # um Axon diameter
}

# set all properties of the bundle
bundleParameters = {    'radius': 150, #150, #um Radius of the bundle (typically 0.5-1.5mm)
                        'length': lengthOfBundle, # um Axon length
                        # 'bundleGuide' : bundleGuide,
                        # 'randomDirectionComponent' : 0,

                        'numberOfAxons': numberOfAxons, # Number of axons in the bundle
                        'pMyel': 1., # Percentage of myelinated fiber type A
                        'pUnmyel': 0., #Percentage of unmyelinated fiber type C
                        'paramsMyel': myelinatedParameters, #parameters for fiber type A
                        'paramsUnmyel': unmyelinatedParameters, #parameters for fiber type C

                        'tStop' : tStop,
                        'timeRes' : timeRes,

                        'saveI':True,
                        'saveV':False
}

# combine parameters for the bundle creation
Parameters = dict(bundleParameters, **recordingParameters)

if calculationFlag:

    # create the bundle with all properties of axons and recording setup
    bundle = PyPN.Bundle(**bundleParameters)

    # spiking through a single electrical stimulation
    if electricalStimulusOn:
        # stimulusInstance = PyPN.Stimulus(**stimulusParameters)
        # plt.plot(stimulusInstance.t, stimulusInstance.stimulusSignal)
        # plt.title('stimulus signal without delay')
        # plt.show()
        # bundle.add_excitation_mechanism(PyPN.StimCuff(**cuffParameters))
        bundle.add_excitation_mechanism(PyPN.StimIntra(**intraParameters))
        # bundle.add_excitation_mechanism(PyPN.SimpleIClamp(**stimulusParameters))

    # bundle.add_recording_mechanism(PyPN.CuffElectrode2D(**recordingParameters))
    # for position in np.arange(0.2, 0.5, 0.001):
    #     bundle.add_recording_mechanism(PyPN.RecCuff2D(radius=1000, positionMax=position, sigma=1.))
    # bundle.add_recording_mechanism(PyPN.RecCuff3D(radius=1000, positionMax=0.5, sigma=1., width=10000))
    # bundle.add_recording_mechanism(PyPN.RecCuff3D(radius=1000, positionMax=0.5, sigma=1.))
    # bundle.add_recording_mechanism(PyPN.RecCuff3D(radius=1000, positionMax=0.5, sigma=1., width=40000))
    # bundle.add_recording_mechanism(PyPN.RecCuff3D(radius=1000, positionMax=0.35, sigma=1., width=120000))

    bundle.add_recording_mechanism(PyPN.RecCuff3D(radius=1000, positionMax=0.2, sigma=1., width=2000))
    # bundle.add_recording_mechanism(PyPN.RecCuff3D(1000, numberOfElectrodes=2, positionMax=0.8, sigma=1., width=1000))


    # PyPN.plot.geometry_definition(bundle)
    # plt.show()


    with PyCallGraph(output=GraphvizOutput()):
        # run the simulation
        bundle.simulate()

    # save the bundle to disk
    PyPN.save_bundle(bundle)
else:

    # try to open a bundle with the parameters set above
    # bundle = PyPN.open_recent_bundle(Parameters)
    # bundle = PyPN.open_bundle_from_location('/media/carl/4ECC-1C44/PyPN/dt=0.0025 tStop=20 pMyel=1.0 pUnmyel=0.0 L=400000 nAxons=1/bundle00001')
    # bundle = PyPN.open_bundle_from_location('/media/carl/4ECC-1C44/PyPN/dt=0.0025 tStop=20 pMyel=1.0 pUnmyel=0.0 L=400000 nAxons=1/bundle00004')
    # bundle = PyPN.open_bundle_from_location('/media/carl/4ECC-1C44/PyPN/dt=0.0025 tStop=20 pMyel=1.0 pUnmyel=0.0 L=400000 nAxons=1/bundle00005')
    bundle = PyPN.open_bundle_from_location('/media/carl/4ECC-1C44/PyPN/dt=0.0025 tStop=20 pMyel=1.0 pUnmyel=0.0 L=4000 nAxons=2/bundle00010')

# # bundle.add_recording_mechanism(PyPN.RecCuff3D(radius=1000, positionMax=0.2, sigma=1., width=2000))
# #
# # bundle.compute_CAPs_from_imem_files()
#
# # # save the bundle to disk
# # PyPN.save_bundle(bundle)
#
# # for axonIndex in range(len(bundle.axons)):
# #     with takeTime('load axon ' + str(axonIndex)):
# #         bundle.get_imem_from_file_axonwise(axonIndex)
#
#
# # # plot geometry, intra and extracellular recording, axon diameters
# # print '\nStarting to plot'
# # PyPN.plot.geometry(bundle)
# # PyPN.plot.CAP1D_singleAxon(bundle, 10)
#
# for i in range(len(bundle.recordingMechanisms)):
#     PyPN.plot.CAP1D(bundle, recMechIndex=i)
#
# # # f, (ax1, ax2) = plt.subplots(2,1, sharex=True)
# # meanCAP = 0
# # CAPs = []
# # for i in range(len(bundle.recordingMechanisms)):
# #     time, CAP = bundle.get_CAP_from_file(i)
# #
# #     # print 'mean amplitude = ' + str(np.mean(CAP[0,:]))
# #
# #     CAPs.append(CAP)
# #
# #     # plt.plot(time, CAP[0,:], label='CAP'+str(i))
# #     meanCAP +=CAP[0,:]
# #
# # # plt.plot(CAPs[0][0,:], label='CAP0')
# # # plt.plot(CAPs[1][0,:], label='CAP1')
# # meanCAP = meanCAP/len(bundle.recordingMechanisms)
# # plt.plot(time, meanCAP, label='mean CAP')
# # plt.legend()
# #
# PyPN.plot.geometry_definition(bundle)
#
# # PyPN.plot.CAP1D(bundle,recMechIndex=0)
# # PyPN.plot.CAP1D(bundle,recMechIndex=1)
# # PyPN.plot.CAP1D(bundle,recMechIndex=3)
#
#
# # PyPN.plot.voltage(bundle)
# # PyPN.plot.voltage_one_myelinated_axon(bundle)
# # PyPN.plot.diameterHistogram(bundle)
#
# # conVelDict = bundle.conduction_velocities(saveToFile=True) # (plot=False)
# # pickle.dump(conVelDict,open( os.path.join(bundle.basePath, 'conductionVelocities.dict'), "wb" ))
#
#
# # import matplotlib2tikz as mtz
# # mtz.save('CAP.tex')
#
# plt.show()

bundle = None