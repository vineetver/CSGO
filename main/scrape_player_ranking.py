from src.dataset.create_dataset import get_player_ranking_dates, get_player_ranking_source, parse_player_ranking
import pandas as pd

START_YEAR = '2015'
END_YEAR = '2023'


def main():
    start, end = get_player_ranking_dates(START_YEAR, END_YEAR)
    for start_date, end_date in zip(start, end):
        start_date = str(start_date.strftime('%Y-%m-%d'))
        end_date = str(end_date.strftime('%Y-%m-%d'))
        player_overview_url = f'https://www.hltv.org/stats/players?startDate={start_date}&endDate={end_date}&rankingFilter=Top30'
        player_overview_html = get_player_ranking_source(player_overview_url)
        

if __name__ == '__main__':
    main()
