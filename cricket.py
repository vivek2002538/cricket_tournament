# Cricket Tournament Points Table and Net Run Rate Calculator
def overs_to_float(overs, balls):
    return overs + (balls / 6)

def get_adjusted_overs(overs, balls, wickets):
    actual_overs = overs_to_float(overs, balls)

    # If team is all out before 20 overs, count as full 20 overs
    if wickets == 10 and actual_overs < 20:
        return 20.0
    return actual_overs

def calculate_nrr(team):
    if team["overs_faced"] == 0 or team["overs_bowled"] == 0:
        return 0.0
    run_rate_scored = team["runs_scored"] / team["overs_faced"]
    run_rate_conceded = team["runs_given"] / team["overs_bowled"]
    return run_rate_scored - run_rate_conceded

def validate_team_name(name, existing_teams):
    if name.strip() == "":
        return False
    if name in existing_teams:
        return False
    return True

def validate_match_data(runs, wickets, overs, balls):
    if runs < 0:
        return False
    if wickets < 0 or wickets > 10:
        return False
    if overs < 0 or overs > 20:
        return False
    if balls < 0 or balls > 5:
        return False
    if overs == 20 and balls > 0:
        return False
    return True

def display_points_table(teams):
    standings = []
    for team_name, data in teams.items():
        nrr = calculate_nrr(data)
        standings.append({
            "team": team_name,"played": data["played"],"won": data["won"],"lost": data["lost"],"tied": data["tied"],"points": data["points"],"runs_scored": data["runs_scored"],"runs_given": data["runs_given"],"overs_faced": data["overs_faced"],"overs_bowled": data["overs_bowled"],"nrr": nrr})

    standings.sort(
        key=lambda team: (team["points"], team["nrr"]),
        reverse=True
    )

    print("\n" + "=" * 150)
    print("FINAL TOURNAMENT STANDINGS")
    print("=" * 150)

    print(f"{'Pos':<5}"f"{'Team':<20}"f"{'Played':<10}"f"{'Won':<8}"f"{'Lost':<8}"f"{'Tied':<8}"f"{'Points':<10}"f"{'Runs Scored':<15}"f"{'Runs Given':<15}"f"{'Overs Faced':<15}"f"{'Overs Bowled':<15}"f"{'NRR':<10}")

    position = 1

    for team in standings:
        print(f"{position:<5}"f"{team['team']:<20}"f"{team['played']:<10}"f"{team['won']:<8}"f"{team['lost']:<8}"f"{team['tied']:<8}"f"{team['points']:<10}"f"{team['runs_scored']:<15}"f"{team['runs_given']:<15}"f"{team['overs_faced']:<15.2f}"f"{team['overs_bowled']:<15.2f}"f"{team['nrr']:<10.3f}")
        position += 1

# -------------------- TEAM REGISTRATION --------------------
while True:
    try:
        number_of_teams = int(input("Enter number of teams: "))

        if number_of_teams < 2:
            print("Minimum 2 teams are required.")
            continue
        break
    except ValueError:
        print("Please enter a valid number.")
teams = {}

for team_number in range(1, number_of_teams + 1):

    while True:
        team_name = input(f"Enter Team {team_number} Name: ").strip()

        if not validate_team_name(team_name, teams):
            print("Invalid or duplicate team name.")
            continue

        teams[team_name] = {"played": 0,"won": 0,"lost": 0,"tied": 0,"points": 0,"runs_scored": 0,"runs_given": 0,"overs_faced": 0.0,"overs_bowled": 0.0}
        break

# -------------------- MATCH CALCULATION --------------------
required_matches = number_of_teams * (number_of_teams - 1)
pair_match_count = {}
completed_matches = 0
while completed_matches < required_matches:
    print("\n")
    print("=" * 60)
    print(f"Enter Details For Match {completed_matches + 1}")
    print("=" * 60)
    match_number = completed_matches + 1
    team_one = input("Enter First Team Name: ").strip()
    team_two = input("Enter Second Team Name: ").strip()

    if team_one not in teams:
        print("First team does not exist.")
        continue

    if team_two not in teams:
        print("Second team does not exist.")
        continue

    if team_one == team_two:
        print("A team cannot play against itself.")
        continue
    pair = tuple(sorted([team_one, team_two]))

    if pair not in pair_match_count:
        pair_match_count[pair] = 0

    if pair_match_count[pair] >= 2:
        print("These teams have already played twice.")
        continue
    try:
        team_one_runs = int(input("First Team Runs: "))
        team_one_wickets = int(input("First Team Wickets Lost: "))
        team_one_overs = int(input("First Team Completed Overs: "))
        team_one_balls = int(input("First Team Remaining Balls (0-5): "))

        team_two_runs = int(input("Second Team Runs: "))
        team_two_wickets = int(input("Second Team Wickets Lost: "))
        team_two_overs = int(input("Second Team Completed Overs: "))
        team_two_balls = int(input("Second Team Remaining Balls (0-5): "))

    except ValueError:
        print("Invalid numeric input.")
        continue

    team_one_valid = validate_match_data(team_one_runs,team_one_wickets,team_one_overs,team_one_balls)

    team_two_valid = validate_match_data(team_two_runs,team_two_wickets,team_two_overs,team_two_balls)

    if not team_one_valid or not team_two_valid:
        print("Invalid match data entered.")
        continue
    team_one_adjusted_overs = get_adjusted_overs(team_one_overs,team_one_balls,team_one_wickets)
    team_two_adjusted_overs = get_adjusted_overs(team_two_overs,team_two_balls, team_two_wickets)

    teams[team_one]["played"] += 1
    teams[team_two]["played"] += 1
    teams[team_one]["runs_scored"] += team_one_runs
    teams[team_one]["runs_given"] += team_two_runs
    teams[team_two]["runs_scored"] += team_two_runs
    teams[team_two]["runs_given"] += team_one_runs
    teams[team_one]["overs_faced"] += team_one_adjusted_overs
    teams[team_one]["overs_bowled"] += team_two_adjusted_overs
    teams[team_two]["overs_faced"] += team_two_adjusted_overs
    teams[team_two]["overs_bowled"] += team_one_adjusted_overs

    # Decide Match Result
    if team_one_runs > team_two_runs:
        teams[team_one]["won"] += 1
        teams[team_one]["points"] += 2
        teams[team_two]["lost"] += 1

    elif team_two_runs > team_one_runs:

        teams[team_two]["won"] += 1
        teams[team_two]["points"] += 2
        teams[team_one]["lost"] += 1

    else:
        teams[team_one]["tied"] += 1
        teams[team_two]["tied"] += 1
        teams[team_one]["points"] += 1
        teams[team_two]["points"] += 1

    pair_match_count[pair] += 1
    completed_matches += 1
    print("Match recorded successfully.")

# -------------------- TOURNAMENT VALIDATION --------------------
tournament_complete = True
for team_a in teams:
    for team_b in teams:
        if team_a >= team_b:
            continue
        pair = tuple(sorted([team_a, team_b]))

        if pair_match_count.get(pair, 0) != 2:
            tournament_complete = False
            print(f"{team_a} and {team_b} have not completed exactly two matches.")

if tournament_complete:
    display_points_table(teams)
else:
    print("\nTournament is not complete.")
