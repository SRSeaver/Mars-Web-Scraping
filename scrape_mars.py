#Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd

# Function to instantiate a browser object using chromdriver
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
    
# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

def scrape_news():    
# URL of NASA page
	url = 'https://mars.nasa.gov/news/'
	
	# Instantiate the browser, store in browser variable
	browser = init_browser()
	# Go to url using .visit
	browser.visit(url)
	# Force a pause to give the articles a chance to load
	time.sleep(2)
	# Scrape the html text
	html = browser.html
	# The browser is still open so quit browser
	browser.quit()
	
	# Beautifulsoup object
	soup = bs(html, 'html.parser')
	
	# Retrieve all the parent divs of news titles and paragraphs
	result = soup.find('ul', class_='item_list')
	
	
	# Dig through the results to get the first slide, title, and paragraph
	slide = result.find('div', class_='list_text')
	news_title = slide.find('div', class_='content_title').text
	paragraph = slide.find('div', class_='article_teaser_body').text
	
	return(news_title, paragraph)
	
def scrape_image(): 	
	# Url for JPL Featured Space Image
	mars_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	# Instantiate the browser, store in browser variable
	browser = init_browser()
	# Go to browser with .visit
	browser.visit(mars_images_url)
	# Force a pause to give page a chance to completely load
	time.sleep(2)
	# Scrape the images
	images_html = browser.html
	# The browser is still open so quit browser
	browser.quit()
	
	# Beautifulsoup object, 
	image_soup = bs(images_html, 'html.parser')
	
	# Narrow down the image_soup and dig through to the feature image 
	image_result = image_soup.find('div', class_='carousel_items').find('article')['style']

	# split the returned string to get only the relevant part for the url
	image_url = image_result.split("'")[1]
	
	# Combine "https://www.jpl.nasa.gov" and the image_url to create the featured image url
	featured_image_url = f"https://www.jpl.nasa.gov{image_url}"
	
	return(featured_image_url)
	

def scrape_weather():
	# Url for Mars weather tweet
	mars_tweet_url = 'https://twitter.com/marswxreport?lang=en'
	# Instantiate the browser, store in browser variable
	browser = init_browser()
	# Go to browser with .visit
	browser.visit(mars_tweet_url)
	# Force a pause to give page a chance to completely load
	time.sleep(2)
	# Scrape the images
	tweets_html = browser.html
	# The browser is still open so quit browser
	browser.quit()
	
	tweet_soup = bs(tweets_html, 'html.parser')

	# Get the latest Mars weather tweet and get the weather text
	weather_result = tweet_soup.find('div', class_='tweet')
	weather = weather_result.find('p', class_='tweet-text').text
	
	return(weather)	
	
		
def scrape_facts():	
	# Url for Mars facts
	mars_facts_url = 'https://space-facts.com/mars/'
	
	# Use pandas to get the tables from the url
	mars_facts = pd.read_html(mars_facts_url)
	facts_df = mars_facts[0]
	
	# Add column names
	facts_df.columns = ['Fact', 'Value']
	facts_df = facts_df.set_index("Fact")
	
	# Use Pandas to convert the data to a HTML table string
	facts_html_table = facts_df.to_html()
	facts_html_table = facts_html_table.replace('\n', '')
	
	return(facts_html_table)
	
def scrape_hemispheres(): 
	# Url for hemispheres
	hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	# Instantiate the browser, store in browser variable
	browser = init_browser()
	# Go to browser with .visit
	browser.visit(hemispheres_url)
	# Scrape the page
	hemispheres_html = browser.html
	
	# Get the list of partial hrefs for each link
	hemisphere_soup = bs(hemispheres_html, 'html.parser')
	
	# Create empty dictionary to hold titles and urls
	hemisphere_dicts = []
	
	# Get the links to click
	buttons = hemisphere_soup.find_all('h3')
	
	# Loop through the buttons to get the titles and url links
	for button in buttons:
	    hemisphere_dict = {}
	    
	    t = button.get_text()
	    title = t.strip(' Enhanced')
	    hemisphere_dict['title'] = title
	    browser.click_link_by_partial_text(t)
	    time.sleep(2)
	    url = browser.find_link_by_partial_href('download')['href']
	    time.sleep(2)
	    hemisphere_dict['img_url'] = url
	    hemisphere_dicts.append(hemisphere_dict)
	    browser.visit(hemispheres_url)
	    
	# The browser is still open so quit browser
	browser.quit()
	return(hemisphere_dicts)
	    
	
def scrape():
	news_title, paragraph = scrape_news()
	image = scrape_image()
	weather = scrape_weather()
	facts = scrape_facts()
	hemispheres = scrape_hemispheres()
	
	
	mars_dictionary = {
	"title": news_title,
	"paragraph": paragraph,
	"image": image,
	"weather": weather,
	"facts": facts,
	"hemispheres": hemispheres
	}
	
	return mars_dictionary

	
	
	
	
					
		
