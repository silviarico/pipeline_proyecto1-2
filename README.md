#Project data pipeline

## OBJECTIVE

This project is aimed to prove that Nike has increased its prices in women's sport shoes since 2018.

Data sources:
        - dataset source: https://www.kaggle.com/datafiniti/womens-shoes-prices
        - websraping: https://www.nike.com/us/es/w/mujeres-calzado-5e1x6zy7ok

Execution: 
        - data cleaning and file creation libraries used:
            re
            src.cleaning as c
            pandas as pd
        - web scrapping libraries used:
            requests
            bs4 import BeautifulSoup
            time
            selenium import webdriver
            selenium.webdriver.chrome.service import Service
            webdriver_manager.chrome import ChromeDriverManager
        - visualization libraries used:
            import seaborn as sns
            import matplotlib.pyplot as plt
            plotly.express as px

deliverables:
    cleaning-scraping: see python_cleaning_scraping/cleaning_scraping.py
    visualization: see jupyter/Visualization_shoes.ipynb
    clean-datasets: see data_clean





