
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from IPython.display import display
import random

def deutsch_jozsa_oracle(n, case='balanced'):
    oracle = QuantumCircuit(n + 1)

    if case == 'constant_0':
        pass

    elif case == 'constant_1':
        oracle.x(n)

    elif case == 'balanced_identity':
        oracle.cx(0, n)

    elif case == 'balanced_not':
        oracle.x(n)
        oracle.cx(0, n)

    for qubit in range(n):
        if qubit % 2 != 0:
            oracle.x(qubit)
            oracle.cx(qubit, n)
            oracle.x(qubit)

    return oracle


def deutsch_jozsa_algorithm(n, case):
    qc = QuantumCircuit(n + 1, n)

    qc.x(n)                  # Output qubit = |1>
    qc.h(range(n + 1))       # Hadamard gates

    qc.append(
        deutsch_jozsa_oracle(n, case),
        range(n + 1)
    )

    qc.h(range(n))
    qc.measure(range(n), range(n))

    return qc


simulator = AerSimulator()

n = random.randint(1, 28)

for case in [
    'constant_0',
    'constant_1',
    'balanced_identity',
    'balanced_not'
]:
    print(f"\n--- Running Case: {case.upper()} ---")

    qc = deutsch_jozsa_algorithm(n, case)

    tqc = transpile(qc, simulator)
    job = simulator.run(tqc, shots=1024)
    result = job.result()
    counts = result.get_counts()

    display(qc.draw(output="mpl"))

    print(f"Case: {case}, Result: {counts}")

    if '0' * n in counts:
        print("-> Function is CONSTANT")
    else:
        print("-> Function is BALANCED")
