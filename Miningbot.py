import os
import discord
from discord.ext import commands
import requests
from pywallet import wallet

# Replace <API_KEY> with your actual BlockCypher API key
api_key = "<API_KEY>"

# Create a Discord bot object
bot = commands.Bot(command_prefix='!')

# Define a function to handle the !start command
@bot.command(name='start')
async def start(ctx):
    """Send a welcome message when the command !start is issued."""
    await ctx.send('Welcome to the Bitcoin address balance bot!')

# Define a function to handle the !balance command
@bot.command(name='balance')
async def balance(ctx):
    """Get the balance of a Bitcoin address."""
    # Generate a random 12-word mnemonic
    mnemonic = wallet.generate_mnemonic()

    # Derive the Bitcoin address from the mnemonic
    wallet = wallet.create_wallet(network="BTC", seed=mnemonic, children=1)
    address = wallet['addresses'][0]

    # Make a GET request to the BlockCypher API to get the address balance
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key}
    response = requests.get(f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance", headers=headers)

    # Get the balance from the response
    balance = response.json()["balance"]

    # Check if the balance is greater than zero
    if balance > 0:
        # Send the balance and mnemonic to the user
        await ctx.send(f"The balance of address {address} is {balance} satoshis. Here's your mnemonic: {mnemonic}")
    else:
        # Send the balance to the user
        await ctx.send(f"The balance of address {address} is {balance} satoshis.")

# Define a function to handle errors
@bot.event
async def on_command_error(ctx, error):
    """Log errors caused by commands."""
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Invalid command.')
    else:
        await ctx.send(f'Error: {error}')

def main():
    """Start the bot."""
    # Start the Discord bot using your bot token
    bot.run(os.environ['DISCORD_BOT_TOKEN'])

if __name__ == '__main__':
    main()
