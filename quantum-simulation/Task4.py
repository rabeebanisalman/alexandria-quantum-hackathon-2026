import numpy as np
import matplotlib.pyplot as plt
from qiskit import transpile
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError, depolarizing_error
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2 as Estimator


"""
service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)

# qubit_op = ...   # SparsePauliOp
# ansatz = ...     # QuantumCircuit
# opt_params = ... # list of floats
# pool_ops = ...   # list of SparsePauliOp
# eigvals_exact = ... # exact eigenvalues
"""

# function makes a longer version of the cuircut behave the same as if without noise 
def folded_circuit(circuit, scale):
    k = (scale - 1) // 2
    out = circuit.copy()
    for _ in range(k):
        out = out.compose(circuit.inverse()).compose(circuit)
    return out


# the p1,p2 are just assumption but to get more real acurate values in real quantam computer we need to get them from hardware calibration data 
def build_gate_noise_model(p1=0.001, p2=0.01):
    noise_model = NoiseModel()  # this create empty qiskit noise model 

    #add to noise model a one-qubit depolarizing error with p=p1,apply error to every qubit when one of these gates is executed.
    noise_model.add_all_qubit_quantum_error(
        depolarizing_error(p1, 1), ["u", "u1", "u2", "u3", "rx", "ry", "rz", "sx", "x"]
    )
    noise_model.add_all_qubit_quantum_error(depolarizing_error(p2, 2), ["cx", "cz"])
    return noise_model


# runs floded-cuircut on noise simulator and give the quantum state as density matrix 
# it gets simulator aersimulator has the gate noise model , base_cuircut is the original vqe , scale the fold factor 
# should return array 'matrics 2d if 1 qbit ad 4d if 2qbit'
def noisy_density_matrix(simulator, base_circuit, scale):
    circ = folded_circuit(base_circuit, scale)
    circ.save_density_matrix()
    result = simulator.run(circ).result()
    return result.data(0)["density_matrix"].data

# tells the energy when x=0 "zero noise "
def zne_linear(x, y):
    return np.polyval(np.polyfit(x, y, 1), 0)

#same as zne linear but draw a curve " more accurate "
def zne_richardson(x, y, order=2):
    return np.polyval(np.polyfit(x, y, order), 0)

