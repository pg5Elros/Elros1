import pandas as pd
import matplotlib 
import boto3


USD_ENDPOINT = 'https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=eur&sort=exchangedate&order=desc&json'
EUR_ENDPOINT = 'https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=usd&sort=exchangedate&order=desc&json'

df_cc = pd.read_json(USD_ENDPOINT)
result_df = df_cc[["exchangedate", "rate"]]
result_df.rename(columns={'rate': 'USD'}, inplace=True)

df_cc = pd.read_json(EUR_ENDPOINT)
result_df['EUR'] = df_cc[df_cc['exchangedate'] == result_df['exchangedate']]['rate']
result_df.to_csv("data1.csv", index=False)


result_df.plot(x='exchangedate', y=['USD', 'EUR'], figsize=(15, 7), title="UAH currency", \
    fontsize=12)
matplotlib.pyplot.savefig('plot.png')


session = boto3.Session(
    aws_access_key_id="AKIA52K7WOQLZ2BLTQNI",
    aws_secret_access_key="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",
)

s3=session.client('s3')
with open('plot.png', "rb") as f:
    s3.upload_fileobj(f, "mybucket113344", 'plot.png')

with open('data1.csv', "rb") as f:
    s3.upload_fileobj(f, "mybucket113344", 'data1.csv')
