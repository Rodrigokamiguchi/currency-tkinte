import tkinter as tk
from tkinter import messagebox
import requests

def obter_taxa(moeda_base, moeda_destino):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{moeda_base}"
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()

        #verificar se a moeda está presente a resposta
        if moeda_destino not in dados['rates']:
            return None

        return dados['rates'][moeda_destino]
    except requests.RequestException as e:
        messagebox.showerror("Erro!", f"erro ao obter a taxa de câmbio: {e}")
        return None
    except KeyError:
       messagebox.showerror("Erro!", "Erro ao processar a resposta da API.")
       return None
    
def converter_valor(valor, taxa):
    return valor * taxa

def exibir_resultados(valor, taxa, valor_convertido, moeda_destino):
    resultado = (
        f"Valor Original: R$ {valor:.2f}"
        f"\nTaxa de Conversão: {taxa:.2f}"
        f"\nValor convertido: {moeda_destino} {valor_convertido:.2f}"
    )
    label_resultado.config(text=resultado)

def calcular():
    try:
        valor = float(entry_valor.get())
        moeda_destino = entry_moeda.get().upper()

        moeda_base = "BRL"
        taxa = obter_taxa(moeda_base, moeda_destino)

        if taxa:
            valor_convertido = converter_valor(valor, taxa)
            exibir_resultados(valor, taxa, valor_convertido, moeda_destino)
        else:
            messagebox.showwarning("Aviso", "Nãoo foi possivel obter a taxa de câmbio. Tente novamente mais tarde.")
            label_resultado.config(text="Erro: Taxa de câmbio não encontrada")

    except ValueError:
        messagebox.showerror("Erro", "Entrada invalida! Por favor, insira um valor númerico.")
        label_resultado.config(texto="Erro: Valor de entrada inválido.")

def main():
    global entry_valor, entry_moeda, label_resultado

    root = tk.Tk()
    root.title("Conversor de Moeda")

    tk.Label(root, text="Informe o valor do produto em reais: R$  ").pack(pady=5)
    entry_valor= tk.Entry(root)
    entry_valor.pack(pady=5)

    tk.Label(root, text="Informe o código da moeda extrangeira (ex.: USD, EUR, GBP ...): ").pack(pady=5)
    entry_moeda = tk.Entry(root)
    entry_moeda.pack(pady=5)

    tk.Button(root, text="Converter", command=calcular).pack(pady=5)
    tk.Button(root, text="Sair", command=root.quit).pack(pady=5)

    label_resultado = tk.Label(root, text="", justify="left", anchor="w", padx=10)
    label_resultado.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()