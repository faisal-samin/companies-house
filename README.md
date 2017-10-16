# sic-classification
A project to exploit data returned from Google Searches to train a machine learning model to classify the SIC (industry) of businesses.

Expected steps:
1) Import and format data from Comapnies House
2) Build web-scraper to return text from Google Search results 
3) Filter out scraped text to leave words with explanatory power for an industry (using the NLTK library).
4) Find a way to order companies in each SIC by size/web-presence. Sample X% of largest companies in each SIC for scraping.
5) Build a dataset of keywords for low-level (700) if not high-level (21) industries.
6) Train a machine learning classification model on known classifications and gathered keywords.
7) Test model to predict known industries and compare with actual industry.
8) If model is accurate, run model through all unclassified and dormant companies in Companies House.
9) Build for production and use.

Current step: (3)
Challenges:
- efficiently removing standard web text and company names and their variants.
