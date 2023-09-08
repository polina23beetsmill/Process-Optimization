from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pandas as pd

codes = [
"B0BCX71XN6", "B0BD5SC4MM", "B089WBMF1V", "B08LW2CQMY", 
    "B099KJ8DCY", "B09N42PRV4", "B09X31H55K", "B0BJKPF3NR", 
    "B0BXT78QQY", "B0BXT776MG", "B0BL3PBDLR","B0BL3Q2LH5",
    "B0BKX1JPS8","B0BKWNHJS1", "B0BRQNL57P", "B0BRQS5GV3",
    "B0BRQSBZW3","B0BRQQ2BJW", "B0BXF7Z5RL", "B0BTT5XT8W", 
    "B0BYT3K8FF", "B0BYT25DGQ", "B08DYG5KL4"
]

ratings = ['five', 'four', 'three', 'two', 'one']
browser = webdriver.Chrome()
df = pd.DataFrame(columns=["ASIN", "average"] + [f"{x} star share" for x in range(5, 0, -1)] + [""] + [rating +" star rating" for rating in ratings] + [""] + [ rating +" star review" for rating in ratings])
for code in codes:
    link0 = f'https://www.amazon.com/product-reviews/{code}/ref=cm_cr_arp_d_bdcrb_top?ie=UTF8#customerReviews'
    
    browser.get(link0)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    
    try:
        total_perc = soup.find_all('div', class_='a-section histogram')
        cust_perc = total_perc[0].get_text()
    except IndexError:
        print(f"Error for code {code}: No review data found.")
        output = [code, "No review data found."] + [""] * (len(df.columns) - 2) # -2 потому что у нас уже есть 2 значения: код и сообщение об ошибке
        df.loc[len(df)] = output
        continue

    keys = re.findall(r'(\d star)', cust_perc)
    values = re.findall(r'(\d+%)', cust_perc)

    result = dict(zip(keys, values))
    percent_values = [result[f"{i} star"] for i in range(5, 0, -1)]

    # Извлечение среднего рейтинга
    avg = str(soup.find('span', {"data-hook": 'rating-out-of-text'}))
    avg_rating = float(avg[avg.index('">') + 2:avg.index(' out of 5')])

    # Списки для хранения количества отзывов и количества отзывов с комментариями
    total_reviews = []
    reviews_with_comments = []

    for rating in ratings:
        link = f'https://www.amazon.com/product-reviews/{code}/ref=cm_cr_unknown?formatType=current_format&pageNumber=1&filterByStar={rating}_star'
        browser.get(link)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        
        data = soup.find('div', class_='a-row a-spacing-base a-size-base').get_text().replace('\n', '').strip().split(', ')
        total_reviews.append(data[0].split()[0].replace(',', ''))
        reviews_with_comments.append(data[1].split()[0].replace(',', ''))
    
    # Объединение данных и вывод
    output = [code, str(avg_rating)] + percent_values + [""] + total_reviews + [""] + reviews_with_comments
    df.loc[len(df)] = output

# Сохранение DataFrame в файл Excel
df.to_excel("output.xlsx", index=False)

browser.quit()


