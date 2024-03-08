import time
import sys

# Define your custom bar sequence
bar_slots = "🍒🍋🔔💰🚁🛩️🛸🚀🛰️"
drone_str = "DRONE2MAX!"
bar_width = len(drone_str)

# Simulate progress
for i in range(101):
    # Determine the index of the next letter to reveal
    letter_index = i // 10
    # Create the bar string with emojis and the portion of the DRONE2MAX string revealed
    bar_str = drone_str[:letter_index] + bar_slots[((i % 10) - 1) % len(bar_slots)] * (bar_width - letter_index)
    # Ensure the bar string isn't longer than the bar width
    bar_str = bar_str[:bar_width]
    
    # Print the progress bar
    sys.stdout.write(f'\r[{bar_str}] {i}%')
    sys.stdout.flush()
    
    # Simulate some work
    time.sleep(0.1)

# Print a new line at the end
print()
