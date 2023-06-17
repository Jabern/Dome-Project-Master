import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
import tensorflow as tf
from tabulate import tabulate

# Load the dataset
dataset = pd.read_csv('sample_dataset.csv')

# Separate the features (numerical representations)
features = dataset.iloc[:, 11:]  # Select columns from 'Extent of Damage (Numeric)' onwards

# Convert the data to TensorFlow tensors
X = tf.convert_to_tensor(features.values, dtype=tf.float32)

# Load the trained models
arch_style_model = tf.keras.models.load_model('arch_style_model_updated')
restoration_model = tf.keras.models.load_model('restoration_model_updated')

# Make predictions for architectural style and restoration practices
arch_style_predictions = arch_style_model.predict(X)
restoration_predictions = restoration_model.predict(X)

# Get the ground truth labels from the dataset
ground_truth_arch_style = dataset['Architectural Style (Numeric)']
ground_truth_restoration = dataset['Restoration Practices (Numeric)']

# Convert ground truth values to numpy arrays
ground_truth_arch_style = np.array(ground_truth_arch_style)
ground_truth_restoration = np.array(ground_truth_restoration)

# Flatten the predictions
arch_style_predictions = np.round(arch_style_predictions).flatten()
restoration_predictions = np.round(restoration_predictions).flatten()

# Select a sample of data for printing
sample_size = 10
sample_indices = np.random.choice(len(arch_style_predictions), sample_size, replace=False)

# Create a table to display the predicted and ground truth labels
table_data = []
for idx in sample_indices:
    arch_style_pred_label = arch_style_predictions[idx]
    restoration_pred_label = restoration_predictions[idx]
    ground_truth_arch_style_label = ground_truth_arch_style[idx]
    ground_truth_restoration_label = ground_truth_restoration[idx]

    table_data.append([arch_style_pred_label, restoration_pred_label,
                       ground_truth_arch_style_label, ground_truth_restoration_label])

headers = ["Arch Style (Pred)", "Restoration (Pred)", "Arch Style (GT)", "Restoration (GT)"]
table = tabulate(table_data, headers, tablefmt="prettify")

# Create a Tkinter window
window = tk.Tk()
window.title("Sample Predictions and Ground Truth Labels")

# Create a Tkinter frame to hold the table
frame = ttk.Frame(window, padding="10")
frame.grid(row=0, column=0)

# Create a Tkinter label for the table
label = ttk.Label(frame, text=table, font=("Courier New", 10), justify="left")
label.grid(row=0, column=0)

# Run the Tkinter event loop
window.mainloop()
