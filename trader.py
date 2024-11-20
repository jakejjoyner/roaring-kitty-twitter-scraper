from logging import lastResort
import alpaca_trade_api as tradeapi
from requests import options
import config
from bs4 import BeautifulSoup
import time
from selenium import webdriver

# Alpaca API credentials
ALPACA_API_KEY = config.api_key
ALPACA_API_SECRET = config.api_secret
BASE_URL = config.base_url

# Alpaca authentication
alpaca_api = tradeapi.REST(ALPACA_API_KEY, ALPACA_API_SECRET, BASE_URL, api_version='v2')

# Function to buy stock
def buy_stock(symbol, qty=1):
    try:
        alpaca_api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        print(f"Market order submitted: buy {qty} share(s) of {symbol}")
    except tradeapi.rest.APIError as e:
        print(f"API Error submitting order: {e}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    username = 'wallstreetbets'   #twitter username

    target_url = f"https://x.com/{username}"

    # op = webdriver.ChromeOptions()
    # op.add_argument('headless')

    driver = webdriver.Chrome() #open browser
    driver.get(target_url) #open url
    time.sleep(5) #wait for site to load

    resp = driver.page_source
    soup = BeautifulSoup(resp, 'html.parser') #parse html with bs4
    tweets = soup.find_all('article', {'data-testid': 'tweet'}) #find all tweets with data-testid equal to tweet
    last_tweet_id = tweets[1] #access 1st element to make sure you bypass pinned post

    while True:
        driver.refresh() #refresh the site
        time.sleep(2) #wait two seconds
        soup = BeautifulSoup(resp, 'html.parser') #parse the html
        tweets = soup.find_all('article', {'data-testid': 'tweet'}) # find the tweets
        tweet = tweets[1] #access first element of the list
        print(f"{tweet}") #print it

        if tweet != last_tweet_id: #if new tweet not equal to last tweet
            print(f"New tweet from {username}: {tweet}")
            print(f"\n")
            buy_stock('GME') #buy stock
            last_tweet_id = tweet #set last tweet equal to latest tweet
        else:
            print("No new tweets.")
            last_tweet_id = tweet #set the last tweet equal to the latest tweet
        time.sleep(6)  # Check for new tweets every 6 seconds

if __name__ == "__main__":
    main()
