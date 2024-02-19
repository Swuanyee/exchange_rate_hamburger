from sqlalchemy import create_engine, Column, String, Float, Integer, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from openpyxl import load_workbook
from datetime import datetime
import os

# PostgreSQL Database setup
# Format: postgresql://user:password@host:port/database_name
# Make sure to replace 'user', 'password', 'host', 'port', and 'database_name' with your actual PostgreSQL credentials
engine = create_engine('postgresql://data_collection:BKadmin2021@localhost:5432/exchange_rates_db')
Base = declarative_base()

# The rest of your code remains unchanged...

# Model definition
class CurrencyRates(Base):
    __tablename__ = 'currency_rates'

    entry_date = Column(String)
    entry_time = Column(String)
    rate_date = Column(String)
    rate_time = Column(String)
    currency = Column(String)
    face_2_face = Column(Float)
    buy = Column(Float)
    sell = Column(Float)
    visa = Column(Float)
    export = Column(Float)
    remittance = Column(Float)
    usdt = Column(Float)


# Creating the table if it doesn't exist
Base.metadata.create_all(engine)

# Define columns for transaction types as per the Excel file layout
currency_rows = {
    'USD': 4,
    'GBP': 5,
    'EURO': 6,
    'SGD': 7,
    'THB': 14
}

transactions = ['C', 'D', 'E', 'F', 'G', 'H', 'I']

# Path to downloaded Excel file
excel_file = 'exchange_rates.xlsx'
sheet_name = 'Exchange'


def store_exchange_rates():
    Session = sessionmaker(bind=engine)
    session = Session()

    wb = load_workbook('exchange_rates.xlsx', data_only=True)
    sheet = wb['Exchange']

    entry_date = datetime.now().date().strftime('%Y-%m-%d')
    entry_time = datetime.now().time().strftime('%H:%M:%S')
    rate_date = sheet['F2'].value.strftime('%Y-%m-%d')
    rate_time = sheet['H2'].value.strftime('%H:%M:%S')

    for currency, row in currency_rows.items():
        rates = [sheet[f'{col}{row}'].value for col in transactions]

        insert_stmt = text("""
            INSERT INTO currency_rates 
            (entry_date, entry_time, rate_date, rate_time, currency, face_2_face, buy, sell, visa, export, remittance, usdt) 
            VALUES 
            (:entry_date, :entry_time, :rate_date, :rate_time, :currency, :face_2_face, :buy, :sell, :visa, :export, :remittance, :usdt)
        """)

        session.execute(insert_stmt, {
            'entry_date': entry_date,
            'entry_time': entry_time,
            'rate_date': rate_date,
            'rate_time': rate_time,
            'currency': currency,
            'face_2_face': rates[0],
            'buy': rates[1],
            'sell': rates[2],
            'visa': rates[3],
            'export': rates[4],
            'remittance': rates[5],
            'usdt': rates[6]
        })

    session.commit()
    session.close()
    print("Exchange rate information has been added to the database using SQL.")

store_exchange_rates()
