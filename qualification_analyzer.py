"""
Qualification Analyzer for FIFA World Cup 2026

This module provides analytics functions for analyzing the qualification process,
pathways, and performance metrics for teams competing to reach the FIFA World Cup 2026.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
import os

class QualificationAnalyzer:
    """Class for analyzing qualification data for the World Cup."""
    
    def __init__(self, data_dir='../../data'):
        """Initialize the QualificationAnalyzer with data directory path."""
        self.data_dir = Path(data_dir)
        self.qualification_data = None
        self.teams_data = None
        self.confederation_formats = None
        self.load_data()
        
    def load_data(self):
        """Load qualification and team data from files."""
        # In a real implementation, this would load actual data files
        # For now, we'll create sample data structures
        
        # Sample teams data
        self.teams_data = {
            'ARG': {'name': 'Argentina', 'confederation': 'CONMEBOL', 'qualified': True, 'ranking': 1},
            'BRA': {'name': 'Brazil', 'confederation': 'CONMEBOL', 'qualified': False, 'ranking': 5},
            'URU': {'name': 'Uruguay', 'confederation': 'CONMEBOL', 'qualified': False, 'ranking': 15},
            'COL': {'name': 'Colombia', 'confederation': 'CONMEBOL', 'qualified': False, 'ranking': 12},
            'CAN': {'name': 'Canada', 'confederation': 'CONCACAF', 'qualified': True, 'ranking': 43},
            'MEX': {'name': 'Mexico', 'confederation': 'CONCACAF', 'qualified': True, 'ranking': 15},
            'USA': {'name': 'United States', 'confederation': 'CONCACAF', 'qualified': True, 'ranking': 13},
            'CRC': {'name': 'Costa Rica', 'confederation': 'CONCACAF', 'qualified': False, 'ranking': 52},
            'JPN': {'name': 'Japan', 'confederation': 'AFC', 'qualified': True, 'ranking': 20},
            'IRN': {'name': 'IR Iran', 'confederation': 'AFC', 'qualified': True, 'ranking': 22},
            'KOR': {'name': 'Korea Republic', 'confederation': 'AFC', 'qualified': False, 'ranking': 24},
            'AUS': {'name': 'Australia', 'confederation': 'AFC', 'qualified': False, 'ranking': 25},
            'QAT': {'name': 'Qatar', 'confederation': 'AFC', 'qualified': False, 'ranking': 37},
            'NZL': {'name': 'New Zealand', 'confederation': 'OFC', 'qualified': True, 'ranking': 103},
            'SOL': {'name': 'Solomon Islands', 'confederation': 'OFC', 'qualified': False, 'ranking': 142},
            'ENG': {'name': 'England', 'confederation': 'UEFA', 'qualified': False, 'ranking': 4},
            'FRA': {'name': 'France', 'confederation': 'UEFA', 'qualified': False, 'ranking': 2},
            'ESP': {'name': 'Spain', 'confederation': 'UEFA', 'qualified': False, 'ranking': 8},
            'GER': {'name': 'Germany', 'confederation': 'UEFA', 'qualified': False, 'ranking': 16},
            'ITA': {'name': 'Italy', 'confederation': 'UEFA', 'qualified': False, 'ranking': 9},
            'EGY': {'name': 'Egypt', 'confederation': 'CAF', 'qualified': False, 'ranking': 36},
            'SEN': {'name': 'Senegal', 'confederation': 'CAF', 'qualified': False, 'ranking': 18},
            'MAR': {'name': 'Morocco', 'confederation': 'CAF', 'qualified': False, 'ranking': 13},
            'NGA': {'name': 'Nigeria', 'confederation': 'CAF', 'qualified': False, 'ranking': 30}
        }
        
        # Sample qualification data
        self.qualification_data = {
            'ARG': {'matches_played': 8, 'wins': 6, 'draws': 1, 'losses': 1, 'goals_for': 16, 'goals_against': 5, 'points': 19, 'status': 'qualified'},
            'BRA': {'matches_played': 8, 'wins': 4, 'draws': 2, 'losses': 2, 'goals_for': 12, 'goals_against': 7, 'points': 14, 'status': 'in_progress'},
            'URU': {'matches_played': 8, 'wins': 4, 'draws': 1, 'losses': 3, 'goals_for': 11, 'goals_against': 9, 'points': 13, 'status': 'in_progress'},
            'COL': {'matches_played': 8, 'wins': 3, 'draws': 3, 'losses': 2, 'goals_for': 9, 'goals_against': 8, 'points': 12, 'status': 'in_progress'},
            'JPN': {'matches_played': 6, 'wins': 6, 'draws': 0, 'losses': 0, 'goals_for': 15, 'goals_against': 2, 'points': 18, 'status': 'qualified'},
            'IRN': {'matches_played': 6, 'wins': 5, 'draws': 1, 'losses': 0, 'goals_for': 12, 'goals_against': 3, 'points': 16, 'status': 'qualified'},
            'KOR': {'matches_played': 6, 'wins': 3, 'draws': 2, 'losses': 1, 'goals_for': 8, 'goals_against': 5, 'points': 11, 'status': 'in_progress'},
            'AUS': {'matches_played': 6, 'wins': 3, 'draws': 1, 'losses': 2, 'goals_for': 9, 'goals_against': 7, 'points': 10, 'status': 'in_progress'},
            'QAT': {'matches_played': 6, 'wins': 2, 'draws': 1, 'losses': 3, 'goals_for': 7, 'goals_against': 8, 'points': 7, 'status': 'in_progress'},
            'NZL': {'matches_played': 4, 'wins': 4, 'draws': 0, 'losses': 0, 'goals_for': 12, 'goals_against': 1, 'points': 12, 'status': 'qualified'},
            'SOL': {'matches_played': 4, 'wins': 2, 'draws': 0, 'losses': 2, 'goals_for': 5, 'goals_against': 7, 'points': 6, 'status': 'eliminated'},
            'ENG': {'matches_played': 4, 'wins': 3, 'draws': 1, 'losses': 0, 'goals_for': 10, 'goals_against': 2, 'points': 10, 'status': 'in_progress'},
            'FRA': {'matches_played': 4, 'wins': 3, 'draws': 0, 'losses': 1, 'goals_for': 8, 'goals_against': 3, 'points': 9, 'status': 'in_progress'},
            'ESP': {'matches_played': 4, 'wins': 2, 'draws': 2, 'losses': 0, 'goals_for': 7, 'goals_against': 2, 'points': 8, 'status': 'in_progress'},
            'GER': {'matches_played': 4, 'wins': 2, 'draws': 1, 'losses': 1, 'goals_for': 8, 'goals_against': 4, 'points': 7, 'status': 'in_progress'},
            'ITA': {'matches_played': 4, 'wins': 2, 'draws': 1, 'losses': 1, 'goals_for': 6, 'goals_against': 4, 'points': 7, 'status': 'in_progress'},
            'EGY': {'matches_played': 4, 'wins': 2, 'draws': 2, 'losses': 0, 'goals_for': 6, 'goals_against': 1, 'points': 8, 'status': 'in_progress'},
            'SEN': {'matches_played': 4, 'wins': 2, 'draws': 1, 'losses': 1, 'goals_for': 5, 'goals_against': 3, 'points': 7, 'status': 'in_progress'},
            'MAR': {'matches_played': 4, 'wins': 3, 'draws': 0, 'losses': 1, 'goals_for': 8, 'goals_against': 2, 'points': 9, 'status': 'in_progress'},
            'NGA': {'matches_played': 4, 'wins': 2, 'draws': 0, 'losses': 2, 'goals_for': 5, 'goals_against': 4, 'points': 6, 'status': 'in_progress'}
        }
        
        # Sample confederation qualification formats
        self.confederation_formats = {
            'UEFA': {
                'total_slots': 16,
                'format': '12 groups of 4-5 teams, group winners qualify directly, best runners-up enter playoffs'
            },
            'CONMEBOL': {
                'total_slots': 6,
                'format': 'Single round-robin league, top 6 teams qualify directly'
            },
            'CONCACAF': {
                'total_slots': 6,
                'format': 'Three rounds: First round (30 teams), Second round (8 groups of 4), Final round (8 teams)'
            },
            'AFC': {
                'total_slots': 8,
                'format': 'Three rounds: First round (22 teams), Second round (9 groups of 4), Final round (3 groups of 6)'
            },
            'CAF': {
                'total_slots': 9,
                'format': 'First round (28 teams), Second round (9 groups of 6), group winners qualify'
            },
            'OFC': {
                'total_slots': 1,
                'format': 'Group stage followed by knockout rounds'
            }
        }
    
    def get_team_qualification_data(self, team_code):
        """Get qualification data for a specific team."""
        if team_code in self.qualification_data:
            return self.qualification_data[team_code]
        return None
    
    def get_confederation_teams(self, confederation):
        """Get all teams from a specific confederation."""
        return {code: data for code, data in self.teams_data.items() 
                if data.get('confederation') == confederation}
    
    def get_qualification_by_status(self, status):
        """Get teams with a specific qualification status."""
        return {code: data for code, data in self.qualification_data.items() 
                if data.get('status') == status}
    
    def get_confederation_format(self, confederation):
        """Get qualification format for a specific confederation."""
        if confederation in self.confederation_formats:
            return self.confederation_formats[confederation]
        return None
    
    def calculate_qualification_efficiency(self, team_code):
        """Calculate qualification efficiency (points per match) for a team."""
        if team_code not in self.qualification_data:
            return 0
        
        qual_data = self.qualification_data[team_code]
        if qual_data['matches_played'] == 0:
            return 0
        
        return qual_data['points'] / qual_data['matches_played']
    
    def calculate_confederation_stats(self, confederation):
        """Calculate aggregate qualification statistics for a confederation."""
        teams = self.get_confederation_teams(confederation)
        
        # Initialize stats
        total_matches = 0
        total_wins = 0
        total_draws = 0
        total_losses = 0
        total_goals_for = 0
        total_goals_against = 0
        total_points = 0
        qualified_teams = 0
        
        # Aggregate stats
        for team_code in teams:
            if team_code in self.qualification_data:
                qual_data = self.qualification_data[team_code]
                total_matches += qual_data.get('matches_played', 0)
                total_wins += qual_data.get('wins', 0)
                total_draws += qual_data.get('draws', 0)
                total_losses += qual_data.get('losses', 0)
                total_goals_for += qual_data.get('goals_for', 0)
                total_goals_against += qual_data.get('goals_against', 0)
                total_points += qual_data.get('points', 0)
                if qual_data.get('status') == 'qualified':
                    qualified_teams += 1
        
        # Calculate averages
        team_count = len(teams)
        if team_count == 0:
            return None
        
        avg_matches = total_matches / team_count
        avg_points = total_points / team_count if total_matches > 0 else 0
        avg_goals_for = total_goals_for / team_count if total_matches > 0 else 0
        avg_goals_against = total_goals_against / team_count if total_matches > 0 else 0
        
        return {
            'confederation': confederation,
            'team_count': team_count,
            'qualified_teams': qualified_teams,
            'avg_matches': avg_matches,
            'avg_points': avg_points,
            'avg_goals_for': avg_goals_for,
            'avg_goals_against': avg_goals_against,
            'total_slots': self.confederation_formats.get(confederation, {}).get('total_slots', 0)
        }
    
    def predict_qualification_probability(self, team_code):
        """Predict qualification probability for a team based on current performance."""
        if team_code not in self.qualification_data or team_code not in self.teams_data:
            return 0
        
        qual_data = self.qualification_data[team_code]
        team_data = self.teams_data[team_code]
        
        # If already qualified or eliminated, return appropriate probability
        if qual_data['status'] == 'qualified':
            return 1.0
        elif qual_data['status'] == 'eliminated':
            return 0.0
        
        # Get confederation data
        confederation = team_data['confederation']
        conf_stats = self.calculate_confederation_stats(confederation)
        if not conf_stats:
            return 0
        
        # Calculate points per match
        points_per_match = self.calculate_qualification_efficiency(team_code)
        
        # Calculate ranking factor (higher ranking = lower value = better)
        ranking_factor = 1 / (team_data['ranking'] + 1)  # Add 1 to avoid division by zero
        
        # Calculate goal difference factor
        goal_diff = qual_data['goals_for'] - qual_data['goals_against']
        goal_diff_factor = (goal_diff + 10) / 20  # Normalize to approximately 0-1 range
        
        # Calculate probability based on weighted factors
        # This is a simplified model - a real model would be more sophisticated
        probability = (0.5 * points_per_match / 3) + (0.3 * ranking_factor) + (0.2 * goal_diff_factor)
        
        # Adjust based on available slots in confederation
        slots_factor = conf_stats['qualified_teams'] / conf_stats['total_slots']
        probability *= (1 - slots_factor)  # Reduce probability if many slots already filled
        
        # Ensure probability is between 0 and 1
        return max(0, min(1, probability))
    
    def generate_confederation_comparison_chart(self, output_file=None):
        """Generate a visualization comparing qualification performance across confederations."""
        confederations = ['UEFA', 'CONMEBOL', 'CONCACAF', 'AFC', 'CAF', 'OFC']
        
        # Calculate stats for each confederation
        stats = []
        for conf in confederations:
            conf_stats = self.calculate_confederation_stats(conf)
            if conf_stats:
                stats.append(conf_stats)
        
        if not stats:
            return None
        
        # Create DataFrame for easier plotting
        df = pd.DataFrame(stats)
        
        # Create multi-bar chart
        fig, ax = plt.subplots(figsize=(12, 8))
        
        x = np.arange(len(confederations))
        width = 0.2
        
        # Plot bars for different metrics
        ax.bar(x - width*1.5, df['avg_points'], width, label='Avg. Points')
        ax.bar(x - width/2, df['avg_goals_for'], width, label='Avg. Goals For')
        ax.bar(x + width/2, df['avg_goals_against'], width, label='Avg. Goals Against')
        ax.bar(x + width*1.5, df['qualified_teams'], width, label='Qualified Teams')
        
        ax.set_xlabel('Confederation')
        ax.set_ylabel('Value')
        ax.set_title('Qualification Performance by Confederation')
        ax.set_xticks(x)
        ax.set_xticklabels(confederations)
        ax.legend()
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file)
            return output_file
        else:
            plt.show()
            return None
    
    def generate_qualification_probability_chart(self, team_codes, output_file=None):
        """Generate a visualization of qualification probabilities for selected teams."""
        # Calculate probabilities for each team
        probabilities = []
        labels = []
        
        for team_code in team_codes:
            if team_code in self.teams_data:
                prob = self.predict_qualification_probability(team_code)
                probabilities.append(prob)
                labels.append(self.teams_data[team_code]['name'])
        
        if not probabilities:
            return None
        
        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, len(probabilities) * 0.5 + 2))
        
        y_pos = np.arange(len(labels))
        ax.barh(y_pos, probabilities, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels)
        ax.invert_yaxis()  # Labels read top-to-bottom
        ax.set_xlabel('Qualification Probability')
        ax.set_title('World Cup 2026 Qualification Probabilities')
        
        # Add percentage labels
        for i, v in enumerate(probabilities):
            ax.text(v + 0.01, i, f"{v:.0%}", va='center')
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file)
            return output_file
        else:
            plt.show()
            return None
    
    def export_qualification_analysis(self, confederation=None, output_dir='../../analytics/qualification_analysis/output'):
        """Export comprehensive qualification analysis to JSON file."""
        # Determine which teams to analyze
        if confederation:
            teams = self.get_confederation_teams(confederation)
            filename = f"{confederation}_qualification_analysis.json"
        else:
            teams = self.teams_data
            filename = "all_qualification_analysis.json"
        
        # Prepare analysis data
        analysis = {
            'teams': {},
            'confederation_stats': {}
        }
        
        # Add team-specific analysis
        for team_code, team_data in teams.items():
            if team_code in self.qualification_data:
                qual_data = self.qualification_data[team_code]
                
                analysis['teams'][team_code] = {
                    'name': team_data['name'],
                    'confederation': team_data['confederation'],
                    'ranking': team_data['ranking'],
                    'qualification_data': qual_data,
                    'efficiency': self.calculate_qualification_efficiency(team_code),
                    'qualification_probability': self.predict_qualification_probability(team_code)
                }
        
        # Add confederation stats
        confederations = [confederation] if confederation else ['UEFA', 'CONMEBOL', 'CONCACAF', 'AFC', 'CAF', 'OFC']
        for conf in confederations:
            stats = self.calculate_confederation_stats(conf)
            if stats:
                analysis['confederation_stats'][conf] = stats
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Write to JSON file
        output_file = os.path.join(output_dir, filename)
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        return output_file

# Example usage
if __name__ == "__main__":
    analyzer = QualificationAnalyzer()
    
    # Get qualification data for Argentina
    arg_data = analyzer.get_team_qualification_data('ARG')
    print(f"Argentina qualification: {arg_data['wins']} wins, {arg_data['draws']} draws, {arg_data['losses']} losses, {arg_data['points']} points")
    
    # Calculate qualification efficiency
    efficiency = analyzer.calculate_qualification_efficiency('ARG')
    print(f"Argentina qualification efficiency: {efficiency:.2f} points per match")
    
    # Get CONMEBOL teams
    conmebol_teams = analyzer.get_confederation_teams('CONMEBOL')
    print(f"CONMEBOL teams: {len(conmebol_teams)}")
    
    # Calculate confederation stats
    conmebol_stats = analyzer.calculate_confederation_stats('CONMEBOL')
    print(f"CONMEBOL avg points: {conmebol_stats['avg_points']:.2f}, qualified teams: {conmebol_stats['qualified_teams']}")
    
    # Predict qualification probability
    probability = analyzer.predict_qualification_probability('BRA')
    print(f"Brazil qualification probability: {probability:.2%}")
    
    # Generate and save confederation comparison chart
    chart_file = analyzer.generate_confederation_comparison_chart('confederation_comparison.png')
    print(f"Confederation comparison chart saved to: {chart_file}")
    
    # Generate and save qualification probability chart for selected teams
    prob_chart = analyzer.generate_qualification_probability_chart(['BRA', 'URU', 'COL', 'ENG', 'FRA', 'ESP'], 'qualification_probabilities.png')
    print(f"Qualification probability chart saved to: {prob_chart}")
    
    # Export comprehensive analysis
    analysis_file = analyzer.export_qualification_analysis('CONMEBOL')
    print(f"CONMEBOL analysis exported to: {analysis_file}")
    
    # Export all qualification analysis
    all_analysis_file = analyzer.export_qualification_analysis()
    print(f"All qualification analysis exported to: {all_analysis_file}")
