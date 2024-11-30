import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog
import os


class SpesePlotter:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizzatore Spese")
        self.df = None
        self.persone = []

        # Frame principale
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Bottone per selezionare il file
        self.file_button = ttk.Button(main_frame, text="Seleziona File CSV", command=self.load_file)
        self.file_button.grid(row=0, column=0, columnspan=2, pady=5)

        # Label per mostrare il file selezionato
        self.file_label = ttk.Label(main_frame, text="Nessun file selezionato")
        self.file_label.grid(row=1, column=0, columnspan=2, pady=5)

        # Frame per la scala temporale
        scale_frame = ttk.LabelFrame(main_frame, text="Scala Temporale", padding="5")
        scale_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

        self.scale_var = tk.StringVar(value="D")
        scales = [
            ("Giornaliera", "D"),
            ("Settimanale", "W"),
            ("Mensile", "M")
        ]

        for i, (text, value) in enumerate(scales):
            ttk.Radiobutton(scale_frame, text=text, value=value,
                            variable=self.scale_var).grid(row=0, column=i, padx=5)

        # Frame per la selezione delle persone
        self.people_frame = ttk.LabelFrame(main_frame, text="Seleziona Persone", padding="5")
        self.people_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

        # Bottone per plottare
        self.plot_button = ttk.Button(main_frame, text="Genera Grafico",
                                      command=self.plot_data, state=tk.DISABLED)
        self.plot_button.grid(row=4, column=0, columnspan=2, pady=5)

        self.checkboxes = []
        self.checkbox_vars = []

    def load_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if file_path:
            self.file_label.config(text=os.path.basename(file_path))
            self.df = pd.read_csv(file_path)

            # Identifica le colonne delle persone
            colonne_base = ['Data', 'Descrizione', 'Categorie', 'Costo', 'Valuta']
            self.persone = self.df.columns[len(colonne_base):].tolist()

            # Aggiorna i checkbox
            for cb in self.checkboxes:
                cb.destroy()
            self.checkboxes = []
            self.checkbox_vars = []

            for i, persona in enumerate(self.persone):
                var = tk.BooleanVar(value=True)
                self.checkbox_vars.append(var)
                cb = ttk.Checkbutton(self.people_frame, text=persona, variable=var)
                cb.grid(row=i // 3, column=i % 3, sticky=tk.W, padx=5)
                self.checkboxes.append(cb)

            self.plot_button.config(state=tk.NORMAL)

    def plot_data(self):
        if self.df is None:
            return

        # Ottieni le persone selezionate
        selected_people = [persona for persona, var in zip(self.persone, self.checkbox_vars)
                           if var.get()]

        if not selected_people:
            tk.messagebox.showwarning("Attenzione", "Seleziona almeno una persona!")
            return

        # Converti la colonna Data in datetime
        self.df['Data'] = pd.to_datetime(self.df['Data'])

        # Filtra il DataFrame
        df_filtered = self.df[['Data', 'Categorie'] + selected_people]

        # Raggruppa per data e categoria
        df_grouped = df_filtered.groupby([pd.Grouper(key='Data', freq=self.scale_var.get()),
                                          'Categorie']).sum()
        df_grouped = df_grouped.reset_index()

        # Pivot per ottenere le categorie come colonne
        df_pivot = df_grouped.pivot(index='Data', columns='Categorie',
                                    values=selected_people)

        # Riempi i valori NaN con 0
        df_pivot = df_pivot.fillna(0)

        # Plot
        plt.figure(figsize=(12, 6))
        df_pivot.plot(kind='bar', stacked=True)
        plt.title('Spese Cumulative per Categoria')
        plt.xlabel('Data')
        plt.ylabel('Euro')
        plt.legend(title='Categorie', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.xticks(rotation=45)
        plt.show()


# Avvio dell'applicazione
if __name__ == "__main__":
    root = tk.Tk()
    app = SpesePlotter(root)
    root.mainloop()