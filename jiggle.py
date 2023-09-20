import asyncio
import argparse
import sys
import logging
import random
from screeninfo import get_monitors
import pydirectinput as pdi

MAX_CHANGE = 100

# Get the current screen size
monitors = get_monitors()
if not monitors:
    print("Error: Unable to detect screen information. Exiting.")
    sys.exit(1)

screen_width = monitors[0].width
screen_height = monitors[0].height


# Create a custom logging formatter
class MyFormatter(logging.Formatter):
    def format(self, record):
        if hasattr(record, 'position') and hasattr(record, 'change'):
            return f"[{record.asctime}] Current Position: ({record.position}), Change: ({record.change})"
        return super().format(record)


# Configure the logging
formatter = MyFormatter('%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.basicConfig(level=logging.DEBUG, format='%(message)s', handlers=[logging.StreamHandler(sys.stdout)])
logging.getLogger().handlers[0].setFormatter(formatter)


async def move_mouse(max_change, wait_time, enable_logging):
    if max_change > MAX_CHANGE:
        print(f"Error: Maximum change cannot exceed {MAX_CHANGE} pixels. Exiting.")
        sys.exit(1)

    if wait_time <= 0:
        print("Error: Wait time must be a positive value. Exiting.")
        sys.exit(1)

    while True:
        current_position = pdi.position()

        # Generate random changes within the specified maximum
        x_change = random.randint(-max_change, max_change)
        y_change = random.randint(-max_change, max_change)

        # Check if the cursor is within the screen boundaries
        if 0 <= current_position[0] + x_change <= screen_width and 0 <= current_position[1] + y_change <= screen_height:
            if x_change != 0 or y_change != 0:
                pdi.move(x_change, y_change)

            # Log the current cursor position and pixel changes if logging is enabled
            if enable_logging:
                log_message = f"Current Position: ({current_position[0]}, {current_position[1]}), Change: ({x_change}, {y_change})"
                logging.debug(log_message)

        await asyncio.sleep(wait_time)


async def main():
    parser = argparse.ArgumentParser(description='Move mouse cursor periodically')
    parser.add_argument('-m', '--max_change', type=int, default=10, help='Maximum change in pixels (default 10)')
    parser.add_argument('-w', '--wait_time', type=int, default=60, help='Change in wait time (must be positive)')
    parser.add_argument('-l', '--log', action='store_true', help='Enable logging')
    args = parser.parse_args()

    await asyncio.gather(move_mouse(args.max_change, args.wait_time, args.log))


if __name__ == '__main__':
    asyncio.run(main())
