import unittest
from RobotPredictor import RobotPredictor

class test_predictor(unittest.TestCase):
    def setUp(self):
        self.degree = 2
        self.predictor = RobotPredictor(self.degree)

    def test_able_to_predict(self):
        ableToPredict = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]
        notAbleToPredict = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]

        self.assertEqual(self.predictor.able_to_predict(ableToPredict), True)
        self.assertEqual(self.predictor.able_to_predict(notAbleToPredict), False)

if __name__ == "__main__":
    unittest.main()