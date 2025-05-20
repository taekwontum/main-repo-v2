
from flask import Flask, request, jsonify
from qiskit import QuantumCircuit, transpile, Aer, execute
from qiskit_ibm_provider import IBMProvider
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def run_quantum_job():
    try:
        # Load IBM Quantum API token
        token = os.environ.get('IBM_QUANTUM_TOKEN')
        if not token:
            return jsonify({'error': 'Missing IBM Quantum token'}), 500

        provider = IBMProvider(token=token)

        # Build a simple quantum circuit
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure_all()

        # Use a simulator backend (or change to a real backend)
        backend = provider.get_backend('ibmq_qasm_simulator')
        transpiled = transpile(qc, backend)
        job = backend.run(transpiled)
        result = job.result()

        counts = result.get_counts()
        return jsonify({'result': counts})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run()
