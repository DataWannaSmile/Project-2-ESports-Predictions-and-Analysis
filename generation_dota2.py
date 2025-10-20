import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Настройки
np.random.seed(42)  # для воспроизводимости
NUM_MATCHES = 30000
NUM_TEAMS = 10

# Список команд (реальные и вымышленные названия для Dota 2)
teams = [
    "Team Spirit", "Gaimin Gladiators", "Team Liquid", "BetBoom Team", 
    "Azure Ray", "Xtreme Gaming", "Shopify Rebellion", "Tundra Esports", 
    "Parivision", "Heroic"
]

# Создаем базовые силы команд 
team_strength = {team: np.random.normal(50, 15) for team in teams}

def generate_matches(num_matches, teams):
    matches = []
    
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 1, 1)
    
    # Словарь для хранения истории матчей между командами
    match_history = {}
    
    for match_id in range(1, num_matches + 1):
        # Случайная дата матча
        days_diff = (end_date - start_date).days
        random_days = random.randint(0, days_diff)
        match_date = start_date + timedelta(days=random_days)
        
        # Выбираем две разные команды
        radiant_team, dire_team = random.sample(teams, 2)
        
        # Создаем ключ для пары команд (сортируем для уникальности)
        team_pair = tuple(sorted([radiant_team, dire_team]))
        
        # Определяем победителя с учетом истории и случайности
        if team_pair in match_history:
            # Если у команд уже была история, учитываем её
            past_matches = match_history[team_pair]
            radiant_wins = past_matches.get(radiant_team, 0)
            dire_wins = past_matches.get(dire_team, 0)
            total_matches = radiant_wins + dire_wins
            
            # Балансируем: если одна команда выиграла много раз подряд,
            # увеличиваем шансы другой команды
            if total_matches > 0:
                radiant_win_ratio = radiant_wins / total_matches
                # Если одна команда доминирует, даем другой больше шансов
                balance_factor = 0.3 if radiant_win_ratio > 0.7 else (
                    0.7 if radiant_win_ratio < 0.3 else 0.5
                )
            else:
                balance_factor = 0.5
        else:
            # Первая встреча - используем базовую силу команд
            balance_factor = team_strength[radiant_team] / (team_strength[radiant_team] + team_strength[dire_team])
        
        # Добавляем случайность и текущую форму
        current_form_radiant = np.random.normal(0, 20)  # текущая форма
        current_form_dire = np.random.normal(0, 20)
        
        # Финальная вероятность победы Radiant
        radiant_prob = balance_factor + 0.1 * current_form_radiant - 0.1 * current_form_dire
        radiant_prob = max(0.2, min(0.8, radiant_prob))  # ограничиваем диапазон
        
        # Определяем победителя
        if random.random() < radiant_prob:
            winner = radiant_team
            winning_side = "Силы света"
        else:
            winner = dire_team
            winning_side = "Силы тьмы"
        
        # Обновляем историю матчей
        if team_pair not in match_history:
            match_history[team_pair] = {}
        match_history[team_pair][winner] = match_history[team_pair].get(winner, 0) + 1
        
        matches.append({
            'ID': match_id,
            'Дата проведения матча': match_date.strftime('%Y-%m-%d'),
            'Команда Силы Света': radiant_team,
            'Команда Силы Тьмы': dire_team,
            'Победитель': winner,
            'Победившая сторона': winning_side
        })
        
        # Прогресс
        if match_id % 5000 == 0:
            print(f"Сгенерировано {match_id} матчей...")
    
    return matches, match_history

# Генерируем матчи
print("Генерация матчей...")
matches_data, history = generate_matches(NUM_MATCHES, teams)

# Создаем DataFrame
df = pd.DataFrame(matches_data)

# Проверяем распределение матчей по командам
print("\nСтатистика по командам:")
team_stats = []
for team in teams:
    team_matches = len(df[(df['Команда Силы Света'] == team) | (df['Команда Силы Тьмы'] == team)])
    team_wins = len(df[df['Победитель'] == team])
    win_rate = (team_wins / team_matches) * 100
    team_stats.append({
        'Команда': team,
        'Матчи': team_matches,
        'Победы': team_wins,
        'Win Rate %': win_rate
    })
    print(f"{team}: {team_matches} матчей, {team_wins} побед ({win_rate:.1f}%)")

# Анализируем встречи между командами
print("\nАнализ встреч между командами (примеры):")
team_pairs_to_check = [
    ("Team Spirit", "Gaimin Gladiators"),
    ("Team Liquid", "Natus Vincere"),
    ("Azure Ray", "Xtreme Gaming")
]

for team1, team2 in team_pairs_to_check:
    pair_key = tuple(sorted([team1, team2]))
    if pair_key in history:
        matches_between = sum(history[pair_key].values())
        team1_wins = history[pair_key].get(team1, 0)
        team2_wins = history[pair_key].get(team2, 0)
        print(f"{team1} vs {team2}: {matches_between} матчей, {team1}: {team1_wins} побед, {team2}: {team2_wins} побед")

# Проверяем распределение сторон
radiant_wins = len(df[df['Победившая сторона'] == 'Силы света'])
dire_wins = len(df[df['Победившая сторона'] == 'Силы тьмы'])

print(f"\nОбщая статистика:")
print(f"Всего матчей: {len(df)}")
print(f"Побед Сил Света: {radiant_wins} ({radiant_wins/len(df)*100:.1f}%)")
print(f"Побед Сил Тьмы: {dire_wins} ({dire_wins/len(df)*100:.1f}%)")

df.to_csv(r'C:\Users\maxbu\OneDrive\Desktop\Проекты\Аналитика\Проект 2\dota2_matches.csv', index=False, encoding='utf-8-sig')


