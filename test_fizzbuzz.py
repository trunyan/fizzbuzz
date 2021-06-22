import unittest
import fizzbuzz


class TestFizzBuzz(unittest.TestCase):

    def setUp(self):
        self.fizzbuzz_standard_input = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']

    def test_fizzbuzz_transformation_1(self):
        expected_output = '1 2 fizz 4 buzz fizz 7 8 fizz buzz 11 fizz 13 14 fizzbuzz 16 17 fizz 19 buzz'
        output = fizzbuzz.fizz_buzz_output(self.fizzbuzz_standard_input)

        self.assertEqual(output, expected_output)

    def test_fizzbuzz_transformation_2(self):
        expected_output = '1 2 lucky 4 buzz fizz 7 8 fizz buzz 11 fizz lucky 14 fizzbuzz 16 17 fizz 19 buzz'
        output = fizzbuzz.fizz_buzz_output(
            self.fizzbuzz_standard_input, lucky_check=True)

        self.assertEqual(output, expected_output)

    def test_fizzbuzz_transformation_3(self):
        expected_output = 'fizz: 4, buzz: 3, fizzbuzz: 1, lucky: 2, integer: 10'
        output = fizzbuzz.fizz_buzz_report(self.fizzbuzz_standard_input)

        self.assertEqual(output, expected_output)

        expected_output = 'fizz: 1, buzz: 1, fizzbuzz: 1, lucky: 1, integer: 1'
        output = fizzbuzz.fizz_buzz_report(['3', '6', '5', '1','15'])

        self.assertEqual(output, expected_output)


    def test_row_validator(self):
        negative_input = ['-1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        decimal_input = ['1.5', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        spaces_input = ['1', '   2', '3    ', ' 4   ', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        null_input = ['None', 'null', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']

        #valid row tests
        self.assertEqual(fizzbuzz.validate_row(self.fizzbuzz_standard_input), None)
        self.assertEqual(fizzbuzz.validate_row(negative_input), None)
        self.assertEqual(fizzbuzz.validate_row(spaces_input), None)

        #invalid row tests
        with self.assertRaises(fizzbuzz.ValuesAreNonInteger):
            fizzbuzz.validate_row(decimal_input)

        with self.assertRaises(fizzbuzz.ValuesAreNonInteger):
            fizzbuzz.validate_row(['one', '1', '2', '3'])

        with self.assertRaises(fizzbuzz.ValuesAreNonInteger):
            fizzbuzz.validate_row(null_input)

        with self.assertRaises(fizzbuzz.InvalidNumberOfValues):
            fizzbuzz.validate_row(['1', '2', '3'])

if __name__ == "__main__":
    unittest.main()
