import pandas as pd
import sqlite3
from datetime import datetime


df = pd.read_json('../../data/data_full.json')

#Setting the pandas for show all columns
pd.options.display.max_columns = None

# Adding a column _source with a fix value
df['_source'] = "https://lista.mercadolivre.com.br/tenis-casual-masculino"

# Adding a column _data_extract with a data and hour now
df['_data_extract'] = datetime.now()

# Treatment null values for numeric columns and of text
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['review_rating_number'] = df['review_rating_number'].fillna(0).astype(float)


# Remove the parentheses of review_amount
df['reviews_amount'] = df['reviews_amount'].str.replace(r'[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

# Treatment the prices as floats and sumarize the total values
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100

# Drop unecessarie columns
df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos'], inplace=True)

# Connect to database: SQLlite (or create a new)
conn = sqlite3.connect('../../data/quotes.db')

# Write dataFrame at database SQLite
df.to_sql('mercadolivre_itens', conn, if_exists='replace', index=False)

print(df)

# close connection with database
conn.close()

