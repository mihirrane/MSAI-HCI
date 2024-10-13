from flask import Flask, request, jsonify
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Sample data for training
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([50, 60, 70, 80, 90])

# Train a linear regression model
model = LinearRegression()
model.fit(X, y)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    study_time = float(data['study_time'])
    predicted_completion = model.predict(np.array([[study_time]]))[0]
    return jsonify({'completion_percentage': predicted_completion})

if __name__ == '__main__':
    app.run(debug=True)
