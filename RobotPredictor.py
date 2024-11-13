import numpy as np
import matplotlib.pyplot as plt

class RobotPredictor:
    def __init__(self, videoFPS):
        self.fps = videoFPS
        self.location = (0, 0)
        self.robotToPredictPos = []  # list of tuples (x, y) of the robot that we want to predict's location

    def able_to_predict(self, importedPositions):
        self.robotToPredictPos = importedPositions
        return True if self.robotToPredictPos else False

    def slope(self, x1, x2, y1, y2):
        return (y1 - y1) / (x2 - x1)

    def predict(self, location, otherRobotLocations, timeStep, timePassed):
        self.robotToPredictPos = otherRobotLocations

        if len(self.robotToPredictPos) >= 2:
            self.location = location
            self.robotToPredictX = [xPositions[0] for xPositions in otherRobotLocations]
            self.robotToPredictY = [yPositions[1] for yPositions in otherRobotLocations]


            self.coefficients = np.polyfit(self.robotToPredictX, self.robotToPredictY, 2)
            xVelocity = (self.robotToPredictX[-1] - self.robotToPredictX[-2]) / timePassed
            predictedXPostition = xVelocity * timeStep
            predictedYPosition = self.coefficients[0] * predictedXPostition**2 + self.coefficients[1] * predictedXPostition + self.coefficients[2]

            print(predictedXPostition)

            self.predictedPosition = (predictedXPostition, predictedYPosition)

            return (self.coefficients, self.predictedPosition)

        return None  # Return None if we don't have enough positions to make a prediction

    def return_xy_values(self):
        return (self.robotToPredictX, self.robotToPredictY)

    def plot_graph(self):
        """
        Plots the actual and predicted positions of the robot.
        """
        if not self.robotToPredictPos:
            print("No data available to plot.")
            return

        # Get the actual x and y positions of the robot
        actualX, actualY = self.return_xy_values()

        # Plot the actual positions
        plt.plot(actualX, actualY, label="Actual Path", color="blue", marker="o")

        # If prediction exists, plot the predicted path
        if hasattr(self, 'predictedPosition'):
            predictedX = self.predictedPosition[0]
            predictedY = self.predictedPosition[1]
            plt.scatter(predictedX, predictedY, color="red", label="Predicted Position")

            # Plot the trajectory predicted by the polynomial fit (if available)
            x_vals = np.linspace(min(actualX), max(actualX), 100)
            y_vals = np.polyval(self.coefficients, x_vals)
            plt.plot(x_vals, y_vals, label="Predicted Trajectory", color="green", linestyle="--")

        plt.title("Robot Path Prediction")
        plt.xlabel("X Position")
        plt.ylabel("Y Position")
        plt.legend()
        plt.grid(True)
        plt.show()
