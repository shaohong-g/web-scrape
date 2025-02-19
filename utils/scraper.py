import requests
import json
import traceback
import time
import bs4 as bs
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta, date
from IPython.display import display

class GoogleRSSFeedScraper():
    def __init__(self, proxy=None):
        self.proxy = proxy
        self.state = {}
        self.base_url = "https://news.google.com/rss/search?"
    
    def scrape(self, search_query, start_time=datetime.now().date(), end_time = datetime.now().date(), scrape_period = 7, add_url_parameters={}, save_state=False, save_result=False, save_folder="./data", preview_result=True, sleep_interval=5):
        """
        Web scrape google news rss feeds. 
        - Use date(YYYY, MM, DD) to initiate date arguments. eg: date(2025, 2, 19)
        Args:
            search_query (String): Search query
            start_time (Date): Default to datetime.now(). 
            end_time (Date): Default to datetime.now(). 
            scrape_period (int): no. of days for each scrape instance (inclusive of start and end: must be more than 1)
            add_url_parameters (dict): Additional url parameters
            save_state (boolean): Save state progress in json file. format: f"/scrape_state_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
            save_result (boolean): Save dataframe as pickle file. format: f"/scrape_result_{datetime.now().strftime('%Y%m%d%H%M%S')}.pkl"
            save_folder (String): root folder to save state and result
            preview_result (boolean): Show pandas dataframe after processing
            sleep_interval (int): Sleep for 3 seconds for every X interations (intervals).
        """
        if end_time < start_time:
            raise ValueError("End time must be greater than start time!")
        elif scrape_period < 1:
            raise ValueError("Scrape period must be more than 1!")
        
        # Save state
        self.state = {
            "parameters": {
                "search_query": search_query,
                "start_time": start_time,
                "end_time": end_time,
                "scrape_period": scrape_period,
                "add_url_parameters": add_url_parameters
            },
            "iter_no": 0
        }
        to_time = None
        df = pd.DataFrame()
        try:
            scrape_period -= 1
            while start_time <= end_time:
                to_time = min(start_time + timedelta(days=scrape_period), end_time)
                # Format and encode URL
                url_parameters = {"q": f"{search_query} after:{start_time.strftime('%Y-%m-%d')} before:{to_time.strftime('%Y-%m-%d')}", **add_url_parameters}
                url = self.base_url + urllib.parse.urlencode(url_parameters)

                self.state["to_time"] = to_time
                self.state["url"] = url
                
                # GET request and parse
                df_intermediate = self.fetch_and_parse(url, pandas= True)
                if len(df_intermediate) > 0:
                    df = pd.concat([df,df_intermediate])
                    df.drop_duplicates(subset=["pubDate", "title", "source"], inplace=True)
                    df.sort_values(by='pubDate', inplace=True)
                    df.reset_index(drop=True, inplace=True)

                self.state["iter_no"] += 1
                if self.state["iter_no"] % sleep_interval == 0:
                    print(f"-- Current state: {start_time}-{to_time}, record_count: {len(df)}, iter: {self.state['iter_no']}")
                    time.sleep(3)
                start_time += timedelta(days=scrape_period+1)  
        except Exception as e:
            print(f"########## Error: {start_time}-{to_time} {end_time} #########")
            print(traceback.format_exc())
        finally:
            self.state["record_count"] = len(df)
            if preview_result:
                print(f"############## Result: {len(df)} records ##############")
                display(df.tail())
            if save_state:
                save_path = save_folder.rstrip("/") + f"/scrape_state_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
                self.state["save_state_path"] = save_path
                with open(save_path, "w") as f:
                    json.dump(self.state, f, indent=4, default=str)
                print("Saved state to:", save_path)
            if save_result and len(df) > 0:
                save_path = save_folder.rstrip("/") + f"/scrape_result_{datetime.now().strftime('%Y%m%d%H%M%S')}.pkl"
                self.state["save_result_path"] = save_path
                df.to_pickle(save_path)
                print("Saved pickle to:", save_path)
            

    def fetch_and_parse(self, url, pandas= True):
        response = requests.get(url, proxies=self.proxy) 
        soup = bs.BeautifulSoup(response.text,'xml')

        result = []
        for item in soup.find_all('item'):
            result.append({
                "title": item.title.text,
                "link": item.link.text,
                "pubDate": item.pubDate.text,
                "source": item.source.text,
                "description": item.description.text,
            })
        if pandas:
            if len(result) == 0:
                return pd.DataFrame()
            df = pd.DataFrame(result)
            df['pubDate'] = pd.to_datetime(df['pubDate'], format='%a, %d %b %Y %H:%M:%S %Z', utc=True)
            return df
        return result
    

class BloombergLawScraper():
    def __init__(self, proxy=None):
        self.proxy = proxy
        self.state = {}
        self.base_url = "https://news.bloomberglaw.com/api/v1/rss/litigation?"
    
    def scrape(self, search_query, start_time=datetime.now().date(), end_time = datetime.now().date(), fetch_limit=10, scrape_period = 7, add_url_parameters={}, save_state=False, save_result=False, save_folder="./data", preview_result=True, sleep_interval=5):
        """
        Web scrape google news rss feeds. 
        - Use date(YYYY, MM, DD) to initiate date arguments. eg: date(2025, 2, 19)
        Args:
            search_query (String): Search query
            start_time (Date): Default to datetime.now(). 
            end_time (Date): Default to datetime.now(). 
            fetch_limit (int): Number of items fetch (default is 10)
            scrape_period (int): no. of days for each scrape instance (inclusive of start and exclusive end: must be more than 1)
            add_url_parameters (dict): Additional url parameters
            save_state (boolean): Save state progress in json file. format: f"/scrape_state_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
            save_result (boolean): Save dataframe as pickle file. format: f"/scrape_result_{datetime.now().strftime('%Y%m%d%H%M%S')}.pkl"
            save_folder (String): root folder to save state and result
            preview_result (boolean): Show pandas dataframe after processing
            sleep_interval (int): Sleep for 3 seconds for every X interations (intervals).
        """
        if end_time < start_time:
            raise ValueError("End time must be greater than start time!")
        elif scrape_period < 1:
            raise ValueError("Scrape period must be more than 1!")
        
        # Save state
        self.state = {
            "parameters": {
                "search_query": search_query,
                "start_time": start_time,
                "end_time": end_time,
                "scrape_period": scrape_period,
                "add_url_parameters": add_url_parameters,
                "fetch_limit": fetch_limit
            },
            "iter_no": 0
        }
        to_time = None
        df = pd.DataFrame()
        try:
            while start_time <= end_time:
                to_time = min(start_time + timedelta(days=scrape_period), end_time)
                # Format and encode URL
                url_parameters = {"query": search_query, "startDate": start_time.strftime('%Y-%m-%d'),"endDate": to_time.strftime('%Y-%m-%d'), "limit": fetch_limit, **add_url_parameters}
                url = self.base_url + urllib.parse.urlencode(url_parameters)

                self.state["to_time"] = to_time
                self.state["url"] = url
                
                # GET request and parse
                df_intermediate = self.fetch_and_parse(url, pandas= True)
                if len(df_intermediate) > 0:
                    df = pd.concat([df,df_intermediate])
                    df.drop_duplicates(subset=["pubDate", "title"], inplace=True)
                    df.sort_values(by='pubDate', inplace=True)
                    df.reset_index(drop=True, inplace=True)

                self.state["iter_no"] += 1
                if self.state["iter_no"] % sleep_interval == 0:
                    print(f"-- Current state: {start_time}-{to_time}, record_count: {len(df)}, iter: {self.state['iter_no']}")
                    time.sleep(3)
                start_time += timedelta(days=scrape_period)  
        except Exception as e:
            print(f"########## Error: {start_time}-{to_time} {end_time} #########")
            print(traceback.format_exc())
        finally:
            self.state["record_count"] = len(df)
            if preview_result:
                print(f"############## Result: {len(df)} records ##############")
                display(df.tail())
            if save_state:
                save_path = save_folder.rstrip("/") + f"/scrape_state_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
                self.state["save_state_path"] = save_path
                with open(save_path, "w") as f:
                    json.dump(self.state, f, indent=4, default=str)
                print("Saved state to:", save_path)
            if save_result and len(df) > 0:
                save_path = save_folder.rstrip("/") + f"/scrape_result_{datetime.now().strftime('%Y%m%d%H%M%S')}.pkl"
                self.state["save_result_path"] = save_path
                df.to_pickle(save_path)
                print("Saved pickle to:", save_path)
            

    def fetch_and_parse(self, url, pandas= True):
        response = requests.get(url, proxies=self.proxy) 
        soup = bs.BeautifulSoup(response.text,'xml')

        result = []
        for item in soup.find_all('item'):
            result.append({
                "title": item.title.text,
                "link": item.link.text,
                "pubDate": item.pubDate.text,
                "description": item.description.text,
                "topic": list(map(lambda x: x.text, item.find_all('md:topic')))
            })
        if pandas:
            if len(result) == 0:
                return pd.DataFrame()
            df = pd.DataFrame(result)
            df['pubDate'] = pd.to_datetime(df['pubDate'], format='%a, %d %b %Y %H:%M:%S %z', utc=True)
            return df
        return result