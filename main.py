import requests

class StockPortfolioTracker:
      def __init__(self, api_key):
          self.portfolio = {}
          self.api_key = api_key

      def add_stock(self, symbol, quantity):
          if symbol not in self.portfolio:
              self.portfolio[symbol] = {'quantity': quantity, 'average_price': None}
              self.update_stock_data(symbol)
          else:
              print(f"You already own {symbol}. Use 'update_stock' to modify your holdings.")

      def update_stock(self, symbol, quantity):
          if symbol in self.portfolio:
              self.portfolio[symbol]['quantity'] += quantity
              self.update_stock_data(symbol)
          else:
              print(f"You don't own {symbol}. Use 'add_stock' to add it to your portfolio.")

      def remove_stock(self, symbol):
          if symbol in self.portfolio:
              del self.portfolio[symbol]
          else:
              print(f"You don't own {symbol} in your portfolio.")

      def update_stock_data(self, symbol):
          api_url = f"https://www.alphavantage.co/query"
          function = "GLOBAL_QUOTE"
          symbol_param = symbol.upper()
          data = {
              "function": function,
              "symbol": symbol_param,
              "apikey": self.api_key
          }

          try:
              response = requests.get(api_url, params=data)
              response.raise_for_status()
              stock_data = response.json()

              if 'Global Quote' in stock_data:
                  stock_price = float(stock_data['Global Quote']['05. price'])
                  if self.portfolio[symbol]['average_price'] is None:
                      self.portfolio[symbol]['average_price'] = stock_price
                  else:
                      total_investment = self.portfolio[symbol]['average_price'] * self.portfolio[symbol]['quantity']
                      total_investment += stock_price * self.portfolio[symbol]['quantity']
                      self.portfolio[symbol]['average_price'] = total_investment / (2 * self.portfolio[symbol]['quantity'])
              else:
                  print(f"Failed to fetch data for {symbol}")
          except requests.exceptions.RequestException as e:
              print(f"Error: {e}")

      def display_portfolio(self):
          print("Stock Portfolio:")
          for symbol, data in self.portfolio.items():
              print(f"{symbol}: Quantity - {data['quantity']}, Average Price - {data['average_price']:.2f}")

  # Get user input
api_key = input("Enter your Alpha Vantage API key: ")
portfolio_tracker = StockPortfolioTracker(api_key)

while True:
      print("\nMenu:")
      print("1. Add Stock")
      print("2. Update Stock")
      print("3. Remove Stock")
      print("4. Display Portfolio")
      print("5. Quit")

      choice = input("Enter your choice (1-5): ")

      if choice == '1':
          symbol = input("Enter stock symbol: ")
          quantity = int(input("Enter quantity: "))
          portfolio_tracker.add_stock(symbol, quantity)
      elif choice == '2':
          symbol = input("Enter stock symbol: ")
          quantity = int(input("Enter quantity to update: "))
          portfolio_tracker.update_stock(symbol, quantity)
      elif choice == '3':
          symbol = input("Enter stock symbol to remove: ")
          portfolio_tracker.remove_stock(symbol)
      elif choice == '4':
          portfolio_tracker.display_portfolio()
      elif choice == '5':
          print("Exiting the program. Goodbye!")
          break
      else:
          print("Invalid choice. Please enter a number between 1 and 5.")
