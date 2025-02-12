# web-scrape

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

docker pull selenium/standalone-chrome
docker run --rm -d -p 4444:4444 --shm-size=2g --env HTTP_PROXY="http://ksafhlba-rotate:ovf9p2blgo9b@p.webshare.io:80" selenium/standalone-chrome


```
- https://github.com/seleniumbase/SeleniumBase/issues/3202
    - Can't mix Wire Mode with Grid Mode
    - Can't mix UC Mode with Wire Mode
    - Can't mix Grid Mode with UC Mode
    
    - Use Wire Mode without Grid Mode.
    - Use Grid Mode without Wire Mode.

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

## Guide
- https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/
- https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
- https://pgaref.com/blog/python-proxy/
- https://stackoverflow.com/questions/53657215/how-to-run-headless-chrome-with-selenium-in-python
- https://proxiesapi.com/articles/the-complete-httpbin-cheatsheet-in-python
- https://stackoverflow.com/questions/76430192/getting-typeerror-webdriver-init-got-an-unexpected-keyword-argument-desi

https://github.com/SeleniumHQ/docker-selenium#building-the-images