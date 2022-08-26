from src.dataset.create_dataset import get_source, parse_detailed_player_ranking
import pandas as pd
import time
import re

START_YEAR = '2015'
END_YEAR = '2023'


def main():
    team_overview = pd.read_parquet('../data/player_overview.parquet', engine='pyarrow')
    player_urls = team_overview['player_link']
    df = pd.DataFrame()
    start_time = time.time()
    for url in player_urls:
        start_date = re.search('startDate=(\d{4}-\d{2}-\d{2})', url).groups(1)[0]
        end_date = re.search('endDate=(\d{4}-\d{2}-\d{2})', url).groups(1)[0]
        player_name = re.search('/stats/players/(\d+)/(.*?)\?', url).groups(1)[1]
        detailed_player_overview_html = get_source(url)
        detailed_player_overview = parse_detailed_player_ranking(detailed_player_overview_html, start_date, end_date, player_name)

        detailed_player_overview_dataframe = pd.DataFrame(
            detailed_player_overview, columns=[
                'start_date', 'end_date', 'player_name', 'rating_2', 'dpr', 'kast', 'impact', 'adr', 'kpr', 'total_kills',
                'headshot_percentage', 'total_deaths', 'damage_per_round', 'grenade_damage_per_round', 'kills_per_round',
                'assists_per_round', 'deaths_per_round', 'saved_by_teammates_per_round', 'saved_teammates_per_round',
                'rating_vs_top_5', 'rating_vs_top_10', 'rating_vs_top_20', 'rating_vs_top_30', 'rating_vs_top_50'
            ])
        df = pd.concat([df, detailed_player_overview_dataframe], axis=0)
        print(f'Completed {start_date} --- {end_date} for {player_name} [==========================] Time: {time.time() - start_time:.2}s')

    df.to_parquet('../data/detailed_player_stats.parquet', engine='pyarrow')


if __name__ == '__main__':
    main()
