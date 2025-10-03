# scripts/test_fetch.py

# Adiciona o diretório raiz ao path para permitir importações da 'app'
import sys
import os
from datetime import date
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.data_fetcher import fetch_and_store_symbol_data

if __name__ == "__main__":
    # --- PARÂMETROS ---
    TICKER = "PETR4.SA"  # Ticker da Petrobras na B3
    START_DATE = "2023-01-01"
    END_DATE = date.today().strftime('%Y-%m-%d') # Pega dados até a data de hoje
    # ------------------

    print("Iniciando o script de teste de coleta de dados...")
    fetch_and_store_symbol_data(ticker=TICKER, start_date=START_DATE, end_date=END_DATE)
    print("Script de teste finalizado.")