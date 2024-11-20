import requests
from bs4 import BeautifulSoup

# Function to get the latest tweet from a user
def get_latest_tweet(username):
    url = f'https://twitter.com/{username}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the latest tweet
    tweets = soup.find_all('div', {'data-testid': 'tweet'})
    if tweets:
        latest_tweet = tweets[0].get_text()
        return latest_tweet
    return None
