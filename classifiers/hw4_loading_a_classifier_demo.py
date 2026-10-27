# import numpy as np
import joblib
import sys
import os

sys.path.append(os.path.abspath(".."))

from DirtDistribution import DirtDistribution

# Load both model + encoder
ai_model, encoder_labels = joblib.load("model.joblib")

print(f"Show the number of inputs expected by this model: {ai_model.n_features_in_}")

# Fake input: 15 features
# sample = np.random.rand(1, 15)

dist = DirtDistribution.random_real()
print(f"Actual distribution: {dist.name}")

sample_list = [dist.generate_distribution_odds(room_count=15)]

# Predict
prediction = ai_model.predict(sample_list)

# Decode
label = encoder_labels.inverse_transform(prediction)

print("Prediction:", label[0])
