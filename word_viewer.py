import tkinter as tk
import threading
import queue


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Word Viewer")
        self.window.geometry("600x800")
        self.window.protocol("WM_DELETE_WINDOW",
                             self.on_close)  # Bind close event

        self.window.configure(bg="#333333")  # Set background color

        self.word_label = tk.Label(
            self.window, text="", font=("Arial", 34), bg="#222222", fg="white"
        )
        self.word_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.wpm_label = tk.Label(
            self.window, text="WPM: 0", font=("Arial", 12), bg="#333333", fg="white"
        )
        self.wpm_label.place(relx=1.0, rely=0, anchor=tk.NE)

        self.time_left_label = tk.Label(
            self.window, text="Time Left: 0", font=("Arial", 12), bg="#333333", fg="white"
        )
        self.time_left_label.place(relx=1.0, rely=1.0, anchor=tk.SE)

        self.wpm = 0

        self.queue = queue.Queue()  # Thread-safe queue for GUI updates
        self.is_running = True  # Flag to track GUI running status

    def change_word(self, new_word):
        self.queue.put(("word", new_word))  # Put update in the queue

    def change_wpm(self, new_wpm):
        self.queue.put(("wpm", new_wpm))  # Put update in the queue

    def set_time_left(self, time_left):
        self.queue.put(("time_left", time_left))  # Put update in the queue

    def update_gui(self):
        while self.is_running:
            try:
                update_type, value = self.queue.get(
                    block=False)  # Get update from the queue
                if update_type == "word":
                    self.word_label.config(text=value)
                elif update_type == "wpm":
                    self.wpm = value
                    self.wpm_label.config(text=f"WPM: {self.wpm}")
                elif update_type == "time_left":
                    self.time_left_label.config(text=f"Time Left: {value}")
            except queue.Empty:
                break

        if self.is_running:
            self.window.after(100, self.update_gui)  # Schedule the next update

    def run(self):
        self.window.after(100, self.update_gui)  # Start the GUI update loop
        self.window.mainloop()

    def on_close(self):
        # Handle the window close event here
        self.is_running = False  # Set running status to False
        self.window.destroy()


# Example usage
if __name__ == "__main__":
    gui = GUI()
    gui.change_word("Hello")
    gui.change_wpm(60)
    gui.set_time_left(10)
    gui.run()
