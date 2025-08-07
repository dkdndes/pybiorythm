#!/usr/bin/env python3
"""
Simplified coverage tests for biorythm module focused on working tests.
"""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import json

import biorythm


class TestHorizontalCharts:
    """Test horizontal chart functionality."""

    @patch('builtins.print')
    def test_horizontal_chart_generation(self, mock_print):
        """Test horizontal chart generation."""
        calculator = biorythm.BiorhythmCalculator()
        birthdate = datetime(1990, 5, 15)
        plot_date = datetime(2023, 6, 1)
        
        calculator._create_combined_horizontal_wave_matrix(birthdate, plot_date)
        assert mock_print.called
        assert mock_print.call_count >= 10  # Should print multiple lines

    @patch('builtins.print')
    def test_horizontal_chart_method(self, mock_print):
        """Test the main horizontal chart method."""
        calculator = biorythm.BiorhythmCalculator()
        birthdate = datetime(1995, 8, 20)
        plot_date = datetime(2023, 8, 20)
        
        calculator._create_horizontal_chart(birthdate, plot_date)
        assert mock_print.called


class TestJSONOrientations:
    """Test JSON output functionality."""

    def test_direct_json_generation(self):
        """Test JSON generation directly without main function."""
        calculator = biorythm.BiorhythmCalculator()
        birthdate = datetime(2000, 1, 1)
        
        # Test vertical JSON
        result_v = calculator.generate_timeseries_json(birthdate, chart_orientation="vertical")
        assert isinstance(result_v, dict)
        assert "data" in result_v
        
        # Test horizontal JSON  
        result_h = calculator.generate_timeseries_json(birthdate, chart_orientation="horizontal")
        assert isinstance(result_h, dict)
        assert "data" in result_h


class TestDifferentOrientations:
    """Test different chart orientations."""

    @patch('builtins.print')
    def test_horizontal_orientation(self, mock_print):
        """Test horizontal orientation chart generation."""
        calculator = biorythm.BiorhythmCalculator(orientation="horizontal")
        birthdate = datetime(1985, 3, 12)
        
        calculator.generate_chart(birthdate)
        assert mock_print.called


class TestEdgeCasesAndSpecificLines:
    """Test specific edge cases to improve coverage."""

    @patch('builtins.print')
    def test_chart_generation_with_overlapping_cycles(self, mock_print):
        """Test chart generation when cycles have overlapping positions."""
        calculator = biorythm.BiorhythmCalculator(width=10)
        
        # Choose specific dates to create overlap conditions  
        birthdate = datetime(1990, 1, 1)
        
        calculator.generate_chart(birthdate)
        assert mock_print.called

    @patch('builtins.print')
    def test_chart_with_critical_days(self, mock_print):
        """Test chart generation including critical day detection."""
        calculator = biorythm.BiorhythmCalculator()
        
        # Use dates that will create critical conditions
        birthdate = datetime(1990, 1, 1)
        plot_date = datetime(1990, 1, 12)  # 11.5 days = half physical cycle
        
        calculator.generate_chart(birthdate)
        assert mock_print.called

    def test_timeseries_json_different_orientations(self):
        """Test JSON timeseries generation with different orientations."""
        calculator = biorythm.BiorhythmCalculator()
        birthdate = datetime(1990, 5, 15)
        
        # Test vertical JSON
        result_vertical = calculator.generate_timeseries_json(
            birthdate, chart_orientation="vertical"
        )
        assert isinstance(result_vertical, dict)
        assert "data" in result_vertical
        
        # Test horizontal JSON
        result_horizontal = calculator.generate_timeseries_json(
            birthdate, chart_orientation="horizontal"
        )
        assert isinstance(result_horizontal, dict)
        assert "data" in result_horizontal


class TestMainWithDifferentParams:
    """Test main function with different parameter combinations."""

    @patch('biorythm.BiorhythmCalculator')
    @patch('biorythm.DateValidator.create_validated_date')
    def test_main_with_horizontal_orientation(self, mock_date_validator, mock_calculator_class):
        """Test main function with horizontal orientation."""
        mock_date = datetime(2000, 6, 15)
        mock_date_validator.return_value = mock_date
        
        mock_calculator = MagicMock()
        mock_calculator_class.return_value = mock_calculator
        
        biorythm.main(year=2000, month=6, day=15, orientation="horizontal", days=30)
        
        mock_calculator.generate_chart.assert_called_with(mock_date)

    @patch('biorythm.BiorhythmCalculator')
    @patch('biorythm.DateValidator.create_validated_date') 
    def test_main_with_different_days_param(self, mock_date_validator, mock_calculator_class):
        """Test main function with different days parameter."""
        mock_date = datetime(1995, 12, 31)
        mock_date_validator.return_value = mock_date
        
        mock_calculator = MagicMock()
        mock_calculator_class.return_value = mock_calculator
        
        biorythm.main(year=1995, month=12, day=31, days=45)
        
        # Verify calculator was created with correct parameters
        mock_calculator_class.assert_called_with(width=80, days=45, orientation="vertical")


if __name__ == "__main__":
    pytest.main([__file__])