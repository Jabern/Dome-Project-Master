import librosa
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pygame
import sys
import ctypes
import view_engine
import threading

# Create the Tkinter window
window = Tk()
window.title('Music Analysis')

# Function to handle the window close event
def on_closing():
    stop_visualizer()
    stop_3d_viewer()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

# Set the window attributes for a maximized but unresizable window
window.resizable(False, False)  # Disable window resizing

# Maximize the window
window.state('zoomed')

# Create a button to load a music file
def load_music_file():
    global audio_path, audio, sr, tempo, mfccs, contrast

    # Open a file dialog to select a music file
    filepath = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])

    # Check if a file is selected
    if filepath:
        # Load the music file
        audio_path = filepath
        audio, sr = librosa.load(audio_path)
        tempo, _ = librosa.beat.beat_track(y=audio, sr=sr)
        mfccs = librosa.feature.mfcc(y=audio, sr=sr)
        contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)

        # Update the file label
        update_file_label()

        # Update the plots
        update_plots()

        # Reload the music in the music player
        pygame.mixer.music.load(audio_path)

# Function to update the plots
def update_plots():
    # Clear the existing plots
    for ax in axs.flatten():
        ax.clear()

    # Plot the waveform
    waveform_plot, = axs[0].plot(audio)
    axs[0].set_title('Waveform')

    # Plot the spectrogram
    spectrogram_plot = axs[1].specgram(audio, NFFT=2048, Fs=2, Fc=0, noverlap=128, cmap='inferno', sides='default', mode='default', scale='dB')
    axs[1].set_title('Spectrogram')

    # Plot the MFCCs
    mfccs_plot = librosa.display.specshow(mfccs, sr=sr, x_axis='time', cmap='viridis', ax=axs[2])
    axs[2].set_title('MFCCs')
    axs[2].set_xlabel('Time')
    axs[2].set_ylabel('MFCC')

    # Adjust spacing between subplots
    plt.tight_layout()

    # Update the canvas
    canvas.draw()

# Function to update the audio attributes
def update_audio_attributes():
    # Update the audio duration
    audio_duration = librosa.get_duration(y=audio, sr=sr)

# Create a frame for the file loader and player
file_loader_frame = Frame(window)
file_loader_frame.pack(padx=10, pady=10)

# Create a file loader button
load_button = Button(file_loader_frame, text="Load Music File", command=load_music_file)
load_button.pack(side=LEFT, padx=10)

# Create a label to display the loaded file path
file_label = Label(file_loader_frame, text="No file loaded")
file_label.pack(side=LEFT)

# Load the default music file
audio_path = 'test.mp3'
audio, sr = librosa.load(audio_path)
tempo, _ = librosa.beat.beat_track(y=audio, sr=sr)
mfccs = librosa.feature.mfcc(y=audio, sr=sr)
contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)

# Create a frame for the plot on the left side
plot_frame = Frame(window)
plot_frame.pack(side=LEFT, padx=10, pady=10)

# Create a figure and subplots
fig, axs = plt.subplots(3, 1, figsize=(8, 10))

# Create a canvas for embedding the plots in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.draw()
canvas.get_tk_widget().pack()

# Close the extra plot window
plt.close()

# Create a frame for the music player and visualizer on the right side
player_frame = Frame(window)
player_frame.pack(side=RIGHT, padx=10, pady=10)

# Initialize the pygame mixer
pygame.mixer.init()
pygame.mixer.music.load(audio_path)

# Get the duration of the audio in seconds
audio_duration = librosa.get_duration(y=audio, sr=sr)

# Define the visualization parameters
num_bars = 20  # Number of bars in the visualizer
bar_width = 10  # Width of each bar
bar_height_scale = 100  # Scale factor for bar height

# Create a canvas for the music visualizer
visualizer_canvas = Canvas(player_frame, width=num_bars * bar_width, height=200, bg='white')
visualizer_canvas.pack()

# Create play, pause, and reset buttons in the player frame
is_playing = False  # Variable to track if music is currently playing
is_paused = False  # Variable to track if music is currently paused

def play_music():
    global is_playing
    global is_paused

    if not is_playing and not is_paused:
        pygame.mixer.music.play()
        is_playing = True
    elif is_paused:
        pygame.mixer.music.unpause()
        is_paused = False

def pause_music():
    global is_playing
    if is_playing:
        pygame.mixer.music.pause()
        global is_paused
        is_paused = True
    else:
        is_playing = False

def reset_music():
    pygame.mixer.music.stop()
    pygame.mixer.music.rewind()
    pygame.mixer.music.play()
    global is_playing
    is_playing = True
    global is_paused
    is_paused = False

play_button = Button(player_frame, text="Play", command=play_music)
play_button.pack(pady=10)

pause_button = Button(player_frame, text="Pause", command=pause_music)
pause_button.pack(pady=10)

reset_button = Button(player_frame, text="Reset", command=reset_music)
reset_button.pack(pady=10)

# Function to update the music visualizer
def update_visualizer():
    if not window.winfo_exists():
        return  # Stop updating the visualizer if the window is closed

    # Get the current time position of the music
    current_time = pygame.mixer.music.get_pos() / 1000  # Convert to seconds

    # Calculate the index of the current time position in the audio
    audio_index = int(current_time * sr)

    # Calculate the index of the audio segment for visualization
    segment_index = audio_index // sr

    # Check if there is enough audio remaining for the visualization segment
    if segment_index >= mfccs.shape[1]:
        return  # Stop updating the visualizer

    # Get the MFCCs for the visualization segment
    segment_mfccs = mfccs[:, segment_index]

    # Clear the visualizer canvas
    visualizer_canvas.delete("all")

    # Calculate the bar heights based on the MFCC values
    bar_heights = segment_mfccs * bar_height_scale

    # Draw the bars in the visualizer canvas
    for i, height in enumerate(bar_heights):
        x = i * bar_width
        y = 200 - height
        visualizer_canvas.create_rectangle(x, y, x + bar_width, 200, fill='blue')

    # Schedule the next update of the visualizer
    window.after(100, update_visualizer)

# Start updating the music visualizer
update_visualizer()

# Create a frame for the 3D viewer button
button_frame = Frame(window)
button_frame.pack(pady=10)

# Function to stop the music visualizer
def stop_visualizer():
    global visualizer_thread

    if visualizer_thread is not None and visualizer_thread.is_alive():
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(visualizer_thread.ident), ctypes.py_object(SystemExit))
        visualizer_thread.join()

# Function to update the file label
def update_file_label():
    file_label.config(text="File: " + audio_path)

# Function to start the 3D viewer thread
viewer_thread = None

def start_3d_viewer():
    global viewer_thread

    if viewer_thread is not None and viewer_thread.is_alive():
        stop_3d_viewer()

    viewer_thread = threading.Thread(target=view_engine.run_viewer)
    viewer_thread.start()

def stop_3d_viewer():
    global viewer_thread

    if viewer_thread is not None and viewer_thread.is_alive():
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(viewer_thread.ident), ctypes.py_object(SystemExit))
        viewer_thread.join()

# Create a button to open the 3D viewer
view_button = Button(button_frame, text="3D View", command=start_3d_viewer)
view_button.pack(padx=10)

# Start the Tkinter event loop
window.mainloop()
