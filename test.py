import unittest
from unittest.mock import MagicMock, patch
from ShiftSchedulerApp import messagebox


class Calculator:
    def __init__(self):
        self.max_hours_entry = MagicMock()
        self.bonus_entry = MagicMock()

    def calculate(self):
        try:
            
            max_hours_per_week = float(self.max_hours_entry.get())
            bonus_per_hour = float(self.bonus_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Maximum hours and bonus must be numbers.")
            return

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    @patch('tkinter.messagebox.showerror')
    def test_valid_input(self, mock_showerror):
        self.calculator.max_hours_entry.get.return_value = '40'
        self.calculator.bonus_entry.get.return_value = '10.5'
        
        self.calculator.calculate()
        mock_showerror.assert_not_called() 

    @patch('tkinter.messagebox.showerror')
    def test_invalid_max_hours(self, mock_showerror):
    
        self.calculator.max_hours_entry.get.return_value = 'invalid'
        self.calculator.bonus_entry.get.return_value = '10.5'
        
    
        self.calculator.calculate()
        
        mock_showerror.assert_called_once_with("Input Error", "Maximum hours and bonus must be numbers.")

    @patch('tkinter.messagebox.showerror')
    def test_invalid_bonus(self, mock_showerror):
        self.calculator.max_hours_entry.get.return_value = '40'
        self.calculator.bonus_entry.get.return_value = 'invalid'
        self.calculator.calculate()
        mock_showerror.assert_called_once_with("Input Error", "Maximum hours and bonus must be numbers.")

if __name__ == '__main__':
    unittest.main()

