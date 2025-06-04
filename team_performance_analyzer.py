"""
Team Performance Analyzer for FIFA World Cup 2026

This module provides analytics functions for analyzing team performance,
historical data, and generating predictive metrics.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
import os

class TeamAnalyzer:
    """Class for analyzing team performance data for the World Cup."""
    
    def __init__(self, data_dir='../../data'):
        """Initialize the TeamAnalyzer with data directory path."""
        self.data_dir = Path(data_dir)
        self.teams_data = None
        self.matches_data = None
        self.load_data()
        
    def load_data(self):
        """Load team and match data from files."""
        # In a real implementation, this would load actual data files
        # For now, we'll create sample data structures
        
        # Sample teams data
        self.teams_data = {
            'ARG': {'name': 'Argentina', 'confederation': 'CONMEBOL', 'qualified': True, 'ranking': 1},
            'BRA': {'name': 'Brazil', 'confederation': 'CONMEBOL', 'qualified': False, 'ranking': 5},
            'CAN': {'name': 'Canada', 'confederation': 'CONCACAF', 'qualified': True, 'ranking': 43},
            'MEX': {'name': 'Mexico', 'confederation': 'CONCACAF', 'qualified': True, 'ranking': 15},
            'USA': {'name': 'United States', 'confederation': 'CONCACAF', 'qualified': True, 'ranking': 13},
            'JPN': {'name': 'Japan', 'confederation': 'AFC', 'qualified': True, 'ranking': 20},
            'IRN': {'name': 'IR Iran', 'confederation': 'AFC', 'qualified': True, 'ranking': 22},
            'NZL': {'name': 'New Zealand', 'confederation': 'OFC', 'qualified': True, 'ranking': 103},
            'ENG': {'name': 'England', 'confederation': 'UEFA', 'qualified': False, 'ranking': 4},
            'FRA': {'name': 'France', 'confederation': 'UEFA', 'qualified': False, 'ranking': 2},
        }
        
        # Sample historical match data
        self.matches_data = [
            {'team1': 'ARG', 'team2': 'FRA', 'score1': 3, 'score2': 3, 'winner': 'ARG', 'tournament': 'World Cup 2022', 'stage': 'Final'},
            {'team1': 'ARG', 'team2': 'BRA', 'score1': 1, 'score2': 0, 'winner': 'ARG', 'tournament': 'Copa America 2021', 'stage': 'Final'},
            {'team1': 'ENG', 'team2': 'FRA', 'score1': 1, 'score2': 2, 'winner': 'FRA', 'tournament': 'World Cup 2022', 'stage': 'Quarter-final'},
            {'team1': 'USA', 'team2': 'MEX', 'score1': 2, 'score2': 0, 'winner': 'USA', 'tournament': 'CONCACAF Nations League 2023', 'stage': 'Final'},
            {'team1': 'JPN', 'team2': 'IRN', 'score1': 3, 'score2': 0, 'winner': 'JPN', 'tournament': 'Asian Cup 2023', 'stage': 'Semi-final'},
        ]
    
    def get_team_info(self, team_code):
        """Get basic information about a team."""
        if team_code in self.teams_data:
            return self.teams_data[team_code]
        return None
    
    def get_qualified_teams(self):
        """Get a list of all qualified teams."""
        return {code: data for code, data in self.teams_data.items() 
                if data.get('qualified', False)}
    
    def get_teams_by_confederation(self, confederation):
        """Get teams from a specific confederation."""
        return {code: data for code, data in self.teams_data.items() 
                if data.get('confederation') == confederation}
    
    def get_team_matches(self, team_code):
        """Get all matches involving a specific team."""
        return [match for match in self.matches_data 
                if match['team1'] == team_code or match['team2'] == team_code]
    
    def calculate_win_percentage(self, team_code):
        """Calculate the win percentage for a team based on historical data."""
        matches = self.get_team_matches(team_code)
        if not matches:
            return 0
        
        wins = sum(1 for match in matches if match['winner'] == team_code)
        return (wins / len(matches)) * 100
    
    def head_to_head(self, team1_code, team2_code):
        """Analyze head-to-head record between two teams."""
        matches = [match for match in self.matches_data 
                  if (match['team1'] == team1_code and match['team2'] == team2_code) or
                     (match['team1'] == team2_code and match['team2'] == team1_code)]
        
        team1_wins = sum(1 for match in matches if match['winner'] == team1_code)
        team2_wins = sum(1 for match in matches if match['winner'] == team2_code)
        draws = len(matches) - team1_wins - team2_wins
        
        return {
            'total_matches': len(matches),
            'team1_wins': team1_wins,
            'team2_wins': team2_wins,
            'draws': draws,
            'matches': matches
        }
    
    def predict_group_standings(self, group_teams):
        """Predict the standings in a group based on team rankings and historical performance."""
        if len(group_teams) != 4:
            raise ValueError("Group must contain exactly 4 teams")
        
        # Simple prediction model based on FIFA ranking and win percentage
        standings = []
        for team in group_teams:
            if team not in self.teams_data:
                raise ValueError(f"Team {team} not found in data")
            
            ranking_score = 1 / self.teams_data[team]['ranking']  # Inverse ranking (higher is better)
            win_pct = self.calculate_win_percentage(team) / 100
            
            # Combined score (70% ranking, 30% win percentage)
            score = (0.7 * ranking_score) + (0.3 * win_pct)
            
            standings.append({
                'team': team,
                'name': self.teams_data[team]['name'],
                'score': score
            })
        
        # Sort by score (higher is better)
        return sorted(standings, key=lambda x: x['score'], reverse=True)
    
    def generate_team_performance_chart(self, team_code, output_file=None):
        """Generate a visualization of team performance."""
        if team_code not in self.teams_data:
            raise ValueError(f"Team {team_code} not found in data")
        
        team_name = self.teams_data[team_code]['name']
        matches = self.get_team_matches(team_code)
        
        # Extract results
        results = []
        for match in matches:
            if match['team1'] == team_code:
                if match['winner'] == team_code:
                    results.append('Win')
                elif match['winner'] is None:
                    results.append('Draw')
                else:
                    results.append('Loss')
            else:  # team2
                if match['winner'] == team_code:
                    results.append('Win')
                elif match['winner'] is None:
                    results.append('Draw')
                else:
                    results.append('Loss')
        
        # Count results
        win_count = results.count('Win')
        draw_count = results.count('Draw')
        loss_count = results.count('Loss')
        
        # Create pie chart
        plt.figure(figsize=(10, 6))
        plt.pie([win_count, draw_count, loss_count], 
                labels=['Wins', 'Draws', 'Losses'],
                autopct='%1.1f%%',
                colors=['green', 'gray', 'red'])
        plt.title(f'{team_name} Performance Analysis')
        
        if output_file:
            plt.savefig(output_file)
            return output_file
        else:
            plt.show()
            return None

    def export_team_analysis(self, team_code, output_dir='../../analytics/team_analysis/output'):
        """Export comprehensive team analysis to JSON file."""
        if team_code not in self.teams_data:
            raise ValueError(f"Team {team_code} not found in data")
        
        team_info = self.get_team_info(team_code)
        matches = self.get_team_matches(team_code)
        win_pct = self.calculate_win_percentage(team_code)
        
        analysis = {
            'team_code': team_code,
            'team_name': team_info['name'],
            'confederation': team_info['confederation'],
            'fifa_ranking': team_info['ranking'],
            'qualified': team_info.get('qualified', False),
            'matches_analyzed': len(matches),
            'win_percentage': win_pct,
            'matches': matches
        }
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Write to JSON file
        output_file = os.path.join(output_dir, f'{team_code}_analysis.json')
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        return output_file

# Example usage
if __name__ == "__main__":
    analyzer = TeamAnalyzer()
    
    # Get all qualified teams
    qualified = analyzer.get_qualified_teams()
    print(f"Qualified teams: {len(qualified)}")
    
    # Analyze Argentina
    arg_info = analyzer.get_team_info('ARG')
    print(f"Argentina FIFA Ranking: {arg_info['ranking']}")
    
    # Calculate win percentage
    win_pct = analyzer.calculate_win_percentage('ARG')
    print(f"Argentina win percentage: {win_pct:.1f}%")
    
    # Head-to-head analysis
    h2h = analyzer.head_to_head('ARG', 'FRA')
    print(f"Argentina vs France: {h2h['team1_wins']} wins, {h2h['team2_wins']} losses, {h2h['draws']} draws")
    
    # Predict group standings
    group_prediction = analyzer.predict_group_standings(['ARG', 'MEX', 'JPN', 'NZL'])
    print("Predicted Group Standings:")
    for i, team in enumerate(group_prediction):
        print(f"{i+1}. {team['name']}")
    
    # Generate and save performance chart
    chart_file = analyzer.generate_team_performance_chart('ARG', 'argentina_performance.png')
    print(f"Chart saved to: {chart_file}")
    
    # Export comprehensive analysis
    analysis_file = analyzer.export_team_analysis('ARG')
    print(f"Analysis exported to: {analysis_file}")
