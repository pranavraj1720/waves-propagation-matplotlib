import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize customtkinter
ctk.set_appearance_mode("System")  # Use "Dark", "Light", or "System" for auto mode
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

# Define wave parameters for each medium
mediums = {
    "Air": {"wavelength": 1.0, "frequency": 343, "speed": 343, "medium_length": 10},
    "Water": {"wavelength": 0.3, "frequency": 5000, "speed": 1480, "medium_length": 5},
    "Steel": {"wavelength": 0.02, "frequency": 300000, "speed": 5960, "medium_length": 1},
    "Earth": {"wavelength": 0.5, "frequency": 10000, "speed": 6000, "medium_length": 2},
    "Glass": {"wavelength": 0.025, "frequency": 200000, "speed": 5000, "medium_length": 1},
    "Rubber": {"wavelength": 0.1, "frequency": 10, "speed": 50, "medium_length": 2},
}

# Function to calculate wave height at a given position x and time t
def wave_height(x, t, medium):
    k = 2 * np.pi / medium["wavelength"]
    omega = 2 * np.pi * medium["frequency"]
    phase = medium["speed"] * t
    return np.sin(k * x - omega * t + phase)

# Function to simulate wave propagation based on selected medium
def simulate_wave(t, medium):
    x_values = np.linspace(0, medium["medium_length"], 500)
    y_values = wave_height(x_values, t, medium)
    line.set_data(x_values, y_values)
    ax.set_xlim(0, medium["medium_length"])
    ax.set_ylim(-1, 1)
    return line,

# Animation function to update the wave based on time
def animate(t):
    current_medium = mediums[medium_var.get()]
    simulate_wave(t, current_medium)
    ax.figure.canvas.draw_idle()
    root.after(100, lambda: animate(t + 0.1))

# Function to update the simulation when a new medium is selected
def update_medium(event):
    animate(0)

# Create customtkinter window
root = ctk.CTk()
root.title("Wave Propagation in Different Mediums")
root.geometry("800x600")

# Create a modern dropdown menu for medium selection
medium_var = ctk.StringVar(value="Choose Medium")
medium_dropdown = ctk.CTkOptionMenu(
    root, 
    values=list(mediums.keys()), 
    command=update_medium, 
    variable=medium_var,
    width=120,
    font=('Inter', 15),
    button_color="#5790DF",
    text_color="white",  # Text color
    corner_radius=6,  # Rounded corners
    fg_color="#5790DF"
)
medium_dropdown.configure()  
medium_dropdown.pack(side=ctk.TOP, anchor='ne', padx=20, pady=20)  # Position at top right with margins

# Create Matplotlib figure
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlabel('Position')
ax.set_ylabel('Wave Amplitude')
ax.set_title('Wave Propagation')
ax.grid(True)

# Embed Matplotlib figure in customtkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)


root.mainloop()
