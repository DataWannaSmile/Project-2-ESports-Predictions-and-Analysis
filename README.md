# Project-2-ESports-Predictions-and-Analysis

Цель проекта:
 - Дать предсказание 100 будущих матчей между 10 командами на основе 30000 матчей

Структура данных:

dota2_matches:
 - ID (PRIMARY KEY)
 - Дата проведения матчка
 - Команда Силы Света
 - Команда Силы Тьмы
 - Победитель
 - Победившая сторона (Силы света или Силы тьмы)

dota2_teams:
 - Team_ID (PRIMARY KEY)
 - Team_Name - название команды
 - Region - регион

dota2_futures:
 - MathcID - id матча (PRIMARY KEY)
 - MathcDate - Предположительная дата матча
 - RadiantTeam - Команда силы света
 - DireTeam - Команда силы тьмы
 - PredictedWinner - Вероятный победитель
 - WinningSide - Победившая сторона
 - Confidence - уверенность в предсказании
 - RadiantWinProbability - вероятность победы силы света
 - H2HMatches - количество личных встреч

Выводы:
 - 
