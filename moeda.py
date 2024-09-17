import tkinter as tk
from tkinter import messagebox
import requests

def get_exchange_rate(base_currency, target_currency):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Check if the target currency is present in the response
        if target_currency not in data['rates']:
            return None

        return data['rates'][target_currency]
    except requests.RequestException as e:
        messagebox.showerror("Error!", f"Error getting exchange rate: {e}")
        return None
    except KeyError:
        messagebox.showerror("Error!", "Error processing the API response.")
        return None

def convert_value(value, rate):
    return value * rate

def display_results(value, rate, converted_value, target_currency):
    result = (
        f"Original Amount: R$ {value:.2f}\n"
        f"Exchange Rate: {rate:.2f}\n"
        f"Converted Value: {target_currency} {converted_value:.2f}"
    )
    label_result.config(text=result)  # Update the display with the result

def calculate():
    try:
        value = float(entry_value.get())
        target_currency = entry_currency.get().upper()

        base_currency = "BRL"
        rate = get_exchange_rate(base_currency, target_currency)

        if rate:
            converted_value = convert_value(value, rate)
            display_results(value, rate, converted_value, target_currency)
        else:
            messagebox.showwarning("Warning", "Could not get the exchange rate. Please try again later.")
            label_result.config(text="Error: Exchange rate not found.")

    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please enter a numeric value.")
        label_result.config(text="Error: Invalid input value.")

def main():
    global entry_value, entry_currency, label_result

    root = tk.Tk()
    root.title("Currency Converter")

    tk.Label(root, text="Enter the product value in BRL: R$ ").pack(pady=5)
    entry_value = tk.Entry(root)
    entry_value.pack(pady=5)

    tk.Label(root, text="Enter the target currency code (e.g., USD, EUR, GBP ...): ").pack(pady=5)
    entry_currency = tk.Entry(root)
    entry_currency.pack(pady=5)

    tk.Button(root, text="Convert", command=calculate).pack(pady=5)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=5)

    # Label to display the results
    label_result = tk.Label(root, text="", justify="left", anchor="w", padx=10)
    label_result.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
