import unittest
from RobotPredictor import RobotPredictor

class test_predictor(unittest.TestCase):
    def setUp(self):
        self.predictor = RobotPredictor()

    def test_able_to_predict(self):
        ableToPredict = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]
        notAbleToPredict = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]

        self.assertEqual(self.predictor.able_to_predict(ableToPredict), True)
        self.assertEqual(self.predictor.able_to_predict(notAbleToPredict), False)

    def test_distance_formula(self):
        test_cases = [
            ((0, 0), (3, 4), 5.0),  # Expected distance is 5.0
            ((1, 1), (4, 5), 5.0),  # Expected distance is 5.0
            ((0, 0), (0, 0), 0.0),  # Expected distance is 0.0
            ((-1, -1), (1, 1), 2.8284271247461903),  # Expected distance is approximately 2.8284271247461903
        ]

        for ((x1, y1), (x2, y2), expected_distance) in test_cases:
            with self.subTest(x1=x1, y1=y1, x2=x2, y2=y2, expected_distance=expected_distance):
                self.assertAlmostEqual(self.predictor.distance_formula(x1, x2, y1, y2), expected_distance)

    def test_find_x_position(self):
        # Set up the necessary attributes for the RobotPredictor instance
        self.predictor.currentXPosition = 10
        self.predictor.lastXPosition = 5
        self.predictor.currentYPosition = 10 
        self.predictor.lastYPosition = 5     
        self.predictor.timeStep = 1
        self.predictor.timePassed = 2

        # Calculate the expected predicted X position
        expected_position = self.predictor.currentXPosition + (self.predictor.currentXPosition - self.predictor.lastXPosition) * self.predictor.timeStep + (1/2 * ((self.predictor.currentXPosition - self.predictor.lastXPosition) / self.predictor.timePassed)) * self.predictor.timeStep**2

        # Assert that the predicted position matches the expected position
        self.assertAlmostEqual(self.predictor.find_x_position(), expected_position)

    def test_find_y_position(self):
        # Set up the necessary attributes for the RobotPredictor instance
        self.predictor.currentXPosition = 10
        self.predictor.lastXPosition = 5
        self.predictor.currentYPosition = 10 
        self.predictor.lastYPosition = 5     
        self.predictor.timeStep = 1
        self.predictor.timePassed = 2
        self.predictor.coefficients = [0.5, 1, 2]  # Example coefficients for a parabola

        # Calculate the predicted X position first
        self.predictor.predictedXPosition = self.predictor.find_x_position()  # Set predictedXPosition

        # Calculate the expected predicted Y position
        expected_position = self.predictor.coefficients[0] * self.predictor.predictedXPosition**2 + self.predictor.coefficients[1] * self.predictor.predictedXPosition + self.predictor.coefficients[2]

        # Assert that the predicted position matches the expected position
        self.assertAlmostEqual(self.predictor.find_y_position(), expected_position)

if __name__ == "__main__":
    unittest.main()