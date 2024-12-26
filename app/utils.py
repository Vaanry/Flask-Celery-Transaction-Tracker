import os

from dotenv import load_dotenv
from tronpy import Tron
from tronpy.keys import PrivateKey

load_dotenv()

# Подключение к тестовой сети Shasta

client = Tron(network="shasta")
private_key = os.getenv("PRIVATE_KEY")
sender = PrivateKey(bytes.fromhex(private_key))
sender_address = sender.public_key.to_base58check_address()


def generate_wallet():
    new_wallet = client.generate_address()
    receiver_address = new_wallet["base58check_address"]
    txn = (
        client.trx.transfer(
            sender_address, receiver_address, 10000
        )  # Отправляем 0.01 TRX на вновь созданный кошелёк для его активации
        .memo("Активируем новый аккаунт")
        .build()
        .sign(sender)
    )
    txn_hash = txn.broadcast().wait()

    print(f"Транзакция выполнена: {txn_hash}")
    return receiver_address


def check_balance(receiver_address):
    balance = client.get_account_balance(receiver_address)
    return balance
