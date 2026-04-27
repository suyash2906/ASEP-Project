import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from datetime import datetime
from tts import text_to_speech
from stt import speech_to_text
from text_to_sign import text_to_sign
from hand_detection import detect_hands
import pygame
import os

class MultimodalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Communication Assistant")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a2e')
        self.root.attributes('-topmost', True)
        
        pygame.mixer.init()
        
        self.entry = None
        
        self.create_widgets()
        self.animate_title()
    
    def animate_title(self):
        colors = ['#3498db', '#e74c3c', '#9b59b6', '#f39c12', '#27ae60']
        color_idx = 0
        
        def change_color():
            nonlocal color_idx
            self.title_label.config(fg=colors[color_idx % len(colors)])
            color_idx += 1
            self.root.after(1000, change_color)
        
        change_color()
    
    def create_widgets(self):
        # Title
        self.title_label = tk.Label(self.root, text="AI Multimodal Communication System", 
                                   font=('Arial', 24, 'bold'), bg='#1a1a2e', fg='#ecf0f1')
        self.title_label.pack(pady=30)
        
        # Buttons frame
        btn_frame = tk.Frame(self.root, bg='#1a1a2e')
        btn_frame.pack(pady=20)
        
        # Buttons
        tk.Button(btn_frame, text="🔊 Text to Speech", command=self.tts_click, 
                 bg='#3498db', fg='white', font=('Arial', 14, 'bold'), width=25, height=2).pack(pady=8)
        tk.Button(btn_frame, text="🎤 Speech to Text", command=self.stt_click, 
                 bg='#e74c3c', fg='white', font=('Arial', 14, 'bold'), width=25, height=2).pack(pady=8)
        tk.Button(btn_frame, text="✋ Text to Sign Language", command=self.sign_click, 
                 bg='#9b59b6', fg='white', font=('Arial', 14, 'bold'), width=25, height=2).pack(pady=8)
        tk.Button(btn_frame, text="🎤➡️✋ Speech to Sign", command=self.speech_to_sign_click, 
                 bg='#f39c12', fg='white', font=('Arial', 14, 'bold'), width=25, height=2).pack(pady=8)
        tk.Button(btn_frame, text="📹 Camera Hand Detection", command=self.hand_detect_click, 
                 bg='#27ae60', fg='white', font=('Arial', 14, 'bold'), width=25, height=2).pack(pady=8)
        
        # Permanent text input (always visible)
        input_frame = tk.Frame(self.root, bg='#1a1a2e')
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="📝 Text Input (for TTS/Sign):", font=('Arial', 14, 'bold'), 
                fg='#ecf0f1', bg='#1a1a2e').pack()
        self.entry = tk.Entry(input_frame, font=('Arial', 16), width=60)
        self.entry.pack(pady=10)
        
        # Log
        log_frame = tk.Frame(self.root, bg='#16213e')
        log_frame.pack(pady=20, padx=30, fill='both', expand=True)
        
        tk.Label(log_frame, text="📋 Activity Log", font=('Arial', 16, 'bold'), 
                fg='#3498db', bg='#16213e').pack(pady=(15,10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, font=('Arial', 11),
                                                 bg='#0f1419', fg='#ecf0f1', 
                                                 insertbackground='white', relief='solid', bd=1)
        self.log_text.pack(pady=5, padx=15, fill='both', expand=True)
    
    def log(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def tts_click(self):
        text = self.entry.get().strip()
        if text:
            threading.Thread(target=lambda: self.run_tts(text), daemon=True).start()
        else:
            self.log("⚠️ Please enter text")
    
    def run_tts(self, text):
        self.log("🔊 Text-to-Speech...")
        text_to_speech(text)
        self.log("✅ TTS Complete")
    
    def stt_click(self):
        threading.Thread(target=self.stt_thread, daemon=True).start()
    
    def stt_thread(self):
        self.log("🎤 Speech-to-Text...")
        text = speech_to_text()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)
        self.log(f"📝 Result: {text}")
    
    def sign_click(self):
        text = self.entry.get().strip()
        if text:
            threading.Thread(target=lambda: self.run_sign(text), daemon=True).start()
        else:
            self.log("⚠️ Please enter text")
    
    def run_sign(self, text):
        self.log("✋ Text-to-Sign...")
        text_to_sign(text)
        self.log("✅ Sign Language Complete")
    
    def speech_to_sign_click(self):
        threading.Thread(target=self.speech_to_sign_thread, daemon=True).start()
    
    def speech_to_sign_thread(self):
        self.log("🎤➡️✋ Speech-to-Sign...")
        text = speech_to_text()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)
        self.log(f"Transcribed: {text} → Showing signs...")
        text_to_sign(text)
        self.log("✅ Full Pipeline Complete")
    
    def hand_detect_click(self):
        self.log("📹 Hand Detection...")
        threading.Thread(target=lambda: (detect_hands(), self.log("✅ Hand detection closed")), daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = MultimodalApp(root)
    root.mainloop()

