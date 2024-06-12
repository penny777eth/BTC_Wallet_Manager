import os
import requests
import time
import pandas as pd
from tabulate import tabulate
from dateutil import parser

class BTCWalletManager:
    def __init__(self, btc_wallets, max_queries_per_batch=5, retry_attempts=3):
        self.btc_wallets = [{'id': i + 1, 'address': wallet['address'], 'label': wallet['label'], 'browser': wallet['browser'], 'type': wallet['type']} for i, wallet in enumerate(btc_wallets)]
        self.max_queries_per_batch = max_queries_per_batch
        self.retry_attempts = retry_attempts
        self.btc_to_usdt_rate = self.get_btc_to_usdt_rate()

    def get_btc_balance(self, address):
        for attempt in range(self.retry_attempts):
            try:
                # Attempt 1: Blockchain.info API
                url = f"https://blockchain.info/q/addressbalance/{address}"
                response = requests.get(url)
                response.raise_for_status()
                balance = int(response.text)
                return balance / 1e8  # Convert satoshi to BTC
            except requests.exceptions.RequestException:
                try:
                    # Attempt 2: Blockcypher API
                    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance"
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()
                    balance = data.get('balance', 0)
                    return balance / 1e8  # Convert satoshi to BTC
                except requests.exceptions.RequestException as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(5)  # Increase sleep time to reduce rate limit issues
        return 0

    def get_last_transaction_time(self, address):
        for attempt in range(self.retry_attempts):
            try:
                # Attempt 1: Blockchain.info API
                url = f"https://blockchain.info/rawaddr/{address}"
                response = requests.get(url)
                response.raise_for_status()
                transactions = response.json().get('txs', [])
                if transactions:
                    last_tx_time = transactions[0]['time']
                    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(last_tx_time))
            except requests.exceptions.RequestException:
                try:
                    # Attempt 2: Blockcypher API
                    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/full"
                    response = requests.get(url)
                    response.raise_for_status()
                    transactions = response.json().get('txs', [])
                    if transactions:
                        last_tx_time = transactions[0]['received']
                        return parser.parse(last_tx_time).strftime('%Y-%m-%d %H:%M:%S')
                except requests.exceptions.RequestException as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(5)  # Increase sleep time to reduce rate limit issues
        return 'No transactions found'

    def get_btc_to_usdt_rate(self):
        for attempt in range(self.retry_attempts):
            try:
                url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                rate = data['bpi']['USD']['rate_float']
                return rate
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(5)  # Increase sleep time to reduce rate limit issues
        return None

    def query_wallets(self):
        grouped_wallets = [self.btc_wallets[i:i + self.max_queries_per_batch] for i in range(0, len(self.btc_wallets), self.max_queries_per_batch)]
        total_btc = 0
        total_usdt = 0
        for group in grouped_wallets:
            for wallet in group:
                balance = self.get_btc_balance(wallet['address'])
                usdt_balance = balance * self.btc_to_usdt_rate if self.btc_to_usdt_rate else 'N/A'
                last_tx_time = self.get_last_transaction_time(wallet['address'])
                wallet['balance'] = balance
                wallet['usdt_balance'] = usdt_balance
                wallet['last_tx_time'] = last_tx_time
                total_btc += balance
                if usdt_balance != 'N/A':
                    total_usdt += usdt_balance
                time.sleep(1)  # To avoid hitting rate limits
            self.display_wallets(group)
            time.sleep(10)  # Increase sleep time between batches to avoid rate limit issues
        self.display_totals(total_btc, total_usdt)

    def display_wallets(self, wallets):
        table = []
        headers = ["Wallet ID", "Address", "Label", "Browser", "Type", "Balance (BTC)", "Balance (USDT)", "Last Transaction Time"]
        for wallet in wallets:
            table.append([wallet['id'], wallet['address'], wallet['label'], wallet['browser'], wallet['type'], wallet['balance'], wallet['usdt_balance'], wallet['last_tx_time']])
        print(tabulate(table, headers, tablefmt="grid"))

    def display_totals(self, total_btc, total_usdt):
        table = [["Total", "", "", "", "", total_btc, total_usdt, ""]]
        headers = ["Wallet ID", "Address", "Label", "Browser", "Type", "Balance (BTC)", "Balance (USDT)", "Last Transaction Time"]
        print(tabulate(table, headers, tablefmt="grid"))

def load_btc_wallets_from_excel(file_path):
    df = pd.read_excel(file_path)
    wallets = []
    for index, row in df.iterrows():
        wallets.append({'address': row['Address'], 'label': row['Label'], 'browser': row['Browser'], 'type': row['Type']})
    return wallets

if __name__ == "__main__":
    # Update the path to your Excel file
    excel_file_path = 'wallets.xlsx'
    btc_wallets = load_btc_wallets_from_excel(excel_file_path)
    wallet_manager = BTCWalletManager(btc_wallets)
    wallet_manager.query_wallets()
