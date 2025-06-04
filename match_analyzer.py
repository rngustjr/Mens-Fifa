"""
Match Analyzer for FIFA World Cup 2026

This module provides analytics functions for analyzing match dynamics,
phase-specific performance, and outcome predictions.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
import os

class MatchAnalyzer:
    """Class for analyzing match data for the World Cup."""
    
    def __init__(self, data_dir='../../data'):
        """Initialize the MatchAnalyzer with data directory path."""
        self.data_dir = Path(data_dir)
        self.matches_data = None
        self.teams_data = None
        self.match_events = None
        self.load_data()
        
    def load_data(self):
        """Load match, team, and event data from files."""
        # In a real implementation, this would load actual data files
        # For now, we'll create sample data structures
        
        # Sample matches data
        self.matches_data = {
            'M001': {
                'team1': 'ARG', 'team2': 'BRA', 
                'score1': 2, 'score2': 1, 
                'date': '2024-11-15', 
                'tournament': 'World Cup Qualifier',
                'stage': 'CONMEBOL Qualifier'
            },
            'M002': {
                'team1': 'FRA', 'team2': 'ENG', 
                'score1': 3, 'score2': 2, 
                'date': '2024-10-12', 
                'tournament': 'UEFA Nations League',
                'stage': 'Group Stage'
            },
            'M003': {
                'team1': 'USA', 'team2': 'MEX', 
                'score1': 2, 'score2': 0, 
                'date': '2024-09-07', 
                'tournament': 'CONCACAF Nations League',
                'stage': 'Final'
            },
            'M004': {
                'team1': 'QAT', 'team2': 'IRN', 
                'score1': 3, 'score2': 1, 
                'date': '2024-11-20', 
                'tournament': 'World Cup Qualifier',
                'stage': 'AFC Qualifier'
            },
            'M005': {
                'team1': 'EGY', 'team2': 'SEN', 
                'score1': 1, 'score2': 1, 
                'date': '2024-10-09', 
                'tournament': 'World Cup Qualifier',
                'stage': 'CAF Qualifier'
            },
            'M006': {
                'team1': 'JPN', 'team2': 'KOR', 
                'score1': 2, 'score2': 2, 
                'date': '2024-11-18', 
                'tournament': 'World Cup Qualifier',
                'stage': 'AFC Qualifier'
            }
        }
        
        # Sample teams data
        self.teams_data = {
            'ARG': {'name': 'Argentina', 'confederation': 'CONMEBOL', 'qualified': True, 'ranking': 1},
            'BRA': {'name': 'Brazil', 'confederation': 'CONMEBOL', 'qualified': False, 'ranking': 5},
            'FRA': {'name': 'France', 'confederation': 'UEFA', 'qualified': False, 'ranking': 2},
            'ENG': {'name': 'England', 'confederation': 'UEFA', 'qualified': False, 'ranking': 4},
            'USA': {'name': 'United States', 'confederation': 'CONCACAF', 'qualified': True, 'ranking': 13},
            'MEX': {'name': 'Mexico', 'confederation': 'CONCACAF', 'qualified': True, 'ranking': 15},
            'QAT': {'name': 'Qatar', 'confederation': 'AFC', 'qualified': False, 'ranking': 37},
            'IRN': {'name': 'IR Iran', 'confederation': 'AFC', 'qualified': True, 'ranking': 22},
            'EGY': {'name': 'Egypt', 'confederation': 'CAF', 'qualified': False, 'ranking': 36},
            'SEN': {'name': 'Senegal', 'confederation': 'CAF', 'qualified': False, 'ranking': 18},
            'JPN': {'name': 'Japan', 'confederation': 'AFC', 'qualified': True, 'ranking': 20},
            'KOR': {'name': 'Korea Republic', 'confederation': 'AFC', 'qualified': False, 'ranking': 24}
        }
        
        # Sample match events data
        self.match_events = [
            # Match M001 (ARG vs BRA)
            {'match_id': 'M001', 'team': 'ARG', 'event_type': 'goal', 'player': 'Messi', 'minute': 23, 'phase': '16-30'},
            {'match_id': 'M001', 'team': 'BRA', 'event_type': 'goal', 'player': 'Vinicius', 'minute': 45, 'phase': '31-45'},
            {'match_id': 'M001', 'team': 'ARG', 'event_type': 'goal', 'player': 'Martinez', 'minute': 78, 'phase': '61-90'},
            {'match_id': 'M001', 'team': 'ARG', 'event_type': 'yellow_card', 'player': 'De Paul', 'minute': 34, 'phase': '31-45'},
            {'match_id': 'M001', 'team': 'BRA', 'event_type': 'yellow_card', 'player': 'Casemiro', 'minute': 56, 'phase': '46-60'},
            
            # Match M002 (FRA vs ENG)
            {'match_id': 'M002', 'team': 'FRA', 'event_type': 'goal', 'player': 'Mbappé', 'minute': 12, 'phase': '0-15'},
            {'match_id': 'M002', 'team': 'ENG', 'event_type': 'goal', 'player': 'Kane', 'minute': 27, 'phase': '16-30'},
            {'match_id': 'M002', 'team': 'FRA', 'event_type': 'goal', 'player': 'Griezmann', 'minute': 43, 'phase': '31-45'},
            {'match_id': 'M002', 'team': 'ENG', 'event_type': 'goal', 'player': 'Bellingham', 'minute': 58, 'phase': '46-60'},
            {'match_id': 'M002', 'team': 'FRA', 'event_type': 'goal', 'player': 'Mbappé', 'minute': 82, 'phase': '61-90'},
            
            # Match M003 (USA vs MEX)
            {'match_id': 'M003', 'team': 'USA', 'event_type': 'goal', 'player': 'Pulisic', 'minute': 36, 'phase': '31-45'},
            {'match_id': 'M003', 'team': 'USA', 'event_type': 'goal', 'player': 'Weah', 'minute': 67, 'phase': '61-90'},
            {'match_id': 'M003', 'team': 'MEX', 'event_type': 'yellow_card', 'player': 'Alvarez', 'minute': 42, 'phase': '31-45'},
            {'match_id': 'M003', 'team': 'USA', 'event_type': 'yellow_card', 'player': 'Adams', 'minute': 51, 'phase': '46-60'},
            
            # Match M004 (QAT vs IRN)
            {'match_id': 'M004', 'team': 'QAT', 'event_type': 'goal', 'player': 'Ali', 'minute': 5, 'phase': '0-15'},
            {'match_id': 'M004', 'team': 'QAT', 'event_type': 'goal', 'player': 'Ali', 'minute': 34, 'phase': '31-45'},
            {'match_id': 'M004', 'team': 'IRN', 'event_type': 'goal', 'player': 'Taremi', 'minute': 52, 'phase': '46-60'},
            {'match_id': 'M004', 'team': 'QAT', 'event_type': 'goal', 'player': 'Afif', 'minute': 88, 'phase': '61-90'},
            
            # Match M005 (EGY vs SEN)
            {'match_id': 'M005', 'team': 'EGY', 'event_type': 'goal', 'player': 'Salah', 'minute': 45, 'phase': '31-45'},
            {'match_id': 'M005', 'team': 'SEN', 'event_type': 'goal', 'player': 'Mané', 'minute': 76, 'phase': '61-90'},
            
            # Match M006 (JPN vs KOR)
            {'match_id': 'M006', 'team': 'JPN', 'event_type': 'goal', 'player': 'Minamino', 'minute': 22, 'phase': '16-30'},
            {'match_id': 'M006', 'team': 'KOR', 'event_type': 'goal', 'player': 'Son', 'minute': 39, 'phase': '31-45'},
            {'match_id': 'M006', 'team': 'JPN', 'event_type': 'goal', 'player': 'Kamada', 'minute': 61, 'phase': '61-90'},
            {'match_id': 'M006', 'team': 'KOR', 'event_type': 'goal', 'player': 'Hwang', 'minute': 84, 'phase': '61-90'}
        ]
    
    def get_match_info(self, match_id):
        """Get basic information about a match."""
        if match_id in self.matches_data:
            return self.matches_data[match_id]
        return None
    
    def get_team_matches(self, team_code):
        """Get all matches involving a specific team."""
        return {mid: match for mid, match in self.matches_data.items() 
                if match['team1'] == team_code or match['team2'] == team_code}
    
    def get_match_events(self, match_id):
        """Get all events from a specific match."""
        return [event for event in self.match_events 
                if event['match_id'] == match_id]
    
    def get_events_by_phase(self, match_id, phase):
        """Get events from a specific match phase."""
        return [event for event in self.match_events 
                if event['match_id'] == match_id and event['phase'] == phase]
    
    def analyze_match_phases(self, match_id):
        """Analyze a match by breaking it down into phases."""
        if match_id not in self.matches_data:
            raise ValueError(f"Match {match_id} not found in data")
        
        match = self.matches_data[match_id]
        events = self.get_match_events(match_id)
        
        # Define phases
        phases = ['0-15', '16-30', '31-45', '46-60', '61-90']
        
        # Analyze each phase
        phase_analysis = {}
        for phase in phases:
            phase_events = [e for e in events if e['phase'] == phase]
            
            # Goals by team
            team1_goals = len([e for e in phase_events if e['event_type'] == 'goal' and e['team'] == match['team1']])
            team2_goals = len([e for e in phase_events if e['event_type'] == 'goal' and e['team'] == match['team2']])
            
            # Cards by team
            team1_cards = len([e for e in phase_events if 'card' in e['event_type'] and e['team'] == match['team1']])
            team2_cards = len([e for e in phase_events if 'card' in e['event_type'] and e['team'] == match['team2']])
            
            phase_analysis[phase] = {
                'events_count': len(phase_events),
                'goals': team1_goals + team2_goals,
                'cards': team1_cards + team2_cards,
                'team1_goals': team1_goals,
                'team2_goals': team2_goals,
                'team1_cards': team1_cards,
                'team2_cards': team2_cards,
                'events': phase_events
            }
        
        return phase_analysis
    
    def calculate_match_momentum(self, match_id):
        """Calculate momentum shifts during a match based on events."""
        if match_id not in self.matches_data:
            raise ValueError(f"Match {match_id} not found in data")
        
        match = self.matches_data[match_id]
        events = sorted(self.get_match_events(match_id), key=lambda x: x['minute'])
        
        # Initialize momentum (0 = neutral, positive = team1 advantage, negative = team2 advantage)
        momentum = [0]
        minutes = [0]
        
        # Calculate momentum shifts
        current_momentum = 0
        for event in events:
            if event['event_type'] == 'goal':
                if event['team'] == match['team1']:
                    current_momentum += 2  # Big boost for team1
                else:
                    current_momentum -= 2  # Big boost for team2
            elif 'card' in event['event_type']:
                if event['team'] == match['team1']:
                    current_momentum -= 0.5  # Small disadvantage for team1
                else:
                    current_momentum += 0.5  # Small disadvantage for team2
            
            momentum.append(current_momentum)
            minutes.append(event['minute'])
        
        # Add final minute
        momentum.append(current_momentum)
        minutes.append(90)
        
        return {'minutes': minutes, 'momentum': momentum}
    
    def predict_match_outcome(self, team1_code, team2_code):
        """Predict match outcome based on team rankings and historical performance."""
        if team1_code not in self.teams_data or team2_code not in self.teams_data:
            raise ValueError("Team not found in data")
        
        team1 = self.teams_data[team1_code]
        team2 = self.teams_data[team2_code]
        
        # Simple prediction model based on FIFA ranking
        team1_strength = 1 / team1['ranking']
        team2_strength = 1 / team2['ranking']
        
        total_strength = team1_strength + team2_strength
        team1_win_prob = team1_strength / total_strength
        team2_win_prob = team2_strength / total_strength
        draw_prob = 0.25  # Arbitrary draw probability
        
        # Adjust to ensure probabilities sum to 1
        team1_win_prob *= (1 - draw_prob)
        team2_win_prob *= (1 - draw_prob)
        
        return {
            'team1_win': team1_win_prob,
            'team2_win': team2_win_prob,
            'draw': draw_prob
        }
    
    def generate_phase_analysis_chart(self, match_id, output_file=None):
        """Generate a visualization of match phases."""
        if match_id not in self.matches_data:
            raise ValueError(f"Match {match_id} not found in data")
        
        match = self.matches_data[match_id]
        phase_analysis = self.analyze_match_phases(match_id)
        
        # Extract team names
        team1_name = self.teams_data[match['team1']]['name'] if match['team1'] in self.teams_data else match['team1']
        team2_name = self.teams_data[match['team2']]['name'] if match['team2'] in self.teams_data else match['team2']
        
        # Extract data for plotting
        phases = list(phase_analysis.keys())
        team1_goals = [phase_analysis[p]['team1_goals'] for p in phases]
        team2_goals = [phase_analysis[p]['team2_goals'] for p in phases]
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.arange(len(phases))
        width = 0.35
        
        ax.bar(x - width/2, team1_goals, width, label=team1_name)
        ax.bar(x + width/2, team2_goals, width, label=team2_name)
        
        ax.set_xlabel('Match Phase (minutes)')
        ax.set_ylabel('Goals Scored')
        ax.set_title(f'Goals by Match Phase: {team1_name} vs {team2_name}')
        ax.set_xticks(x)
        ax.set_xticklabels(phases)
        ax.legend()
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file)
            return output_file
        else:
            plt.show()
            return None
    
    def generate_momentum_chart(self, match_id, output_file=None):
        """Generate a visualization of match momentum shifts."""
        if match_id not in self.matches_data:
            raise ValueError(f"Match {match_id} not found in data")
        
        match = self.matches_data[match_id]
        momentum_data = self.calculate_match_momentum(match_id)
        
        # Extract team names
        team1_name = self.teams_data[match['team1']]['name'] if match['team1'] in self.teams_data else match['team1']
        team2_name = self.teams_data[match['team2']]['name'] if match['team2'] in self.teams_data else match['team2']
        
        # Create line chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(momentum_data['minutes'], momentum_data['momentum'], 'b-', linewidth=2)
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        
        # Add shading
        ax.fill_between(momentum_data['minutes'], momentum_data['momentum'], 0, 
                        where=[m > 0 for m in momentum_data['momentum']], 
                        color='blue', alpha=0.3, label=team1_name + ' Advantage')
        ax.fill_between(momentum_data['minutes'], momentum_data['momentum'], 0, 
                        where=[m < 0 for m in momentum_data['momentum']], 
                        color='red', alpha=0.3, label=team2_name + ' Advantage')
        
        ax.set_xlabel('Match Minute')
        ax.set_ylabel('Momentum')
        ax.set_title(f'Momentum Shifts: {team1_name} vs {team2_name}')
        ax.legend()
        
        # Add match phases
        phase_boundaries = [0, 15, 30, 45, 60, 90]
        for boundary in phase_boundaries:
            ax.axvline(x=boundary, color='gray', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file)
            return output_file
        else:
            plt.show()
            return None
    
    def export_match_analysis(self, match_id, output_dir='../../analytics/match_analysis/output'):
        """Export comprehensive match analysis to JSON file."""
        if match_id not in self.matches_data:
            raise ValueError(f"Match {match_id} not found in data")
        
        match = self.matches_data[match_id]
        events = self.get_match_events(match_id)
        phase_analysis = self.analyze_match_phases(match_id)
        momentum = self.calculate_match_momentum(match_id)
        
        # Get team info
        team1_info = self.teams_data[match['team1']] if match['team1'] in self.teams_data else {'name': match['team1']}
        team2_info = self.teams_data[match['team2']] if match['team2'] in self.teams_data else {'name': match['team2']}
        
        analysis = {
            'match_id': match_id,
            'team1': {
                'code': match['team1'],
                'name': team1_info.get('name', match['team1']),
                'score': match['score1']
            },
            'team2': {
                'code': match['team2'],
                'name': team2_info.get('name', match['team2']),
                'score': match['score2']
            },
            'date': match['date'],
            'tournament': match['tournament'],
            'stage': match['stage'],
            'events_count': len(events),
            'phase_analysis': phase_analysis,
            'momentum_data': {
                'minutes': momentum['minutes'],
                'values': momentum['momentum']
            }
        }
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Write to JSON file
        output_file = os.path.join(output_dir, f'{match_id}_analysis.json')
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        return output_file

# Example usage
if __name__ == "__main__":
    analyzer = MatchAnalyzer()
    
    # Get match info
    match_info = analyzer.get_match_info('M001')
    print(f"Match: {match_info['team1']} vs {match_info['team2']}, Score: {match_info['score1']}-{match_info['score2']}")
    
    # Analyze match phases
    phases = analyzer.analyze_match_phases('M001')
    print("\nMatch Phase Analysis:")
    for phase, data in phases.items():
        print(f"{phase} mins: {data['goals']} goals, {data['cards']} cards")
    
    # Calculate momentum
    momentum = analyzer.calculate_match_momentum('M001')
    print(f"\nMomentum shifts at minutes: {momentum['minutes']}")
    print(f"Momentum values: {momentum['momentum']}")
    
    # Predict match outcome
    prediction = analyzer.predict_match_outcome('ARG', 'BRA')
    print(f"\nMatch Prediction - ARG vs BRA:")
    print(f"ARG win: {prediction['team1_win']:.2f}, BRA win: {prediction['team2_win']:.2f}, Draw: {prediction['draw']:.2f}")
    
    # Generate and save phase analysis chart
    chart_file = analyzer.generate_phase_analysis_chart('M001', 'match_phases.png')
    print(f"\nPhase analysis chart saved to: {chart_file}")
    
    # Generate and save momentum chart
    momentum_file = analyzer.generate_momentum_chart('M001', 'match_momentum.png')
    print(f"Momentum chart saved to: {momentum_file}")
    
    # Export comprehensive analysis
    analysis_file = analyzer.export_match_analysis('M001')
    print(f"Analysis exported to: {analysis_file}")
