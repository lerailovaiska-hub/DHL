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
## Unilife backend:
clean_posts.py - cleaning function, tokenizer
reddit_posts.txt - scraping reddit 
scraping-programmes.txt - scraping uva programmes
uva_facebook_posts.csv - scraped facebook posts 
search_evaluation.py - search engine evaluation

## Unilife frontend:
home.html, index.html and signup.html - structuring website pages
home.js, index.js and signup.js - interactivity, website behaviour and search engine
styles.css - styling and formatting
