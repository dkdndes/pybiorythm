#!/usr/bin/env python3
"""Enhanced Python module for generating biorhythm charts.
Plots a chart of physical, emotional, and intellectual cycles based on the 
pseudoscientific biorhythm theory developed by Wilhelm Fliess in the late 19th century.

https://en.wikipedia.org/wiki/Biorhythm_(pseudoscience)

IMPORTANT DISCLAIMER:
This software implements the biorhythm theory, which is considered PSEUDOSCIENCE.
Extensive scientific research has found NO VALIDITY to biorhythm theory beyond 
coincidence. Multiple controlled studies have consistently failed to find any 
correlation between the proposed 23, 28, and 33-day cycles and human performance
or life events. This implementation is provided FOR ENTERTAINMENT PURPOSES ONLY
and should NOT be used for making any important life decisions.

Historical Context:
The biorhythm theory was developed by German otolaryngologist Wilhelm Fliess,
a friend of Sigmund Freud, in the late 19th century. It was popularized in 
the United States in the late 1970s through books by Bernard Gittelson.
Despite its popularity, scientific testing has consistently shown no evidence
supporting the theory's claims.

Mathematical Note:
- The 23- and 28-day cycles repeat every 644 days (1.76 years)
- All three cycles (23, 28, 33 days) repeat every 21,252 days (58.18 years)

Usage Examples:
    # Interactive mode with orientation choice
    python biorhythm_enhanced.py
    
    # Programmatic mode - vertical chart (traditional)
    main(year=1990, month=5, day=15, orientation='vertical')
    
    # Programmatic mode - horizontal chart (timeline left-to-right)
    main(year=1990, month=5, day=15, orientation='horizontal')

Chart Orientations:
- Vertical: Traditional format, time flows top-to-bottom, cycles across width
- Horizontal: Timeline flows left-to-right, cycles plotted as separate tracks

History:
01.00 2023-Jun-21 Scott S. Initial release.
01.01 2024-Nov-25 Scott S. Added plot date percentages.
02.00 2025-Aug-07 Enhanced version with logging, error handling, and modular design.
02.01 2025-Aug-07 Added stronger scientific disclaimers and critical days detection.
02.02 2025-Aug-07 Added horizontal chart orientation (left-to-right timeline).

MIT License

FOR ENTERTAINMENT PURPOSES ONLY - NOT SCIENTIFICALLY VALID.
"""

import logging
import math
import sys
from datetime import datetime, timedelta
from typing import Optional, Tuple, List


# Constants based on traditional biorhythm theory
PHYSICAL_CYCLE_DAYS = 23      # Wilhelm Fliess's "male" cycle
EMOTIONAL_CYCLE_DAYS = 28     # Fliess's "female" cycle (matches menstrual cycle)
INTELLECTUAL_CYCLE_DAYS = 33  # Alfred Teltscher's intellectual cycle
MIN_CHART_WIDTH = 12
DEFAULT_CHART_WIDTH = 55
DEFAULT_DAYS_TO_PLOT = 29
MIN_YEAR = 1
MAX_YEAR = 9999

# Critical day threshold - values within this range of zero are considered "critical"
CRITICAL_DAY_THRESHOLD = 0.05  # Within 5% of zero


class BiorhythmError(Exception):
    """Custom exception for biorhythm calculation errors."""
    pass


class DateValidationError(BiorhythmError):
    """Exception raised for invalid date inputs."""
    pass


class ChartParameterError(BiorhythmError):
    """Exception raised for invalid chart parameters."""
    pass


class BiorhythmCalculator:
    """Handles biorhythm calculations and chart generation."""
    
    def __init__(self, width: int = DEFAULT_CHART_WIDTH, days: int = DEFAULT_DAYS_TO_PLOT, 
                 orientation: str = 'vertical'):
        """Initialize the biorhythm calculator.
        
        Args:
            width: Width of the chart (for vertical) or height scale (for horizontal)
            days: Number of days to plot
            orientation: 'vertical' (traditional) or 'horizontal' (left-to-right)
            
        Raises:
            ChartParameterError: If parameters are invalid
        """
        self.logger = logging.getLogger(__name__)
        self._validate_chart_parameters(width, days)
        self._validate_orientation(orientation)
        
        self.width = max(width, MIN_CHART_WIDTH)
        self.days = days
        self.orientation = orientation.lower()
        self.midwidth = math.floor(self.width / 2)
        self.middays = math.floor(self.days / 2)
        
        self.logger.info(f"BiorhythmCalculator initialized: width={self.width}, days={self.days}, orientation={self.orientation}")
    
    def _validate_orientation(self, orientation: str) -> None:
        """Validate chart orientation parameter.
        
        Args:
            orientation: Chart orientation ('vertical' or 'horizontal')
            
        Raises:
            ChartParameterError: If orientation is invalid
        """
        if not isinstance(orientation, str) or orientation.lower() not in ['vertical', 'horizontal']:
            raise ChartParameterError(f"Orientation must be 'vertical' or 'horizontal', got: {orientation}")
    
    def _validate_chart_parameters(self, width: int, days: int) -> None:
        """Validate chart parameters.
        
        Args:
            width: Chart width
            days: Number of days to plot
            
        Raises:
            ChartParameterError: If parameters are invalid
        """
        if not isinstance(width, int) or width < 1:
            raise ChartParameterError(f"Width must be a positive integer, got: {width}")
        if not isinstance(days, int) or days < 1:
            raise ChartParameterError(f"Days must be a positive integer, got: {days}")
    
    def is_critical_day(self, physical: float, emotional: float, intellectual: float) -> Tuple[bool, List[str]]:
        """Determine if any cycles are in a critical period (near zero).
        
        According to biorhythm theory, days when cycles cross the zero line
        are considered "critical days" of greater risk or uncertainty.
        
        Args:
            physical: Physical cycle value (-1 to 1)
            emotional: Emotional cycle value (-1 to 1)
            intellectual: Intellectual cycle value (-1 to 1)
            
        Returns:
            Tuple of (is_critical, list_of_critical_cycles)
        """
        critical_cycles = []
        
        if abs(physical) <= CRITICAL_DAY_THRESHOLD:
            critical_cycles.append('Physical')
        if abs(emotional) <= CRITICAL_DAY_THRESHOLD:
            critical_cycles.append('Emotional')
        if abs(intellectual) <= CRITICAL_DAY_THRESHOLD:
            critical_cycles.append('Intellectual')
            
        return len(critical_cycles) > 0, critical_cycles
    
    def calculate_biorhythm_values(self, birthdate: datetime, target_date: datetime) -> Tuple[float, float, float]:
        """Calculate biorhythm values for a specific date.
        
        Args:
            birthdate: Birth date
            target_date: Date to calculate values for
            
        Returns:
            Tuple of (physical, emotional, intellectual) values between -1 and 1
        """
        days_alive = (target_date - birthdate).days
        self.logger.debug(f"Calculating biorhythm for {days_alive} days since birth")
        
        # Calculate sine wave values
        physical = math.sin((2 * math.pi * days_alive) / PHYSICAL_CYCLE_DAYS)
        emotional = math.sin((2 * math.pi * days_alive) / EMOTIONAL_CYCLE_DAYS)
        intellectual = math.sin((2 * math.pi * days_alive) / INTELLECTUAL_CYCLE_DAYS)
        
        return physical, emotional, intellectual
    
    def _calculate_chart_positions(self, physical: float, emotional: float, intellectual: float) -> Tuple[int, int, int]:
        """Calculate chart positions for biorhythm values.
        
        Args:
            physical: Physical biorhythm value (-1 to 1)
            emotional: Emotional biorhythm value (-1 to 1)
            intellectual: Intellectual biorhythm value (-1 to 1)
            
        Returns:
            Tuple of chart positions (physical_pos, emotional_pos, intellectual_pos)
        """
        p_pos = math.floor(physical * (self.midwidth - 1)) + self.midwidth
        e_pos = math.floor(emotional * (self.midwidth - 1)) + self.midwidth
        i_pos = math.floor(intellectual * (self.midwidth - 1)) + self.midwidth
        
        return p_pos, e_pos, i_pos
    
    def _create_chart_line(self, p_pos: int, e_pos: int, i_pos: int, 
                          is_plot_date: bool = False, is_critical: bool = False) -> str:
        """Create a single line of the biorhythm chart.
        
        Args:
            p_pos: Physical position
            e_pos: Emotional position  
            i_pos: Intellectual position
            is_plot_date: Whether this is the main plot date
            is_critical: Whether this is a critical day
            
        Returns:
            Formatted chart line string
        """
        space_char = '-' if is_plot_date else ('.' if is_critical else ' ')
        chart_line = list(space_char * self.width)
        chart_line[self.midwidth] = ':'
        
        # Place markers
        marker_p = 'P' if is_critical else 'p'
        marker_e = 'E' if is_critical else 'e'
        marker_i = 'I' if is_critical else 'i'
        
        chart_line[p_pos] = marker_p
        chart_line[e_pos] = marker_e
        chart_line[i_pos] = marker_i
        
        # Handle overlapping positions
        if p_pos == e_pos:
            chart_line[p_pos] = '!' if is_critical else '*'
        if e_pos == i_pos:
            chart_line[e_pos] = '!' if is_critical else '*'
        if i_pos == p_pos:
            chart_line[i_pos] = '!' if is_critical else '*'
        
        return ''.join(chart_line)
    
    def _print_chart_header(self, birthdate: datetime, plot_date: datetime, days_alive: int) -> None:
        """Print the chart header information with scientific disclaimers.
        
        Args:
            birthdate: Birth date
            plot_date: Plot date
            days_alive: Number of days alive
        """
        longdate_format = '%a %b %d %Y'
        orientation_display = self.orientation.upper()
        print('=' * 60)
        print(f'BIORHYTHM CHART ({orientation_display}) - FOR ENTERTAINMENT ONLY')
        print('⚠️  WARNING: This theory has NO SCIENTIFIC BASIS')
        print('=' * 60)
        print('Birth:  ', birthdate.strftime(longdate_format), sep='')
        print('Plot:   ', plot_date.strftime(longdate_format), sep='')
        print('Alive:  ', f"{days_alive:,}", ' days', sep='')
        print()
        print('Legend:')
        print('p:      Physical (23-day cycle) - coordination, strength, well-being')
        print('e:      Emotional (28-day cycle) - creativity, sensitivity, mood')
        print('i:      Intellectual (33-day cycle) - alertness, analytical functioning')
        print('*:      Multiple cycles overlap at this position')
        print('!:      Critical day (cycle near zero - traditionally considered risky)')
        print()
        
        # Calculate cycle repetition information
        days_to_23_28_repeat = 644 - (days_alive % 644)
        days_to_full_repeat = 21252 - (days_alive % 21252)
        print(f'Cycle Info: Physical+Emotional repeat in {days_to_23_28_repeat} days')
        print(f'           All cycles repeat in {days_to_full_repeat} days')
        print()
    
    def _print_chart_title(self, plot_date: datetime) -> None:
        """Print the chart title and scale for vertical charts.
        
        Args:
            plot_date: The plot date for formatting
        """
        if self.orientation == 'horizontal':
            return  # Horizontal charts have their own title method
            
        title = 'PASSIVE  CRITICAL  ACTIVE'
        shortdate_format = '%a %b %d'
        datepad = len(plot_date.strftime(shortdate_format)) + 1
        pad = datepad + self.midwidth - math.floor(len(title) / 2)
        
        print(' ' * pad, title, sep='')
        print(' ' * datepad, '-100% ', '=' * (self.width - 12), ' +100%', sep='')
    
    def generate_chart(self, birthdate: datetime, plot_date: datetime = None) -> None:
        """Generate and print the complete biorhythm chart.
        
        Args:
            birthdate: Birth date
            plot_date: Date to center chart on (defaults to today)
            
        Raises:
            BiorhythmError: If chart generation fails
        """
        if plot_date is None:
            plot_date = datetime.now()
        
        try:
            days_alive = (plot_date - birthdate).days
            self.logger.info(f"Generating {self.orientation} chart for {days_alive} days since birth")
            
            # Print header
            self._print_chart_header(birthdate, plot_date, days_alive)
            
            # Generate chart based on orientation
            if self.orientation == 'horizontal':
                self._create_horizontal_chart(birthdate, plot_date)
            else:
                self._generate_vertical_chart(birthdate, plot_date)
            
            print()
            print('REMEMBER: This is pseudoscience with no proven validity!')
            
            self.logger.info("Chart generation completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error generating chart: {str(e)}")
            raise BiorhythmError(f"Failed to generate chart: {str(e)}") from e
    
    def _generate_vertical_chart(self, birthdate: datetime, plot_date: datetime) -> None:
        """Generate the traditional vertical biorhythm chart.
        
        Args:
            birthdate: Birth date
            plot_date: Date to center chart on
        """
        self._print_chart_title(plot_date)
        
        # Calculate starting date for chart
        start_date = plot_date - timedelta(days=self.middays)
        
        # Track percentages for plot date and critical days
        plot_percentages = None
        critical_days = []
        shortdate_format = '%a %b %d'
        
        # Generate chart lines
        for day_offset in range(self.days):
            current_date = start_date + timedelta(days=day_offset)
            is_plot_date = current_date == plot_date
            
            # Calculate biorhythm values
            physical, emotional, intellectual = self.calculate_biorhythm_values(birthdate, current_date)
            
            # Check for critical days
            is_critical, critical_cycles = self.is_critical_day(physical, emotional, intellectual)
            if is_critical:
                critical_days.append((current_date, critical_cycles))
            
            # Store percentages for plot date
            if is_plot_date:
                plot_percentages = (physical * 100, emotional * 100, intellectual * 100)
            
            # Calculate chart positions
            p_pos, e_pos, i_pos = self._calculate_chart_positions(physical, emotional, intellectual)
            
            # Create and print chart line
            chart_line = self._create_chart_line(p_pos, e_pos, i_pos, is_plot_date, is_critical)
            critical_marker = ' ⚠️' if is_critical else ''
            print(current_date.strftime(shortdate_format), chart_line, critical_marker, sep='')
        
        # Print percentages and critical days summary
        if plot_percentages:
            datepad = len(plot_date.strftime(shortdate_format)) + 1
            p_pct, e_pct, i_pct = plot_percentages
            print(' ' * datepad, f'p:{p_pct:+.1f}% e:{e_pct:+.1f}% i:{i_pct:+.1f}%', sep='')
        
        # Show critical days in the chart period
        if critical_days:
            print()
            print('⚠️  CRITICAL DAYS detected in chart period:')
            for crit_date, cycles in critical_days:
                cycles_str = ', '.join(cycles)
                print(f'   {crit_date.strftime(shortdate_format)}: {cycles_str} cycle(s) near zero')
        else:
            print()
            print('ℹ️  No critical days in the displayed period.')


class DateValidator:
    """Handles date validation for biorhythm calculations."""
    
    @staticmethod
    def validate_date_components(year: int, month: int, day: int) -> None:
        """Validate individual date components.
        
        Args:
            year: Year (1-9999)
            month: Month (1-12)
            day: Day (1-31)
            
        Raises:
            DateValidationError: If any component is invalid
        """
        if not isinstance(year, int) or not (MIN_YEAR <= year <= MAX_YEAR):
            raise DateValidationError(f"Year must be between {MIN_YEAR} and {MAX_YEAR}, got: {year}")
        
        if not isinstance(month, int) or not (1 <= month <= 12):
            raise DateValidationError(f"Month must be between 1 and 12, got: {month}")
        
        if not isinstance(day, int) or not (1 <= day <= 31):
            raise DateValidationError(f"Day must be between 1 and 31, got: {day}")
    
    @staticmethod
    def create_validated_date(year: int, month: int, day: int) -> datetime:
        """Create and validate a datetime object.
        
        Args:
            year: Year
            month: Month
            day: Day
            
        Returns:
            Validated datetime object
            
        Raises:
            DateValidationError: If date is invalid
        """
        DateValidator.validate_date_components(year, month, day)
        
        try:
            date_obj = datetime(year, month, day)
        except ValueError as e:
            raise DateValidationError(f"Invalid date {year}-{month:02d}-{day:02d}: {str(e)}") from e
        
        # Check if birth date is in the future
        if date_obj > datetime.now():
            raise DateValidationError("Birth date cannot be in the future")
        
        return date_obj


class UserInterface:
    """Handles user interaction and input."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_user_input(self) -> Tuple[int, int, int, str]:
        """Get birth date and chart orientation from user input with educational context.
        
        Returns:
            Tuple of (year, month, day, orientation)
            
        Raises:
            DateValidationError: If input is invalid
        """
        try:
            print('\nBiorhythm Chart Generator (Pseudoscience Demonstration):')
            print('Historical Context:')
            print('• Developed by Wilhelm Fliess (friend of Sigmund Freud) in 1890s')
            print('• Popularized in USA during 1970s by Bernard Gittelson')
            print('• Extensively tested - no scientific evidence found')
            print('• All 134+ studies confirm it has no predictive value')
            print()
            
            year_input = input(f'  Enter your birth YEAR ({MIN_YEAR}-{MAX_YEAR}): ').strip()
            month_input = input('  Enter your birth MONTH (1-12): ').strip()
            day_input = input('  Enter your birth DAY (1-31): ').strip()
            
            print('\nChart Orientation:')
            print('  1. Vertical (traditional, top-to-bottom timeline)')
            print('  2. Horizontal (left-to-right timeline)')
            orientation_input = input('  Choose orientation (1 or 2, default=1): ').strip()
            
            # Convert to integers
            try:
                year = int(year_input)
                month = int(month_input)
                day = int(day_input)
            except ValueError as e:
                raise DateValidationError(f"Invalid number format: {str(e)}") from e
            
            # Handle orientation choice
            orientation = 'vertical'  # default
            if orientation_input == '2':
                orientation = 'horizontal'
            elif orientation_input and orientation_input != '1':
                print(f"Invalid orientation choice '{orientation_input}', using vertical")
            
            self.logger.info(f"User input received: {year}-{month:02d}-{day:02d}, orientation={orientation}")
            return year, month, day, orientation
            
        except KeyboardInterrupt:
            self.logger.info("User cancelled input")
            raise DateValidationError("Input cancelled by user")
        except EOFError:
            self.logger.info("EOF encountered during input")
            raise DateValidationError("Unexpected end of input")


def setup_logging(level: int = logging.INFO) -> None:
    """Setup logging configuration.
    
    Args:
        level: Logging level
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def main(year: Optional[int] = None, month: Optional[int] = None, day: Optional[int] = None, 
         orientation: str = 'vertical') -> None:
    """Main entry point for the biorhythm program.
    
    SCIENTIFIC DISCLAIMER: Biorhythm theory has been extensively tested and 
    consistently found to have no scientific validity. This program is for
    entertainment purposes only.
    
    Args:
        year: Birth year (optional, will prompt if not provided)
        month: Birth month (optional, will prompt if not provided)
        day: Birth day (optional, will prompt if not provided)
        orientation: Chart orientation ('vertical' or 'horizontal')
    """
    logger = logging.getLogger(__name__)
    
    # Display scientific warning
    print("\n" + "!" * 70)
    print("⚠️  SCIENTIFIC WARNING ⚠️")
    print("Biorhythm theory is PSEUDOSCIENCE with NO scientific evidence.")
    print("Multiple peer-reviewed studies have found NO correlation between")
    print("biorhythm cycles and human performance beyond random chance.")
    print("This program is provided for ENTERTAINMENT PURPOSES ONLY.")
    print("!" * 70)
    
    try:
        # Get birth date and orientation
        if year is None or month is None or day is None:
            ui = UserInterface()
            year, month, day, orientation = ui.get_user_input()
        
        # Validate and create birth date
        birthdate = DateValidator.create_validated_date(year, month, day)
        logger.info(f"Birth date validated: {birthdate.strftime('%Y-%m-%d')}")
        
        # Generate chart
        calculator = BiorhythmCalculator(orientation=orientation)
        print()  # Add spacing before chart
        calculator.generate_chart(birthdate)
        
        logger.info("Chart generation completed successfully")
        
    except DateValidationError as e:
        logger.error(f"Date validation error: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)
    except BiorhythmError as e:
        logger.error(f"Biorhythm calculation error: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}")
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    setup_logging(level=logging.INFO)  # Change to logging.DEBUG for more verbose output
    
    try:
        main()
        print()
        print('Educational Resources:')
        print('• Wikipedia: https://en.wikipedia.org/wiki/Biorhythm_(pseudoscience)')
        print('• The Skeptic\'s Dictionary: http://skepdic.com/biorhyth.html')
        print('• "Comprehensive Review of Biorhythm Theory" by Terence Hines (1998)')
        print()
        input('Press ENTER to Continue: ')
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)
