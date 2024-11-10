import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from pykalman import KalmanFilter

class RobotPredictor:
    def __init__(self, videoFPS):
        self.fps = videoFPS
        self.location = (0, 0)
        self.otherRobotLocations = []  # list of tuples (x, y) of the other robot

    def predict(self, location, otherRobotLocations, timeStep):
        self.location = location
        self.otherRobotLocations = otherRobotLocations

        if len(self.otherRobotLocations) >= 2:
            predictions = []  # To store predictions for each robot

            for robot_location in self.otherRobotLocations:
                # Prepare the data for Kalman filter for each robot
                kf = KalmanFilter(initial_state_mean=np.array([robot_location[0], robot_location[1], 0, 0]),
                                initial_state_covariance=np.eye(4) * 1000,
                                transition_matrices=np.array([[1, 0, timeStep, 0],
                                                                [0, 1, 0, timeStep],
                                                                [0, 0, 1, 0],
                                                                [0, 0, 0, 1]]),
                                observation_matrices=np.array([[1, 0, 0, 0],
                                                                [0, 1, 0, 0]]))

                # Use only the x and y positions as observations
                measurements = np.array([[loc[0], loc[1]] for loc in self.otherRobotLocations])
                kf = kf.em(measurements, n_iter=10)  # Estimate the parameters
                (filtered_state_means, filtered_state_covariances) = kf.filter(measurements)

                print(filtered_state_means)

                # Ensure the dimensions match for the smooth function
                if filtered_state_means.shape[1] == 4:  # Check if the state has 4 dimensions
                    next_state_mean = kf.smooth(filtered_state_means)[0][-1]
                    predictions.append((next_state_mean[0], next_state_mean[1]))  # Store the predicted (x, y) position
                else:
                    raise ValueError("Filtered state means do not have the expected shape.")

            return predictions  # Return all predictions for each robot

        return None  # Return None if we don't have enough positions to make a prediction

