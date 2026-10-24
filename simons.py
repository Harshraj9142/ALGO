
import pandas as pd
from IPython.display import display
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

secret_string = "11"
n = len(secret_string)

qc = QuantumCircuit(2 * n, n)

# Step 1: Apply Hadamard gates
for qubit in range(n):
    qc.h(qubit)

qc.barrier()

# Step 2: Oracle
# Correct oracle for secret string "11"
qc.cx(0, n)
qc.cx(1, n)

qc.barrier()

# Step 3: Apply Hadamard gates again
for qubit in range(n):
    qc.h(qubit)

# Step 4: Measure input register
for qubit in range(n):
    qc.measure(qubit, qubit)

# Display circuit diagram
print("--- Simon's Algorithm Quantum Circuit Diagram ---")

fig_circuit = qc.draw(output='mpl')
fig_circuit.suptitle(
    "Simon's Algorithm Circuit Design Layout",
    fontsize=14,
    y=1.05
)
display(fig_circuit)

# Step 5: Simulation
simulator = AerSimulator()
compiled_circuit = transpile(qc, simulator)

result = simulator.run(
    compiled_circuit, shots=1024
).result()

counts = result.get_counts()

# Create DataFrame
df = pd.DataFrame(
    list(counts.items()),
    columns=['Measured Bitstring (b)', 'Shot Count']
)

df['Probability'] = (
    df['Shot Count'] / df['Shot Count'].sum()
)

print("\n--- Simon's Algorithm Execution Results ---")
print(f"Secret Mask 's' to resolve: {secret_string}\n")
print(df.to_string(index=False))

# Display histogram
display(plot_histogram(counts))
