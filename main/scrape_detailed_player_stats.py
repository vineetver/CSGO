import pandas as pd
import time

from src.dataset.create_dataset import get_player_ranking_dates, get_player_ranking_source

START_YEAR = '2015'
END_YEAR = '2023'


def main():
    start, end = get_player_ranking_dates(START_YEAR, END_YEAR)
    df = pd.DataFrame()
    start_time = time.time()
    for start_date, end_date in zip(start, end):
        start_date = str(start_date.strftime('%Y-%m-%d'))
        end_date = str(end_date.strftime('%Y-%m-%d'))
        detailed_player_overview_url = f'https://www.hltv.org/stats/players/2757/guardian?startDate={start_date}&endDate={end_date}&rankingFilter=Top30'
        player_overview_html = get_player_ranking_source(detailed_player_overview_url)
        # player_overview_data = parse_player_ranking(player_overview_html)
        #
        # player_overview_dataframe = pd.DataFrame(player_overview_data,
        #                                          columns=['date_start', 'date_end', 'player_name', 'player_country', 'player_link',
        #                                                   'team_name',
        #                                                   'team_link', 'map_number', 'rounds', 'kd_diff', 'kd',
        #                                                   'rating'])
        # df = pd.concat([df, player_overview_dataframe], axis=0)
        print(f'Completed {start_date} --- {end_date} [==========================] Time: {time.time() - start_time:.2}s')


if __name__ == '__main__':
    main()
