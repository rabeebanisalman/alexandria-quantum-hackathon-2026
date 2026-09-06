from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.transformers import ActiveSpaceTransformer
from qiskit_nature.second_q.mappers import JordanWignerMapper

eth_mol = PySCFDriver(
    atom="C 0 0 0.67; H 0 0.928 1.2355; H 0 -0.928 1.2355; C 0 0 -0.67; H 0 0.928 -1.2355; H 0 -0.928 -1.2355",
    basis='sto3g'
)

eth_mol_twisted = PySCFDriver(
    atom="C 0 0 0.73; H 0.928 0 1.26; H -0.928 0 1.26; C 0 0 -0.73; H 0.928 0 -1.26; H -0.928 0 -1.26",
    basis='sto3g'
)

es_problem = eth_mol.run()

es_problem_twisted = eth_mol_twisted.run()

n_e = 2
n_orb = 2 # change to 4 for expansion

from qiskit_nature.second_q.transformers import ActiveSpaceTransformer

transformer = ActiveSpaceTransformer(num_electrons=n_e,num_spatial_orbitals=n_orb)

reduced_problem = transformer.transform(es_problem)
reduced_problem_twisted = transformer.transform(es_problem_twisted)

mapper = JordanWignerMapper()
ham = mapper.map(reduced_problem.second_q_ops()[0]) # index of the main hamiltonian in returned tuple
ham_twisted = mapper.map(reduced_problem_twisted.second_q_ops()[0])