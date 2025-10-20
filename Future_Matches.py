import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

df_matches = pd.read_csv('dota2_matches.csv')
# Данные команд после посчета
teams_winrate = {
    "Heroic": 0.511, "Parivision": 0.508, "BetBoom Team": 0.506,
    "Xtreme Gaming": 0.506, "Team Liquid": 0.501, "Azure Ray": 0.498,
    "Tundra Esports": 0.498, "Shopify Rebellion": 0.493, 
    "Team Spirit": 0.492, "Gaimin Gladiators": 0.486
}

# Функция для анализа истории личных встреч
def calculate_h2h_stats(df_historical_matches):
    """Рассчитывает статистику личных встреч между командами"""
    h2h_stats = {}
    
    for _, match in df_historical_matches.iterrows():
        team1 = match['Команда Силы Света']
        team2 = match['Команда Силы Тьмы']
        winner = match['Победитель']
        
        # Уникальный ключ для пары команд
        pair = tuple(sorted([team1, team2]))
        
        if pair not in h2h_stats:
            h2h_stats[pair] = {team1: 0, team2: 0, 'total_matches': 0}
        
        # Считаем победы каждой команды
        h2h_stats[pair][winner] += 1
        h2h_stats[pair]['total_matches'] += 1
    
    return h2h_stats

# Функция для генерации матчей С учетом H2H
def generate_future_matches_with_h2h(num_matches, teams_winrate, df_historical_matches):
    matches = []
    teams = list(teams_winrate.keys())
    start_date = datetime(2024, 1, 15)
    
    # Рассчитываем статистику H2H из исторических данных
    h2h_stats = calculate_h2h_stats(df_historical_matches)
    
    for match_id in range(1, num_matches + 1):
        # Выбираем случайные команды
        radiant_team, dire_team = random.sample(teams, 2)
        match_date = start_date + timedelta(hours=match_id * 3)
        
        # Базовая вероятность 
        winrate_radiant = teams_winrate[radiant_team]
        winrate_dire = teams_winrate[dire_team]
        base_prob_radiant = winrate_radiant / (winrate_radiant + winrate_dire)
        
        # Коррекция на основе H2H истории
        h2h_correction = 0
        pair = tuple(sorted([radiant_team, dire_team]))
        
        if pair in h2h_stats:
            stats = h2h_stats[pair]
            total_h2h = stats['total_matches']
            
            if total_h2h >= 3:  
                radiant_wins = stats.get(radiant_team, 0)
                h2h_winrate_radiant = radiant_wins / total_h2h
                
                # Корректируем вероятность на основе H2H
                h2h_correction = (h2h_winrate_radiant - 0.5) * 0.3
        
        # Случайные факторы
        form_correction = random.uniform(-0.08, 0.08)
        
        # Финальная вероятность
        final_prob_radiant = base_prob_radiant + h2h_correction + form_correction
        final_prob_radiant = max(0.2, min(0.8, final_prob_radiant))
        
        # Определяем победителя
        if random.random() < final_prob_radiant:
            winner = radiant_team
            winning_side = "Силы света"
            confidence = final_prob_radiant
        else:
            winner = dire_team
            winning_side = "Силы тьмы"
            confidence = 1 - final_prob_radiant
        
        matches.append({
            'MatchID': match_id,
            'MatchDate': match_date,
            'RadiantTeam': radiant_team,
            'DireTeam': dire_team,
            'PredictedWinner': winner,
            'WinningSide': winning_side,
            'Confidence': round(confidence, 3),
            'RadiantWinProbability': round(final_prob_radiant, 3),
            'H2HMatches': h2h_stats[pair]['total_matches'] if pair in h2h_stats else 0
        })
    
    return matches

# Генерируем 100 матчей
future_matches_data = generate_future_matches_with_h2h(100, teams_winrate, df_matches)


future_matches_df = pd.DataFrame(future_matches_data)

