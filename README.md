# web-scrape
This repository is updated as at `15/2/2025`.

## Environment
```sh
# Create python virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate.bat
```

## Pre-requisite
```sh
pip install -r requirements.txt
```

- Run a standalone chrome or download chrome driver/exe at [https://googlechromelabs.github.io/chrome-for-testing/](https://googlechromelabs.github.io/chrome-for-testing/)
```sh
docker pull selenium/standalone-chrome
docker run --rm -d -p 4444:4444 --shm-size=2g selenium/standalone-chrome

# Testing
docker exec -it <container id> sh
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://httpbin.org/get
```


## Selenium functionalities
- Additional features
    1. `uc mode` : Undetected-Chromedriver Mode [Link](https://seleniumbase.io/help_docs/uc_mode/)
    2. `wire` : implement proxy using selenium-wire package
    3. `standalone chrome` : Remote chrome (save the hassle of downloading chrome driver)
    4. `proxy` : proxy flag in seleniumbase package
- [Issue 3202] (https://github.com/seleniumbase/SeleniumBase/issues/3202)
    - Can't mix Wire Mode with Grid Mode
    - Can't mix UC Mode with Wire Mode
    - Can't mix Grid Mode with UC Mode (false)

| Package | Combination    | Doable?    | Remarks    |
| :-----   | :--- | :---: | :--- |
| seleniumbase | `standalone chrome` + `wire`  | &cross;   | TypeError: WebDriver.__init__() got an unexpected keyword argument 'desired_capabilities' <br> Compatibility issue with selenium-wire and selenium (subpackage in seleniumbase) as selenium-wire has not been maintained  |
| seleniumbase | `uc mode` +  `wire`    | &cross;    | AttributeError: 'Chrome' object has no attribute 'set_wire_proxy'   |
| seleniumbase | `standalone chrome` + `proxy`    | &cross;    | Runnable but proxy flag is not applied   |
| seleniumbase | `uc mode` + `standalone chrome`   | &check;    |   |
| seleniumbase | `uc mode` + `proxy`   | &check;    |   |
| **selenium-wire** | `standalone chrome` + `wire`  | &check;  | Downgrade selenium version. Refer to [requirements-downgrade.txt](./requirements-downgrade.txt)|

## Proxies
- Rotating proxies (10 free proxies)
    - [https://www.webshare.io/](https://www.webshare.io/)
- Python Library - package wrapper that get from free proxy list
    - [proxy_randomizer](https://github.com/Esequiel378/proxy_randomizer/tree/master)
- Free Proxy List
    - [https://free-proxy-list.net/](https://free-proxy-list.net/)
    - https://topproxylinks.com/
- User Agent List
    - [Chrome](https://explore.whatismybrowser.com/useragents/explore/software_name/chrome/)
    - https://www.useragents.me/
    - https://github.com/fake-useragent/fake-useragent
- Endpoint for testing
    - http://httpbin.org/get
    - https://httpbin.org/ip
    - https://api.ipify.org

## Web-scrape
1. Google News
    - Google News Tab - require use of selenium *(A section within Google Search that displays news articles related to your search query, providing a wider range of news sources on a topic.)*
        - https://www.google.com/search?q=Singapore&tbs=cdr:1,cd_min:1/1/2025,cd_max:2/2/2025&tbm=nws'
            - encoded version: https://www.google.com/search?q=Singapore&tbs=cdr%3A1%2Ccd_min%3A1%2F1%2F2025%2Ccd_max%3A2%2F2%2F2025&tbm=nws
        - **q=Singapore** : query
        - **tbs=cdr:1** : search for results within a custom date range
        - **cd_min:1/1/2025,cd_max:2/2/2025** : date range
        - **tbm=nws** : get results from Google news
    - News RSS page: can return only up to 100 results. More details [here](https://www.newscatcherapi.com/blog/google-news-rss-search-parameters-the-missing-documentaiton#toc-8) and [stackoverflow](https://stackoverflow.com/questions/78194686/how-to-web-scrape-google-news-headline-of-a-particular-year-e-g-news-from-2020)
        - https://news.google.com/rss/search?q=Singapore+after:2020-06-01+before:2020-06-02&hl=en-SG&gl=SG&ceid=SG:en
        - **q=Singapore** : query
        - **after:2020-06-01+before:2020-06-02** : search for results within a custom date range
        - **hl=en-SG&gl=SG&ceid=SG:en** : country, location and geolocation parameters. *(automatically append based on your location)*
        - Can choose to leave out **/rss/** to get the google page instead of xml
        - Others:
            ```
            # top news
            https://news.google.com/rss

            # by topic
            https://news.google.com/rss/topics/<TOPIC_ID>
            https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pKVGlnQVAB

            # by topic section
            https://news.google.com/rss/topics/<TOPIC_ID>/sections/<SECTION_ID>
            https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pKVGlnQVAB/sections/CAQiSkNCQVNNUW9JTDIwdk1EWnVkR29TQldWdUxVZENHZ0pKVGlJT0NBUWFDZ29JTDIwdk1EZGljekFxQ2dvSUVnWlVaVzV1YVhNb0FBKi4IACoqCAoiJENCQVNGUW9JTDIwdk1EWnVkR29TQldWdUxVZENHZ0pKVGlnQVABUAE?hl=en-IN&gl=IN&ceid=IN%3Aen

            # by custom search keyword
            https://news.google.com/rss/search?q=<KEYWORD>
            https://news.google.com/rss/search?q=instagram

            # by country and language
            https://news.google.com/rss?hl=<LANGUAGE_CODE>&gl=<COUNTRY_CODE>&ceid=<COUNTRY_CODE>:<LANGUAGE_CODE>
            https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en
            ```
2. *Pending...*

## Guide
- https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/
- https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
- https://pgaref.com/blog/python-proxy/
- https://stackoverflow.com/questions/53657215/how-to-run-headless-chrome-with-selenium-in-python
- https://proxiesapi.com/articles/the-complete-httpbin-cheatsheet-in-python
- https://stackoverflow.com/questions/76430192/getting-typeerror-webdriver-init-got-an-unexpected-keyword-argument-desi
- https://stackoverflow.com/questions/30109037/how-can-i-forward-localhost-port-on-my-container-to-localhost-on-my-host


## Others
- SeleniumBase: ChomeDriver downloaded for you automatically. **(Have to install chrome.exe yourself)**
    ```
    Warning: uc_driver not found. Getting it now:

    *** chromedriver to download = 133.0.6943.98 (Latest Stable) 

    Downloading chromedriver-win64.zip from:
    https://storage.googleapis.com/chrome-for-testing-public/133.0.6943.98/win64/chromedriver-win64.zip ...
    Download Complete!

    Extracting ['chromedriver.exe'] from chromedriver-win64.zip ...
    Unzip Complete!

    The file [uc_driver.exe] was saved to:
    C:\Users\gansh\Downloads\2 - Projects\web-scrape\.venv\Lib\site-packages\seleniumbase\drivers\
    uc_driver.exe

    Making [uc_driver.exe 133.0.6943.98] executable ...
    [uc_driver.exe 133.0.6943.98] is now ready for use!

    -----------------------------------------------

    Warning: chromedriver not found. Getting it now:

    *** chromedriver to download = 133.0.6943.98 (Latest Stable) 

    Downloading chromedriver-win64.zip from:
    https://storage.googleapis.com/chrome-for-testing-public/133.0.6943.98/win64/chromedriver-win64.zip ...
    Download Complete!

    Extracting ['chromedriver.exe'] from chromedriver-win64.zip ...
    Unzip Complete!

    The file [chromedriver.exe] was saved to:
    C:\Users\gansh\Downloads\2 - Projects\web-scrape\.venv\Lib\site-packages\seleniumbase\drivers\
    chromedriver.exe

    Making [chromedriver.exe 133.0.6943.98] executable ...
    [chromedriver.exe 133.0.6943.98] is now ready for use!

    ```