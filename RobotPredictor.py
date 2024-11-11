import numpy as np

class RobotPredictor:
    def __init__(self, videoFPS):
        self.fps = videoFPS
        self.location = (0, 0)
        self.robotToPredictPos = []  # list of tuples (x, y) of the robot that we want to predict's location

    def able_to_predict(self, importedPositions):
        self.robotToPredictPos = importedPositions

        return True if self.robotToPredictPos else False

    def predict(self, location, otherRobotLocations, timeStep):
        self.robotToPredictPos = otherRobotLocations

        if len(self.robotToPredictPos) >= 2:
            self.location = location
            self.robotToPredictX = [xPositions[0] for xPositions in otherRobotLocations]
            self.robotToPredictY = [xPositions[1] for xPositions in otherRobotLocations]

            self.coefficients = np.polyfit(self.robotToPredictX, self.robotToPredictY, 2)
            self.predictedPosition = self.coefficients[0] * timeStep**2 + self.coefficients[1] * timeStep + self.coefficients[2]

            return self.coefficients, self.predictedPosition
        
        return None  # Return None if we don't have enough positions to make a prediction
        
    def return_xy_values(self):
        return (self.robotToPredictX, self.robotToPredictY)
            

            
        

