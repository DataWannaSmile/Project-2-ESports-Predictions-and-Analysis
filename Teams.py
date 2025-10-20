import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


np.random.seed(42)  
NUM_MATCHES = 30000
NUM_TEAMS = 10


teams = [
    "Team Spirit", "Gaimin Gladiators", "Team Liquid", "BetBoom Team", 
    "Azure Ray", "Xtreme Gaming", "Shopify Rebellion", "Tundra Esports", 
    "Parivision", "Heroic"
]


teams_table = pd.DataFrame({
    'Team_ID': range(1, NUM_TEAMS + 1),
    'Team_Name': teams,
    'Region': ['CIS', 'EU', 'EU', 'CIS', 'CN', 'CN', 'NA', 'EU', 'CIS', 'SA'],
    
})


teams_df=pd.DataFrame(teams_table)

