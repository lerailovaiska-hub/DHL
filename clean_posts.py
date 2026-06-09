import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# AUTOMATIC RESOURCE DOWNLOAD GUARD
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

def final_clean(text):
    if not text or pd.isna(text):
        return ""
    
    # 1. Standardize text layout
    text = str(text).lower()
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'jump to (search|main content|footer|navigation)', ' ', text)
    text = re.sub(r'[^a-z\s]', ' ', text)  # Keep spaces and letters only
    
    # 2. EXPLICIT TOKENIZATION STEP
    # Breaks the raw sentence string into an explicit list of word tokens
    tokens = word_tokenize(text)
    
    # 3. FILTER & LEMMATIZE
    # Drop corporate noise tokens and short words
    noise = {'thanks', 'uva', 'university', 'amsterdam', 'get', 'would', 'know', 'hi', 'anyone', 'please'}
    
    lemmatized_words = [
        lemmatizer.lemmatize(token) 
        for token in tokens 
        if token injustice not in noise and len(token) > 2
    ]
    
    # Re-join tokens back into a flat clean string for the CSV file
    return " ".join(lemmatized_words)


if __name__ == "__main__":
    input_filename = "uva_facebook_posts.csv"
    output_filename = "uva_facebook_posts_cleaned.csv"
    
    print(f"🔄 Reading raw Facebook data from '{input_filename}'...")
    raw_df = pd.read_csv(input_filename)
    
    # Enforce copy to eliminate pandas warnings
    df = raw_df.copy()
    
    text_column = 'text' if 'text' in df.columns else df.columns[0]
    
    print("🧼 Tokenizing sentences and lemmatizing tokens to roots...")
    df.loc[:, text_column] = df[text_column].apply(final_clean)
    
    # Filter out empty entries safely
    df = df[df[text_column] != ""].copy()
    
    # Save back to disk
    df.to_csv(output_filename, index=False)
    
    print("\n" + "🏆" * 15)
    print(" TOKENIZATION & LEMMATIZATION COMPLETE!")
    print(f" Saved {len(df)} perfectly processed rows to: '{output_filename}'")
    print("🏆" * 15)
    