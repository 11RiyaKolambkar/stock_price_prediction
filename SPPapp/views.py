from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import StockPredictionForm
from .models import StockPrediction
import pickle
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from django.utils.dateformat import format

# Load the model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Initialize the scaler with dummy data
scaler = MinMaxScaler()
scaler.fit([[0, 0, 0, 0]])

def logout_view(request):
    logout(request)
    return redirect('home')
def results_view(request):
    # Example data retrieval, adjust as per your actual implementation
    old_predictions = StockPrediction.objects.all()
    
    dates = [pred.date.strftime('%Y-%m-%d') for pred in old_predictions]
    predicted_prices = [pred.predicted_price for pred in old_predictions]

    return render(request, 'result.html', {
        'dates': dates,
        'predicted_prices': predicted_prices,
        'old_predictions': old_predictions,
    })

def home(request):
    # Fetch old predictions
    old_predictions = StockPrediction.objects.all()

    # Extract data for the plot
    dates = [pred.date.strftime('%Y-%m-%d %H:%M') for pred in old_predictions]
    predicted_prices = [pred.predicted_price for pred in old_predictions]

    return render(request, 'home.html', {
        'dates': dates,
        'predicted_prices': predicted_prices
    })

def predict_stock_price(open_price, high_price, low_price, volume):
    data = np.array([open_price, high_price, low_price, volume]).reshape(1, -1)
    data_scaled = scaler.transform(data)
    prediction = model.predict(data_scaled)
    return prediction[0]

@login_required
def predict_view(request):
    if request.method == 'POST':
        form = StockPredictionForm(request.POST)
        if form.is_valid():
            # Extract form data
            open_price = form.cleaned_data['open_price']
            high_price = form.cleaned_data['high_price']
            low_price = form.cleaned_data['low_price']
            volume = form.cleaned_data['volume']

            # Make prediction
            prediction = predict_stock_price(open_price, high_price, low_price, volume)
            
            # Save the prediction to the database
            StockPrediction.objects.create(
                user=request.user,
                open_price=open_price,
                high_price=high_price,
                low_price=low_price,
                volume=volume,
                predicted_price=prediction
            )
            
            # Fetch old predictions
            old_predictions = StockPrediction.objects.filter(user=request.user)

            # Extract data for the plot
            dates = [format(pred.date, 'Y-m-d %H:%M') for pred in old_predictions]
            predicted_prices = [pred.predicted_price for pred in old_predictions]
            
            # Render the result template with prediction and historical data
            return render(request, 'result.html', {
                'prediction': prediction,
                'old_predictions': old_predictions,
                'dates': dates,
                'predicted_prices': predicted_prices
            })
    else:
        form = StockPredictionForm()
    
    # Fetch old predictions for initial render
    old_predictions = StockPrediction.objects.filter(user=request.user)
    dates = [format(pred.date, 'Y-m-d %H:%M') for pred in old_predictions]
    predicted_prices = [pred.predicted_price for pred in old_predictions]
    
    return render(request, 'predict.html', {'form': form, 'dates': dates, 'predicted_prices': predicted_prices})

@login_required
def prediction_history(request):
    predictions = StockPrediction.objects.filter(user=request.user)
    
    # Extract data for the plot
    dates = [format(pred.date, 'Y-m-d %H:%M') for pred in predictions]
    predicted_prices = [pred.predicted_price for pred in predictions]
    
    return render(request, 'history.html', {
        'predictions': predictions,
        'dates': dates,
        'predicted_prices': predicted_prices
    })

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})