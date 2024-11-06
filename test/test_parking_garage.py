from datetime import datetime
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock
from mock import GPIO
from mock.SDL_DS3231 import SDL_DS3231
from src.parking_garage import ParkingGarage
from src.parking_garage import ParkingGarageError

class TestParkingGarage(TestCase):

    @patch.object(GPIO, "input")
    def test_check_occupancy(self, mock_distance_sensor: Mock):
        mock_distance_sensor.return_value = GPIO.HIGH

        system = ParkingGarage()
        is_occupied = system.check_occupancy(system.INFRARED_PIN1)
        self.assertTrue(is_occupied)
        
    def test_check_occupancy_throws_error_if_not_correct_sensor(self):
        sut = ParkingGarage()
        with self.assertRaises(ParkingGarageError):
            sut.check_occupancy(sut.LED_PIN)
        
        


