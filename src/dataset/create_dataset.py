"""
This file contain functions used to create the dataset for the analysis and model.
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests
import re


def get_team_ranking_dates(start_year: str, end_year: str) -> list:
    """
    This function returns a list of monday dates between the start_year and end_year. Since HLTV team rankings are updated
    every week on monday. The first ever recorded ranking is on 2015-10-26.
    :param start_year: year to start collecting team rankings
    :param end_year:  year to end collecting team rankings
    :return: list of monday dates
    """
    dates = pd.date_range(start=start_year, end=end_year, freq='W-MON').tolist()
    monday_dates = []
    for monday in dates:
        if pd.to_datetime(pd.Timestamp(year=2015, month=10, day=26)) <= monday < pd.to_datetime(pd.Timestamp.now()):
            monday_dates.append(monday)
        else:
            continue
    return monday_dates


def get_source(url: str) -> bytes:
    """"
    This function reads the html from the url, scrolls down the page and returns the source code for that link.
    :param url: url of the page to be scraped
    :return: html of the page
    """

    source = requests.get(url)
    return source.content


def parse_team_ranking(html: bytes, start_year: str, end_year: str) -> list:
    """
    This function receives the html and parses it to return a list of teams and their respective rankings.
    :param start_year: year to start collecting player rankings
    :param end_year:  year to end collecting player rankings
    :param html: html of the page
    :return: list of teams and their respective rankings
    """
    soup = BeautifulSoup(html, 'html.parser')
    team_list = soup.findAll('div', class_='ranked-team standard-box')
    pattern = re.compile('\#(\d+)')
    team_ranking = []
    dates = get_team_ranking_dates(start_year, end_year)
    for date in dates:
        for team in team_list:
            rank = pattern.match(
                team.find("span", class_='position').text).groups(1)[0]
            team_name = team.find('span', class_='name').text
            players = team.findAll('div', class_='rankingNicknames')
            playernames = [names.text for names in players]
            team_ranking.append([date, rank, team_name, playernames])
    return team_ranking


def get_player_ranking_dates(start_year: str, end_year: str) -> tuple[list, list]:
    """
    This function returns a tuple of pairs of dates for which the player rankings are available each year. For example,
    2015-01-01 and 2015-12-31 are the first and last dates for which the player rankings are available for year 2015.
    :param start_year: year to start collecting player rankings
    :param end_year:  year to end collecting player rankings
    :return: tuple of dates
    """
    start = pd.date_range(start=start_year, end=end_year, freq='MS').tolist()
    end = pd.date_range(start=start_year, end=end_year, freq='M').tolist()
    return start, end


def parse_player_ranking(html: bytes) -> list:
    """
    This function parses the html of the player ranking page and returns a list of players and other various statistics. For example
    player name, rating, K/D ratio, K/D Diff, etc.
    :param html: html of the player ranking page
    :return:
    """
    driver = BeautifulSoup(html, 'html.parser')
    player_overview_stats = driver.find('table', class_='stats-table player-ratings-table')
    player_overview_table_body = player_overview_stats.find('tbody')
    player_overview_table_rows = player_overview_table_body.find_all('tr')
    player_overview_data = []
    for rows in player_overview_table_rows:
        player_col = rows.find_all('td', class_='playerCol')
        for col in player_col:
            player_country = col.find('img').get('alt')
            player_name = col.find('a').text
            player_link = 'https://www.hltv.org' + col.find('a').get('href')
            start_date = re.search('startDate=(\d{4}-\d{2}-\d{2})', player_link).groups(1)[0]
            end_date = re.search('endDate=(\d{4}-\d{2}-\d{2})', player_link).groups(1)[0]

        team_col = rows.find_all('td', class_='teamCol')
        for col in team_col:
            team_name = col.find('img').get('title')
            team_link = col.find('a').get('href')

        maps_played = rows.find_all('td')[2]
        for col in maps_played:
            map_number = col.text

        rounds_played = rows.find_all('td', class_='statsDetail gtSmartphone-only')
        for col in rounds_played:
            rounds = col.text

        kd_diff_col = rows.find_all('td', class_='kdDiffCol won')
        for col in kd_diff_col:
            kd_diff = col.text[1:]

        kd_col = rows.find_all('td', class_='statsDetail')
        for col in kd_col:
            kd = col.text

        rating_col = rows.find_all('td', class_='ratingCol')
        for col in rating_col:
            rating = col.text

        player_overview_data.append([start_date, end_date, player_name, player_country, player_link, team_name,
                                     team_link, map_number, rounds, kd_diff, kd, rating])

    return player_overview_data


def parse_detailed_player_ranking(html: bytes, start_date: str, end_date: str, player_name: str) -> list:
    """
    This function parses the html of the player detailed ranking page and returns a list of players and other various detailed statistics.
    For example player age, DPR, ADR, KAST, etc.
    :param player_name: name of the player
    :param start_date: start date of the player ranking
    :param end_date: end date of the player ranking
    :param url: url of the player detailed ranking page
    :param html: html of the player detailed ranking page
    :return: list of players and other various detailed statistics
    """
    driver = BeautifulSoup(html, 'html.parser')
    advanced_player_stats = []
    summary_data_breakdown_values = [
        value for value in driver.find_all(class_='summaryStatBreakdownDataValue')
    ]

    advanced_data_breakdown_values = [
        value for value in driver.find_all(class_='stats-row')
    ]

    rating_vs_opponents = [
        value for value in driver.find_all(class_='rating-breakdown')
    ]

    rating_2 = summary_data_breakdown_values[0].text
    dpr = summary_data_breakdown_values[1].text
    kast = summary_data_breakdown_values[2].text
    impact = summary_data_breakdown_values[3].text
    adr = summary_data_breakdown_values[4].text
    kpr = summary_data_breakdown_values[5].text

    total_kills = advanced_data_breakdown_values[0].find_all('span')[1].text
    headshot_percentage = advanced_data_breakdown_values[1].find_all('span')[1].text
    total_deaths = advanced_data_breakdown_values[2].find_all('span')[1].text
    damage_per_round = advanced_data_breakdown_values[4].find_all('span')[1].text
    grenade_damage_per_round = advanced_data_breakdown_values[5].find_all('span')[1].text
    kills_per_round = advanced_data_breakdown_values[8].find_all('span')[1].text
    assists_per_round = advanced_data_breakdown_values[9].find_all('span')[1].text
    deaths_per_round = advanced_data_breakdown_values[10].find_all('span')[1].text
    saved_by_teammates_per_round = advanced_data_breakdown_values[11].find_all('span')[1].text
    saved_teammates_per_round = advanced_data_breakdown_values[12].find_all('span')[1].text

    rating_vs_top_5 = rating_vs_opponents[0].find_all('div')[0].text
    rating_vs_top_10 = rating_vs_opponents[1].find_all('div')[0].text
    rating_vs_top_20 = rating_vs_opponents[2].find_all('div')[0].text
    rating_vs_top_30 = rating_vs_opponents[3].find_all('div')[0].text
    rating_vs_top_50 = rating_vs_opponents[4].find_all('div')[0].text

    advanced_player_stats.append(
        [start_date, end_date, player_name, rating_2, dpr, kast, impact, adr, kpr, total_kills, headshot_percentage, total_deaths,
         damage_per_round, grenade_damage_per_round,
         kills_per_round, assists_per_round, deaths_per_round, saved_by_teammates_per_round,
         saved_teammates_per_round, rating_vs_top_5,
         rating_vs_top_10, rating_vs_top_20, rating_vs_top_30, rating_vs_top_50])

    return advanced_player_stats
