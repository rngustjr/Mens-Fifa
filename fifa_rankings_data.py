"""
FIFA Rankings Data Collection for UEFA and CONCACAF Teams
This script collects and processes FIFA ranking data for top UEFA and CONCACAF teams
for visualization in an interactive chart.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import json
import os

# Create directories for data storage
os.makedirs('data', exist_ok=True)

# Define the teams we want to track (top UEFA and CONCACAF teams)
uefa_teams = [
    {"name": "Spain", "code": "ESP", "qualified": True, "confederation": "UEFA"},
    {"name": "France", "code": "FRA", "qualified": True, "confederation": "UEFA"},
    {"name": "England", "code": "ENG", "qualified": True, "confederation": "UEFA"},
    {"name": "Netherlands", "code": "NED", "qualified": True, "confederation": "UEFA"},
    {"name": "Portugal", "code": "POR", "qualified": True, "confederation": "UEFA"},
    {"name": "Belgium", "code": "BEL", "qualified": True, "confederation": "UEFA"},
    {"name": "Italy", "code": "ITA", "qualified": False, "confederation": "UEFA"},
    {"name": "Germany", "code": "GER", "qualified": True, "confederation": "UEFA"},
    {"name": "Croatia", "code": "CRO", "qualified": False, "confederation": "UEFA"},
    {"name": "Switzerland", "code": "SUI", "qualified": False, "confederation": "UEFA"},
    {"name": "Denmark", "code": "DEN", "qualified": False, "confederation": "UEFA"},
    {"name": "Austria", "code": "AUT", "qualified": False, "confederation": "UEFA"}
]

concacaf_teams = [
    {"name": "USA", "code": "USA", "qualified": True, "confederation": "CONCACAF", "host": True},
    {"name": "Mexico", "code": "MEX", "qualified": True, "confederation": "CONCACAF", "host": True},
    {"name": "Canada", "code": "CAN", "qualified": True, "confederation": "CONCACAF", "host": True},
    {"name": "Costa Rica", "code": "CRC", "qualified": False, "confederation": "CONCACAF"},
    {"name": "Jamaica", "code": "JAM", "qualified": False, "confederation": "CONCACAF"},
    {"name": "Honduras", "code": "HON", "qualified": False, "confederation": "CONCACAF"},
    {"name": "Panama", "code": "PAN", "qualified": False, "confederation": "CONCACAF"},
    {"name": "El Salvador", "code": "SLV", "qualified": False, "confederation": "CONCACAF"}
]

# Combine all teams
all_teams = uefa_teams + concacaf_teams

# Generate historical ranking data (simulated for demonstration)
# In a real scenario, this would be fetched from an API or database
def generate_historical_rankings():
    # Time periods (months from 2023 to 2025)
    months = pd.date_range(start='2023-01-01', end='2025-06-01', freq='MS')
    
    rankings_data = []
    
    # Base rankings (approximate starting points based on current FIFA rankings)
    base_rankings = {
        "ESP": 2, "FRA": 3, "ENG": 4, "NED": 6, "POR": 7, "BEL": 8, "ITA": 9, "GER": 10,
        "CRO": 11, "SUI": 20, "DEN": 21, "AUT": 22, "USA": 16, "MEX": 17, "CAN": 45,
        "CRC": 50, "JAM": 55, "HON": 80, "PAN": 85, "SLV": 90
    }
    
    # Generate data for each team over time
    for team in all_teams:
        base_rank = base_rankings[team["code"]]
        
        for date in months:
            # Add some random variation to create realistic ranking changes
            # Teams with higher base rankings have less volatility
            volatility = 5 if base_rank > 30 else 3 if base_rank > 10 else 2
            
            # Trend component - slight improvement for most teams over time
            trend = -0.5 * (date - months[0]).days / 30  # negative because lower rank is better
            
            # Random component
            random_change = np.random.normal(0, volatility)
            
            # Calculate rank for this month (ensure it's at least 1)
            rank = max(1, int(base_rank + trend + random_change))
            
            # Add entry to data
            rankings_data.append({
                "team_name": team["name"],
                "team_code": team["code"],
                "confederation": team["confederation"],
                "date": date.strftime('%Y-%m'),
                "rank": rank,
                "qualified": team.get("qualified", False),
                "host": team.get("host", False)
            })
    
    # Convert to DataFrame
    df = pd.DataFrame(rankings_data)
    return df

# Generate the data
rankings_df = generate_historical_rankings()

# Save to CSV
rankings_df.to_csv('data/fifa_rankings_history.csv', index=False)

# Create a JSON file with team information for the visualization
team_info = []
for team in all_teams:
    status = "Host" if team.get("host", False) else "Qualified" if team["qualified"] else "Potential"
    
    # Get latest rank and convert numpy.int64 to regular int for JSON serialization
    latest_rank = rankings_df[(rankings_df["team_code"] == team["code"]) & 
                             (rankings_df["date"] == rankings_df["date"].max())]["rank"].values[0]
    
    # Convert numpy.int64 to regular int
    latest_rank = int(latest_rank)
    
    team_info.append({
        "name": team["name"],
        "code": team["code"],
        "confederation": team["confederation"],
        "status": status,
        "latest_rank": latest_rank
    })

# Sort by latest ranking
team_info = sorted(team_info, key=lambda x: x["latest_rank"])

# Save team info to JSON
with open('data/team_info.json', 'w') as f:
    json.dump(team_info, f, indent=2)

print("Data collection and processing complete.")
print(f"Generated data for {len(all_teams)} teams across {len(rankings_df['date'].unique())} time periods.")
print("Files saved: data/fifa_rankings_history.csv and data/team_info.json")
