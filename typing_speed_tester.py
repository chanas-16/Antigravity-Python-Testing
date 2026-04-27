import tkinter as tk
from tkinter import font
import random
import time

class TypingSpeedTester:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Tester")
        self.root.geometry("800x650")
        self.root.configure(bg="#f4f4f9")

        # List of predefined sentences (at least 10)
        self.sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "Programming is the art of telling another human what one wants the computer to do.",
            "In software, the most beautiful code is the code that is never written.",
            "A journey of a thousand miles begins with a single step.",
            "To be or not to be, that is the question.",
            "All that glitters is not gold.",
            "The only way to do great work is to love what you do.",
            "Simplicity is the ultimate sophistication.",
            "Code is like humor. When you have to explain it, it's bad.",
            "First, solve the problem. Then, write the code."
        ]

        self.current_sentence = ""
        self.start_time = 0
        self.is_running = False
        self.is_ready = False

        self.setup_ui()

    def setup_ui(self):
        # Clean and modern fonts
        self.title_font = font.Font(family="Helvetica", size=26, weight="bold")
        self.text_font = font.Font(family="Helvetica", size=16)
        self.info_font = font.Font(family="Helvetica", size=14)

        # Main Layout Frame
        self.main_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.main_frame.pack(expand=True, fill="both", padx=40, pady=30)

        # Title
        self.title_label = tk.Label(self.main_frame, text="Typing Speed Tester", font=self.title_font, bg="#f4f4f9", fg="#2c3e50")
        self.title_label.pack(pady=(0, 20))

        # Sentence Display Box (Read-only)
        self.sentence_display = tk.Text(self.main_frame, font=self.text_font, height=4, width=60, wrap="word", state="disabled", bg="#ffffff", relief="flat", padx=15, pady=15)
        self.sentence_display.pack(pady=10)
        
        # Tags for highlighting correct/incorrect characters in real-time
        self.sentence_display.tag_configure("correct", foreground="#27ae60")
        self.sentence_display.tag_configure("incorrect", foreground="#e74c3c", background="#fadbd8")

        # Info Frame (Timer & Mistakes count)
        self.info_frame = tk.Frame(self.main_frame, bg="#f4f4f9")
        self.info_frame.pack(fill="x", pady=10)
        
        self.timer_label = tk.Label(self.info_frame, text="Time: 0.0s", font=self.info_font, bg="#f4f4f9", fg="#7f8c8d")
        self.timer_label.pack(side="left", padx=20)

        self.mistakes_label = tk.Label(self.info_frame, text="Mistakes: 0", font=self.info_font, bg="#f4f4f9", fg="#7f8c8d")
        self.mistakes_label.pack(side="right", padx=20)

        # Input Box
        self.input_box = tk.Text(self.main_frame, font=self.text_font, height=4, width=60, wrap="word", state="disabled", bg="#e0e0e0", relief="flat", padx=15, pady=15)
        self.input_box.pack(pady=10)
        self.input_box.bind("<KeyRelease>", self.check_typing)

        # Buttons Frame
        self.btn_frame = tk.Frame(self.main_frame, bg="#f4f4f9")
        self.btn_frame.pack(pady=25)

        # Buttons with flat design and modern colors
        self.start_btn = tk.Button(self.btn_frame, text="Start Test", font=self.info_font, command=self.start_test, bg="#2ecc71", fg="white", activebackground="#27ae60", activeforeground="white", width=12, relief="flat", cursor="hand2")
        self.start_btn.grid(row=0, column=0, padx=15)

        self.submit_btn = tk.Button(self.btn_frame, text="Submit", font=self.info_font, command=self.submit_test, state="disabled", bg="#bdc3c7", fg="white", activebackground="#3498db", activeforeground="white", width=12, relief="flat", cursor="hand2")
        self.submit_btn.grid(row=0, column=1, padx=15)

        self.reset_btn = tk.Button(self.btn_frame, text="Reset", font=self.info_font, command=self.reset_test, bg="#e74c3c", fg="white", activebackground="#c0392b", activeforeground="white", width=12, relief="flat", cursor="hand2")
        self.reset_btn.grid(row=0, column=2, padx=15)

        # Results Label
        self.results_label = tk.Label(self.main_frame, text="", font=font.Font(family="Helvetica", size=20, weight="bold"), bg="#f4f4f9", fg="#2c3e50")
        self.results_label.pack(pady=20)

    def start_test(self):
        if self.is_running or self.is_ready:
            return
        
        # Select a random predefined sentence
        self.current_sentence = random.choice(self.sentences)
        
        # Display the sentence
        self.sentence_display.config(state="normal")
        self.sentence_display.delete("1.0", tk.END)
        self.sentence_display.insert("1.0", self.current_sentence)
        self.sentence_display.config(state="disabled")

        # Enable input box and wait for user to type
        self.input_box.config(state="normal", bg="#ffffff")
        self.input_box.delete("1.0", tk.END)
        self.input_box.focus()

        # Reset labels
        self.results_label.config(text="")
        self.mistakes_label.config(text="Mistakes: 0")
        self.timer_label.config(text="Time: 0.0s")
        
        # Test is ready, timer starts on first keypress
        self.is_ready = True
        self.is_running = False
        
        # Update button states and colors
        self.start_btn.config(state="disabled", bg="#a9dfbf")
        self.submit_btn.config(state="normal", bg="#3498db")

    def update_timer(self):
        if self.is_running:
            elapsed_time = time.time() - self.start_time
            self.timer_label.config(text=f"Time: {elapsed_time:.1f}s")
            self.root.after(100, self.update_timer)

    def check_typing(self, event):
        if not self.is_ready:
            return

        # Start timer on first keystroke when test is ready
        if not self.is_running:
            # Ignore modifier keys that shouldn't trigger the timer
            if event.keysym in ("Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R", "Caps_Lock", "Tab"):
                return
            self.start_time = time.time()
            self.is_running = True
            self.update_timer()

        typed_text = self.input_box.get("1.0", "end-1c")
        
        # Clear previous text highlighting
        self.sentence_display.config(state="normal")
        self.sentence_display.tag_remove("correct", "1.0", tk.END)
        self.sentence_display.tag_remove("incorrect", "1.0", tk.END)
        
        mistakes = 0
        for i in range(len(typed_text)):
            if i < len(self.current_sentence):
                start_index = f"1.{i}"
                end_index = f"1.{i+1}"
                if typed_text[i] == self.current_sentence[i]:
                    self.sentence_display.tag_add("correct", start_index, end_index)
                else:
                    self.sentence_display.tag_add("incorrect", start_index, end_index)
                    mistakes += 1
            else:
                # Extra typed characters count as mistakes
                mistakes += 1
                
        self.sentence_display.config(state="disabled")
        self.mistakes_label.config(text=f"Mistakes: {mistakes}")

    def submit_test(self):
        if not self.is_ready:
            return
            
        # Stop timer
        self.is_running = False
        self.is_ready = False
        elapsed_time = time.time() - self.start_time if self.start_time > 0 else 0
        
        typed_text = self.input_box.get("1.0", "end-1c")
        
        # Calculate Accuracy (compare typed text with original sentence)
        correct_chars = 0
        for i, c in enumerate(typed_text):
            if i < len(self.current_sentence) and c == self.current_sentence[i]:
                correct_chars += 1
                
        total_chars = max(len(self.current_sentence), len(typed_text))
        accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 0

        # Calculate WPM: (number of words typed / time in minutes)
        words_typed = len(typed_text.split())
        time_in_minutes = elapsed_time / 60
        wpm = (words_typed / time_in_minutes) if time_in_minutes > 0 else 0

        # Disable input to stop further typing
        self.input_box.config(state="disabled", bg="#e0e0e0")
        
        # Reset buttons
        self.start_btn.config(state="normal", bg="#2ecc71")
        self.submit_btn.config(state="disabled", bg="#bdc3c7")

        # Display final results with color-coding
        if accuracy >= 90:
            result_color = "#27ae60" # Green
        elif accuracy >= 70:
            result_color = "#f39c12" # Orange
        else:
            result_color = "#c0392b" # Red
            
        self.results_label.config(text=f"WPM: {wpm:.0f}   |   Accuracy: {accuracy:.1f}%", fg=result_color)

    def reset_test(self):
        # Reset logical state
        self.is_running = False
        self.is_ready = False
        
        # Clear displays
        self.sentence_display.config(state="normal")
        self.sentence_display.delete("1.0", tk.END)
        self.sentence_display.config(state="disabled")
        
        self.input_box.config(state="normal", bg="#e0e0e0")
        self.input_box.delete("1.0", tk.END)
        self.input_box.config(state="disabled")
        
        self.timer_label.config(text="Time: 0.0s")
        self.mistakes_label.config(text="Mistakes: 0")
        self.results_label.config(text="")
        
        # Reset buttons
        self.start_btn.config(state="normal", bg="#2ecc71")
        self.submit_btn.config(state="disabled", bg="#bdc3c7")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTester(root)
    root.mainloop()
