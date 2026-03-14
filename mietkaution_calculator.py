import tkinter as tk
from tkinter import ttk, messagebox

class MietkautionCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Mietkaution Rechner")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = tk.Frame(root, bg="#f5f5f5", padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🏠 Mietkaution Rechner",
            font=("Segoe UI", 20, "bold"),
            bg="#f5f5f5",
            fg="#333"
        )
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Berechnen Sie Ihre Mietkaution schnell und einfach",
            font=("Segoe UI", 10),
            bg="#f5f5f5",
            fg="#666"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Kaltmiete input
        kaltmiete_frame = tk.Frame(main_frame, bg="#f5f5f5")
        kaltmiete_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            kaltmiete_frame,
            text="Kaltmiete (€)",
            font=("Segoe UI", 11, "bold"),
            bg="#f5f5f5",
            fg="#555"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.kaltmiete_var = tk.StringVar()
        kaltmiete_entry = tk.Entry(
            kaltmiete_frame,
            textvariable=self.kaltmiete_var,
            font=("Segoe UI", 12),
            relief=tk.FLAT,
            bg="white",
            bd=2
        )
        kaltmiete_entry.pack(fill=tk.X, ipady=8)
        
        # Months selection
        months_frame = tk.Frame(main_frame, bg="#f5f5f5")
        months_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            months_frame,
            text="Anzahl der Monatsmieten",
            font=("Segoe UI", 11, "bold"),
            bg="#f5f5f5",
            fg="#555"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        self.months_var = tk.IntVar(value=3)
        
        radio_frame = tk.Frame(months_frame, bg="#f5f5f5")
        radio_frame.pack(fill=tk.X)
        
        for i, month in enumerate([1, 2, 3]):
            radio = tk.Radiobutton(
                radio_frame,
                text=f"{month} Monat" if month == 1 else f"{month} Monate",
                variable=self.months_var,
                value=month,
                font=("Segoe UI", 10),
                bg="#f5f5f5",
                activebackground="#f5f5f5",
                selectcolor="#667eea"
            )
            radio.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        # Nebenkosten input
        nebenkosten_frame = tk.Frame(main_frame, bg="#f5f5f5")
        nebenkosten_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            nebenkosten_frame,
            text="Nebenkosten (€) - Optional",
            font=("Segoe UI", 11, "bold"),
            bg="#f5f5f5",
            fg="#555"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.nebenkosten_var = tk.StringVar()
        nebenkosten_entry = tk.Entry(
            nebenkosten_frame,
            textvariable=self.nebenkosten_var,
            font=("Segoe UI", 12),
            relief=tk.FLAT,
            bg="white",
            bd=2
        )
        nebenkosten_entry.pack(fill=tk.X, ipady=8)
        
        # Calculate button
        calc_button = tk.Button(
            main_frame,
            text="Kaution Berechnen",
            command=self.calculate,
            font=("Segoe UI", 12, "bold"),
            bg="#667eea",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#5568d3",
            activeforeground="white"
        )
        calc_button.pack(fill=tk.X, ipady=10, pady=(0, 20))
        
        # Result frame
        self.result_frame = tk.Frame(main_frame, bg="#e8eaf6", relief=tk.FLAT, bd=0)
        self.result_frame.pack(fill=tk.BOTH, expand=True)
        self.result_frame.pack_forget()  # Hide initially
        
        # Info box
        info_frame = tk.Frame(main_frame, bg="#e3f2fd", relief=tk.FLAT)
        info_frame.pack(fill=tk.X, pady=(20, 0))
        
        info_text = "ℹ️ Hinweis: In Deutschland beträgt die Mietkaution\nmaximal 3 Monatsmieten der Kaltmiete.\nDie Kaution kann in 3 Raten gezahlt werden."
        tk.Label(
            info_frame,
            text=info_text,
            font=("Segoe UI", 9),
            bg="#e3f2fd",
            fg="#1976d2",
            justify=tk.LEFT
        ).pack(padx=15, pady=15)
    
    def format_currency(self, amount):
        return f"{amount:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
    
    def calculate(self):
        try:
            kaltmiete = float(self.kaltmiete_var.get().replace(",", "."))
            if kaltmiete <= 0:
                raise ValueError("Kaltmiete muss größer als 0 sein")
        except ValueError:
            messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Kaltmiete ein.")
            return
        
        try:
            nebenkosten = float(self.nebenkosten_var.get().replace(",", ".")) if self.nebenkosten_var.get() else 0
        except ValueError:
            nebenkosten = 0
        
        months = self.months_var.get()
        warmmiete = kaltmiete + nebenkosten
        kaution = kaltmiete * months
        
        # Clear previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Show result frame
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Result items
        results = [
            ("Kaltmiete:", self.format_currency(kaltmiete)),
            ("Nebenkosten:", self.format_currency(nebenkosten)),
            ("Warmmiete:", self.format_currency(warmmiete)),
            ("Anzahl Monate:", str(months))
        ]
        
        for label, value in results:
            item_frame = tk.Frame(self.result_frame, bg="#e8eaf6")
            item_frame.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(
                item_frame,
                text=label,
                font=("Segoe UI", 10, "bold"),
                bg="#e8eaf6",
                fg="#555"
            ).pack(side=tk.LEFT)
            
            tk.Label(
                item_frame,
                text=value,
                font=("Segoe UI", 10, "bold"),
                bg="#e8eaf6",
                fg="#333"
            ).pack(side=tk.RIGHT)
        
        # Total
        total_frame = tk.Frame(self.result_frame, bg="white", relief=tk.FLAT)
        total_frame.pack(fill=tk.X, padx=20, pady=(15, 20))
        
        total_inner = tk.Frame(total_frame, bg="white")
        total_inner.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(
            total_inner,
            text="Mietkaution:",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#555"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            total_inner,
            text=self.format_currency(kaution),
            font=("Segoe UI", 16, "bold"),
            bg="white",
            fg="#667eea"
        ).pack(side=tk.RIGHT)

def main():
    root = tk.Tk()
    app = MietkautionCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
