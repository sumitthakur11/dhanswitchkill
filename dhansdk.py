


from dhanhq import dhanhq















class Setup(object):
    def __init__(self, accountnumber, AuthToken):
        self.client_id= accountnumber
        self.access_token=AuthToken
        print("Initializing DhanHQ SDK...")
        print(self.client_id,self.access_token)
        self.dhan = dhanhq(self.client_id,self.access_token)

    def login(self):
        self.dhan = dhanhq(self.client_id,self.access_token)
        data =self.dhan.get_fund_limits()
        print(data)
        if data['status']=='success':

            return True,None
        else: return False,data

        
    


 

class HTTP(Setup):
    
  
    
   

    def cancel_order(self, orderno):
        data = self.dhan.cancel_order( orderno=orderno)
        return data
    
    


    def checkfunds(self):
        try :
            data =self.dhan.get_fund_limits()
            print(data)
            return data['data']['availabelBalance'],None
        
        except Exception as e:
            return None, e

    
    def getposition(self):
        try:
            findata = dict()
            listfin=[]
            totalrealised=0
            totalunrealised=0

            data = self.dhan.get_positions()
        
            positionall= data['data']
            print(data,"positiondata...................................................")
            if positionall:

                for i in positionall:
                    findata['exchange'] = i['exchangeSegment']
                    findata['tradingsymbol'] = i['tradingSymbol']
                    findata['symboltoken'] = i['securityId']
                    findata['buyavgprice'] = i['buyAvg']
                    findata['sellavgprice'] =  i['sellAvg']
                    findata['netqty'] = i['netQty']
                    findata['realised'] = i['realizedProfit']
                    findata['unrealised'] = i['unrealizedProfit']
                    listfin.append(findata)
                    findata= {}

                totalrealised=sum(float(d['realised']) for d in listfin)
                totalunrealised=sum(float(d['unrealised']) for d in listfin)
                    
        





            return totalrealised,totalunrealised,listfin,None
        except Exception as e:
            return None, None, None,e

  
    def killswitch(self,action):
        try:

            data = self.dhan.kill_switch(action)
            return data
        except Exception as e:
            return None,e
    
        

    
 


