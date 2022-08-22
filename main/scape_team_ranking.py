from src.dataset.create_dataset import get_team_ranking_dates, get_team_ranking_source, parse_team_ranking
import pandas as pd

HEADERS = {
    "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15"
}

URL = 'https://www.hltv.org/ranking/teams'
START_YEAR = '2015'
END_YEAR = '2023'


def main():
    monday_dates = get_team_ranking_dates(START_YEAR, END_YEAR)
    df = pd.DataFrame()
    for monday in monday_dates:
        month = str(monday.strftime('%B')).lower()
        day = str(monday.strftime('%d'))
        year = monday.strftime('%Y')

        team_ranking_source = get_team_ranking_source(f'{URL}/{year}/{month}/{day}')
        team_ranking = parse_team_ranking(team_ranking_source, START_YEAR, END_YEAR)

        teams_dataframe = pd.DataFrame(team_ranking, columns=['date', 'team', 'rank', 'players'])
        df = pd.concat([df, teams_dataframe], axis=0)
        print(df)
    df.to_csv('../data/teams.csv', index=False)


if __name__ == '__main__':
    main()
