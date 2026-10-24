import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from IPython.display import display

# PHASE ORACLE
def phase_oracle(n, target_state):
    """Creates a phase oracle that flips the phase of target_state."""

    if len(target_state) != n:
        raise ValueError(
            f"Target state must contain exactly {n} bits."
        )

    if any(bit not in "01" for bit in target_state):
        raise ValueError("Target state must contain only 0 and 1.")

    qc = QuantumCircuit(n, name="Oracle")
    reversed_target = target_state[::-1]

    # Convert target state to |111...1>
    for qubit, bit in enumerate(reversed_target):
        if bit == "0":
            qc.x(qubit)

    # Multi-controlled Z
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)

    # Restore original state
    for qubit, bit in enumerate(reversed_target):
        if bit == "0":
            qc.x(qubit)

    return qc


# DIFFUSION OPERATOR
def diffusion_operator(n):
    """Creates the diffuser (inversion about the mean)."""

    qc = QuantumCircuit(n, name="Diffuser")
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))

    return qc


# GROVER ALGORITHM
def grover_algorithm(n, r, target_state):
    qc = QuantumCircuit(n, n)

    # Create equal superposition
    qc.h(range(n))
    qc.barrier()

    # Create oracle and diffuser
    oracle = phase_oracle(n, target_state)
    diffuser = diffusion_operator(n)

    # Grover iterations
    for _ in range(r):
        qc.append(oracle, range(n))
        qc.append(diffuser, range(n))
        qc.barrier()

    # Measurement
    qc.measure(range(n), range(n))

    return qc


# PARAMETERS
num_qubits = 3
target_state = "011"

optimal_r = int(
    np.round((np.pi / 4) * np.sqrt(2 ** num_qubits))
)

# PRINT PARAMETERS
print("GROVER'S ALGORITHM")
print(f"Number of qubits: {num_qubits}")
print(f"Target state: |{target_state}>")
print(f"Calculated optimal iterations (r): {optimal_r}")

# CREATE CIRCUIT
grover_circuit = grover_algorithm(
    num_qubits,
    r=optimal_r,
    target_state=target_state
)

# SIMULATION
simulator = AerSimulator()
transpiled_circuit = transpile(
    grover_circuit,
    simulator
)

result = simulator.run(
    transpiled_circuit,
    shots=1024
).result()

counts = result.get_counts()

# RESULTS
print("\nMeasurement Results:")
print(counts)

print(f"\nTarget state searched: |{target_state}>")

most_likely_state = max(counts, key=counts.get)
print(f"Most frequently measured state: |{most_likely_state}>")
 
if most_likely_state == target_state:
    print("\nSUCCESS: Target state was found!")
else:
    print("\nTarget state was NOT the most frequent result.")

# VISUALIZATIONS
print("\nRendering Visualizations Inline Below:")

fig1 = grover_circuit.draw("mpl")
fig1.suptitle(
    "Grover's Algorithm High-Level Schema",
    fontsize=16
)
display(fig1)

fig2 = grover_circuit.decompose().draw("mpl")
fig2.suptitle(
    "Grover's Algorithm Gate-Level (Decomposed)",
    fontsize=16
)
display(fig2)

fig3 = plot_histogram(
    counts,
    title=f"Grover Search Results — Target |{target_state}>"
)
display(fig3)
