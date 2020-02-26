from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store in dictionary.
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        headline = slide_elem.find("div", class_='content_title').get_text()
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    
    return headline, news_p

def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    
    img = img_soup.select_one("figure.lede a img")
    
    try:
        img_url_rel = img.get("src")
        
    except AttributeError:
        return None
    
    img_url = f"https://www.jpl.nasa.gov{img_url_rel}"
    
    return img_url

def hemispheres(browser):
    
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    hemisphere_image_urls = []

  
    links = browser.find_by_css("a.product-item h3")


    for i in range(len(links)):
        hemisphere = {}

        browser.find_by_css("a.product-item h3")[i].click()

        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']

        hemisphere['title'] = browser.find_by_css("h2.title").text

        hemisphere_image_urls.append(hemisphere)

        browser.back()
        
    return hemisphere_image_urls

# def mars_facts():
#     try:
#         df = pd.read_html("http://space-facts.com/mars/")[1]
#     except BaseException:
#         return None
    
#     df.columns = ["description", "value"]
#     df.set_index("description",inplace=True)
    
#     return df.to_html(classes="table table-striped")

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

