

#----------------------------------------------------------------
# IMPORTING MODULES 

  
  

from web3 import Web3
import json,requests,cryptonator,os,time,string,random,time
from classes import *
from reports import *
from pythonpancakes import PancakeSwapAPI
from telegram.ext import *
from telegram import *
from ads import get_current_add as myads
from ads import *
ps = PancakeSwapAPI()

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))


#---------------------------------------------------------------------------   
# import some important abi
abis = [{"inputs":[{"internalType":"address[]","name":"addresses","type":"address[]"},{"internalType":"uint256[]","name":"balances","type":"uint256[]"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]

abi = '''[
    {
      "constant": true,
      "inputs": [],
      "name": "owner",
      "outputs": [
        {
          "name": "",
          "type": "address"
        }
      ],
      "payable": false,
      "type": "function"
    },
    {
      "inputs": [],
      "payable": false,
      "type": "constructor"
    }
]'''   

directory = './abi/'
filename = "fac.json"
file_path = os.path.join(directory, filename)
with open(file_path) as json_file:
    factoryAbi = json.load(json_file)


bolo = "joe.json"

file_path = os.path.join(directory, bolo)
with open(file_path) as json_file:
    joeRouter = json.load(json_file)
    
 
jok = "bal.json"   
file_path = os.path.join(directory, jok)
with open(file_path) as json_file:
    balance_abi = json.load(json_file)
    
lplp = "lp.json"

file_path = os.path.join(directory, lplp)
with open(file_path) as json_file:
    lpAbi = json.load(json_file)
    
    
client = Web3(Web3.HTTPProvider(bsc))


routerAddress = Web3.toChecksumAddress("0x10ED43C718714eb63d5aA57B78B54704E256024E")
factoryAddress = Web3.toChecksumAddress("0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73")

routerContract = client.eth.contract(address=routerAddress, abi=joeRouter)
factoryContract = client.eth.contract(address=factoryAddress, abi=factoryAbi)
    
    
#-------------------------------------------------------------------
interpretations = {
  "UNKNOWN": ('The status of this token is unknown. '
                          'This is usually a system error but could \n also be a bad sign for the token. Be careful.'),
  "OK": ('Honeypot tests passed. Our program was able to buy and sell it successfully. \n'
                       'This however does not guarantee that it is not a honeypot.'),
  "NO_PAIRS": ( 'Could not find any trading pair for this token '
                           'on the default router and could thus not test it.'),
  "SEVERE_FEE": ('A severely high trading fee (over 50%) was '
                             'detected when selling or buying this token.'),
  "HIGH_FEE": ('A high trading fee (Between 20% and 50%) was detected when '
                              'selling or buying this token. Our system was\n however able to sell the token again.'),
  "MEDIUM_FEE": ('A trading fee of over 10% but less then 20% was detected when selling '
                                'or buying this token. Our system was however able to sell the token again.'),
  "APPROVE_FAILED": ('Failed to approve the token.\n This is likely a honeypot.'),
  "SWAP_FAILED": ('Failed to sell the token. \n This is likely a honeypot.')
}

#-----------------------------------------------------------------------

def price_contract(address):
    dates = "%Y-%m-%d %H:%M:%S"
    query = """
    query
    {
      ethereum(network: bsc) {
        dexTrades(
        exchangeName: {in:["Pancake","Pancake v2"]},
        baseCurrency: {is: "%s"}
        quoteCurrency: {is: "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"}
        options: {desc: ["block.height", "transaction.index"], limit: 1}
        ) {
        block {
            height
            timestamp {
            time(format: "%s")
            }
        }
        transaction {
            index
        }
        baseCurrency {
            symbol
        }
        quoteCurrency {
            symbol
        }
        quotePrice
       }
      }
    }
    """ % (address, dates)

    d = {'query': query, 'variables': {}}
    payload = json.dumps(d)
    url = "https://graphql.bitquery.io"
    headers = {
            'X-API-KEY': 'BQYxBh0DXYCwroM9PKnGS2tZXWDZhNEx',
            'Content-Type': 'application/json'
        }
    
    try:
        di = requests.request("POST", url, headers=headers, data=payload).json()['data']['ethereum']['dexTrades'][0]['quotePrice']
        pp = "{0:.15f}".format(float(di))
        bnb = cryptonator.get_exchange_rate("bnb", "usd")
        price = float(pp)*float(bnb)
        pps = "{0:.12f}".format(float(price))
        return pps
    except Exception:
        try:
            pup = ps.tokens(address)['data']['price']
            return "{0:.12f}".format(float(pup))
        except Exception:
            return "0.0000"
          
          
          
def name_contract(address):
    contract = web3.eth.contract(address=address, abi=abis)
    c_name = contract.functions.name().call()
    return c_name

def symbol_contract(address):
  try:
      contract = web3.eth.contract(address=address, abi=abis)
      c_name = contract.functions.symbol().call()
      name = name_contract(address)
      lover = f"<b>📃 Contract:</b> <code>{address}</code>\n\n" \
              f"<b>ℹ️ {name} ({c_name})</b>"
      return lover
  except Exception:
      return "no info"
  
  
def owner_contract(address):
    try:
        contract = web3.eth.contract(address=address, abi=abi)
        owner = contract.functions.owner().call()
        if "0x0000000000000000" in owner:
            own = f"<a href='https://bscscan.com/address/{owner}'>Renounced</a>"
            return own
        else:
            own = f"<a href='https://bscscan.com/address/{owner}'>Still Holding</a>"
            return own
            
    except Exception as err:
        own = "no info"
        return own
    
    
    
    
 
def supply_contract(address):
    try:
        contract = web3.eth.contract(address=address, abi=abis)
        decimal = decimals_contract(address)
        c_name = float(contract.functions.totalSupply().call()/10 ** decimal)
        return c_name
    except Exception:
        return "0.0000"

def decimals_contract(address):
    try:
        contract = web3.eth.contract(address=address, abi=abis)
        dec = contract.functions.decimals().call()
        return dec
    except Exception:
        return "0"
    
    
def dead(address):
    try:
        contract = web3.eth.contract(address=address, abi=abis)
        decimal = decimals_contract(address)
        wal = Web3.toChecksumAddress("0x000000000000000000000000000000000000dEaD") 
        dead1 = float(contract.functions.balanceOf(wal).call({'from': address})/10 ** decimal)
        return dead1
    except Exception:
        return "0"
    
def main_supply(address):
    try:
        supply_coins = supply_contract(address)
        burn_coin = dead(address)
        supply = float(supply_coins)-float(burn_coin)
        return supply
    except Exception:
        return "0.0000"

def mcap_contract(address):
    try:
        token_supply = main_supply(address=address)
        token_price = price_contract(address=address)
        mcap = float(token_supply)*float(token_price)
        mcap = "{0:,.4f}".format(float(mcap))
        return mcap
    except Exception:
        return "0.0000"   

#------------------------------------------------------------------------------


def fetch_pair(inToken):
    
    weth_address = Web3.toChecksumAddress("0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c") 
    pair = factoryContract.functions.getPair(inToken, weth_address ).call()
    pair_contract = client.eth.contract(address=pair, abi=lpAbi)
    block = get_block_at_timestamp(unixtime)
    fees_tax = fees_contract(inToken)
    gas_fees = gas_contract(inToken)
    balance_check_contract = client.eth.contract(address=weth_address, abi=balance_abi)
    balance_now = balance_check_contract.functions.balanceOf(pair).call({'from': weth_address})
    liquidity = client.fromWei(balance_now, "ether")
    liquidity = "{:0,.4f}".format(liquidity)
    
    lover = f"<code>LP:</code> <b>{liquidity} WBNB</b>\n\n<b>💰 Trading Tax's</b>\n" \
            f"<b>Fees: {fees_tax}\n</b>" \
            f"<b>Gas Used: {gas_fees}</b>"
    return lover
  


unixtime = int(time.time())

def get_block_at_timestamp(unixtime):
    
    block = requests.get(f"https://api.bscscan.com/api?module=block&action=getblocknobytime&timestamp={unixtime}&closest=before&apikey=5K1X4N4YP3NE9PBF9V99XBVX69SZ5UNT7Y")
    block = json.loads(block.content)
    block = block["result"]
    return int(block)
#----------------------------------------------------------------------------------------------
def fees_contract(address):
  try:
    buy = requests.get(f"https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain=bsc2&token={address}").json()
    buy_tax = buy["BuyTax"]
    sell_tax = buy["SellTax"]
    msg = f"Buy: {buy_tax}% || Sell: {sell_tax}%"
    return msg
  except Exception:
    return "no info now"
  
  
def gas_contract(address):
  try:
    buy = requests.get(f"https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain=bsc2&token={address}").json()
    buy_gas = '{0:,}'.format(buy["BuyGas"])
    sell_gas = '{0:,}'.format(buy["SellGas"])
    msg = f"Buy: {buy_gas} || Sell: {sell_gas}"
    return msg
  except Exception:
    return "no info now"


def honeypot_check(address):
    try:
        url = f"https://honeypot.api.rugdoc.io/api/honeypotStatus.js?address={address}&chain=bsc"
    # sending get request and saving the response as response object
        honeypot = requests.get(url)
        d = json.loads(honeypot.content)   
        for key, value in interpretations.items():
            if d["status"] in key:
                honeypot_status = value
                honeypot_code = key
                return honeypot_status
    except Exception:
        return ""






def scan_command(update: Update, context: CallbackContext) -> None:
    text = update.message.text.split()
    
    if update.message.chat['type'] == "private":
        if len(text) >=2 and len(text[1])==42:
            try:
                address = Web3.toChecksumAddress(text[1])
                
                namooooo = name_contract(address=address)
                fetching = context.bot.send_message(chat_id=update.message.chat_id, text="<b>Analyzing Contract...</b>",parse_mode="html")
                start = Analyzer(symbol_contract(address),owner_contract(address),price_contract(address),main_supply(address),mcap_contract(address),fetch_pair(address),check_all(address),honeypot_check(address=address),myads())
                best = start.info()
                keymap = [[InlineKeyboardButton("🔸 Bscscan", url=f"https://bscscan.com/token/{address}#balances"),InlineKeyboardButton("💩 PooCoin",url=f"https://poocoin.app/tokens/{address}"),InlineKeyboardButton("🥞 PCS", url=f"https://pancakeswap.finance/swap#/swap?outputCurrency={address}")]]
                reply_markto = InlineKeyboardMarkup(keymap)
                fetching.edit_text(best,parse_mode="html",disable_web_page_preview=True,reply_markup=reply_markto)
            except Exception:
                update.message.reply_text("<code>Probably you sent a wallet address or a contract from another chain</code>",parse_mode="html")
            
        else:
            update.message.reply_text("<code>Error Encountered\neither contract address wrong or you didn't provide it in second arg.</code>",parse_mode="html")
    else:
        if len(text) >=2 and len(text[1])==42:
            try:
                address = Web3.toChecksumAddress(text[1])
                namooooo = name_contract(address=address)
                fetching = context.bot.send_message(chat_id=update.message.chat_id, text="<b>Analyzing Contract...</b>",parse_mode="html")
                start = Analyzer(symbol_contract(address),owner_contract(address),price_contract(address),main_supply(address),mcap_contract(address),fetch_pair(address),check_all(address),honeypot_check(address=address),myads())
                best = start.info()
                keymap = [[InlineKeyboardButton("🔸 Bscscan", url=f"https://bscscan.com/token/{address}#balances"),InlineKeyboardButton("💩 PooCoin",url=f"https://poocoin.app/tokens/{address}"),InlineKeyboardButton("🥞 PCS", url=f"https://pancakeswap.finance/swap#/swap?outputCurrency={address}")]]
                reply_markto = InlineKeyboardMarkup(keymap)
                fetching.edit_text(best,parse_mode="html",disable_web_page_preview=True,reply_markup=reply_markto)
            except Exception:
                update.message.reply_text("<code>Probably you sent a wallet address or a contract from another chain</code>",parse_mode="html")
            
        else:
            update.message.reply_text("<code>Error Encountered\neither contract address wrong or you didn't provide it in second arg.</code>",parse_mode="html")
  

def start_command(update,context) -> None:
    if update.message.chat['type'] == "private":
        text = f"<b>Hey {update.message.chat['first_name']}</b>\n" \
               f"I am a contract analyzer bot with some fuctions\n\n" \
               f"<b>Checking your balance for a token</b>\n" \
               f"/bal [wallet] [contract address]\n\n" \
               f"<b>Calculating some math</b>\n" \
               f"/calc [num 1][operator][num2]\n/calc 200+250\n\n\n<b>Suggestions or Help @AmaDevs</b>"
        update.message.reply_text(text,parse_mode="html")
    else:
        text = f"<b>Hey {update.message.from_user['first_name']}</b>\n" \
               f"I am a contract analyzer bot with some fuctions\n\n" \
               f"<b>Checking your balance for a token</b>\n" \
               f"/bal [wallet] [contract address]\n\n" \
               f"<b>Calculating some math</b>\n" \
               f"/calc [num 1][operator][num2]\n/calc 200+250\n\n\n<b>Suggestions or Help @AmaDevs</b>"
        update.message.reply_text(text,parse_mode="html")

def calculator(update,context) -> None:
    chat_id = update.message.chat['id']
    te = update.message.text.split()
    if len(te) == 2:
        ar = eval(context.args[0])
        if ar > 0.0001:
            ar = "{:,.7f}".format(float(ar))
        else:
            ar = "{:,.12f}".format(float(ar))
        update.message.reply_text(f"<b>{ar}</b>", parse_mode="html")
        
def balance(update,context) -> None:
    text = update.message.text.split()
    print(len(text))
    if len(text)>=3:
        print(text[1], text[2])
        try:
            wallet = Web3.toChecksumAddress(text[2])
            address = Web3.toChecksumAddress(text[1])
            tyhum = update.message.reply_text("<b>Fetching Balance...</b>",parse_mode="html")
            contract = web3.eth.contract(address=address, abi=abis)
            price = price_contract(address=address)
            name = name_contract(address=address)
            decimal = decimals_contract(address)
            dead1 = float(contract.functions.balanceOf(wallet).call({'from': address})/10 ** decimal)
            bally = '{0:,.4f}'.format(float(dead1))
            amount =  float(dead1)*float(price)
            amount1 = "${0:,.4f}".format(amount)
            msg = f"<b>{bally} {name} || ({amount1})</b>"
            tyhum.edit_text(msg,parse_mode="html")
            return
       
        except Exception:
            tyhum.edit_text("/bal [contract] [wallet]",parse_mode="html")
            return
def bal(update,context) -> None:
    text = update.message.text.split()
    print(len(text))
    if len(text)>=2:
        hood = update.message.reply_text("<b>Fetching Balance...</b>",parse_mode="html")
        wallet = Web3.toChecksumAddress(text[1])
        account_from_account_balance = web3.eth.get_balance(wallet)/10**18
        bals = float(account_from_account_balance)*float(cryptonator.get_exchange_rate("bnb", "usd"))
        bals = "{0:,.4f}".format(float(bals))
        mnj = f"<b>{account_from_account_balance} BNB ({bals})</b>"
        hood.edit_text(mnj,parse_mode="html")
        
             
def main() -> None:
    # Create the Updater and pass it your bot's token.
    token = "5091805020:AAH4Z82hN4bOI2yywG9L_hZtCwkQwpbhfHY"
    updater = Updater(token)
   
    print('started bot')
    updater.dispatcher.add_handler(CommandHandler('start', start_command))
    updater.dispatcher.add_handler(CommandHandler('scan', scan_command))
    updater.dispatcher.add_handler(CommandHandler("newads", new_ad, pass_args=True, pass_user_data=True))
    updater.dispatcher.add_handler(CommandHandler("delads", del_ad, pass_args=True, pass_user_data=True))
    updater.dispatcher.add_handler(CommandHandler("ads", see_all_adds))
    updater.dispatcher.add_handler(CommandHandler("calc", calculator))
    updater.dispatcher.add_handler(CommandHandler("bal", balance))
    updater.dispatcher.add_handler(CommandHandler("b", bal))
    
    
   
    
   
    updater.start_polling()
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
    
    
if __name__ == '__main__':
    main()
    
