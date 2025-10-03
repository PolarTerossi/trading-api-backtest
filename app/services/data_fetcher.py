# app/services/data_fetcher.py

import yfinance as yf
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Symbol, Price

def fetch_and_store_symbol_data(ticker: str, start_date: str, end_date: str):
    """
    Busca dados históricos de um ticker usando yfinance e os armazena no banco de dados.
    """
    db: Session = SessionLocal()
    try:
        # 1. Verifica se o símbolo já existe no banco de dados
        symbol = db.query(Symbol).filter(Symbol.ticker == ticker).first()
        if not symbol:
            print(f"Símbolo {ticker} não encontrado no banco. Cadastrando...")
            # Pega informações do ticker para enriquecer nosso cadastro
            ticker_info = yf.Ticker(ticker).info
            symbol = Symbol(
                ticker=ticker,
                name=ticker_info.get('longName'),
                exchange=ticker_info.get('exchange'),
                currency=ticker_info.get('currency')
            )
            db.add(symbol)
            db.commit()
            db.refresh(symbol)
            print(f"Símbolo {ticker} cadastrado com ID {symbol.id}.")

        # 2. Baixa os dados históricos do Yahoo Finance
        print(f"Baixando dados para {ticker} de {start_date} a {end_date}...")
        data = yf.download(ticker, start=start_date, end=end_date)

        if data.empty:
            print(f"Nenhum dado encontrado para {ticker} no período especificado.")
            return

        # 3. Itera sobre os dados e salva no banco
        prices_to_add = []
        for index, row in data.iterrows():
            # Evita duplicatas caso o script seja rodado mais de uma vez
            price_exists = db.query(Price).filter(Price.symbol_id == symbol.id, Price.date == index.date()).first()
            if not price_exists:
                price = Price(
                    symbol_id=symbol.id,
                    date=index.date(),
                    open=row['Open'],
                    high=row['High'],
                    low=row['Low'],
                    close=row['Close'],
                    volume=int(row['Volume'])
                )
                prices_to_add.append(price)

        if prices_to_add:
            db.add_all(prices_to_add)
            db.commit()
            print(f"Sucesso! {len(prices_to_add)} novos registros de preços para {ticker} foram salvos.")
        else:
            print("Nenhum registro novo para adicionar. O banco de dados já está atualizado.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        db.rollback()
    finally:
        db.close()