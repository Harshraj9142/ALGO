
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from IPython.display import display

def deutsch_oracle(case='balanced_identity'):
    oracle = QuantumCircuit(2)

    if case == 'constant_0':
        pass

    elif case == 'constant_1':
        oracle.x(1)

    elif case == 'balanced_identity':
        oracle.cx(0, 1)

    elif case == 'balanced_not':
        oracle.x(1)
        oracle.cx(0, 1)

    return oracle


def deutsch_algorithm(case):
    qc = QuantumCircuit(2, 1)

    # Prepare the qubits
    qc.x(1)
    qc.h([0, 1])
    qc.barrier()

    # Apply the oracle
    qc.append(deutsch_oracle(case), [0, 1])
    qc.barrier()

    # Apply Hadamard to input qubit
    qc.h(0)

    # Measure
    qc.measure(0, 0)

    return qc


simulator = AerSimulator()

for case in [
    'constant_0',
    'constant_1',
    'balanced_identity',
    'balanced_not'
]:
    print(f"\n--- Running Case: {case.upper()} ---")

    qc = deutsch_algorithm(case)

    print("Circuit Diagram:")
    display(qc.draw(output='mpl'))

    tqc = transpile(qc, simulator)
    job = simulator.run(tqc, shots=1024)
    counts = job.result().get_counts()

    print(f"Result: {counts}")

    if counts.get('0', 0) == 1024:
        print("-> Function is CONSTANT")
    else:
        print("-> Function is BALANCED")
