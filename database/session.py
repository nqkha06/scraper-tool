from sqlalchemy import create_engine, text

DATABASE_URL = "sqlite:///database/app.db"

engine = create_engine(
    DATABASE_URL,
    future=True,
    echo=False
)

def get_conn():
    return engine.connect()
