from constants import NIFTY50
from monthly_closing_prices import main


for symbol in NIFTY50:
  print('Starting processing for %s.' % symbol)
  main(symbol)
  print('Processing for %s completed.' % symbol)
