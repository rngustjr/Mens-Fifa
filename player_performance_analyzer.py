"""
Player Performance Analyzer for FIFA World Cup 2026

This module provides analytics functions for analyzing player performance,
statistics, and generating performance metrics.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
import os

class PlayerAnalyzer:
    """Class for analyzing player performance data for the World Cup."""
    
    def __init__(self, data_dir='../../data'):
        """Initialize the PlayerAnalyzer with data directory path."""
        self.data_dir = Path(data_dir)
        self.players_data = None
        self.teams_data = None
        self.matches_data = None
        self.load_data()
        
    def load_data(self):
        """Load player, team, and match data from files."""
        # In a real implementation, this would load actual data files
        # For now, we'll create sample data structures
        
        # Sample players data
        self.players_data = {
            'P001': {'name': 'Lionel Messi', 'team': 'ARG', 'position': 'Forward', 'age': 37, 'caps': 180, 'goals': 106},
            'P002': {'name': 'Cristiano Ronaldo', 'team': 'POR', 'position': 'Forward', 'age': 40, 'caps': 206, 'goals': 128},
            'P003': {'name': 'Kylian Mbappé', 'team': 'FRA', 'position': 'Forward', 'age': 26, 'caps': 76, 'goals': 46},
            'P004': {'name': 'Alphonso Davies', 'team': 'CAN', 'position': 'Defender', 'age': 24, 'caps': 44, 'goals': 14},
            'P005': {'name': 'Christian Pulisic', 'team': 'USA', 'position': 'Midfielder', 'age': 26, 'caps': 64, 'goals': 27},
            'P006': {'name': 'Hirving Lozano', 'team': 'MEX', 'position': 'Forward', 'age': 29, 'caps': 67, 'goals': 18},
            'P007': {'name': 'Almoez Ali', 'team': 'QAT', 'position': 'Forward', 'age': 28, 'caps': 85, 'goals': 42},
            'P008': {'name': 'Mohamed Salah', 'team': 'EGY', 'position': 'Forward', 'age': 33, 'caps': 93, 'goals': 54},
            'P009': {'name': 'Takumi Minamino', 'team': 'JPN', 'position': 'Midfielder', 'age': 30, 'caps': 56, 'goals': 21},
            'P010': {'name': 'Mehdi Taremi', 'team': 'IRN', 'position': 'Forward', 'age': 32, 'caps': 73, 'goals': 45},
        }
        
        # Sample teams data
        self.teams_data = {
            'ARG': {'name': 'Argentina', 'confederation': 'CONMEBOL', 'qualified': True, 'ranking': 1},
            'POR': {'name': 'Portugal', 'confederation': 'UEFA', 'qualified': False, 'ranking': 6},
            'FRA': {'name': 'France', 'confederation': 'UEFA', 'qualified': False, 'ranking': 2},
            'CAN': {'name': 'Canada', 'confederation': 'CONCACAF', 'qualified': True, 'ranking': 43},
            'USA': {'name': 'United States', 'confederation': 'CONCACAF', 'qualified': True, 'ranking': 13},
            'MEX': {'name': 'Mexico', 'confederation': 'CONCACAF', 'qualified': True, 'ranking': 15},
            'QAT': {'name': 'Qatar', 'confederation': 'AFC', 'qualified': False, 'ranking': 37},
            'EGY': {'name': 'Egypt', 'confederation': 'CAF', 'qualified': False, 'ranking': 36},
            'JPN': {'name': 'Japan', 'confederation': 'AFC', 'qualified': True, 'ranking': 20},
            'IRN': {'name': 'IR Iran', 'confederation': 'AFC', 'qualified': True, 'ranking': 22},
        }
        
        # Sample match events data (goals, assists, etc.)
        self.match_events = [
            {'match_id': 'M001', 'player_id': 'P001', 'event_type': 'goal', 'minute': 23},
            {'match_id': 'M001', 'player_id': 'P001', 'event_type': 'assist', 'minute': 64},
            {'match_id': 'M002', 'player_id': 'P003', 'event_type': 'goal', 'minute': 12},
            {'match_id': 'M002', 'player_id': 'P003', 'event_type': 'goal', 'minute': 78},
            {'match_id': 'M003', 'player_id': 'P005', 'event_type': 'assist', 'minute': 56},
            {'match_id': 'M004', 'player_id': 'P007', 'event_type': 'goal', 'minute': 34},
            {'match_id': 'M004', 'player_id': 'P007', 'event_type': 'goal', 'minute': 67},
            {'match_id': 'M005', 'player_id': 'P008', 'event_type': 'goal', 'minute': 45},
            {'match_id': 'M006', 'player_id': 'P010', 'event_type': 'goal', 'minute': 22},
            {'match_id': 'M006', 'player_id': 'P010', 'event_type': 'assist', 'minute': 51},
        ]
    
    def get_player_info(self, player_id):
        """Get basic information about a player."""
        if player_id in self.players_data:
            return self.players_data[player_id]
        return None
    
    def get_players_by_team(self, team_code):
        """Get all players from a specific team."""
        return {pid: data for pid, data in self.players_data.items() 
                if data.get('team') == team_code}
    
    def get_players_by_position(self, position):
        """Get all players with a specific position."""
        return {pid: data for pid, data in self.players_data.items() 
                if data.get('position') == position}
    
    def get_player_events(self, player_id):
        """Get all match events involving a specific player."""
        return [event for event in self.match_events 
                if event['player_id'] == player_id]
    
    def calculate_goals_per_match(self, player_id):
        """Calculate goals per match for a player based on events data."""
        if player_id not in self.players_data:
            return 0
        
        player = self.players_data[player_id]
        goals = len([event for event in self.match_events 
                    if event['player_id'] == player_id and event['event_type'] == 'goal'])
        
        # In a real implementation, we would count actual matches played
        # Here we'll use a simplified approach with caps
        if player['caps'] == 0:
            return 0
        
        return goals / player['caps']
    
    def calculate_assists_per_match(self, player_id):
        """Calculate assists per match for a player based on events data."""
        if player_id not in self.players_data:
            return 0
        
        player = self.players_data[player_id]
        assists = len([event for event in self.match_events 
                      if event['player_id'] == player_id and event['event_type'] == 'assist'])
        
        if player['caps'] == 0:
            return 0
        
        return assists / player['caps']
    
    def get_top_scorers(self, limit=10):
        """Get the top goal scorers based on total goals."""
        # Sort players by goals
        sorted_players = sorted(self.players_data.items(), 
                               key=lambda x: x[1]['goals'], 
                               reverse=True)
        
        # Return top N players
        return sorted_players[:limit]
    
    def get_top_scorers_by_confederation(self, confederation, limit=5):
        """Get the top goal scorers from a specific confederation."""
        # Filter players by confederation
        confederation_players = []
        for pid, player in self.players_data.items():
            team_code = player.get('team')
            if team_code in self.teams_data and self.teams_data[team_code]['confederation'] == confederation:
                confederation_players.append((pid, player))
        
        # Sort by goals
        sorted_players = sorted(confederation_players, 
                               key=lambda x: x[1]['goals'], 
                               reverse=True)
        
        # Return top N players
        return sorted_players[:limit]
    
    def generate_player_comparison(self, player_ids, metrics=None):
        """Generate a comparison between multiple players on specified metrics."""
        if not metrics:
            metrics = ['goals', 'caps', 'goals_per_match']
        
        comparison = {}
        for pid in player_ids:
            if pid not in self.players_data:
                continue
            
            player = self.players_data[pid]
            player_metrics = {
                'name': player['name'],
                'team': player['team'],
                'position': player['position']
            }
            
            for metric in metrics:
                if metric == 'goals_per_match':
                    player_metrics[metric] = self.calculate_goals_per_match(pid)
                elif metric == 'assists_per_match':
                    player_metrics[metric] = self.calculate_assists_per_match(pid)
                elif metric in player:
                    player_metrics[metric] = player[metric]
            
            comparison[pid] = player_metrics
        
        return comparison
    
    def generate_player_radar_chart(self, player_id, output_file=None):
        """Generate a radar chart visualization of player attributes."""
        if player_id not in self.players_data:
            raise ValueError(f"Player {player_id} not found in data")
        
        player = self.players_data[player_id]
        player_name = player['name']
        
        # Define attributes to visualize (in a real implementation, these would be more comprehensive)
        attributes = ['goals', 'caps', 'age']
        values = [player['goals'], player['caps'], player['age']]
        
        # Add calculated metrics
        goals_per_match = self.calculate_goals_per_match(player_id)
        assists_per_match = self.calculate_assists_per_match(player_id)
        attributes.extend(['goals_per_match', 'assists_per_match'])
        values.extend([goals_per_match * 100, assists_per_match * 100])  # Scale for visualization
        
        # Create radar chart
        angles = np.linspace(0, 2*np.pi, len(attributes), endpoint=False).tolist()
        values += values[:1]  # Close the polygon
        angles += angles[:1]  # Close the polygon
        attributes += attributes[:1]  # Close the polygon
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        ax.plot(angles, values, 'o-', linewidth=2)
        ax.fill(angles, values, alpha=0.25)
        ax.set_thetagrids(np.degrees(angles[:-1]), attributes[:-1])
        ax.set_title(f"{player_name} Performance Profile", size=15)
        
        if output_file:
            plt.savefig(output_file)
            return output_file
        else:
            plt.show()
            return None
    
    def export_player_analysis(self, player_id, output_dir='../../analytics/player_analysis/output'):
        """Export comprehensive player analysis to JSON file."""
        if player_id not in self.players_data:
            raise ValueError(f"Player {player_id} not found in data")
        
        player = self.players_data[player_id]
        events = self.get_player_events(player_id)
        goals_per_match = self.calculate_goals_per_match(player_id)
        assists_per_match = self.calculate_assists_per_match(player_id)
        
        analysis = {
            'player_id': player_id,
            'name': player['name'],
            'team': player['team'],
            'team_name': self.teams_data[player['team']]['name'] if player['team'] in self.teams_data else None,
            'position': player['position'],
            'age': player['age'],
            'caps': player['caps'],
            'goals': player['goals'],
            'goals_per_match': goals_per_match,
            'assists_per_match': assists_per_match,
            'events': events
        }
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Write to JSON file
        output_file = os.path.join(output_dir, f'{player_id}_analysis.json')
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        return output_file

# Example usage
if __name__ == "__main__":
    analyzer = PlayerAnalyzer()
    
    # Get top scorers
    top_scorers = analyzer.get_top_scorers(5)
    print("Top 5 Goal Scorers:")
    for i, (pid, player) in enumerate(top_scorers):
        print(f"{i+1}. {player['name']} ({player['team']}) - {player['goals']} goals")
    
    # Get top CONCACAF scorers
    concacaf_scorers = analyzer.get_top_scorers_by_confederation('CONCACAF', 3)
    print("\nTop 3 CONCACAF Goal Scorers:")
    for i, (pid, player) in enumerate(concacaf_scorers):
        print(f"{i+1}. {player['name']} ({player['team']}) - {player['goals']} goals")
    
    # Player comparison
    comparison = analyzer.generate_player_comparison(['P001', 'P003', 'P005'], 
                                                   ['goals', 'caps', 'goals_per_match'])
    print("\nPlayer Comparison:")
    for pid, metrics in comparison.items():
        print(f"{metrics['name']} ({metrics['team']}): {metrics['goals']} goals, {metrics['goals_per_match']:.3f} goals/match")
    
    # Generate and save radar chart
    chart_file = analyzer.generate_player_radar_chart('P001', 'messi_profile.png')
    print(f"\nRadar chart saved to: {chart_file}")
    
    # Export comprehensive analysis
    analysis_file = analyzer.export_player_analysis('P001')
    print(f"Analysis exported to: {analysis_file}")
