from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from openpyxl import load_workbook
from datetime import datetime
import os

# Database setup
engine = create_engine('sqlite:///exchange_rates.db')
Base = declarative_base()
print("Current working directory:", os.getcwd())


# Model definition
class CurrencyRates(Base):
    __tablename__ = 'currency_rates'

    id = Column(Integer, primary_key=True)
    entry_date = Column(String)
    entry_time = Column(String)
    rate_date = Column(String)
    rate_time = Column(String)
    currency = Column(String, unique=True)
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

    wb = load_workbook(excel_file, data_only=True)
    sheet = wb[sheet_name]

    # Fetch and format the entry date and time
    entry_date = datetime.now().date().strftime('%Y-%m-%d')
    entry_time = datetime.now().time().strftime('%H:%M:%S')

    # Fetch the rate date and time
    rate_date = sheet['F2'].value.strftime('%Y-%m-%d')
    rate_time = sheet['H2'].value.strftime('%H:%M:%S')

    for currency, row in currency_rows.items():
        rates = [sheet[f'{col}{row}'].value for col in transactions]

        # Attempt to find an existing record for this currency
        currency_rate = session.query(CurrencyRates).filter_by(currency=currency).first()

        # If found, update existing record
        if currency_rate:
            currency_rate.entry_date, currency_rate.entry_time, \
                currency_rate.rate_date, currency_rate.rate_time, \
                currency_rate.face_2_face, currency_rate.buy, currency_rate.sell, \
                currency_rate.visa, currency_rate.export, currency_rate.remittance, \
                currency_rate.usdt = entry_date, entry_time, rate_date, rate_time, *rates
        else:
            # Otherwise, create a new record
            new_currency_rate = CurrencyRates(entry_date=entry_date, entry_time=entry_time,
                                              rate_date=rate_date, rate_time=rate_time,
                                              currency=currency, face_2_face=rates[0],
                                              buy=rates[1], sell=rates[2], visa=rates[3],
                                              export=rates[4], remittance=rates[5], usdt=rates[6])
            session.add(new_currency_rate)

    # Save changes to the database
    session.commit()
    session.close()
    print("Exchange rate information has been updated in the database.")


store_exchange_rates()
