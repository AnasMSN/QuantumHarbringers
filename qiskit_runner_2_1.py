from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Estimator
from qiskit_ibm_runtime.fake_provider import FakeAlmadenV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


class QiskitRunner:
    def __init__(self, backend_type='local', backend_name='aer_simulator', token=None, instance=None):
        self.backend_type = backend_type
        self.backend_name = backend_name
        self.token = token
        self.instance = instance
        self.provider = None
        self.backend = self._get_backend()

    def _get_backend(self):
        # if self.backend_type == 'local':
        #     return AerSimulator()
        if self.backend_type == 'qpu':
            self.provider = QiskitRuntimeService(channel='ibm_quantum', token=self.token, instance=self.instance)
            return self.provider.least_busy(simulator=False, operational=True)
        elif self.backend_type == 'fake':
            return FakeAlmadenV2()
        else:
            raise ValueError(f"Unknown backend type: {self.backend_type}")

    def run_circuit(self, circuit: QuantumCircuit, shots=1024, observables=None):
        if self.backend_type == 'qpu' and observables is not None:
            # ISA transpilation and mapped observable flow
            pm = generate_preset_pass_manager(backend=self.backend, optimization_level=1)
            isa_circuit = pm.run(circuit)
            mapped_observables = [obs.apply_layout(isa_circuit.layout) for obs in observables]

            estimator = Estimator(self.backend)
            job = estimator.run([(isa_circuit, mapped_observables)])
            return job.result()[0]  # Result from the single pub
        else:
            transpiled = transpile(circuit, self.backend)
            job = self.backend.run(transpiled, shots=shots)
            result = job.result()
            return result.get_counts()
