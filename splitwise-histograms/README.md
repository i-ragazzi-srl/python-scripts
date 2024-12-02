# Expense Plotter

A Python application to visualize shared expenses from a CSV file using stacked histogram plots.

## Usage

1. Run the script:
```bash
python expense_plotter.py
```

2. From the GUI:
    - Click "Select CSV File" to load your expense file
    - Choose the desired time scale:
        - Daily
        - Weekly
        - Monthly
    - Select the people whose expenses you want to visualize
    - Click "Generate Plot" to display the chart

## CSV File Format

The CSV file must have the following format:
    ```csv
    Data,Descrizione,Categorie,Costo,Valuta,Persona1,Persona2,...
    2024-11-11,Descrizione spesa,Categoria,100.00,EUR,50.00,50.00,...
    ```

- First row must contain headers
- Columns up to "Currency" are fixed
- Subsequent columns represent people and their respective amounts
- Date must be in YYYY-MM-DD format
- Decimal values must use dot as separator

## Features

- Expense visualization aggregated by category
- Person filter
- Three time scales available (day, week, month)
- Interactive stacked histogram plot
- Category legend
- Multi-currency support (displayed in Euro)

## Troubleshooting

If you encounter "tkinter not found" error:

### Ubuntu/Debian
```bash
sudo apt-get install python3-tk
```

### Fedora
```bash
sudo dnf install python3-tkinter
```

### Windows
Tkinter should be included in the standard Python installation.

## Contributing

Feel free to open issues or pull requests to improve the application.
