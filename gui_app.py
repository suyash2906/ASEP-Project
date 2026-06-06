"""GUI Application for AI Multimodal Communication System.

This module provides a tkinter-based graphical interface for interacting with
the various modules of the ASEP communication system.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from datetime import datetime
from typing import Optional

import pygame

from tts import text_to_speech
from stt import speech_to_text
from text_to_sign import text_to_sign
from hand_detection import detect_hands


class MultimodalApp:
    """GUI application for AI Multimodal Communication System.

    Provides a user-friendly interface for text-to-speech, speech-to-text,
    text-to-sign language, and hand gesture detection functionalities.
    """

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the application.

        Args:
            root (tk.Tk): The root tkinter window.
        """
        self.root = root
        self.root.title("🤖 AI Communication Assistant")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a1a2e")
        self.root.attributes("-topmost", True)

        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
        except Exception as e:
            print(f"Mixer init warning: {e}")

        self.entry: Optional[tk.Entry] = None
        self.log_text: Optional[scrolledtext.ScrolledText] = None
        self.is_processing = False

        self.create_widgets()
        self.animate_title()

    def animate_title(self) -> None:
        """Animate the title color."""
        colors = ["#3498db", "#e74c3c", "#9b59b6", "#f39c12", "#27ae60"]
        color_idx = 0

        def change_color() -> None:
            nonlocal color_idx
            self.title_label.config(fg=colors[color_idx % len(colors)])
            color_idx += 1
            self.root.after(1000, change_color)

        change_color()

    def create_widgets(self) -> None:
        """Create and layout the GUI widgets."""
        # Title
        self.title_label = tk.Label(
            self.root,
            text="AI Multimodal Communication System",
            font=("Arial", 24, "bold"),
            bg="#1a1a2e",
            fg="#ecf0f1",
        )
        self.title_label.pack(pady=30)

        # Buttons frame
        btn_frame = tk.Frame(self.root, bg="#1a1a2e")
        btn_frame.pack(pady=20)

        # Buttons with improved error handling
        buttons = [
            ("🔊 Text to Speech", self.tts_click, "#3498db"),
            ("🎤 Speech to Text", self.stt_click, "#e74c3c"),
            ("✋ Text to Sign Language", self.sign_click, "#9b59b6"),
            ("🎤➡️✋ Speech to Sign", self.speech_to_sign_click, "#f39c12"),
            ("📹 Camera Hand Detection", self.hand_detect_click, "#27ae60"),
        ]

        for text, command, color in buttons:
            tk.Button(
                btn_frame,
                text=text,
                command=command,
                bg=color,
                fg="white",
                font=("Arial", 14, "bold"),
                width=25,
                height=2,
            ).pack(pady=8)

        # Text input
        input_frame = tk.Frame(self.root, bg="#1a1a2e")
        input_frame.pack(pady=20)

        tk.Label(
            input_frame,
            text="📝 Text Input (for TTS/Sign):",
            font=("Arial", 14, "bold"),
            fg="#ecf0f1",
            bg="#1a1a2e",
        ).pack()
        self.entry = tk.Entry(input_frame, font=("Arial", 16), width=60)
        self.entry.pack(pady=10)

        # Activity Log
        log_frame = tk.Frame(self.root, bg="#16213e")
        log_frame.pack(pady=20, padx=30, fill="both", expand=True)

        tk.Label(
            log_frame,
            text="📋 Activity Log",
            font=("Arial", 16, "bold"),
            fg="#3498db",
            bg="#16213e",
        ).pack(pady=(15, 10))

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=12,
            font=("Arial", 11),
            bg="#0f1419",
            fg="#ecf0f1",
            insertbackground="white",
            relief="solid",
            bd=1,
        )
        self.log_text.pack(pady=5, padx=15, fill="both", expand=True)

    def log(self, message: str) -> None:
        """Log a message to the activity log.

        Args:
            message (str): Message to log.
        """
        if self.log_text:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.log_text.see(tk.END)
            self.root.update()

    def _run_in_thread(self, func, *args) -> None:
        """Run a function in a separate thread to prevent UI freezing.

        Args:
            func: The function to run.
            *args: Arguments to pass to the function.
        """
        if self.is_processing:
            messagebox.showwarning("In Progress", "A task is already running. Please wait.")
            return

        self.is_processing = True

        def wrapper() -> None:
            try:
                func(*args)
            except Exception as e:
                self.log(f"❌ Error: {str(e)}")
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            finally:
                self.is_processing = False

        thread = threading.Thread(target=wrapper, daemon=True)
        thread.start()

    def tts_click(self) -> None:
        """Handle Text-to-Speech button click."""
        if not self.entry:
            messagebox.showerror("Error", "Entry widget not found")
            return

        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("Empty Input", "Please enter some text for TTS.")
            self.log("⚠️ Empty text input for TTS")
            return

        self.log("🔊 Text-to-Speech...")
        self._run_in_thread(text_to_speech, text)
        self.log("✅ TTS Complete")

    def stt_click(self) -> None:
        """Handle Speech-to-Text button click."""
        self.log("🎤 Speech-to-Text...")
        self._run_in_thread(self._stt_wrapper)

    def _stt_wrapper(self) -> None:
        """Wrapper for STT to update UI."""
        result = speech_to_text()
        if self.entry:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, result)
        self.log(f"📝 Result: {result}")

    def sign_click(self) -> None:
        """Handle Text-to-Sign button click."""
        if not self.entry:
            messagebox.showerror("Error", "Entry widget not found")
            return

        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("Empty Input", "Please enter some text for Sign Language.")
            self.log("⚠️ Empty text input for Sign Language")
            return

        self.log("✋ Text-to-Sign...")
        self._run_in_thread(text_to_sign, text)
        self.log("✅ Sign Language Complete")

    def speech_to_sign_click(self) -> None:
        """Handle Speech-to-Sign button click."""
        self.log("🎤➡️✋ Speech-to-Sign...")
        self._run_in_thread(self._speech_to_sign_wrapper)

    def _speech_to_sign_wrapper(self) -> None:
        """Wrapper for Speech-to-Sign pipeline."""
        text = speech_to_text()
        if self.entry:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, text)
        self.log(f"📝 Transcribed: {text}")
        self.log("✋ Showing signs...")
        text_to_sign(text)
        self.log("✅ Full Pipeline Complete")

    def hand_detect_click(self) -> None:
        """Handle Hand Detection button click."""
        self.log("📹 Hand Detection...")
        self._run_in_thread(self._hand_detect_wrapper)

    def _hand_detect_wrapper(self) -> None:
        """Wrapper for hand detection."""
        detect_hands()
        self.log("✅ Hand detection closed")


def main() -> None:
    """Run the GUI application."""
    root = tk.Tk()
    app = MultimodalApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
