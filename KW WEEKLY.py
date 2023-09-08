import pandas as pd

codes = ['B0BCX71XN6','B0BD5SC4MM','B0BTT5XT8W','B089WBMF1V', 'B08LW2CQMY', 'B099KJ8DCY', 'B09N42PRV4','B09X31H55K','B0BJKPF3NR','B0BXT78QQY','B0BL3PBDLR','B0BXT776MG','B0BL3Q2LH5','B0BKWNHJS1','B0BRQNL57P','B0BRQS5GV3','B0BRQSBZW3','B0BRQQ2BJW','B0BXF7Z5RL','B0BYT3K8FF','B0BYT25DGQ'] 
all_dfs = []

for code in codes:
    input_file_path = f'C:/Users/polin/OneDrive/Рабочий стол/Works/Beetsmill/KW REPORT/US_AMAZON_cerebro_{code}_.xlsx'
    df = pd.read_excel(input_file_path, engine='openpyxl', header=None).iloc[1:].reset_index(drop=True)

    cols_to_drop = [1, 2] + list(range(6, 24))
    df = df.drop(columns=cols_to_drop)

    num_rows = df.shape[0] 
    new_data = pd.DataFrame({'08.09.2023': ['08.09.2023'] * num_rows, 'Code': [code] * num_rows})

    df = pd.concat([new_data, df], axis=1)
    all_dfs.append(df)

final_df = pd.concat(all_dfs, axis=0)

final_df.to_excel("Total.xlsx", index=False, header=False, engine='openpyxl')

print("Готово")



















