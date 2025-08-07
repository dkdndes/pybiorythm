#!/usr/bin/env python3
"""
Test suite for main.py command line interface.
"""

import pytest
from unittest.mock import patch, MagicMock

import main


class TestCommandLineParser:
    """Test cases for command line argument parsing."""

    def test_create_parser(self):
        """Test that parser is created correctly."""
        parser = main.create_parser()
        assert parser is not None

        # Test that all expected arguments are present
        help_text = parser.format_help()
        assert "--year" in help_text
        assert "--month" in help_text
        assert "--day" in help_text
        assert "--orientation" in help_text
        assert "--days" in help_text

    def test_parser_with_all_arguments(self):
        """Test parser with all arguments provided."""
        parser = main.create_parser()
        args = parser.parse_args(
            [
                "--year",
                "1990",
                "--month",
                "5",
                "--day",
                "15",
                "--orientation",
                "horizontal",
                "--days",
                "30",
            ]
        )

        assert args.year == 1990
        assert args.month == 5
        assert args.day == 15
        assert args.orientation == "horizontal"
        assert args.days == 30

    def test_parser_with_short_arguments(self):
        """Test parser with short argument forms."""
        parser = main.create_parser()
        args = parser.parse_args(["-y", "1995", "-m", "12", "-d", "25"])

        assert args.year == 1995
        assert args.month == 12
        assert args.day == 25
        assert args.orientation == "vertical"  # default
        assert args.days == 29  # default

    def test_parser_defaults(self):
        """Test that parser defaults are correct."""
        parser = main.create_parser()
        args = parser.parse_args([])

        assert args.year is None
        assert args.month is None
        assert args.day is None
        assert args.orientation == "vertical"
        assert args.days == 29

    def test_parser_invalid_orientation(self):
        """Test parser with invalid orientation choice."""
        parser = main.create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["--orientation", "invalid"])

    def test_parser_help_option(self):
        """Test that help option works."""
        parser = main.create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["--help"])


class TestMainFunction:
    """Test cases for main() function behavior."""

    @patch("main.biorythm_main")
    @patch("sys.argv", ["main.py"])
    def test_main_no_arguments_interactive(self, mock_biorythm_main):
        """Test main() with no arguments calls interactive mode."""
        main.main()
        mock_biorythm_main.assert_called_once_with()

    @patch("main.biorythm_main")
    @patch("sys.argv", ["main.py", "-y", "1990", "-m", "5", "-d", "15"])
    def test_main_with_all_date_arguments(self, mock_biorythm_main):
        """Test main() with all required date arguments."""
        main.main()
        mock_biorythm_main.assert_called_once_with(
            year=1990, month=5, day=15, orientation="vertical", days=29
        )

    @patch("main.biorythm_main")
    @patch(
        "sys.argv",
        [
            "main.py",
            "-y",
            "1990",
            "-m",
            "5",
            "-d",
            "15",
            "--orientation",
            "horizontal",
            "--days",
            "60",
        ],
    )
    def test_main_with_all_arguments(self, mock_biorythm_main):
        """Test main() with all arguments specified."""
        main.main()
        mock_biorythm_main.assert_called_once_with(
            year=1990, month=5, day=15, orientation="horizontal", days=60
        )

    @patch("main.biorythm_main")
    @patch("builtins.print")
    @patch("sys.exit")
    @patch("sys.argv", ["main.py", "-y", "1990"])
    def test_main_incomplete_date_arguments(
        self, mock_exit, mock_print, mock_biorythm_main
    ):
        """Test main() with incomplete date arguments."""
        # Configure sys.exit to raise SystemExit to properly simulate program termination
        mock_exit.side_effect = SystemExit(1)

        with pytest.raises(SystemExit):
            main.main()

        # Should print error message and exit without calling biorythm_main
        mock_print.assert_called_with(
            "Error: When using command line arguments, all date components (--year, --month, --day) must be provided"
        )
        mock_exit.assert_called_with(1)
        mock_biorythm_main.assert_not_called()

    @patch("main.biorythm_main")
    @patch("builtins.print")
    @patch("sys.exit")
    @patch("sys.argv", ["main.py", "-m", "5", "-d", "15"])
    def test_main_missing_year(self, mock_exit, mock_print, mock_biorythm_main):
        """Test main() with missing year argument."""
        # Configure sys.exit to raise SystemExit to properly simulate program termination
        mock_exit.side_effect = SystemExit(1)

        with pytest.raises(SystemExit):
            main.main()

        mock_print.assert_called_with(
            "Error: When using command line arguments, all date components (--year, --month, --day) must be provided"
        )
        mock_exit.assert_called_with(1)
        mock_biorythm_main.assert_not_called()

    @patch("main.biorythm_main")
    @patch(
        "sys.argv",
        [
            "main.py",
            "-y",
            "2000",
            "-m",
            "1",
            "-d",
            "1",
            "--orientation",
            "json-vertical",
        ],
    )
    def test_main_json_orientation(self, mock_biorythm_main):
        """Test main() with JSON orientation."""
        main.main()
        mock_biorythm_main.assert_called_once_with(
            year=2000, month=1, day=1, orientation="json-vertical", days=29
        )


class TestIntegration:
    """Integration tests that test the full command line workflow."""

    @patch("biorythm.core.BiorhythmCalculator")
    @patch("biorythm.core.DateValidator.create_validated_date")
    @patch("sys.argv", ["main.py", "-y", "1990", "-m", "5", "-d", "15"])
    def test_integration_flow(self, mock_date_validator, mock_calculator_class):
        """Test the integration flow from command line to biorhythm calculation."""
        from datetime import datetime

        # Setup mocks
        mock_date = datetime(1990, 5, 15)
        mock_date_validator.return_value = mock_date

        mock_calculator = MagicMock()
        mock_calculator_class.return_value = mock_calculator

        # Run main
        main.main()

        # Verify the flow
        mock_date_validator.assert_called_once_with(1990, 5, 15)
        mock_calculator_class.assert_called_once()
        mock_calculator.generate_chart.assert_called_once()

    def test_command_line_examples_from_help(self):
        """Test the examples provided in the help text."""
        parser = main.create_parser()

        # Example 1: basic usage
        args1 = parser.parse_args(["-y", "1990", "-m", "5", "-d", "15"])
        assert args1.year == 1990
        assert args1.month == 5
        assert args1.day == 15

        # Example 2: with orientation
        args2 = parser.parse_args(
            [
                "--year",
                "1990",
                "--month",
                "5",
                "--day",
                "15",
                "--orientation",
                "horizontal",
            ]
        )
        assert args2.orientation == "horizontal"

        # Example 3: with JSON output
        args3 = parser.parse_args(
            [
                "-y",
                "1990",
                "-m",
                "5",
                "-d",
                "15",
                "--days",
                "30",
                "--orientation",
                "json-vertical",
            ]
        )
        assert args3.days == 30
        assert args3.orientation == "json-vertical"


class TestErrorScenarios:
    """Test various error scenarios."""

    @patch("sys.argv", ["main.py", "--year", "not_a_number", "-m", "5", "-d", "15"])
    def test_invalid_year_type(self):
        """Test behavior with invalid year type."""
        with pytest.raises(SystemExit):
            main.main()

    @patch("sys.argv", ["main.py", "-y", "1990", "--month", "not_a_number", "-d", "15"])
    def test_invalid_month_type(self):
        """Test behavior with invalid month type."""
        with pytest.raises(SystemExit):
            main.main()

    @patch("sys.argv", ["main.py", "-y", "1990", "-m", "5", "--day", "not_a_number"])
    def test_invalid_day_type(self):
        """Test behavior with invalid day type."""
        with pytest.raises(SystemExit):
            main.main()

    @patch(
        "sys.argv",
        ["main.py", "-y", "1990", "-m", "5", "-d", "15", "--days", "not_a_number"],
    )
    def test_invalid_days_type(self):
        """Test behavior with invalid days type."""
        with pytest.raises(SystemExit):
            main.main()


if __name__ == "__main__":
    pytest.main([__file__])
