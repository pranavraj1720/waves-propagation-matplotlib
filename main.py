import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize customtkinter
ctk.set_appearance_mode("System")  # Use "Dark", "Light", or "System"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

# Define wave parameters for each medium
mediums = {
    "Air": {"wavelength": 1.0, "frequency": 343, "speed": 343, "medium_length": 10},
    "Water": {"wavelength": 0.3, "frequency": 5000, "speed": 1480, "medium_length": 5},
    "Steel": {"wavelength": 0.01, "frequency": 5960, "speed": 5960, "medium_length": 2},
    "Earth": {"wavelength": 0.1, "frequency": 1500, "speed": 3000, "medium_length": 4},
    "Glass": {"wavelength": 0.02, "frequency": 5640, "speed": 5640, "medium_length": 2.5},
    "Rubber": {"wavelength": 0.005, "frequency": 40, "speed": 40, "medium_length": 0.2},
    "Custom": {"wavelength": 1.0, "frequency": 1.0, "speed": 1.0, "medium_length": 10},
}

# Function to calculate wave height at a given position x and time t
def water_wave_height(x, t, k, omega, phase):
    return np.sin(k * x - omega * t + phase)

# Function to simulate wave propagation
def simulate_wave(t, medium):
    k = 2 * np.pi / medium["wavelength"]
    omega = 2 * np.pi * medium["frequency"]
    phase = medium["speed"] * t
    x_values = np.linspace(0, medium["medium_length"], 500)
    y_values = water_wave_height(x_values, t, k, omega, phase)
    line.set_data(x_values, y_values)
    ax.set_xlim(0, medium["medium_length"])
    ax.set_ylim(-1, 1)
    return line,

# Create Tkinter window
root = ctk.CTk()
root.title("Wave Propagation Simulator")

# Create Matplotlib figure
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlabel('Position')
ax.set_ylabel('Wave Height')
ax.set_title('Wave Propagation')
ax.grid(True)

# Embed Matplotlib figure in Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)

# Function to update simulation based on selected medium
def update_medium(selected_medium):
    global current_medium, animating
    if selected_medium == "Custom":
        slider_frame.pack(side=ctk.TOP, fill=ctk.BOTH, padx=20, pady=10)
    else:
        slider_frame.pack_forget()
    if selected_medium in mediums:
        current_medium = mediums[selected_medium]
        update_steady_wave()  
    animating = False  
    animate_button.configure(text="Animate")  

# Function to update the steady wave display
def update_steady_wave():
    line.set_data([], []) 
    simulate_wave(0, current_medium)
    ax.figure.canvas.draw_idle()

# Animation control
animating = False

def toggle_animation():
    global animating
    if animating:
        animating = False
        animate_button.configure(text="Animate")
    else:
        animating = True
        animate_button.configure(text="Stop Animation")
        animate_wave()

def animate_wave(t=0):
    if animating:
        simulate_wave(t, current_medium)
        ax.figure.canvas.draw_idle()
        root.after(100, lambda: animate_wave(t + 0.1))
    else:
        animate_button.configure(text="Animate")  

# Function to update custom parameters
def update_custom_params():
    current_medium["wavelength"] = wavelength_slider.get()
    current_medium["frequency"] = frequency_slider.get()
    current_medium["speed"] = speed_slider.get()
    current_medium["medium_length"] = length_slider.get()
    update_steady_wave()

# Frame to hold the dropdown and button
control_frame = ctk.CTkFrame(root)
control_frame.pack(side=ctk.TOP, anchor="ne", padx=10, pady=10)

# Dropdown menu to select medium
selected_medium = ctk.StringVar(value="Choose Medium")
dropdown = ctk.CTkOptionMenu(control_frame, variable=selected_medium, values=list(mediums.keys()), command=update_medium)
dropdown.pack(side=ctk.LEFT, padx=10, pady=(0, 10))

# Toggle animation button
animate_button = ctk.CTkButton(control_frame, text="Animate", command=toggle_animation)
animate_button.pack(side=ctk.LEFT, padx=10, pady=(0, 10))

# Frame for sliders
slider_frame = ctk.CTkFrame(root)

# Initialize sliders
wavelength_slider = None
frequency_slider = None
speed_slider = None
length_slider = None

# Function to create a labeled slider
def create_labeled_slider(frame, label_text, from_, to_, number_of_steps, command):
    label_frame = ctk.CTkFrame(frame)
    label_frame.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=5)
    label = ctk.CTkLabel(label_frame, text=label_text, text_color="white", font=("Inter", 12, "bold"))
    label.pack(side=ctk.LEFT, padx=(0, 10))  
    slider = ctk.CTkSlider(label_frame, from_=from_, to=to_, number_of_steps=number_of_steps, command=command)
    slider.set(mediums["Custom"].get(label_text.lower().replace(" ", "_"), 1.0))
    slider.pack(side=ctk.RIGHT, fill=ctk.X, padx=(0, 10)) 
    return slider

# Creating sliders with labels on the left
wavelength_slider = create_labeled_slider(slider_frame, "Wavelength", 0.1, 10, 100, lambda v: update_custom_params())
frequency_slider = create_labeled_slider(slider_frame, "Frequency", 1, 10000, 100, lambda v: update_custom_params())
speed_slider = create_labeled_slider(slider_frame, "Speed (click the Animate button to check the speed of the wave)", 1, 10000, 100, lambda v: update_custom_params())
length_slider = create_labeled_slider(slider_frame, "Medium Length", 1, 20, 100, lambda v: update_custom_params())

# Initialize the simulation with no graph
current_medium = None

# Start the main loop
root.mainloop()
