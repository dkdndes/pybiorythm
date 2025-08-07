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
#!/usr/bin/env python3
"""
Enhanced Python module for generating biorhythm charts.
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
"""

import logging
import math
import sys
import shutil
from datetime import datetime, timedelta
from typing import Optional, Tuple, List
import numpy as np

# Constants
PHYSICAL_CYCLE_DAYS = 23
EMOTIONAL_CYCLE_DAYS = 28
INTELLECTUAL_CYCLE_DAYS = 33
MIN_CHART_WIDTH = 12
DEFAULT_CHART_WIDTH = 55
DEFAULT_DAYS_TO_PLOT = 29
MIN_YEAR = 1
MAX_YEAR = 9999
CRITICAL_DAY_THRESHOLD = 0.05

# --- Exception Classes ---
class BiorhythmError(Exception):
    pass

class DateValidationError(BiorhythmError):
    pass

class ChartParameterError(BiorhythmError):
    pass

# --- Core Classes ---
class BiorhythmCalculator:
    def __init__(
        self,
        width: int = DEFAULT_CHART_WIDTH,
        days: int = DEFAULT_DAYS_TO_PLOT,
        orientation: str = "vertical",
    ):
        self.logger = logging.getLogger(__name__)
        self._validate_chart_parameters(width, days)
        self._validate_orientation(orientation)
        self.width = max(width, MIN_CHART_WIDTH)
        self.days = days
        self.orientation = orientation.lower()
        self.midwidth = math.floor(self.width / 2)
        self.middays = math.floor(self.days / 2)
        self.logger.info(
            f"BiorhythmCalculator initialized: width={self.width}, days={self.days}, orientation={self.orientation}"
        )

    def _validate_orientation(self, orientation: str) -> None:
        if not isinstance(orientation, str) or orientation.lower() not in [
            "vertical", "horizontal",
        ]:
            raise ChartParameterError(
                f"Orientation must be 'vertical' or 'horizontal', got: {orientation}"
            )

    def _validate_chart_parameters(self, width: int, days: int) -> None:
        if not isinstance(width, int) or width < 1:
            raise ChartParameterError(f"Width must be a positive integer, got: {width}")
        if not isinstance(days, int) or days < 1:
            raise ChartParameterError(f"Days must be a positive integer, got: {days}")

    def is_critical_day(
        self, physical: float, emotional: float, intellectual: float
    ) -> Tuple[bool, List[str]]:
        critical_cycles = []
        if abs(physical) <= CRITICAL_DAY_THRESHOLD:
            critical_cycles.append("Physical")
        if abs(emotional) <= CRITICAL_DAY_THRESHOLD:
            critical_cycles.append("Emotional")
        if abs(intellectual) <= CRITICAL_DAY_THRESHOLD:
            critical_cycles.append("Intellectual")
        return len(critical_cycles) > 0, critical_cycles

    def calculate_biorhythm_values(
        self, birthdate: datetime, target_date: datetime
    ) -> Tuple[float, float, float]:
        days_alive = (target_date - birthdate).days
        self.logger.debug(f"Calculating biorhythm for {days_alive} days since birth")
        physical = math.sin((2 * math.pi * days_alive) / PHYSICAL_CYCLE_DAYS)
        emotional = math.sin((2 * math.pi * days_alive) / EMOTIONAL_CYCLE_DAYS)
        intellectual = math.sin((2 * math.pi * days_alive) / INTELLECTUAL_CYCLE_DAYS)
        return physical, emotional, intellectual

    def _calculate_chart_positions(
        self, physical: float, emotional: float, intellectual: float
    ) -> Tuple[int, int, int]:
        p_pos = math.floor(physical * (self.midwidth - 1)) + self.midwidth
        e_pos = math.floor(emotional * (self.midwidth - 1)) + self.midwidth
        i_pos = math.floor(intellectual * (self.midwidth - 1)) + self.midwidth
        return p_pos, e_pos, i_pos

    def _create_chart_line(
        self,
        p_pos: int,
        e_pos: int,
        i_pos: int,
        is_plot_date: bool = False,
        is_critical: bool = False,
    ) -> str:
        space_char = "-" if is_plot_date else ("." if is_critical else " ")
        chart_line = list(space_char * self.width)
        chart_line[self.midwidth] = ":"
        marker_p = "P" if is_critical else "p"
        marker_e = "E" if is_critical else "e"
        marker_i = "I" if is_critical else "i"
        chart_line[p_pos] = marker_p
        chart_line[e_pos] = marker_e
        chart_line[i_pos] = marker_i
        # Handle overlapping positions
        if p_pos == e_pos:
            chart_line[p_pos] = "!" if is_critical else "*"
        if e_pos == i_pos:
            chart_line[e_pos] = "!" if is_critical else "*"
        if i_pos == p_pos:
            chart_line[i_pos] = "!" if is_critical else "*"
        return "".join(chart_line)

    def _print_chart_header(
        self, birthdate: datetime, plot_date: datetime, days_alive: int
    ) -> None:
        longdate_format = "%a %b %d %Y"
        orientation_display = self.orientation.upper()
        print("=" * 60)
        print(f"BIORHYTHM CHART ({orientation_display}) - FOR ENTERTAINMENT ONLY")
        print("⚠️  WARNING: This theory has NO SCIENTIFIC BASIS")
        print("=" * 60)
        print("Birth:  ", birthdate.strftime(longdate_format), sep="")
        print("Plot:   ", plot_date.strftime(longdate_format), sep="")
        print("Alive:  ", f"{days_alive:,}", " days", sep="")
        print()
        print("Legend:")
        print("p:      Physical (23-day cycle) - coordination, strength, well-being")
        print("e:      Emotional (28-day cycle) - creativity, sensitivity, mood")
        print("i:      Intellectual (33-day cycle) - alertness, analytical functioning")
        print("*:      Multiple cycles overlap at this position")
        print("!:      Critical day (cycle near zero - traditionally considered risky)")
        print()
        days_to_23_28_repeat = 644 - (days_alive % 644)
        days_to_full_repeat = 21252 - (days_alive % 21252)
        print(f"Cycle Info: Physical+Emotional repeat in {days_to_23_28_repeat} days")
        print(f"           All cycles repeat in {days_to_full_repeat} days")
        print()

    def _print_chart_title(self, plot_date: datetime) -> None:
        if self.orientation == "horizontal":
            return
        title = "PASSIVE  CRITICAL  ACTIVE"
        shortdate_format = "%a %b %d"
        datepad = len(plot_date.strftime(shortdate_format)) + 1
        pad = datepad + self.midwidth - math.floor(len(title) / 2)
        print(" " * pad, title, sep="")
        print(" " * datepad, "-100% ", "=" * (self.width - 12), " +100%", sep="")

    def generate_chart(self, birthdate: datetime, plot_date: datetime = None) -> None:
        if plot_date is None:
            plot_date = datetime.now()
        try:
            days_alive = (plot_date - birthdate).days
            self.logger.info(
                f"Generating {self.orientation} chart for {days_alive} days since birth"
            )
            self._print_chart_header(birthdate, plot_date, days_alive)
            if self.orientation == "horizontal":
                # self._create_horizontal_chart(birthdate, plot_date)
                self._create_combined_horizontal_wave_matrix(birthdate, plot_date)
            else:
                self._generate_vertical_chart(birthdate, plot_date)
            print()
            print("REMEMBER: This is pseudoscience with no proven validity!")
            self.logger.info("Chart generation completed successfully")
        except Exception as e:
            self.logger.error(f"Error generating chart: {str(e)}")
            raise BiorhythmError(f"Failed to generate chart: {str(e)}") from e

    def _generate_vertical_chart(
        self, birthdate: datetime, plot_date: datetime
    ) -> None:
        self._print_chart_title(plot_date)
        start_date = plot_date - timedelta(days=self.middays)
        plot_percentages = None
        critical_days = []
        shortdate_format = "%a %b %d"
        for day_offset in range(self.days):
            current_date = start_date + timedelta(days=day_offset)
            is_plot_date = current_date == plot_date
            physical, emotional, intellectual = self.calculate_biorhythm_values(
                birthdate, current_date
            )
            is_critical, critical_cycles = self.is_critical_day(
                physical, emotional, intellectual
            )
            if is_critical:
                critical_days.append((current_date, critical_cycles))
            if is_plot_date:
                plot_percentages = (physical * 100, emotional * 100, intellectual * 100)
            p_pos, e_pos, i_pos = self._calculate_chart_positions(
                physical, emotional, intellectual
            )
            chart_line = self._create_chart_line(
                p_pos, e_pos, i_pos, is_plot_date, is_critical
            )
            critical_marker = " ⚠️" if is_critical else ""
            print(
                current_date.strftime(shortdate_format),
                chart_line,
                critical_marker,
                sep="",
            )
        if plot_percentages:
            datepad = len(plot_date.strftime(shortdate_format)) + 1
            p_pct, e_pct, i_pct = plot_percentages
            print(
                " " * datepad,
                f"p:{p_pct:+.1f}% e:{e_pct:+.1f}% i:{i_pct:+.1f}%",
                sep="",
            )
        if critical_days:
            print()
            print("⚠️  CRITICAL DAYS detected in chart period:")
            for crit_date, cycles in critical_days:
                cycles_str = ", ".join(cycles)
                print(
                    f"   {crit_date.strftime(shortdate_format)}: {cycles_str} cycle(s) near zero"
                )
        else:
            print()
            print("ℹ️  No critical days in the displayed period.")

    def _create_horizontal_chart(self, birthdate: datetime, plot_date: datetime) -> None:
        """
        Draws a 'wave matrix' for each cycle: rows = amplitude levels (high=+1, low=-1), columns=days.
        """
        cycles = [
            ("Physical", 23, "p", "P"),
            ("Emotional", 28, "e", "E"),
            ("Intellectual", 33, "i", "I"),
        ]
        chart_height = 20
        width = self.width
        days = width

        start_date = plot_date - timedelta(days=days // 2)
        dates = [start_date + timedelta(days=i) for i in range(days)]
        shortdate_format = "%d.%m."

        for (label, period, mark, mark_crit) in cycles:
            # Prepare matrix
            mat = [[" " for _ in range(width)] for _ in range(chart_height)]
            for col, current_date in enumerate(dates):
                days_alive = (current_date - birthdate).days
                val = math.sin((2 * math.pi * days_alive) / period)
                # Map -1...+1 → row 0..height-1 (invert so top is +1)
                row = int(round((1 - val) / 2 * (chart_height - 1)))
                # Is this the plot date?
                is_plot = (current_date == plot_date)
                # Is this a critical day?
                crit = abs(val) <= CRITICAL_DAY_THRESHOLD
                char = mark_crit if crit else (mark.upper() if is_plot else mark)
                mat[row][col] = char
            # Print
            print(f"{label:<12}:")
            for r in range(chart_height):
                print("".join(mat[r]))
            print()  # Blank between curves

        # Print date axis at the bottom
        date_axis = [" "] * width
        label_interval = max(1, width // 6)
        for i in range(0, width, label_interval):
            label = (start_date + timedelta(days=int(i))).strftime(shortdate_format)
            for j, c in enumerate(label):
                if i + j < width:
                    date_axis[i + j] = c
        print(f"{'Date':<12}: {''.join(date_axis)}")

    def _create_combined_horizontal_wave_matrix(self, birthdate: datetime, plot_date: datetime) -> None:
        """
        Draws all three biorhythm curves in one 2D ASCII chart (height=20, width=terminal).
        Overlapping cycles are marked with * (2 overlap) or ! (all three).
        """
        chart_height = 20
        width = self.width
        start_date = plot_date - timedelta(days=width // 2)
        dates = [start_date + timedelta(days=i) for i in range(width)]
        shortdate_format = "%d.%m."

        # Calculate wave positions for each cycle (row, col)
        waves = []
        cycles = [
            ("p", PHYSICAL_CYCLE_DAYS),
            ("e", EMOTIONAL_CYCLE_DAYS),
            ("i", INTELLECTUAL_CYCLE_DAYS),
        ]
        for symbol, period in cycles:
            pos = []
            for col, date in enumerate(dates):
                days_alive = (date - birthdate).days
                val = math.sin((2 * math.pi * days_alive) / period)
                row = int(round((1 - val) / 2 * (chart_height - 1)))  # top=+1, bottom=-1
                pos.append((row, col))
            waves.append(pos)

        # Prepare the matrix
        mat = [[" " for _ in range(width)] for _ in range(chart_height)]
        for idx, wave in enumerate(waves):
            symbol = cycles[idx][0]
            for (row, col) in wave:
                current = mat[row][col]
                # For overlaps:
                if current == " ":
                    mat[row][col] = symbol
                elif current in ("p", "e", "i"):
                    mat[row][col] = "*"
                elif current == "*":
                    mat[row][col] = "!"
                # More than 3 overlap not possible with 3 curves

        # Mark the plot date with uppercase
        center_col = width // 2
        for idx, wave in enumerate(waves):
            row, col = wave[center_col]
            if mat[row][col] in ("p", "e", "i"):
                mat[row][col] = mat[row][col].upper()
            elif mat[row][col] == "*":
                mat[row][col] = "*"

        # Print chart
        print(f"{'BIORHYTHM WAVE (all cycles)':<12}")
        for r in range(chart_height):
            print("".join(mat[r]))

        # Draw zero axis (amplitude=0)
        zero_row = chart_height // 2
        axis_line = [" " for _ in range(width)]
        axis_line[center_col] = "|"
        print(f"{'Zero Axis':<12}: {''.join(axis_line)}")

        # Draw timeline/date labels
        date_labels = [" "] * width
        label_interval = max(1, width // 6)
        for i in range(0, width, label_interval):
            label = (start_date + timedelta(days=int(i))).strftime(shortdate_format)
            for j, c in enumerate(label):
                if i + j < width:
                    date_labels[i + j] = c
        print(f"{'Date':<12}: {''.join(date_labels)}")
        print()
        print("Legend: p=Physical  e=Emotional  i=Intellectual  *=2 overlap  !=3 overlap")

    def generate_timeseries_json(
        self,
        birthdate: datetime,
        plot_date: datetime = None,
        chart_orientation: str = "vertical"
    ) -> dict:
        """
        Generate a biorhythm timeseries and critical days JSON payload for analytics use.
        """
        if plot_date is None:
            plot_date = datetime.now()
        timeseries = []
        critical_days = []
        start_date = plot_date - timedelta(days=self.middays)
        for day_offset in range(self.days):
            current_date = start_date + timedelta(days=day_offset)
            days_alive = (current_date - birthdate).days
            physical, emotional, intellectual = self.calculate_biorhythm_values(birthdate, current_date)
            is_critical, critical_cycles = self.is_critical_day(physical, emotional, intellectual)
            entry = {
                "date": current_date.strftime("%Y-%m-%d"),
                "days_alive": days_alive,
                "physical": float(physical),
                "emotional": float(emotional),
                "intellectual": float(intellectual),
                "critical_cycles": critical_cycles
            }
            timeseries.append(entry)
            if is_critical:
                critical_days.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "cycles": critical_cycles
                })

        # Meta info
        days_alive = (plot_date - birthdate).days
        next_23_28 = 644 - (days_alive % 644)
        next_all = 21252 - (days_alive % 21252)

        return {
            "meta": {
                "generator": "biorhythm_enhanced.py",
                "version": "2025-08-07",
                "birthdate": birthdate.strftime("%Y-%m-%d"),
                "plot_date": plot_date.strftime("%Y-%m-%d"),
                "days_alive": days_alive,
                "cycle_lengths_days": {
                    "physical": PHYSICAL_CYCLE_DAYS,
                    "emotional": EMOTIONAL_CYCLE_DAYS,
                    "intellectual": INTELLECTUAL_CYCLE_DAYS
                },
                "chart_orientation": chart_orientation,
                "days": self.days,
                "width": self.width,
            },
            "cycle_repeats": {
                "physical_emotional_repeat_in_days": next_23_28,
                "all_cycles_repeat_in_days": next_all
            },
            "critical_days": critical_days,
            "data": timeseries
        }


class DateValidator:
    @staticmethod
    def validate_date_components(year: int, month: int, day: int) -> None:
        if not isinstance(year, int) or not (MIN_YEAR <= year <= MAX_YEAR):
            raise DateValidationError(
                f"Year must be between {MIN_YEAR} and {MAX_YEAR}, got: {year}"
            )
        if not isinstance(month, int) or not (1 <= month <= 12):
            raise DateValidationError(f"Month must be between 1 and 12, got: {month}")
        if not isinstance(day, int) or not (1 <= day <= 31):
            raise DateValidationError(f"Day must be between 1 and 31, got: {day}")

    @staticmethod
    def create_validated_date(year: int, month: int, day: int) -> datetime:
        DateValidator.validate_date_components(year, month, day)
        try:
            date_obj = datetime(year, month, day)
        except ValueError as e:
            raise DateValidationError(
                f"Invalid date {year}-{month:02d}-{day:02d}: {str(e)}"
            ) from e
        if date_obj > datetime.now():
            raise DateValidationError("Birth date cannot be in the future")
        return date_obj

class UserInterface:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_user_input(self) -> Tuple[int, int, int, str]:
        try:
            print("\nBiorhythm Chart Generator (Pseudoscience Demonstration):")
            print("Historical Context:")
            print("• Developed by Wilhelm Fliess (friend of Sigmund Freud) in 1890s")
            print("• Popularized in USA during 1970s by Bernard Gittelson")
            print("• Extensively tested - no scientific evidence found")
            print("• All 134+ studies confirm it has no predictive value")
            print()
            year_input = input(f"  Enter your birth YEAR ({MIN_YEAR}-{MAX_YEAR}): ").strip()
            month_input = input("  Enter your birth MONTH (1-12): ").strip()
            day_input = input("  Enter your birth DAY (1-31): ").strip()
            print("\nChart Orientation:")
            print("  1. Vertical (traditional, top-to-bottom timeline)")
            print("  2. Horizontal (left-to-right timeline)")
            orientation_input = input("  Choose orientation (1 or 2, default=1): ").strip()
            try:
                year = int(year_input)
                month = int(month_input)
                day = int(day_input)
            except ValueError as e:
                raise DateValidationError(f"Invalid number format: {str(e)}") from e
            orientation = "vertical"
            if orientation_input == "2":
                orientation = "horizontal"
            elif orientation_input and orientation_input != "1":
                print(f"Invalid orientation choice '{orientation_input}', using vertical")
            self.logger.info(
                f"User input received: {year}-{month:02d}-{day:02d}, orientation={orientation}"
            )
            return year, month, day, orientation
        except KeyboardInterrupt:
            self.logger.info("User cancelled input")
            raise DateValidationError("Input cancelled by user")
        except EOFError:
            self.logger.info("EOF encountered during input")
            raise DateValidationError("Unexpected end of input")

# --- Utility and entrypoint ---
def setup_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

def get_terminal_width(default=80, min_width=40):
    try:
        width = shutil.get_terminal_size().columns
        return max(width, min_width)
    except Exception:
        return default

def main(
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    orientation: str = "vertical",
) -> None:
    logger = logging.getLogger(__name__)
    print("\n" + "!" * 70)
    print("⚠️  SCIENTIFIC WARNING ⚠️")
    print("Biorhythm theory is PSEUDOSCIENCE with NO scientific evidence.")
    print("Multiple peer-reviewed studies have found NO correlation between")
    print("biorhythm cycles and human performance beyond random chance.")
    print("This program is provided for ENTERTAINMENT PURPOSES ONLY.")
    print("!" * 70)
    try:
        if year is None or month is None or day is None:
            ui = UserInterface()
            year, month, day, orientation = ui.get_user_input()
        birthdate = DateValidator.create_validated_date(year, month, day)
        logger.info(f"Birth date validated: {birthdate.strftime('%Y-%m-%d')}")
        width = get_terminal_width()
        # --- Set days/minimum height for vertical chart
        days = 20 if orientation == "vertical" else None
        calculator = BiorhythmCalculator(width=width, orientation=orientation)
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
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}")
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    setup_logging(level=logging.INFO)
    try:
        main()
        print()
        print("Educational Resources:")
        print("• Wikipedia: https://en.wikipedia.org/wiki/Biorhythm_(pseudoscience)")
        print("• The Skeptic's Dictionary: http://skepdic.com/biorhyth.html")
        print('• "Comprehensive Review of Biorhythm Theory" by Terence Hines (1998)')
        print()
        input("Press ENTER to Continue: ")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)