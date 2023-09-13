from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
excel_file_path = 'BSR Report.xlsx'
df = pd.read_excel(excel_file_path)

codes = df['Competitor ASIN'].tolist()

browser = webdriver.Chrome()


bsr_values = []

for code in codes:
    link0 = f'https://www.amazon.com/dp/{code}'
    
    browser.get(link0)
    time.sleep(8)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    
    total_perc = str(soup.find_all(id="productDetails_db_sections"))
    index = total_perc.find("Best Sellers Rank")
    
    if index != -1:
        hash_index = total_perc.find("#", index)
        end_index = total_perc.find(" ", hash_index)
        
        if hash_index != -1 and end_index != -1:
            best_sellers_rank = total_perc[hash_index + 1:end_index]
            bsr_values.append(best_sellers_rank)
        else:
            bsr_values.append(None)
    else:
        bsr_values.append(None)


df['BSR'] = bsr_values


df.to_excel(excel_file_path, index=False)

print("Готово")
browser.quit()

