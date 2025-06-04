# Match Phase Analysis LLM Prompts Design

## Overview
This document outlines the design for language model prompts that will analyze different phases of World Cup matches, providing insights, predictions, and analysis based on real-time and historical data.

## Match Phase Prompts

### Phase 1: 0-15 Minutes (Starting Lineup Analysis)
```
Analyze the starting lineup of [TEAM] against [OPPONENT] in this World Cup match.
Based on the selected players, their recent form, and historical data:
1. Identify which players are likely to be most active with the ball in the first 15 minutes
2. Calculate the probability of an early goal based on both teams' starting formations
3. Predict potential early fouls based on player matchups and referee tendencies
4. Analyze how the chosen formation might influence early possession patterns
5. Identify key player matchups that could define the early stages of the match
```

### Phase 2: 16-30 Minutes (Possession and Expected Goals)
```
Based on the first 15 minutes of play between [TEAM] and [OPPONENT]:
1. Analyze the possession patterns that have emerged
2. Calculate the expected goals (xG) for each team based on current play style
3. Identify which team is controlling the midfield and territorial advantage
4. Predict how possession trends might influence goal-scoring opportunities
5. Analyze which tactical adjustments might be beneficial for each team
```

### Phase 3: 31-45 Minutes (Stamina and Concentration)
```
As we approach halftime in the match between [TEAM] and [OPPONENT]:
1. Identify players showing signs of fatigue or concentration lapses
2. Based on historical data, calculate the likelihood of a late first-half goal
3. Analyze how stamina issues might be affecting tactical execution
4. Predict potential halftime substitutions based on current performance
5. Compare current performance to historical patterns of late first-half goals or concessions
```

### Phase 4: 45-60 Minutes (Substitution and Tactical Changes)
```
Analyzing the start of the second half between [TEAM] and [OPPONENT]:
1. Evaluate the impact of any halftime substitutions or tactical changes
2. Predict which players might be substituted in the coming minutes based on conditioning data
3. Analyze how the importance of upcoming fixtures might influence substitution strategies
4. Identify key tactical adjustments made by each team after halftime
5. Calculate how these changes have affected possession and attacking threat
```

### Phase 5: 60-90 Minutes (Prediction Aggregation and Outcome)
```
For the final 30 minutes of the match between [TEAM] and [OPPONENT]:
1. Aggregate viewer predictions for the match outcome
2. Calculate win probability based on current score, momentum, and remaining substitutions
3. Identify key players likely to influence the closing stages
4. Predict potential game-changing moments based on fatigue levels and tactical setups
5. Analyze how current game state compares to historical patterns for these teams
```

## Implementation Considerations

1. **Data Integration Requirements**:
   - Real-time match statistics feed
   - Player performance metrics
   - Historical head-to-head data
   - Current tournament context
   - Team and player condition reports

2. **Technical Requirements**:
   - API connection to match data sources
   - Processing pipeline for statistical calculations
   - Templating system for dynamic prompt generation
   - Response parsing and formatting for dashboard integration

3. **Output Format**:
   - Structured JSON for dashboard integration
   - Natural language summaries for viewer presentation
   - Visual elements (charts, heatmaps) based on analysis
   - Confidence scores for predictions

4. **Evaluation Metrics**:
   - Prediction accuracy tracking
   - User engagement with insights
   - Correlation between predictions and actual outcomes
   - Novelty and uniqueness of insights

## Future Enhancements
- Personalization based on user team preferences
- Multi-match simultaneous analysis
- Integration with video highlights
- Tactical visualization enhancements
- Historical comparison with classic World Cup matches
