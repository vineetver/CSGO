from src.dataset.create_dataset import get_team_ranking_dates, get_team_ranking_source, parse_team_ranking
import pandas as pd
import time

URL = 'https://www.hltv.org/ranking/teams'
START_YEAR = '2015'
END_YEAR = '2023'


def main():
    monday_dates = get_team_ranking_dates(START_YEAR, END_YEAR)
    df = pd.DataFrame()
    start_time = time.time()
    for monday in monday_dates:
        month = str(monday.strftime('%B')).lower()
        day = str(monday.strftime('%d'))
        year = monday.strftime('%Y')
        team_ranking_source = get_team_ranking_source(f'{URL}/{year}/{month}/{day}')
        team_ranking = parse_team_ranking(team_ranking_source, START_YEAR, END_YEAR)

        teams_dataframe = pd.DataFrame(team_ranking, columns=['date', 'rank', 'team', 'players'])
        df = pd.concat([df, teams_dataframe], axis=0)
        print(f'Completed {monday} [==========================] Time: {time.time() - start_time:.2}s')

    df.to_parquet('../data/teams.csv', index=False, engine='pyarrow')


if __name__ == '__main__':
    main()
