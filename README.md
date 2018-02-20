# foodDescriptionBot
A Twitter bot that describes food images

## Usage

1. Clone the repository ```git clone https://github.com/sqrg/foodDescriptionBot.git```
2. Install the required packages with pip ```pip install -r requirements.txt```
3. Create a ```database.db``` file and leave it empty
4. Create a ```credentials.py``` file and add the following lines (replace ```abc123``` with your own keys)

```
# Reddit credentials
CLIENT_ID = 'abc123'
CLIENT_SECRET = 'abc123'

# Azure credentials
SUBSCRIPTION_KEY = 'abc123'

# Azure URL
AZURE_URL = 'https://brazilsouth.api.cognitive.microsoft.com/vision/v1.0/analyze'

# Twitter credentials
CONSUMER_KEY = 'abc123'
CONSUMER_SECRET = 'abc123'
ACCESS_TOKEN = 'abc123'
ACCESS_TOKEN_SECRET = 'abc123'
```

(You can also use a different AZURE_URL)

5. Then just do ```python main.py``` and the bot will start working

## TO DO
* Add some kind of logging
* Support URLs that don't end with '.jpg' or '.png'
