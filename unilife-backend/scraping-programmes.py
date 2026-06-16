import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

# 1. CLEANING ENGINE (Word space protection intact)
def final_clean(text):
    if not text:
        return ""
    text = str(text).lower()
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'jump to (search|main content|footer|navigation)', ' ', text)
    
    # Force spaces around non-letters to guarantee words never mash
    text = re.sub(r'[^a-z]', ' ', text)
    
    # Filter out research pipeline noise tokens
    noise = {'thanks', 'uva', 'university', 'amsterdam', 'get', 'would', 'know', 'hi', 'anyone', 'please'}
    words = text.split()
    return " ".join([w for w in words if w not in noise and len(w) > 2])


# 2. THE PRODUCTION SCRAPER PIPELINE
def bachelors_only_scraper(url_list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    master_records = []
    total_links = len(url_list)
    
    print(f"🚀 Scraping the {total_links} Official English Bachelor Programs...")
    
    for idx, url in enumerate(url_list):
        try:
            res = requests.get(url, headers=headers, timeout=12)
            if res.status_code != 200:
                print(f"❌ Failed (Status {res.status_code}): {url}")
                continue
                
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Decompose layout frames, headers, and footers completely
            for block in soup.select('nav, footer, header, script, style, .menu, .header, .footer, .accessibility-links'):
                block.decompose()
                
            title = soup.find('h1').get_text(strip=True) if soup.find('h1') else "UvA Bachelor Program"
            main_content = soup.find('main') or soup.find('article') or soup.find('body') or soup
            raw_text = main_content.get_text(separator=" ", strip=True)
            
            master_records.append({
                "source": "Official UvA",
                "title": title,
                "url": url,
                "full_content": final_clean(title + " " + raw_text)
            })
            print(f"✅ [{idx + 1}/{total_links}] Processed: {title}")
            time.sleep(1) # Courteous sleep delay
            
        except Exception as e:
            print(f"❌ Error on {url}: {e}")
            
    return pd.DataFrame(master_records)


if __name__ == "__main__":
    # PURE ENGLISH-TAUGHT BACHELOR PROGRAM ENDPOINTS ONLY
    pure_bachelor_urls = [
        "https://www.uva.nl/en/programmes/bachelors/actuarial-science/actuarial-science.html",
        "https://www.uva.nl/en/programmes/bachelors/ancient-studies/ancient-studies.html",
        "https://www.uva.nl/en/programmes/bachelors/archaeology/archaeology.html",
        "https://www.uva.nl/en/programmes/bachelors/business-analytics/business-analytics.html",
        "https://www.uva.nl/en/programmes/bachelors/business-administration/business-administration.html",
        "https://www.uva.nl/en/programmes/bachelors/cognition-language-and-communication/cognition-language-and-communication.html",
        "https://www.uva.nl/en/programmes/bachelors/communication-science/communication-science.html",
        "https://www.uva.nl/en/programmes/bachelors/computational-social-science/computational-social-science.html",
        "https://www.uva.nl/en/programmes/bachelors/cultural-anthropology-and-development-sociology/cultural-anthropology-and-development-sociology.html",
        "https://www.uva.nl/en/programmes/bachelors/econometrics/econometrics.html",
        "https://www.uva.nl/en/programmes/bachelors/economics-and-business-economics/economics-and-business-economics.html",
        "https://www.uva.nl/en/programmes/bachelors/english-language-and-culture/english-language-and-culture.html",
        "https://www.uva.nl/en/programmes/bachelors/european-studies/european-studies.html",
        "https://www.uva.nl/en/programmes/bachelors/global-arts-culture-and-politics/global-arts-culture-and-politics.html",
        "https://www.uva.nl/en/programmes/bachelors/history/history.html",
        "https://www.uva.nl/en/programmes/bachelors/human-geography-and-planning/human-geography-and-planning.html",
        "https://www.uva.nl/en/programmes/bachelors/linguistics/linguistics.html",
        "https://www.uva.nl/en/programmes/bachelors/literary-studies/literary-studies.html",
        "https://www.uva.nl/en/programmes/bachelors/media-and-culture/media-and-culture.html",
        "https://www.uva.nl/en/programmes/bachelors/media-and-information/media-and-information.html",
        "https://www.uva.nl/en/programmes/bachelors/political-science/political-science.html",
        "https://www.uva.nl/en/programmes/bachelors/politics-psychology-law-and-economics/politics-psychology-law-and-economics.html",
        "https://www.uva.nl/en/programmes/bachelors/psychology/psychology.html",
        "https://www.uva.nl/en/programmes/bachelors/sign-language-linguistics/sign-language-linguistics.html",
        "https://www.uva.nl/en/programmes/bachelors/sociology/sociology.html",
        "https://www.auc.nl/programme/the-auc-programme.html"
    ]
    
    # Run pipeline
    df = bachelors_only_scraper(pure_bachelor_urls)
    
    # Save step
    if not df.empty:
        filename = "uva_all_english_bachelors.csv"
        df.to_csv(filename, index=False)
        print(f"\n🎉 Success! Generated a clean dataset with exactly {len(df)} entries.")
        print(f"💾 File committed to: '{filename}'")

        import os
import pandas as pd

def extract_clean_programme_names(url_list):
    cleaned_records = []
    
    for url in url_list:
        # 1. Extract the filename piece right before '.html'
        filename = url.split('/')[-1].replace('.html', '')
        
        # 2. Hardcoded exception mappings for unique/abbreviated server URLs
        if filename == "the-auc-programme":
            display_name = "Liberal Arts and Sciences (Amsterdam University College)"
        elif filename == "politics-psychology-law-and-economics":
            display_name = "Politics, Psychology, Law and Economics (PPLE)"
        else:
            # 3. Clean standard slug strings: replace hyphens with spaces and fix capitalization
            # Handles edge cases like lowercase joining words safely (e.g., 'and')
            raw_title = filename.replace('-', ' ').strip()
            words = raw_title.split()
            capitalized_words = [
                w.lower() if w.lower() in ['and'] else w.capitalize() 
                for w in words
            ]
            display_name = " ".join(capitalized_words)
            
        cleaned_records.append({
            "Official Programme Name": display_name,
            "Source URL": url
        })
        
    return pd.DataFrame(cleaned_records)


if __name__ == "__main__":
    # Your target list of English-taught Bachelor endpoints
    pure_bachelor_urls = [
        "https://www.uva.nl/en/programmes/bachelors/actuarial-science/actuarial-science.html",
        "https://www.uva.nl/en/programmes/bachelors/ancient-studies/ancient-studies.html",
        "https://www.uva.nl/en/programmes/bachelors/archaeology/archaeology.html",
        "https://www.uva.nl/en/programmes/bachelors/business-analytics/business-analytics.html",
        "https://www.uva.nl/en/programmes/bachelors/business-administration/business-administration.html",
        "https://www.uva.nl/en/programmes/bachelors/cognition-language-and-communication/cognition-language-and-communication.html",
        "https://www.uva.nl/en/programmes/bachelors/communication-science/communication-science.html",
        "https://www.uva.nl/en/programmes/bachelors/computational-social-science/computational-social-science.html",
        "https://www.uva.nl/en/programmes/bachelors/cultural-anthropology-and-development-sociology/cultural-anthropology-and-development-sociology.html",
        "https://www.uva.nl/en/programmes/bachelors/econometrics/econometrics.html",
        "https://www.uva.nl/en/programmes/bachelors/economics-and-business-economics/economics-and-business-economics.html",
        "https://www.uva.nl/en/programmes/bachelors/english-language-and-culture/english-language-and-culture.html",
        "https://www.uva.nl/en/programmes/bachelors/european-studies/european-studies.html",
        "https://www.uva.nl/en/programmes/bachelors/global-arts-culture-and-politics/global-arts-culture-and-politics.html",
        "https://www.uva.nl/en/programmes/bachelors/history/history.html",
        "https://www.uva.nl/en/programmes/bachelors/human-geography-and-planning/human-geography-and-planning.html",
        "https://www.uva.nl/en/programmes/bachelors/linguistics/linguistics.html",
        "https://www.uva.nl/en/programmes/bachelors/literary-studies/literary-studies.html",
        "https://www.uva.nl/en/programmes/bachelors/media-and-culture/media-and-culture.html",
        "https://www.uva.nl/en/programmes/bachelors/media-and-information/media-and-information.html",
        "https://www.uva.nl/en/programmes/bachelors/political-science/political-science.html",
        "https://www.uva.nl/en/programmes/bachelors/politics-psychology-law-and-economics/politics-psychology-law-and-economics.html",
        "https://www.uva.nl/en/programmes/bachelors/psychology/psychology.html",
        "https://www.uva.nl/en/programmes/bachelors/sociology/sociology.html",
        "https://www.auc.nl/programme/the-auc-programme.html"
    ]
    
    # Process text conversion
    df_names = extract_clean_programme_names(pure_bachelor_urls)
    
    # Write dataset directly to disk
    output_file = "uva_english_programme_titles.csv"
    df_names.to_csv(output_file, index=False)
    
    print("\n" + "="*55)
    print(f"🎉 Complete! Generated names for all {len(df_names)} Bachelor tracks.")
    print(f"💾 File saved to: '{output_file}'")
    print("="*55)