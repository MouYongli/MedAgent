import logging

# Define custom log levels for NOTE and SUCCESS
NOTE_LEVEL_NUM = 25
SUCCESS_LEVEL_NUM = 26
logging.addLevelName(NOTE_LEVEL_NUM, "NOTE")
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")


def note(self, message, *args, **kwargs):
    if self.isEnabledFor(NOTE_LEVEL_NUM):
        self._log(NOTE_LEVEL_NUM, message, args, **kwargs)


def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kwargs)

def progress(self, name, current, total, bar_length=50):
    """Log a progress bar at INFO level, updating on the same line."""
    fraction = current / total if total > 0 else 0
    filled_length = int(round(bar_length * fraction))
    bar = '=' * (filled_length - 1 if filled_length > 0 else 0)
    bar += '>' if ((filled_length > 0) and (filled_length < bar_length)) else ''
    bar += ' ' * (bar_length - filled_length)
    progress_str = f"\r{name}: [{bar}] {int(fraction * 100)}% ({current}/{total})"

    # Apply the INFO color to the progress bar
    info_color = "\033[38;5;208m"  # Orange color for INFO level
    reset_color = "\033[0m"
    colored_progress_str = f"{info_color}{progress_str}{reset_color}"

    # Use the logger's underlying stream to write the progress bar
    self.handlers[0].stream.write(colored_progress_str)
    self.handlers[0].flush()

    # Print a newline character when complete to move to the next line
    if current >= total:
        self.handlers[0].stream.write('\n')

logging.Logger.note = note
logging.Logger.success = success
logging.Logger.progress = progress


class ColorFormatter(logging.Formatter):
    """
    Custom formatter that prints:
      - Time (asctime) in white.
      - Levelname in bold and in the level-specific color.
      - The entire log message in that same color.

    Colors:
      - INFO: Orange (ANSI extended color 208)
      - ERROR: Red
      - NOTE: Italic gray (if supported)
      - SUCCESS: Green
      - DEBUG: Cyan (as an example)
    """
    RESET = "\033[0m"
    BOLD = "\033[1m"
    WHITE = "\033[37m"

    # Define colors for each level.
    # For NOTE, we add italic (3) along with gray (90).
    LOG_COLORS = {
        "INFO": "\033[38;5;208m",  # Orange
        "ERROR": "\033[31m",  # Red
        "NOTE": "\033[3;90m",  # Italic Gray
        "SUCCESS": "\033[32m",  # Green
        "DEBUG": "\033[36m"  # Cyan
    }

    def format(self, record):
        # Format the time in white.
        formatted_time = f"{self.WHITE}{self.formatTime(record, self.datefmt)}{self.RESET}"

        # Get the level name and its color.
        level = record.levelname
        level_color = self.LOG_COLORS.get(level, "")

        # Format the level name as bold in its respective color.
        formatted_level = f"{self.WHITE}[{self.RESET}" + f"{self.BOLD}{level_color}{level}{self.RESET}" + f"{self.WHITE}]{self.RESET}"

        # Format the message text in the same color (retain any formatting like italic for NOTE).
        message = record.getMessage()
        if record.exc_info:
            message += "\n" + self.formatException(record.exc_info)
        formatted_message = f"{level_color}{message}{self.RESET}"

        # Construct the final log string.
        log_line = f"{formatted_time} {formatted_level} {formatted_message}"
        return log_line


# Configure the logger
logger = logging.getLogger("myLogger")
logger.setLevel(logging.DEBUG)

# Create a console handler with the custom formatter.
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = ColorFormatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
