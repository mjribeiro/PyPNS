from neuron import h

def test_nrn_mpi():
    h.nrnmpi_init()       # initialize MPI
    pc = h.ParallelContext()
    print('I am {} of {}'.format(pc.id(), pc.nhost()))
    h.quit()              # necessary to avoid a warning message on parallel exit on some systems