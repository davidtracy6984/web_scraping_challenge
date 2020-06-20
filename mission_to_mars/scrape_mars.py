from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd
import time

# Create an executable path, initialize chrome driver
#executable_path = {"executable_path": "chromedriver.exe"}
#browser = Browser("chrome", **executable_path)
def get_mars_news():
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204%3A19&blank_scope=Latest"
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')

    headline = soup.find_all('div', class_ = 'image_and_description_container')
    title = headline[0].find_all('img')[1]['alt']
    paragraph = headline[0].find_all('a')[0].text.strip()
    #print(title)
    return(title, paragraph)

def get_space_images():
    # JPL Mars Space Images
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path)

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    browser.click_link_by_id('full_image')
    moreButton = browser.links.find_by_partial_text('more info')
    moreButton.click()

    jplHtml = browser.html
    jpl_image = BeautifulSoup(jplHtml, "html.parser")
    jpl_image_url = jpl_image.select_one("figure.lede a img").get("src")
    jpl_image_url = f"https://www.jpl.nasa.gov{jpl_image_url}"
    #print(jpl_image_url)
    browser.quit()
    return(jpl_image_url)

def get_mars_weather():
    # Mars Weather
    # Create an executable path, initialize chrome driver
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path)
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)
    time.sleep(10)
    mars_tweet_url = browser.html
    mars_tweet = BeautifulSoup(mars_tweet_url,"html.parser")

    mars_tweet_url = browser.html
    mars_tweet = BeautifulSoup(mars_tweet_url,"html.parser")
    tweets = mars_tweet.find_all("div", class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    mars_weather = tweets[1].span.text
    #print(mars_weather)
    browser.quit()
    return (mars_weather)


def get_mars_facts():
    factsUrl = "https://space-facts.com/mars/"
    marsFacts_df = pd.read_html(factsUrl)[0]
    marsFacts_df.columns=["Description", "Value"]
    marsFacts_df.set_index("Description", inplace=True)
    marsFacts = marsFacts_df.to_html()     
    marsFacts2 = marsFacts.replace('<tr style="text-align: right;">','<tr style="text-align: left;">') 
    return marsFacts2

def get_mars_hemi():
    # Mars Hemispheres
    mar_hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    request_hemi = requests.get(mar_hemi_url)
    hemi_soup = BeautifulSoup(request_hemi.text, 'html.parser')

    hemi_names = hemi_soup.find_all('h3')
    hemi_links = hemi_soup.find_all('a',class_='itemLink product-item')
    #mocklist = [hemi_names,hemi_links]

    hemisphere_image_urls = []
    mini_url = "https://astrogeology.usgs.gov"
    for name,links in zip(hemi_names, hemi_links):
        hemi_name = name.text.replace(" Enhanced","")
        full_url = mini_url + links['href']
        full_image_request = requests.get(full_url)
        full_image_soup = BeautifulSoup(full_image_request.text, 'html.parser')
        full_image_link = full_image_soup.find('img', class_="wide-image")
        full_image_total_url = mini_url + full_image_link['src']
        hemisphere_image_urls.append({'title':hemi_name,"img_url":full_image_total_url})
        time.sleep(1)
    #print(hemisphere_image_urls)  
    return(hemisphere_image_urls)


def scrape():
    news_title, news_paragraph = get_mars_news()
    jpl_image_url = get_space_images()
    mars_weather = get_mars_weather()
    marFact_df = get_mars_facts()
    hemisphere_image_urls = get_mars_hemi()

    python_dict = {'News':news_title,
                'paragraph':news_paragraph,
                'SpaceImages':jpl_image_url,
                'MarsWeather':mars_weather,
                'MarsFacts':marFact_df,
                'MarsHemi':hemisphere_image_urls
                }
    return(python_dict)



