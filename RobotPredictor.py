
import numpy as np
import math

class RobotPredictor:
    """Class that allows the prediction of robot positions based on their previous positions using numpy.polyfit and a kinematic equation"""
    def __init__(self, degree):
        self.location = (0, 0)
        self.robotToPredictPos = []  # list of tuples (x, y) of the robot that we want to predict's location
        self.degree = degree

    def able_to_predict(self, importedPositions):
        """Determines if a robot's future positions are able to be predicted"""

        self.robotToPredictPos = importedPositions

        # Checks predictability to not have any errors when predicting
        if self.robotToPredictPos and len(importedPositions) >= 2:
            moving = False if self.robotToPredictPos[-1][0] - self.robotToPredictPos[-2][0] == 0 or self.robotToPredictPos[-1][1] - self.robotToPredictPos[-2][1] == 0 else True
            return True if moving else False
        else:
            return False
            

    def distance_formula(self, x1, x2, y1, y2):
        """Calculates the distance between 4 points in a 2 dimensional plane"""

        return math.sqrt((x2-x1)**2 + (y2-y1)**2)

    def predict(self, otherRobotLocations, timeStep, timePassed):
        """Predicts the robot's future locations based on its previous locations"""

        self.robotToPredictPos = otherRobotLocations

        self.robotToPredictX = [xPositions[0] for xPositions in otherRobotLocations]
        self.robotToPredictY = [yPositions[1] for yPositions in otherRobotLocations]

        # Uses a second degree polynomial because robot mostly moves in a parabola
        self.coefficients = np.polyfit(self.robotToPredictX, self.robotToPredictY, self.degree)

        currentXPosition = self.robotToPredictX[-1]
        lastXPosition = self.robotToPredictX[-2]

        currentYPosition = self.robotToPredictY[-1]
        lastYPosition = self.robotToPredictY[-2]

        distanceBetweenTheTwoVariables = self.distance_formula(lastXPosition, currentXPosition, lastYPosition, currentYPosition)
        divisor = timePassed / timeStep # only used to calculate the predictedXPostition
        predictedXPostition = divisor * distanceBetweenTheTwoVariables
        velocityX = currentXPosition - lastXPosition
        accelerationInXDirection = velocityX / timePassed

        # Main equation of Kinematics. We can't find the X position without using some form of velocity calculation, so this equation serves that purpose
        predictedXPostition = currentXPosition + velocityX * timeStep + (1/2 * accelerationInXDirection) * timeStep**2

        predictedYPosition = self.coefficients[0] * predictedXPostition**2 + self.coefficients[1] * predictedXPostition + self.coefficients[2]

        self.predictedPosition = (predictedXPostition, predictedYPosition)

        return (self.coefficients, self.predictedPosition)

    def return_xy_values(self):
        return (self.robotToPredictX, self.robotToPredictY)
