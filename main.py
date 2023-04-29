import time
import threading
from word_reader import WordReader
from word_viewer import GUI
from average_wpm import AverageWPM
from keyboard import KeyboardListener


wait_time_gain = 0.5
slow_down_multiplier = 1.1


def has_non_char(string):
    for char in string:
        if not char.isalpha():
            return True
    return False


def is_word_long(word):
    return len(word) > 7


def is_word_super_long(word):
    return len(word) > 12


def calculate_wait_time(word):
    ret = 0.2
    if has_non_char(word):
        ret = ret * slow_down_multiplier
    if is_word_long(word):
        ret = ret * slow_down_multiplier
    if is_word_super_long(word):
        ret = ret * slow_down_multiplier * slow_down_multiplier
    return ret  # seconds


def convert_minutes_to_hours(minutes):
    hours = int(minutes // 60)
    minutes_remaining = int(minutes % 60)
    time_str = f"{hours}h {minutes_remaining}min"
    return time_str


def display_words(reader, gui, wpm_calculator, terminate_event, pause_event):
    while True:
        word = reader.get_next_word()
        if terminate_event.is_set():
            break

        # Wait for pause event
        while pause_event.is_set() and not terminate_event.is_set():
            time.sleep(0.1)

        wait_time = calculate_wait_time(word)
        wpm = int(wpm_calculator.get_average_wpm())  # Update average WPM

        if threading.main_thread().is_alive():  # Check if the main thread is still running
            gui.change_wpm(wpm)
            gui.change_word(word)
            time_left = reader.get_words_left()/(wpm+1)
            time_left = convert_minutes_to_hours(time_left)
            gui.set_time_left(time_left)
            time.sleep(wait_time)
        else:
            break


def pause_callback(key, is_paused, pause_event):
    if is_paused:
        pause_event.set()
        print("Paused")
    else:
        pause_event.clear()
        print("Resumed")


def main():
    file_path = "meditations.txt"

    # Read the file using WordReader
    reader = WordReader(file_path)
    reader.read_file()

    # Create GUI instance
    gui = GUI()

    # Create AverageWPM instance
    wpm_calculator = AverageWPM()

    # Create an event to signal termination
    terminate_event = threading.Event()

    # Create an event to pause and resume the display
    pause_event = threading.Event()

    # Create KeyboardListener instance
    keyboard_listener = KeyboardListener(
        lambda key, is_paused: pause_callback(key, is_paused, pause_event)
    )

    # Create a separate thread for GUI update
    display_thread = threading.Thread(target=display_words, args=(
        reader, gui, wpm_calculator, terminate_event, pause_event))
    display_thread.start()

    # Start keyboard listener
    keyboard_listener.start()

    # Run the GUI
    gui.run()

    # Signal termination to the display thread
    terminate_event.set()

    # Wait for the display thread to complete
    display_thread.join()

    # Stop keyboard listener
    keyboard_listener.stop()


if __name__ == "__main__":
    main()
