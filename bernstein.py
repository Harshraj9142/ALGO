from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from IPython.display import display

def bernstein_vazirani(secret_string: str) -> dict:
    """Implements the Bernstein-Vazirani algorithm for a given secret binary string."""
    n = len(secret_string)

    # Initialize a circuit: n input qubits + 1 target qubit, and n classical bits
    qc = QuantumCircuit(n + 1, n)

    # Step 1: Put input qubits into superposition (+) state
    for qubit in range(n):
        qc.h(qubit)

    # Step 2: Prepare the target qubit in the |-> state for phase kickback
    qc.x(n)
    qc.h(n)
    qc.barrier()  # Visual separator for the circuit diagram

    # Step 3: The Oracle
    # Apply a CNOT gate from input qubit i to target qubit n if the i-th bit is '1'
    # Note: Qiskit uses little-endian ordering, so reverse the string
    # to match standard index ordering
    for i, bit in enumerate(reversed(secret_string)):
        if bit == '1':
            qc.cx(i, n)

    qc.barrier()

    # Step 4: Apply Hadamard gates to input qubits again
    # to reverse superposition
    for qubit in range(n):
        qc.h(qubit)

    # Step 5: Measure the input qubits
    for qubit in range(n):
        qc.measure(qubit, qubit)

    # Step 6: Simulate the circuit
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()

    print("--- Quantum Circuit Diagram ---")
    display(qc.draw(output='mpl'))

    return result.get_counts()


# --- Execution ---
if __name__ == "__main__":

    # Define your secret binary string here
    secret = "1011"

    print(f"Secret string to find: {secret}\n")

    counts = bernstein_vazirani(secret)

    print("\n--- Simulation Results ---")
    print(f"Measured Bitstring (Counts): {counts}")
