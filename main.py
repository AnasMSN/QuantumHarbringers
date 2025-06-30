
from qiskit import QuantumCircuit
from qiskit_runner_2_1 import QiskitRunner
from qiskit.quantum_info import Pauli
from qiskit.quantum_info import SparsePauliOp

from dotenv import load_dotenv
import os
load_dotenv()

token = os.getenv("QISKIT_TOKEN")
instance = os.getenv("QISKIT_INSTANCE")

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

observable = SparsePauliOp.from_list([("ZZ", 1)])
runner = QiskitRunner(backend_type='fake')

runner = QiskitRunner(backend_type='qpu', backend_name='ibmq_qasm_simulator', token=token, instance=instance)
result = runner.run_circuit(qc, observables=[observable])
print(result)
