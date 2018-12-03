from stellar_base.keypair import Keypair
from stellar_base.builder import Builder
from stellar_base.address import Address
import requests
import json

# Generate Alice's Keypair for ultimately signing and setting as the source
alice_kp = Keypair.random()
seed = alice_kp.seed().decode()
alice_address = alice_kp.address().decode()
print('alice_address: {}'.format(alice_address))
#to play in the Stellar test network, you can ask Friendbot to create an account
url = 'https://friendbot.stellar.org'
r = requests.get(url, params={'addr': alice_address})


address = Address(address=alice_address) # See signature for additional args
address.get() # Get the latest information from Horizon

print('Alice Balances: {}'.format(address.balances))

# Bob's address, for the destination
kp = Keypair.random()
bob_address = kp.address().decode()
print('bobs_address: {}'.format(bob_address))
url = 'https://friendbot.stellar.org'
r = requests.get(url, params={'addr': bob_address})

address = Address(address=bob_address) # See signature for additional args
address.get() # Get the latest information from Horizon

print('Bobs Balances: {}'.format(address.balances))

builder = Builder(secret=seed)
builder.append_payment_op(bob_address, '100', 'XLM')
builder.add_text_memo('For beers') # string length <= 28 bytes
builder.sign()

# Uses an internal horizon instance to submit over the network
response = builder.submit()

address = Address(address=bob_address) # See signature for additional args
address.get() # Get the latest information from Horizon

print('Bobs Balances: {}'.format(address.balances))

address = Address(address=alice_address) # See signature for additional args
address.get() # Get the latest information from Horizon

print('Alice Balances: {}'.format(address.balances))