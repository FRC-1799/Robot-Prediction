import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

class RobotPredictor:
    def __init__(self, videoFPS):
        self.fps = videoFPS
        self.location = (0, 0)
        self.otherRobotLocations = []  # list of tuples (x, y) of the other robot

    def predict(self, location, otherRobotLocations, timeStep):
        self.location = location
        self.otherRobotLocations = otherRobotLocations

        if len(self.otherRobotLocations) >= 2:
            # Prepare the data for polynomial regression
            x_points = np.array([coord[0] for coord in self.otherRobotLocations]).reshape(-1, 1)
            y_points = np.array([coord[1] for coord in self.otherRobotLocations]).reshape(-1, 1)

            # Create polynomial features
            degree = 6  # You can adjust the degree as needed
            poly_features = PolynomialFeatures(degree=degree)
            x_poly = poly_features.fit_transform(x_points)

            # Fit the polynomial regression model
            model = LinearRegression()
            model.fit(x_poly, y_points)

            # Predict the next position based on the last x value
            last_x = x_points[-1][0]
            next_x = last_x + timeStep  # Predicting the next position after timeStep
            next_x_poly = poly_features.transform(np.array([[next_x]]))  # Transform to polynomial features
            predicted_y = model.predict(next_x_poly)

            return next_x, predicted_y[0][0]  # Return the predicted (x, y) position

        return None  # Return None if we don't have enough positions to make a prediction
