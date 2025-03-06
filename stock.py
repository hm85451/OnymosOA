import threading

class HashTable:
    def __init__(self, size=1024):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def _hash(self, key):
        return hash(key) % self.size
    
    def insert(self, key, value):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1].append(value)
                return
        self.table[index].append([key, [value]])
    
    def get(self, key):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        return None
    
    def contains(self, key):
        return self.get(key) is not None
    
    def iterate(self):
        for bucket in self.table:
            for pair in bucket:
                key = pair[0]
                values = pair[1]
                print(f"Key: {key}, Values: {values}")


class Order:
    def __init__(self, order_type, ticker_symbol, quantity, price):
        self.order_type = order_type
        self.ticker_symbol = ticker_symbol
        self.quantity = quantity
        self.price = price
        
    def __repr__(self):
        return f"Order(ticker_symbol={self.ticker_symbol}, quantity={self.quantity}, price={self.price})"

class OrderBook:
    def __init__(self):
        self.buy_orders = HashTable()  # custom hashtable
        self.sell_orders = HashTable()  # custom hashtable

    def add_order(self, order_type, ticker_symbol, quantity, price):
        order = Order(order_type, ticker_symbol, quantity, price)  # Create the order object
        
        if order_type == "buy":
            if not self.buy_orders.contains(ticker_symbol):# if the ticker is not found, create the entry and order list
                self.buy_orders.insert(ticker_symbol, order)
            else:
                # Insert the order into the sorted list by price (descending)
                inserted = False
                ticker_orders = self.buy_orders.get(ticker_symbol)
                for i in range(len(ticker_orders)):
                    if ticker_orders[i].price < price:
                        ticker_orders.insert(i, order)
                        inserted = True
                        break
                
                if not inserted:  # If the order wasn't inserted, append to the end
                    ticker_orders.append(order)

        elif order_type == "sell":
            if not self.sell_orders.contains(ticker_symbol):# if the ticker is not found, create the entry and order list
                self.sell_orders.insert(ticker_symbol, order)
            else:
                # Insert the sell order in ascending order (lowest price first)
                inserted = False
                ticker_orders = self.sell_orders.get(ticker_symbol)
                for i in range(len(ticker_orders)):
                    if ticker_orders[i].price > price:
                        ticker_orders.insert(i, order)
                        inserted = True
                        break
                
                if not inserted:
                    ticker_orders.append(order)
    
    def match_orders(self):
        for i in range(self.buy_orders.size):
            for buy_pair in self.buy_orders.table[i]:
                ticker = buy_pair[0]
                buy_orders = buy_pair[1]
                
                sell_orders = self.sell_orders.get(ticker)
                if not sell_orders:
                    continue

                # Try to match orders
                i, j = 0, 0
                while i < len(buy_orders) and j < len(sell_orders):
                    buy_order = buy_orders[i]
                    sell_order = sell_orders[j]

                    if buy_order.price >= sell_order.price:
                        match_quantity = min(buy_order.quantity, sell_order.quantity)
                        print(f"Matched {match_quantity} of {ticker} at price {sell_order.price}")
                        buy_order.quantity -= match_quantity
                        sell_order.quantity -= match_quantity

                        if buy_order.quantity == 0:
                            i += 1
                        if sell_order.quantity == 0:
                            j += 1
                    else:
                        break 
                    

def simulate_order_matching(order_book):
    # Adding some random orders concurrently
    orders = [
        ("buy", "AAPL", 100, 150.00),
        ("buy", "AAPL", 50, 152.00),
        ("buy", "AAPL", 200, 155.00),
        ("buy", "AAPL", 150, 158.00),
        ("buy", "AMAZ", 150, 158.00),
        ("sell", "AMAZ", 200, 140.00),
        ("sell", "AMAZ", 150, 160.00),
        ("sell", "AAPL", 100, 150.00),
        ("sell", "AAPL", 50, 155.00),
        ("sell", "AAPL", 200, 156.00),
        ("sell", "AAPL", 150, 157.00)
    ]
    
    
    threads = []
    for order in orders:
        t = threading.Thread(target=order_book.add_order, args=order)
        threads.append(t)
        
    for t in threads:
        t.start()  # wait for all threads to finish
        
    for t in threads:
        t.join()  # wait for all threads to finish

    # After all orders have been added, attempt to match them
    order_book.match_orders()


# Test the matching functionality
def test():
    order_book = OrderBook()
     
    simulate_order_matching(order_book)
    
    print("\nAfter matching:")
    print("Buy Orders:")
    order_book.buy_orders.iterate()
    print("Sell Orders:")
    order_book.sell_orders.iterate()

# Run the test
test()

   