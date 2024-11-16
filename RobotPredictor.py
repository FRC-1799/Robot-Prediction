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

