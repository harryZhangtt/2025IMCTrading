# #Trade Class: contains the trading logic and a run 
# """_During each iteration the run method will be called and provided with a TradingState object.
# This object contains an overview of all the trades that have happened since the last iteration, 
# both the algorithms own trades as well as trades that happened between other market participants.
   
   
# the TradingState will contain a per product overview of all the outstanding buy and sell orders 
# (also called “quotes”) originating from the bots. 


# how the order book is matched: 
#  Based on the logic in the run method the algorithm can then decide to either send orders that will 
#  fully or partially match with the existing orders, e.g. sending a buy (sell) order with a price equal 
#  to or higher (lower) than one of the outstanding bot quotes, which will result in a trade. If the algorithm 
#  sends a buy (sell) order with an associated quantity that is larger than the bot sell (buy) quote that it is 
#  matched to, the remaining quantity will be left as an outstanding buy (sell) quote with which the trading bots 
#  will then potentially trade. """
 
 
#  #TradingState will then reveal whether any of the bots decided to “trade on” the player’s outstanding quote. 
#  # If none of the bots trade on an outstanding player quote, the quote is automatically cancelled at the end of the iteration.



# #trader class: 
# """Below an abstract representation of what the trader class should look like is shown. The class only requires 
# a single method called run, which is called by the simulation every time a new TraderState is available. The logic 
# within this run method is written by the player and determines the behaviour of the algorithm. The output of the 
# method is a dictionary named result, which contains all the orders that the algorithm decides to send based on this logic."""

# from datamodel import OrderDepth, UserId, TradingState, Order
# from typing import List
# import string

# class Trader:
    
#     def run(self, state: TradingState):
#         print("traderData: " + state.traderData)
#         print("Observations: " + str(state.observations))

# 				# Orders to be placed on exchange matching engine
#         result = {}
#         for product in state.order_depths:
#             order_depth: OrderDepth = state.order_depths[product]# this is the order book we can trade now
# """to call and see the buy and sell order available to trade, do order_depth.sell_orders, and order_depth.buy_orders.
#         """
#             orders: List[Order] = []
#             acceptable_price = 10  # Participant should calculate this value
#             print("Acceptable price : " + str(acceptable_price))
#             print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
    
#             if len(order_depth.sell_orders) != 0:
#                 best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
#                 if int(best_ask) < acceptable_price:
#                     print("BUY", str(-best_ask_amount) + "x", best_ask)
#                     orders.append(Order(product, best_ask, -best_ask_amount))#send order as Order class
    
#             if len(order_depth.buy_orders) != 0:
#                 best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
#                 if int(best_bid) > acceptable_price:
#                     print("SELL", str(best_bid_amount) + "x", best_bid)
#                     orders.append(Order(product, best_bid, -best_bid_amount))#send order as Order class
            
#             result[product] = orders
    
# 		    # String value holding Trader state data required. 
# 				# It will be delivered as TradingState.traderData on next execution.
#         traderData = "SAMPLE" 
        
# 				# Sample conversion request. Check more details below. 
#         conversions = 1
#         return result, conversions, traderData
    
    
# """The TradingState class holds all the important market information that an algorithm needs to make decisions 
#      about which orders to send. Below the definition is provided for the TradingState class:
#  """
        
        
# Time = int
# Symbol = str
# Product = str
# Position = int

# class TradingState(object):
#    def __init__(self,
#                  traderData: str,
#                  timestamp: Time,
#                  listings: Dict[Symbol, Listing],
#                  order_depths: Dict[Symbol, OrderDepth],
#                  own_trades: Dict[Symbol, List[Trade]],
#                  market_trades: Dict[Symbol, List[Trade]],
#                  position: Dict[Product, Position],
#                  observations: Observation):
#         self.traderData = traderData
#         self.timestamp = timestamp
#         self.listings = listings
#         self.order_depths = order_depths
#         self.own_trades = own_trades
#         self.market_trades = market_trades
#         self.position = position
#         self.observations = observations
        
#     def toJSON(self):
#         return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
    


# """
# The most important properties

# - own_trades: the trades the algorithm itself has done since the last `TradingState` came in. 
# This property is a dictionary of `Trade` objects with key being a product name. The definition of 
# the `Trade` class is provided in the subsections below.(this could be useful for calcualting risk exposure, PnL)

# - market_trades: the trades that other market participants have done since the last `TradingState` came in. 
# This property is also a dictionary of `Trade` objects with key being a product name.(tthis is the volume at this iteration)

# - position: the long or short position that the player holds in every tradable product.
# This property is a dictionary with the product as the key for which the value is a signed integer denoting the position.
# (this kind of indicates the market sentiment)

# - order_depths: all the buy and sell orders per product that other market participants have sent and that the algorithm is 
# able to trade with. This property is a dict where the keys are the products and the corresponding values are instances of the `OrderDepth` class. 
# This `OrderDepth` class then contains all the buy and sell orders. An overview of the `OrderDepth` class is also provided in the subsections below.
#         """
        
        
# #for own_trades and market_trades: lists that contain Trade objects, each treated as single order people made in the past
# Symbol = str
# UserId = str

# class Trade:
#     def __init__(self, symbol: Symbol, price: int, quantity: int, buyer: UserId = None, seller: UserId = None, timestamp: int = 0) -> None:
#         self.symbol = symbol
#         self.price: int = price
#         self.quantity: int = quantity
#         self.buyer = buyer
#         self.seller = seller
#         self.timestamp = timestamp

#     def __str__(self) -> str:
#         return "(" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ", " + str(self.timestamp) + ")"

#     def __repr__(self) -> str:
#         return "(" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ", " + str(self.timestamp) + ")" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ")"
    
#  """These trades have five distinct properties:

# 1. The symbol/product that the trade corresponds to (i.e. are we exchanging apples or oranges)
# 2. The price at which the product was exchanged
# 3. The quantity that was exchanged
# 4. The identity of the buyer in the transaction
# 5. The identity of the seller in this transaction
#         """
        
        
# #order depth class: these are basically collection of ongoing(not yet completed) trade in the order book
# #given by dict of int: int, indicate the price and the quantity available at that price'

# class OrderDepth:
#     def __init__(self):
#         self.buy_orders: Dict[int, int] = {}
#         self.sell_orders: Dict[int, int] = {}
# """Every price level at which there are buy orders should always be strictly lower than all the levels at which there are sell orders. 
#         If not, then there is a potential match between buy and sell orders, and a trade between the bots should have happened.
        
#         positive for buy, negative for sell
#         """
        

# #finnaly send order: 
# Symbol = str

# class Order:
#     def __init__(self, symbol: Symbol, price: int, quantity: int) -> None:
#         self.symbol = symbol
#         self.price = price
#         self.quantity = quantity

#     def __str__(self) -> str:
#         return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"

#     def __repr__(self) -> str:
#         return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"

#  """1. The symbol of the product for which the order is sent.
# 2. The price of the order: the maximum price at which the algorithm wants to buy in case of a BUY order, 
# or the minimum price at which the algorithm wants to sell in case of a SELL order.
# 3. The quantity of the order: the maximum quantity that the algorithm wishes to buy or sell. If the sign of 
# the quantity is positive, the order is a buy order, if the sign of the quantity is negative it is a sell order.
#         """
        
        
#  """If there are active orders from counterparties for the same product against which the algorithms’ orders can be matched,
#  the algorithms’ order will be (partially) executed right away. If no immediate or partial execution is possible, the remaining 
#  order quantity will be visible for the bots in the market, and it might be that one of them sees it as a good trading opportunity
#  and will trade against it. If none of the bots decides to trade against the remaining order quantity, it is cancelled. 
#         """
        
        
        
# #there is position limit for each product, specified 
# # https://imc-prosperity.notion.site/Writing-an-Algorithm-in-Python-19ee8453a0938114a15eca1124bf28a1#:~:text=Rounds%E2%80%99%20section%20on-,Prosperity%203%20Wiki.,-Below%20two%20example
        
        