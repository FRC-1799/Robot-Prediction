import numpy as np

class RobotPredictor:
    def __init__(self, videoFPS):
        self.self = self
        self.fps = videoFPS

        self.location = (0, 0)
        self.otherRobotLocations = [] # list of tuples (x, y) of the other robot
        self.previous_locations = []  # Store previous locations to calculate velocity
    
    def predict(self, location, otherRobotLocations, timeStep):
        self.location = location
        self.otherRobotLocations = otherRobotLocations

        if len(self.otherRobotLocations) >= 2:

            self.xPoints = np.array([coord[0] for coord in self.otherRobotLocations])
            self.yPoints = np.array([coord[1] for coord in self.otherRobotLocations])

            slope, intercept = np.polyfit(self.xPoints, self.yPoints, 1)
            print(slope, intercept)

            return slope, intercept


        # # How far ahead to predict the other robot's location (in frames)
        # framesToPredict = self.fps * timeStep # timeStep is in seconds

        # if len(self.otherRobotLocations) >= 2:
        #     # Calculate average velocity across all consecutive positions
        #     total_velocity_x = 0
        #     total_velocity_y = 0
        #     num_velocities = 0
            
        #     for i in range(1, len(self.otherRobotLocations)):
        #         current = self.otherRobotLocations[i]
        #         previous = self.otherRobotLocations[i-1]
                
        #         # Add up velocity between each consecutive pair
        #         total_velocity_x += current[0] - previous[0] 
        #         total_velocity_y += current[1] - previous[1]
        #         num_velocities += 1
            
        #     # Calculate average velocity
        #     avg_velocity_x = total_velocity_x / num_velocities
        #     avg_velocity_y = total_velocity_y / num_velocities
            
        #     # Predict future position using the LAST position of the target robot
        #     latest_pos = self.otherRobotLocations[-1]
        #     predicted_x = latest_pos[0] + (avg_velocity_x * framesToPredict)
        #     predicted_y = latest_pos[1] + (avg_velocity_y * framesToPredict)
        #     return (predicted_x, predicted_y)
        
        return None  # Return None if we don't have enough positions to make a prediction
