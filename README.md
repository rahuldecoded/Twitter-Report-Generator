# Twitter-Report-Generator
The script will generate various reports using Twitter Streaming API


## Getting Started

1. Install Python3
2. Create an virtual environment. `virtualenv -p python3 venv`
3. Activate the virtal environment.  
  `source activate venv` (Linux)  
  `.\venv\Scripts\activate` (Windows)
4. Install the required packages. `pip install -r requirements.txt`
5. Add your keys in run.py
```
import tweepy
import json

consumer_key = 'your consumer key'
consumer_secret = 'your consumer secret'

access_token = 'access token'
access_token_secret = 'access token secret'
```
6. Change the keyword according to your choice.
```
myStream.filter(track=['enter your keyword'])
```
7. Run the application. `python run.py`

