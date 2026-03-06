import pickle
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load the model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Load the scaler
scaler = MinMaxScaler()
scaler.fit([[0, 0, 0, 0]])  # Initialize with dummy data

def predict_stock_price(open_price, high_price, low_price, volume):
    data = np.array([open_price, high_price, low_price, volume]).reshape(1, -1)
    data_scaled = scaler.transform(data)
    prediction = model.predict(data_scaled)
    return prediction[0]
