import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Updated mediums for selection
all_layers = [
    {"name": "Air", "wavelength": 1.0, "frequency": 343, "speed": 343, "medium_length": 5, "color": "b"},
    {"name": "Water", "wavelength": 0.3, "frequency": 5000, "speed": 1480, "medium_length": 5, "color": "g"},
    {"name": "Steel", "wavelength": 0.01, "frequency": 5960, "speed": 5960, "medium_length": 5, "color": "r"},
    {"name": "Earth", "wavelength": 0.15, "frequency": 600, "speed": 2500, "medium_length": 5, "color": "brown"},
    {"name": "Glass", "wavelength": 0.02, "frequency": 4000, "speed": 5500, "medium_length": 5, "color": "c"},
    {"name": "Rubber", "wavelength": 0.08, "frequency": 200, "speed": 1500, "medium_length": 5, "color": "orange"},
]

selected_layers = []

# Function to calculate wave height at a given position x and time t
def water_wave_height(x, t, k, omega, phase):
    return np.sin(k * x - omega * t + phase)

# Function to simulate wave propagation through selected mediums
def simulate_wave(t):
    x_values = []
    y_values = []

    current_position = 0
    for layer in selected_layers:
        k = 2 * np.pi / layer["wavelength"]
        omega = 2 * np.pi * layer["frequency"]
        phase = layer["speed"] * t

        # Generate points for this layer
        x_layer = np.linspace(current_position, current_position + layer["medium_length"], 200)
        y_layer = water_wave_height(x_layer, t, k, omega, phase)

        # Append the points for this layer to the full wave
        x_values.extend(x_layer)
        y_values.extend(y_layer)

        # Update current position
        current_position += layer["medium_length"]

    line.set_data(x_values, y_values)
    ax.set_xlim(0, sum(layer["medium_length"] for layer in selected_layers))
    ax.set_ylim(-1, 1)
    return line,

# Function to start the wave animation
def animate_wave(t=0):
    if animating:
        simulate_wave(t)
        ax.figure.canvas.draw_idle()
        root.after(100, lambda: animate_wave(t + 0.1))

# Function to start or stop animation
def toggle_animation():
    global animating
    if animating:
        animating = False
        animate_button.configure(text="Animate")
    else:
        animating = True
        animate_button.configure(text="Stop Animation")
        animate_wave()

# Function to create checkboxes for selecting mediums (horizontally)
def create_medium_checkboxes():
    for index, layer in enumerate(all_layers):
        var = ctk.StringVar(value="off")
        checkbox = ctk.CTkCheckBox(select_frame, text=layer["name"], variable=var, onvalue="on", offvalue="off",
                                   command=lambda v=var, l=layer: update_selected_layers(v, l))
        checkbox.pack(side=ctk.LEFT, padx=10, pady=5)  # Horizontal layout

# Function to update selected layers based on user input
def update_selected_layers(var, layer):
    if var.get() == "on":
        selected_layers.append(layer)
    else:
        selected_layers.remove(layer)

# Create the main Tkinter window
root = ctk.CTk()
root.title("Multiple Medium Transition Wave Simulator")

# Create a Matplotlib figure
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlabel('Position')
ax.set_ylabel('Wave Height')
ax.set_title('Wave Propagation Through Multiple Mediums')
ax.grid(True)

# Embed Matplotlib figure in Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)

# Animation control
animating = False

# Frame to hold the control elements
control_frame = ctk.CTkFrame(root)
control_frame.pack(side=ctk.TOP, padx=10, pady=10)

# Layer selection frame (for horizontal layout of checkboxes)
select_frame = ctk.CTkFrame(control_frame)
select_frame.pack(side=ctk.TOP, padx=10, pady=10)

# Button to toggle animation
animate_button = ctk.CTkButton(control_frame, text="Animate", command=toggle_animation)
animate_button.pack(side=ctk.BOTTOM, padx=10, pady=10)

# Create horizontal checkboxes for medium selection
create_medium_checkboxes()

# Start the main loop
root.mainloop()
