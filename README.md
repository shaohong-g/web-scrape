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