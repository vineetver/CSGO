from src.dataset.create_dataset import get_player_ranking_dates, get_source, parse_detailed_player_ranking
import pandas as pd
import time

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
        detailed_player_overview_html = get_source(detailed_player_overview_url)
        detailed_player_overview_data = parse_detailed_player_ranking(detailed_player_overview_html)

        return detailed_player_overview_data
        # detailed_player_overview_dataframe = pd.DataFrame(detailed_player_overview_data,
        #                                                   columns=[])
        # df = pd.concat([df, detailed_player_overview_dataframe], axis=0)
        # print(f'Completed {start_date} --- {end_date} [==========================] Time: {time.time() - start_time:.2}s')


if __name__ == '__main__':
    main()
