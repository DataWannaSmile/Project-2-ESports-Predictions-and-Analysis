import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Настройки
np.random.seed(42)  # для воспроизводимости
NUM_MATCHES = 30000
NUM_TEAMS = 10

# Список команд (указанные команды)
teams = [
    "Team Spirit", "Gaimin Gladiators", "Team Liquid", "BetBoom Team", 
    "Azure Ray", "Xtreme Gaming", "Shopify Rebellion", "Tundra Esports", 
    "Parivision", "Heroic"
]

# Создаем таблицу команд
teams_table = pd.DataFrame({
    'Team_ID': range(1, NUM_TEAMS + 1),
    'Team_Name': teams,
    'Region': ['CIS', 'EU', 'EU', 'CIS', 'CN', 'CN', 'NA', 'EU', 'CIS', 'SA'],
    
})

print("Таблица команд:")
print(teams_table.to_string(index=False))

teams_df=pd.DataFrame(teams_table)

teams_df.to_csv(r'C:\Users\maxbu\OneDrive\Desktop\Проекты\Аналитика\Проект 2\dota2_teams.csv', index=False, encoding='utf-8-sig')