
import numpy as np
import math

class RobotPredictor:
    """Class that allows the prediction of robot positions based on their previous positions using numpy.polyfit and the second equation of motion"""
    
    def __init__(self):
        self.robotToPredictPos = []  # list of tuples (x, y) of the robot that we want to predict's location

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
    
    def find_x_position(self):
        """Uses the second equation of motion to predict the future X position of the robot"""

        distanceBetweenTheTwoVariables = self.distance_formula(self.lastXPosition, self.currentXPosition, self.lastYPosition, self.currentYPosition)
        divisor = self.timePassed / self.timeStep # only used to calculate the predictedXPostition
        predictedXPostition = divisor * distanceBetweenTheTwoVariables
        velocityX = self.currentXPosition - self.lastXPosition
        accelerationInXDirection = velocityX / self.timePassed

        predictedXPostition = self.currentXPosition + velocityX * self.timeStep + (1/2 * accelerationInXDirection) * self.timeStep**2
        return predictedXPostition
    
    def find_y_position(self):
        predictedYPosition = self.coefficients[0] * self.predictedXPosition**2 + self.coefficients[1] * self.predictedXPosition + self.coefficients[2]

        return predictedYPosition

    def predict(self, otherRobotLocations, timeStep, timePassed):
        """Predicts the robot's future locations based on its previous locations"""

        self.timeStep = timeStep
        self.timePassed = timePassed

        # Is a binomial. You must chagne the way predictedYPosition is calculated if you change the degree
        self.degree = 2 
        self.robotToPredictPos = otherRobotLocations
        self.robotToPredictX = [xPositions[0] for xPositions in otherRobotLocations]
        self.robotToPredictY = [yPositions[1] for yPositions in otherRobotLocations]

        # Uses a second degree polynomial because robot mostly moves in a parabola
        self.coefficients = np.polyfit(self.robotToPredictX, self.robotToPredictY, self.degree)

        self.currentXPosition = self.robotToPredictX[-1]
        self.lastXPosition = self.robotToPredictX[-2]
        self.currentYPosition = self.robotToPredictY[-1]
        self.lastYPosition = self.robotToPredictY[-2]

        # Main equation of Kinematics. We can't find the X position without using some form of velocity calculation, so this equation serves that purpose
        self.predictedXPosition = self.find_x_position()
        self.predictedYPosition = self.find_y_position()
        predictedPosition = (self.predictedXPosition, self.predictedYPosition)

        return (self.coefficients, predictedPosition)

    def return_xy_values(self):
        return (self.robotToPredictX, self.robotToPredictY)
