import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

# Check available GPUs and print GPU information
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
        print("GPU:", gpu)
else:
    print("No GPU available. Please make sure you have TensorFlow GPU installed and configured correctly.")

# Load the dataset
dataset = pd.read_csv('sample_dataset.csv')

# Separate the features (numerical representations) and target variables
features = dataset.iloc[:, 11:]  # Select columns from 'Extent of Damage (Numeric)' onwards
target_arch_style = dataset['Architectural Style (Numeric)']
target_restoration = dataset['Restoration Practices (Numeric)']

# Split the dataset into training and testing sets
X_train, X_test, y_train_arch_style, y_test_arch_style, y_train_restoration, y_test_restoration = train_test_split(
    features, target_arch_style, target_restoration, test_size=0.2, random_state=126)

# Convert the data to TensorFlow tensors
X_train = tf.convert_to_tensor(X_train.values, dtype=tf.float32)
X_test = tf.convert_to_tensor(X_test.values, dtype=tf.float32)
y_train_arch_style = tf.convert_to_tensor(y_train_arch_style.values, dtype=tf.float32)
y_test_arch_style = tf.convert_to_tensor(y_test_arch_style.values, dtype=tf.float32)
y_train_restoration = tf.convert_to_tensor(y_train_restoration.values, dtype=tf.float32)
y_test_restoration = tf.convert_to_tensor(y_test_restoration.values, dtype=tf.float32)

# Load the pre-trained models
arch_style_model = tf.keras.models.load_model('arch_style_model')
restoration_model = tf.keras.models.load_model('restoration_model')

# Compile the models
arch_style_model.compile(optimizer='adam', loss='mean_squared_error')
restoration_model.compile(optimizer='adam', loss='mean_squared_error')

# Train the models for additional epochs
arch_style_history = arch_style_model.fit(X_train, y_train_arch_style, epochs=50, verbose=0)
restoration_history = restoration_model.fit(X_train, y_train_restoration, epochs=50, verbose=0)

# Make predictions for architectural style and restoration practices on the test set
arch_style_predictions = arch_style_model.predict(X_test)
restoration_predictions = restoration_model.predict(X_test)

# Output the predictions
print("Architectural Style Predictions:")
print(arch_style_predictions)
print()
print("Restoration Practices Predictions:")
print(restoration_predictions)

# Plot the training loss for architectural style prediction
plt.figure(figsize=(8, 6))
plt.plot(arch_style_history.history['loss'])
plt.title('Architectural Style Model - Training Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.show()

# Plot the training loss for restoration practices prediction
plt.figure(figsize=(8, 6))
plt.plot(restoration_history.history['loss'])
plt.title('Restoration Practices Model - Training Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.show()

# Save the updated trained models
arch_style_model.save('arch_style_model_updated')
restoration_model.save('restoration_model_updated')
