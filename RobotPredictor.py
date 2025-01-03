
import numpy as np
import math

class RobotPredictor:
    """
    Class that allows the prediction of robot positions based on their previous positions using numpy.polyfit and the second equation of motion
    """
    
    def __init__(self):
        self.robotToPredictPos = []  # list of tuples (x, y) of the robot that we want to predict's location

    def able_to_predict(self, importedPositions: list[tuple[int, int]]) -> bool:
        """
        Determines if a robot's future positions are able to be predicted

        Parameters:
        Imported Positions (list of tuples): Last positions that we have collected from the other robot

        Returns:
        bool: True if we are able to predict the robot, False if we cannot.
        """

        self.robotToPredictPos = importedPositions

        # Checks predictability to not have any errors when predicting
        if self.robotToPredictPos and len(importedPositions) >= 2:
            moving = False if self.robotToPredictPos[-1][0] - self.robotToPredictPos[-2][0] == 0 or self.robotToPredictPos[-1][1] - self.robotToPredictPos[-2][1] == 0 else True
            return True if moving else False
        else:
            return False

    def distance_formula(self, x1: int, x2: int, y1: int, y2: int) -> float:
        """
        Calculates the distance between 2 points in a 2 dimensional plane
        
        Parameters:
        x1, x2, y1, y2 (ints): X and Y position of the robot's last position vs. the X and Y position that they are at now

        Returns:
        float: The distance (hypotenuse length) between the 2 points
        """

        return math.sqrt((x2-x1)**2 + (y2-y1)**2)
    
    def find_x_position(self) -> float:
        """
        Uses the second equation of motion to predict the future X position of the robot

        Returns:
        float: Decimal value of the X position based on the previous X positions
        """

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

    def predict(self, otherRobotLocations: list[tuple[float, float]], timeStep: float, timePassed: float) -> tuple[list[float], tuple[float, float]]:
        """
        Predicts the robot's future locations based on its previous locations
        
        Parameters:
        otherRobotLocations (list[tuple[float, float]]): list of the robot's previous locations. For example [(24.3, 54.3), (48.6, 108.6)]
        timeStep (float): How far ahead you want the prediction to be
        timePassed (float): How much time has passed since the last prediction

        Returns:
        tuple[list[float], tuple[float, float]]: Tuple containing the coefficients of the parabola and the predicted x and y locations based on that parabola
        """

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