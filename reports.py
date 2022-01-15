
import requests,json

api = "5K1X4N4YP3NE9PBF9V99XBVX69SZ5UNT7Y"

def verified(address):
  try:
    you = requests.get(f"https://api.bscscan.com/api?module=contract&action=getabi&address={address}&apikey={api}").json()
    result = you['result']
    status = you['status']
    message = you['message']
    if status == "1" and message == "OK":
      MSG = "YES 🟢"
      return MSG
    elif status == "0" and message == "NOTOK":
      MSG = "NO 🔴"
      return MSG
  except Exception:
    your = "no info now"
    return your


def minter(address):
    try:
        contractCodeGetRequestURL = f"https://api.bscscan.com/api?module=contract&action=getsourcecode&address={address}&apikey={api}"
        contractCodeRequest = requests.get(url = contractCodeGetRequestURL)
        tokenContractCode = contractCodeRequest.json()
        if "mint" in str(tokenContractCode['result'][0]['SourceCode']):
            mints = "mint found!"
            return mints
        else:
            mints = ""
            return mints
    except Exception:
        return ""
  
  

def trade1(address):
    try:
        s = requests.get(f'https://api.bscscan.com/api?module=contract&action=getsourcecode&address={address}&apikey=NQDD6TXH7G3PBESQWPWSXI5YPA63F6PRXT').json()
        _contract = s['result']
        for verified in _contract:
            if verified['ABI'] != 'Contract source code not verified':
                for contract in _contract:
                    source = contract['SourceCode']
                    if 'tradingEnabled' or "tradingOpen" or "swapEnabled" or "sellLockDisabled" or "pause" in verified['ABI'] or 'tradingEnabled' or "tradingOpen" or "swapEnabled" or "sellLockDisabled" or "paused" in source:
                        return "trading lock in contract!"
                    else:
                        return ""
            else:
                return ""
    except Exception:
        return ""
    
def blacklist(address):
    try:
        s = requests.get(f'https://api.bscscan.com/api?module=contract&action=getsourcecode&address={address}&apikey=NQDD6TXH7G3PBESQWPWSXI5YPA63F6PRXT').json()
        _contract = s['result']
        for verified in _contract:
            if verified['ABI'] != 'Contract source code not verified':
                for contract in _contract:
                    source = contract['SourceCode']              
                    if 'isBlacklisted' in verified['ABI'] or 'isBlacklisted' in source:
                        return "blacklist funtion in contract!"
                    else:
                        return ""
            else:
                return ""
                    
    except Exception:
        return ""  
    
    
def honey(address):
    try:
        buy = requests.get(f"https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain=bsc2&token={address}").json()
        honey = buy["IsHoneypot"]
        reason = buy["Error"]
      
        if honey == True:
            if reason == None:
                reason = ""
    
            else:
                reason = reason

            honey_pot = f"honeypot (DYOR)\n{reason}"
            return honey_pot
        else:
            return ""
    except Exception:
        return ""

    

def check_all(address):
    try:
        verifiedss = verified(address=address)
        mint = minter(address=address)
        trade1_lock = trade1(address=address)
        blacklists = blacklist(address=address)
        honeys = honey(address=address)
        msg = f"Contract Verified: {verifiedss}\n" \
              f"{mint} {trade1_lock} {blacklists}\n{honeys}"
        return msg
        
    except Exception:
        return ""
    
