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

    @patch.object(GPIO, "input")
    def test_get_number_occupied_spots(self, mock_distance_sensor: Mock):
        mock_distance_sensor.side_effect = [GPIO.HIGH, GPIO.HIGH, GPIO.LOW]

        sut = ParkingGarage()
        occupied_spots = sut.get_number_occupied_spots()
        self.assertEqual(2, occupied_spots)
    
    @patch.object(SDL_DS3231, "read_datetime")
    def test_calculate_parking_fee_weekday(self, mock_rtc: Mock):
        entry_time = datetime(2024, 11, 4, 12, 30) # Monday
        exit_time = datetime(2024, 11, 4, 15, 24)
        mock_rtc.return_value = exit_time

        sut = ParkingGarage()
        parking_fee = sut.calculate_parking_fee(entry_time)
        self.assertEqual(7.5, parking_fee)

    
    @patch.object(SDL_DS3231, "read_datetime")
    def test_calculate_parking_fee_weekend(self, mock_rtc: Mock):
        entry_time = datetime(2024, 11, 3, 10, 15) # Saturday
        exit_time = datetime(2024, 11, 3, 18, 12)
        mock_rtc.return_value = exit_time

        sut = ParkingGarage()
        parking_fee = sut.calculate_parking_fee(entry_time)
        self.assertEqual(25, parking_fee)

    @patch.object(ParkingGarage, "change_servo_angle")
    def test_open_garage_door(self, mock_servo: Mock):
        sut = ParkingGarage()
        sut.open_garage_door()
        mock_servo.assert_called_with(12) # indirect outputs
        self.assertTrue(sut.door_open) # direct outputs

    @patch.object(ParkingGarage, "change_servo_angle")
    def test_close_garage_door(self, mock_servo: Mock):
        sut = ParkingGarage()
        sut.close_garage_door()
        mock_servo.assert_called_with(0) # indirect outputs
        self.assertFalse(sut.door_open) # direct outputs

    @patch.object(GPIO, "output")
    def test_turn_on_red_light(self, mock_light: Mock):
        sut = ParkingGarage()
        sut.turn_on_red_light()
        mock_light.assert_called_with(sut.LED_PIN, True)
        self.assertTrue(sut.red_light_on)
    

    @patch.object(GPIO, "output")
    def test_turn_off_red_light(self, mock_light: Mock):
        sut = ParkingGarage()
        sut.turn_off_red_light()
        mock_light.assert_called_with(sut.LED_PIN, False)
        self.assertFalse(sut.red_light_on)
