import json
from urllib.parse import urlparse, parse_qs
import requests
from pprint import pprint
from requests.exceptions import ConnectTimeout
from time import sleep

# API Key is obtained from the Webex Teams developers website.
api_key = 'MzcwZThhMGUtNTc0Yy00ZGE3LWEwN2YtYzk1MzY2NWE5YTNlOGIwMzM2NWEtYzIz_PF84_consumer'
# roomId is a required parameter when fetching messages, 
# and identifies the space (room) from which the messages will be retrieved.
# roomId can be configured here, or collected by the set_room_id method
room_id = 'Y2lzY29zcGFyazovR1'
# Maximum number of messages per page
max_items = 3
# Webex Teams messages API endpoint
base_url = 'https://api.ciscospark.com/v1/messages'


class Messenger(): 
    def __init__(self, base_url=base_url, api_key=api_key, room_id=room_id, requests=requests, request_retries=3): 
        self.base_url = base_url 
        self.api_key = api_key 
        self.room_id = room_id 
        self.api_url = f'{self.base_url}?roomId={self.room_id}&max={max_items}' 
        self.headers = { 
            "Authorization": f"Bearer {api_key}", 
        } 
        self.requests = requests 
        self.request_retries = request_retries 


    def get_messages(self): 
        """ Get a list of messages in a room.  
        Maximum number of items per page is set to 3 """ 

        tries = 0 
        while True: 
            tries += 1 
            self.response = self.requests.get(self.api_url, headers=self.headers) 

            # Everything ok? 
            if self.response: 
                self.print_current_page() 
                return self.response 

            # If not, should we try again later? 

            # Throw if not ok (2xx) 
            self.response.raise_for_status() 
  
            # Network timeout, should we retry? 

        return self.response 

    def print_current_page(self): 
        """ Print just the text of the messages  
        on the current page """ 
        for msg in (self.response.json())['items']: 
            print(msg['text']) 
        print()

