# Uni-Life: Multi-Perspective Complex Information-Seeking
a research project that aims to group university-related information from different resources into one platform.

# Set Up 
(make sure you are using python version 3.9.6) <br/>
git clone https://github.com/lerailovaiska-hub/DHL <br/>
cd unilife-backend<br/>
python3 -m venv venv<br/>
source venv/bin/activate<br/>
pip install flask flask-cors pandas rank-bm25<br/>
pip install -r requirements.txt

python3 app.py<br/>

### Project description
## UniLife backend:
Used to collect data, clean it, and perform quantitative and qualitative analysis. This code shows the methods that we used to obtain our outcomes through topic modelling and data visualisation. The folder includes both python files and other format files, such as csv's with data and txt files, scraped with API keys. 

clean_posts.py - cleaning function, tokenizer

reddit_posts.txt - scraping reddit 

scraping-programmes.txt - scraping uva programmes

uva_facebook_posts.csv - scraped facebook posts 

search_evaluation.py - search engine evaluation

## UniLife frontend:
Used to create the interface. The interface is available through a local host. JavaScript and HTML work together to provide the structure and the interactive basis of the website. 

home.html, index.html and signup.html - structuring website pages

home.js, index.js and signup.js - interactivity, website behaviour and search engine

styles.css - styling and formatting
