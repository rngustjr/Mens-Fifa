# SQL Queries Design for World Cup 2026 Analytics

## Overview
This document outlines the design for SQL queries that will support data extraction, analysis, and visualization for the FIFA World Cup 2026 analytics project.

## Database Schema Design

### Teams Table
```sql
CREATE TABLE teams (
  team_id VARCHAR(3) PRIMARY KEY,
  team_name VARCHAR(100) NOT NULL,
  confederation VARCHAR(10) NOT NULL,
  fifa_ranking INT,
  world_cup_appearances INT,
  best_finish VARCHAR(50),
  qualified_status VARCHAR(20),
  group_assigned VARCHAR(2)
);
```

### Players Table
```sql
CREATE TABLE players (
  player_id INT PRIMARY KEY,
  full_name VARCHAR(100) NOT NULL,
  team_id VARCHAR(3) REFERENCES teams(team_id),
  position VARCHAR(20),
  club VARCHAR(100),
  age INT,
  caps INT,
  goals INT,
  previous_world_cups INT
);
```

### Coaches Table
```sql
CREATE TABLE coaches (
  coach_id INT PRIMARY KEY,
  full_name VARCHAR(100) NOT NULL,
  team_id VARCHAR(3) REFERENCES teams(team_id),
  nationality VARCHAR(100),
  appointment_date DATE,
  previous_teams TEXT,
  win_percentage DECIMAL(5,2)
);
```

### Matches Table
```sql
CREATE TABLE matches (
  match_id INT PRIMARY KEY,
  stage VARCHAR(50),
  team1_id VARCHAR(3) REFERENCES teams(team_id),
  team2_id VARCHAR(3) REFERENCES teams(team_id),
  team1_score INT,
  team2_score INT,
  match_date TIMESTAMP,
  venue_id INT REFERENCES venues(venue_id),
  attendance INT,
  referee VARCHAR(100)
);
```

### Match_Events Table
```sql
CREATE TABLE match_events (
  event_id INT PRIMARY KEY,
  match_id INT REFERENCES matches(match_id),
  event_type VARCHAR(50),
  event_time INT,
  player_id INT REFERENCES players(player_id),
  team_id VARCHAR(3) REFERENCES teams(team_id),
  additional_info TEXT
);
```

### Venues Table
```sql
CREATE TABLE venues (
  venue_id INT PRIMARY KEY,
  venue_name VARCHAR(100) NOT NULL,
  city VARCHAR(100) NOT NULL,
  country VARCHAR(100) NOT NULL,
  capacity INT,
  latitude DECIMAL(9,6),
  longitude DECIMAL(9,6)
);
```

### Qualification Table
```sql
CREATE TABLE qualification (
  qualification_id INT PRIMARY KEY,
  team_id VARCHAR(3) REFERENCES teams(team_id),
  confederation VARCHAR(10),
  matches_played INT,
  wins INT,
  draws INT,
  losses INT,
  goals_for INT,
  goals_against INT,
  points INT,
  qualified_status VARCHAR(20)
);
```

## Key SQL Queries

### Team Analysis Queries

#### Team Performance History
```sql
SELECT t.team_name, COUNT(m.match_id) as matches_played,
  SUM(CASE WHEN (m.team1_id = t.team_id AND m.team1_score > m.team2_score) OR 
               (m.team2_id = t.team_id AND m.team2_score > m.team1_score) THEN 1 ELSE 0 END) as wins,
  SUM(CASE WHEN m.team1_score = m.team2_score THEN 1 ELSE 0 END) as draws,
  SUM(CASE WHEN (m.team1_id = t.team_id AND m.team1_score < m.team2_score) OR 
               (m.team2_id = t.team_id AND m.team2_score < m.team1_score) THEN 1 ELSE 0 END) as losses
FROM teams t
LEFT JOIN matches m ON t.team_id = m.team1_id OR t.team_id = m.team2_id
WHERE t.team_id = :team_id
GROUP BY t.team_name;
```

#### Team Qualification Journey
```sql
SELECT t.team_name, q.matches_played, q.wins, q.draws, q.losses, 
  q.goals_for, q.goals_against, q.points, q.qualified_status
FROM teams t
JOIN qualification q ON t.team_id = q.team_id
WHERE t.team_id = :team_id;
```

### Player Analysis Queries

#### Top Goal Scorers
```sql
SELECT p.full_name, t.team_name, COUNT(me.event_id) as goals
FROM players p
JOIN teams t ON p.team_id = t.team_id
JOIN match_events me ON p.player_id = me.player_id
WHERE me.event_type = 'goal'
GROUP BY p.full_name, t.team_name
ORDER BY goals DESC
LIMIT 20;
```

#### Player Performance by Position
```sql
SELECT p.position, AVG(p.goals) as avg_goals, AVG(p.caps) as avg_caps
FROM players p
GROUP BY p.position
ORDER BY p.position;
```

### Match Analysis Queries

#### Match Phase Analysis
```sql
SELECT m.match_id, m.team1_id, m.team2_id, 
  COUNT(CASE WHEN me.event_time BETWEEN 0 AND 15 THEN 1 END) as events_0_15,
  COUNT(CASE WHEN me.event_time BETWEEN 16 AND 30 THEN 1 END) as events_16_30,
  COUNT(CASE WHEN me.event_time BETWEEN 31 AND 45 THEN 1 END) as events_31_45,
  COUNT(CASE WHEN me.event_time BETWEEN 46 AND 60 THEN 1 END) as events_46_60,
  COUNT(CASE WHEN me.event_time BETWEEN 61 AND 90 THEN 1 END) as events_61_90
FROM matches m
LEFT JOIN match_events me ON m.match_id = me.match_id
WHERE m.match_id = :match_id
GROUP BY m.match_id, m.team1_id, m.team2_id;
```

#### Head-to-Head Analysis
```sql
SELECT 
  COUNT(m.match_id) as total_matches,
  SUM(CASE WHEN (m.team1_id = :team1_id AND m.team1_score > m.team2_score) OR 
               (m.team2_id = :team1_id AND m.team2_score > m.team1_score) THEN 1 ELSE 0 END) as team1_wins,
  SUM(CASE WHEN (m.team1_id = :team2_id AND m.team1_score > m.team2_score) OR 
               (m.team2_id = :team2_id AND m.team2_score > m.team1_score) THEN 1 ELSE 0 END) as team2_wins,
  SUM(CASE WHEN m.team1_score = m.team2_score THEN 1 ELSE 0 END) as draws
FROM matches m
WHERE (m.team1_id = :team1_id AND m.team2_id = :team2_id) OR 
      (m.team1_id = :team2_id AND m.team2_id = :team1_id);
```

### Qualification Analysis Queries

#### Qualification by Confederation
```sql
SELECT q.confederation, 
  COUNT(CASE WHEN q.qualified_status = 'qualified' THEN 1 END) as qualified_teams,
  AVG(q.points) as avg_points,
  AVG(q.goals_for) as avg_goals_for,
  AVG(q.goals_against) as avg_goals_against
FROM qualification q
GROUP BY q.confederation;
```

#### Qualification Probability
```sql
SELECT t.team_name, q.points, q.matches_played,
  (q.points / (q.matches_played * 3.0)) * 100 as points_percentage,
  CASE 
    WHEN q.qualified_status = 'qualified' THEN 100
    WHEN q.qualified_status = 'eliminated' THEN 0
    ELSE (q.points / (q.matches_played * 3.0)) * 100 -- simplified example
  END as qualification_probability
FROM teams t
JOIN qualification q ON t.team_id = q.team_id
WHERE t.team_id = :team_id;
```

## Implementation Notes

1. These queries will need to be adapted based on the actual database system used
2. Parameterized queries should be used to prevent SQL injection
3. Indexes should be created on frequently queried columns
4. Consider using views for complex, frequently-used queries
5. Performance optimization may be needed for large datasets
6. Additional queries will be developed as specific analysis needs arise
