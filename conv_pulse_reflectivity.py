import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the finite pulse and the reflectivity function
def finite_pulse(length=20):
    t = np.linspace(-1, 1, length)
    pulse = np.exp(-t**2 * 10)
    return pulse

def reflectivity_function(length=100):
    reflectivity = np.zeros(length)
    spikes = [(20, 1), (40, -0.5), (60, 0.8), (80, -0.3)]
    for pos, amp in spikes:
        reflectivity[pos] = amp
    return reflectivity

# Generate the pulse and reflectivity function
# pulse = finite_pulse()
# Ask the user for the pulse width
pulse_width = int(input("Enter the pulse width: "))
pulse = finite_pulse(pulse_width)

reflectivity = reflectivity_function()
convolution_length = len(pulse) + len(reflectivity) - 1

# Set up the figure and axis
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

ax1.set_title('Finite Pulse')
line1, = ax1.plot(np.zeros(convolution_length), lw=2)
ax1.set_xlim(0, convolution_length)
ax1.set_ylim(-1.5, 1.5)

ax2.set_title('Reflectivity Function')
line2, = ax2.plot(np.arange(len(reflectivity)), reflectivity, lw=2)
ax2.set_xlim(0, convolution_length)
ax2.set_ylim(-1.5, 1.5)

ax3.set_title('Convolution Result')
line3, = ax3.plot(np.arange(convolution_length), np.zeros(convolution_length), lw=2)
ax3.set_xlim(0, convolution_length)
ax3.set_ylim(-1.5, 1.5)

# Animation function
def animate(i):
    # Shift the pulse over the reflectivity function
    shifted_pulse = np.zeros(convolution_length)
    shifted_pulse[i:i+len(pulse)] = pulse
    
    # Compute the convolution up to the current frame
    current_conv = np.convolve(pulse[:min(i+1, len(pulse))], reflectivity[:i+1], mode='full')
    
    # Update the plots
    line1.set_ydata(shifted_pulse)
    line3.set_ydata(np.pad(current_conv, (0, convolution_length - len(current_conv)), 'constant'))
    
    return line1, line3,

# Create the animation
ani = animation.FuncAnimation(fig, animate, frames=len(reflectivity), interval=50, blit=True)

# Display the animation
plt.tight_layout()
plt.show()
