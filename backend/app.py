from flask import Flask, jsonify, request # type: ignore
from flask_cors import CORS # type: ignore
import pandas as pd # type: ignore
from nba_api.stats.static.teams import get_teams # type: ignore
from nba_api.stats.endpoints import teamyearbyyearstats # type: ignore
import json
from math import sqrt

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8080"],  # Vue.js 開發伺服器的位置
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

@app.route('/api/nba-teams', methods=['GET'])
def get_nba_teams_stats():
    try:
        with open('./data/nba_team.json') as f:
            nba_data = json.load(f)

        formatted_data = []
        
        # 遍歷每個球隊的每個賽季
        for team, seasons in nba_data.items():
            for season, players in seasons.items():
                # 計算該賽季所有球員的總和
                total_defense = sum(
                    player['defensive_rebounds'] + 
                    player['steals'] + 
                    player['blocks']
                    for player in players
                )
                
                total_offense = sum(
                    player['points']
                    for player in players
                )
                
                formatted_data.append({
                    'team': team,
                    'season': season,
                    'total_defense': total_defense,
                    'total_offense': total_offense
                })
        
        return jsonify({
            "status": "success",
            "data": formatted_data
        })
        
    except Exception as e:
        print("Error:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/nba-stats', methods=['GET'])
def get_nba_stats():
    try:
        # Read the JSON data
        df = pd.read_json("./data/nba_data.json")

        # Filter relevant seasons
        all_seasons = ["2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024"]
        team_data = df[df["season"].isin(all_seasons)].copy()

        # Calculate three-point scores
        team_data['three_points'] = team_data['three_point_field_goals_made'] * 3

        # Group data by team and season
        grouped = team_data.groupby(["team", "season"]).agg(
            total_points=('points', 'sum'),
            three_points=('three_points', 'sum')
        ).reset_index()

        # Convert to dictionary format
        result = grouped.to_dict(orient="records")
        
        return jsonify({
            "status": "success",
            "data": result
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
        
@app.route('/api/teams', methods=['GET'])
def get_teams_list():
    try:
        teams = get_teams()
        return jsonify({
            "status": "success",
            "data": teams
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/team-stats', methods=['GET'])
def get_team_stats():
    try:
        # 從 query string 獲取 team_ids
        team_ids_str = request.args.get('team_ids', '')
        team_ids = team_ids_str.split(',') if team_ids_str else []
        
        if not team_ids:
            return jsonify({
                "status": "error",
                "message": "No teams selected"
            }), 400

        selected_data = []
        for team_id in team_ids:
            try:
                stats = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id)
                team_stats_df = stats.get_data_frames()[0]
                
                filtered_df = team_stats_df[
                    (team_stats_df['YEAR'] >= '2018-19') & 
                    (team_stats_df['YEAR'] <= '2023-24')
                ]

                for _, row in filtered_df.iterrows():
                    selected_data.append({
                        'team': row['TEAM_NAME'],
                        'season': row['YEAR'],
                        'total_points': row['PTS'],
                        'three_points': row.get('FG3M', 0) * 3,
                        'blocks': row['BLK'],
                        'steals': row['STL'],
                        'defensive_rebounds': row['DREB']
                    })
            except Exception as e:
                print(f"Error fetching stats for team ID {team_id}: {e}")

        return jsonify({
            "status": "success",
            "data": selected_data
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)