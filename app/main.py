# app/main.py
from fastapi import FastAPI

app = FastAPI(
    title="Trading Backtest API",
    description="API para executar backtests de estratégias de trading.",
    version="0.1.0"
)

@app.get("/health", tags=["Health Check"])
def read_root():
    """Verifica a saúde da aplicação."""
    return {"status": "ok", "message": "API is running!"}