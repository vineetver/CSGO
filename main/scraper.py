from src.dataset.create_dataset import get_team_ranking_dates, parse_team_ranking, get_source, \
    parse_detailed_player_ranking, get_player_ranking_dates, parse_player_ranking
import pandas as pd
import time
import typer
from config import config
from config.config import logger
from pathlib import Path

app = typer.Typer()


@app.command()
def get_team_ranking():
    logger.info('🏁 Starting up scraper for team ranking 🏁')
    monday_dates = get_team_ranking_dates(config.START_YEAR, config.END_YEAR)
    df = pd.DataFrame()
    start_time = time.time()
    for monday in monday_dates:
        month = str(monday.strftime('%B')).lower()
        day = str(monday.strftime('%d'))
        year = monday.strftime('%Y')
        team_ranking_source = get_source(f'{config.TEAM_URL}/{year}/{month}/{day}')
        team_ranking = parse_team_ranking(team_ranking_source, config.START_YEAR, config.END_YEAR)

        teams_dataframe = pd.DataFrame(team_ranking, columns=['date', 'rank', 'team', 'players'])
        df = pd.concat([df, teams_dataframe], axis=0)
        logger.info(f'🕐 Completed {monday} [==========================] Time: {time.time() - start_time:.2}s 🕐')

    df.to_parquet(Path(config.DATA_DIR, 'teams.csv'), index=False, engine='pyarrow')

    logger.info(f'✅ Finished scraping for team ranking and saved data to {Path(config.DATA_DIR, "teams.csv")} ✅')


@app.command()
def get_player_stats():
    logger.info('🏁 Starting up scraper for player ranking 🏁')
    start, end = get_player_ranking_dates(config.START_YEAR, config.END_YEAR)
    df = pd.DataFrame()
    start_time = time.time()
    for start_date, end_date in zip(start, end):
        start_date = str(start_date.strftime('%Y-%m-%d'))
        end_date = str(end_date.strftime('%Y-%m-%d'))
        player_overview_url = f'https://www.hltv.org/stats/players?startDate={start_date}&endDate={end_date}&rankingFilter=Top30'
        player_overview_html = get_source(player_overview_url)
        player_overview_data = parse_player_ranking(player_overview_html)

        player_overview_dataframe = pd.DataFrame(player_overview_data,
                                                 columns=['date_start', 'date_end', 'player_name', 'player_country', 'player_link',
                                                          'team_name',
                                                          'team_link', 'map_number', 'rounds', 'kd_diff', 'kd',
                                                          'rating'])
        df = pd.concat([df, player_overview_dataframe], axis=0)
        logger.info(f'🕐 Completed {start_date} --- {end_date} [==========================] Time: {time.time() - start_time:.2}s 🕐')

    df.to_parquet(Path(config.DATA_DIR, 'player_overview.csv'), index=False, engine='pyarrow')
    logger.info(f'✅ Finished scraping for player ranking and saved data to {Path(config.DATA_DIR, "player_overview.csv")} ✅')


@app.command()
def get_detailed_player_stats():
    logger.info('🏁 Starting up scraper for detailed player ranking 🏁')
    team_overview = pd.read_parquet(Path(config.DATA_DIR, 'player_overview.parquet'), engine='pyarrow')
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
        logger.info(
            f'🕐 Completed {start_date} --- {end_date} for {player_name} [==========================] Time: {time.time() - start_time:.2}s 🕐')

    df.to_parquet(Path(config.DATA_DIR, 'detailed_player_stats.parquet'), index=False, engine='pyarrow')
    logger.info(
        f'✅ Finished scraping for detailed player ranking and saved data to {Path(config.DATA_DIR, "detailed_player_stats.parquet")} ✅')


if __name__ == '__main__':
    app()
