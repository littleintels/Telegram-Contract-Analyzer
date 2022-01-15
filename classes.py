class Analyzer:
    def __init__(self,name,owner,price,supply,mcap,lp,reports,honeypot,ads):
        self.name = name
        self.owner=owner
        self.price=price
        self.supply=supply
        self.mcap=mcap
        self.lp = lp
        self.reports = reports
        self.honeypot = honeypot
        self.ads = ads
        
    def info(self):
        sup = "{0:,.4f}".format(float(self.supply))
        infos = f"✅ <b>@LITTLEINTEL</b> ✅\n\n{self.name}\n" \
                f"<b>🆔 Owner:</b> {self.owner}\n\n" \
                f"<code>Price:</code>  <b>${self.price}\n</b>" \
                f"<code>Supply:</code> <b>{sup}\n</b>" \
                f"<code>MarketCap:</code> <b>${self.mcap}\n</b>" \
                f"{self.lp}\n\n<b>⏳ Reports</b>\n" \
                f"<b>{self.reports}</b>\n<code>{self.honeypot}</code>\n\n{self.ads}" 
        return infos
        
    
 