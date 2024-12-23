import streamlit as st
import numpy as np
import plotly.graph_objects as go
import json
import time

st.title("Genesis Physics Simulator")

# Sidebar for user settings
st.sidebar.header("Simulation Settings")
sim_steps = st.sidebar.slider("Simulation Steps", 10, 500, 100)
time_step = st.sidebar.slider("Time Step (s)", 0.01, 0.1, 0.05)
gravity = st.sidebar.slider("Gravity Strength", 0.0, 20.0, 9.8)
elasticity = st.sidebar.slider("Elasticity (0=inelastic, 1=perfectly elastic)", 0.0, 1.0, 0.9)

# User-defined configuration
st.sidebar.subheader("Custom Configuration")
default_config = '{"positions": [[1, 1], [9, 9]], "velocities": [[1, 1], [-1, -1]], "masses": [1, 1]}'
config_input = st.sidebar.text_area("Initial Conditions (JSON)", default_config)

# Load configuration
try:
    config = json.loads(config_input)
    positions = np.array(config["positions"])
    velocities = np.array(config["velocities"])
    masses = np.array(config["masses"])
except (json.JSONDecodeError, KeyError, ValueError):
    st.error("Invalid JSON input. Please ensure it contains 'positions', 'velocities', and 'masses'.")
    st.stop()

# Scenario Library
st.sidebar.subheader("Predefined Scenarios")
scenario = st.sidebar.selectbox("Select Scenario", ["Custom", "Elastic Collision", "Gravity Well", "Projectile Motion"])

if scenario != "Custom":
    if scenario == "Elastic Collision":
        positions = np.array([[3, 5], [7, 5]])
        velocities = np.array([[-2, 0], [2, 0]])
        masses = np.array([1, 1])
    elif scenario == "Gravity Well":
        positions = np.random.rand(10, 2) * 10
        velocities = np.zeros((10, 2))
        masses = np.random.rand(10) + 0.5
    elif scenario == "Projectile Motion":
        positions = np.array([[0, 0]])
        velocities = np.array([[5, 10]])
        masses = np.array([1])

# Simulation logic
def simulate(positions, velocities, masses, gravity, elasticity, steps, time_step):
    history = [positions.copy()]
    for _ in range(steps):
        # Apply gravity
        velocities[:, 1] -= gravity * time_step

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

# Run the simulation
st.write("Running simulation...")
trajectory = simulate(positions, velocities, masses, gravity, elasticity, sim_steps, time_step)

# Real-time rendering
st.write("Rendering simulation...")
placeholder = st.empty()
for frame in trajectory:
    fig = go.Figure()

    # Add particle positions
    fig.add_trace(go.Scatter(
        x=frame[:, 0],
        y=frame[:, 1],
        mode='markers',
        marker=dict(size=10, color='blue'),
    ))

    fig.update_layout(
        xaxis=dict(range=[0, 10]),
        yaxis=dict(range=[0, 10]),
        title="Particle Simulation",
        xaxis_title="X Position",
        yaxis_title="Y Position",
    )
    placeholder.plotly_chart(fig, use_container_width=True)
    time.sleep(0.1)  # Simulate real-time rendering
