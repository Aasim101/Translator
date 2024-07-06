import tkinter as tk
from tkinter import ttk
from googletrans import Translator, LANGUAGES

class TranslatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Enhanced Translator")
        self.geometry("800x650")
        self.minsize(500, 550)
        self.config(bg='#F0F0F0')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="Translator", font=("Arial", 24, "bold"), bg='#F0F0F0')
        title_label.grid(row=0, column=0, pady=20, sticky="ew")

        # Source Text
        source_frame = ttk.LabelFrame(self, text="Source Text")
        source_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        source_frame.grid_columnconfigure(0, weight=1)

        self.source_text = tk.Text(source_frame, wrap=tk.WORD, font=("Arial", 12), height=7)
        self.source_text.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        source_scroll = ttk.Scrollbar(source_frame, orient="vertical", command=self.source_text.yview)
        source_scroll.grid(row=0, column=1, sticky="ns")
        self.source_text.configure(yscrollcommand=source_scroll.set)

        # Language selection and translate button
        controls_frame = ttk.Frame(self)
        controls_frame.grid(row=2, column=0, pady=10, sticky="ew")
        controls_frame.grid_columnconfigure(1, weight=1)

        lang_list = ["Auto-detect"] + list(LANGUAGES.values())
        self.source_lang = ttk.Combobox(controls_frame, values=lang_list, width=20)
        self.source_lang.set("Auto-detect")
        self.source_lang.grid(row=0, column=0, padx=5)

        self.translate_button = ttk.Button(controls_frame, text="Translate", command=self.translate)
        self.translate_button.grid(row=0, column=1, padx=5)

        self.target_lang = ttk.Combobox(controls_frame, values=list(LANGUAGES.values()), width=20)
        self.target_lang.set("english")
        self.target_lang.grid(row=0, column=2, padx=5)

        # Translated Text
        target_frame = ttk.LabelFrame(self, text="Translated Text")
        target_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        target_frame.grid_columnconfigure(0, weight=1)

        self.target_text = tk.Text(target_frame, wrap=tk.WORD, font=("Arial", 12), height=7, state="disabled")
        self.target_text.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        target_scroll = ttk.Scrollbar(target_frame, orient="vertical", command=self.target_text.yview)
        target_scroll.grid(row=0, column=1, sticky="ns")
        self.target_text.configure(yscrollcommand=target_scroll.set)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, sticky="ew")

    def translate(self):
        try:
            self.status_var.set("Translating...")
            self.update_idletasks()

            translator = Translator()
            source_text = self.source_text.get(1.0, tk.END).strip()
            source_lang = self.source_lang.get()
            target_lang = self.target_lang.get()

            # Handle auto-detection
            if source_lang == "Auto-detect":
                detected = translator.detect(source_text)
                source_lang = detected.lang
            else:
                source_lang = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(source_lang)]

            target_lang = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(target_lang)]

            translation = translator.translate(source_text, src=source_lang, dest=target_lang)

            self.target_text.config(state="normal")
            self.target_text.delete(1.0, tk.END)
            self.target_text.insert(tk.END, translation.text)
            self.target_text.config(state="disabled")

            detected_lang = LANGUAGES.get(source_lang, "Unknown")
            self.status_var.set(f"Translated from {detected_lang} to {LANGUAGES[target_lang]}")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")

#Main
app = TranslatorApp()
app.mainloop()