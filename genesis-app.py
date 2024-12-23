import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Genesis Physics Simulator")

# Sidebar settings
st.sidebar.header("Simulation Settings")
num_particles = st.sidebar.number_input("Number of Particles", min_value=1, max_value=100, value=10)
gravity = st.sidebar.slider("Gravity Strength", 0.0, 20.0, 9.8)
elasticity = st.sidebar.slider("Elasticity (0=inelastic, 1=perfectly elastic)", 0.0, 1.0, 0.9)
simulation_steps = st.sidebar.slider("Simulation Steps", 10, 500, 100)
time_step = st.sidebar.slider("Time Step (s)", 0.01, 0.1, 0.05)

# User-defined forces
enable_repulsion = st.sidebar.checkbox("Enable Particle Repulsion")
repulsion_strength = st.sidebar.slider("Repulsion Strength", 0.0, 10.0, 1.0) if enable_repulsion else 0

# Initialize particles
st.sidebar.subheader("Particle Initialization")
positions = np.random.rand(num_particles, 2) * 10  # Random positions
velocities = np.random.randn(num_particles, 2) * 2  # Random velocities
masses = np.random.rand(num_particles) * 2 + 0.5  # Random masses (0.5 to 2.5)

# Simulation logic
def simulate(positions, velocities, masses, gravity, elasticity, steps, time_step, repulsion_strength):
    history = [positions.copy()]
    for _ in range(steps):
        # Apply gravity
        velocities[:, 1] -= gravity * time_step
        
        # Apply repulsion if enabled
        if repulsion_strength > 0:
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    displacement = positions[j] - positions[i]
                    distance = np.linalg.norm(displacement) + 1e-5  # Avoid division by zero
                    force_magnitude = repulsion_strength / distance**2
                    force = (displacement / distance) * force_magnitude
                    velocities[i] -= force / masses[i] * time_step
                    velocities[j] += force / masses[j] * time_step

        # Update positions
        positions += velocities * time_step
        
        # Boundary collisions
        for i, pos in enumerate(positions):
            for dim in range(2):  # x and y
                if pos[dim] < 0 or pos[dim] > 10:  # Wall collision
                    velocities[i, dim] *= -elasticity
                    positions[i, dim] = np.clip(pos[dim], 0, 10)
        
        history.append(positions.copy())
    return history

# Run simulation
trajectory = simulate(positions, velocities, masses, gravity, elasticity, simulation_steps, time_step, repulsion_strength)

# Visualization
fig, ax = plt.subplots(figsize=(6, 6))
for particle_path in zip(*trajectory):
    ax.plot(*zip(*particle_path), alpha=0.7)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_title("Particle Trajectories")
ax.set_xlabel("X Position")
ax.set_ylabel("Y Position")

st.pyplot(fig)
