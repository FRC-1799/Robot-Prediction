import numpy as np
from numpy import RankWarning
import matplotlib.pyplot as plt
import math

class RobotPredictor:
    def __init__(self, videoFPS):
        self.fps = videoFPS
        self.location = (0, 0)
        self.robotToPredictPos = []  # list of tuples (x, y) of the robot that we want to predict's location

    def able_to_predict(self, importedPositions):
        self.robotToPredictPos = importedPositions

        if self.robotToPredictPos and len(importedPositions) >= 2:
            moving = False if self.robotToPredictPos[-1][0] - self.robotToPredictPos[-2][0] == 0 or self.robotToPredictPos[-1][1] - self.robotToPredictPos[-2][1] == 0 else True
            return True if moving else False
        else:
            return False
            

    def distance_formula(self, x1, x2, y1, y2):
        return math.sqrt((x2-x1)**2 + (y2-y1)**2)

    def predict(self, location, otherRobotLocations, timeStep, timePassed):
        self.robotToPredictPos = otherRobotLocations

        self.location = location
        self.robotToPredictX = [xPositions[0] for xPositions in otherRobotLocations]
        self.robotToPredictY = [yPositions[1] for yPositions in otherRobotLocations]

        self.coefficients = np.polyfit(self.robotToPredictX, self.robotToPredictY, 2)


        currentXPosition = self.robotToPredictX[-1]
        lastXPosition = self.robotToPredictX[-2]
        currentYPosition = self.robotToPredictY[-1]
        lastYPosition = self.robotToPredictY[-2]
        

        distanceBetweenTheTwoVariables = self.distance_formula(lastXPosition, currentXPosition, lastYPosition, currentYPosition)

        # print(self.coefficients)

        divisor = timePassed / timeStep

        predictedXPostition = divisor * distanceBetweenTheTwoVariables

        velocityX = currentXPosition - lastXPosition
        accelerationInXDirection = velocityX / timePassed

        # Calculate average velocity

        predictedXPostition = currentXPosition + velocityX * timeStep + (1/2 * accelerationInXDirection) * timeStep**2

        # predictedYPosition = self.coefficients[0] * predictedXPostition**2 + self.coefficients[1] * predictedXPostition + self.coefficients[2]

        predictedYPosition = self.coefficients[0] * predictedXPostition**2 + self.coefficients[1] * predictedXPostition + self.coefficients[2]

        self.predictedPosition = (predictedXPostition, predictedYPosition)

        return (self.coefficients, self.predictedPosition)

        # return None  # Return None if we don't have enough positions to make a prediction

    def return_xy_values(self):
        return (self.robotToPredictX, self.robotToPredictY)
