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


def get_team_ranking_source(url: str) -> str:
    """"
    This function reads the html from the url, scrolls down the page and returns the source code for that link.
    :param url: url of the page to be scraped
    :return: html of the page
    """

    source = requests.get(url)
    return source.content


def parse_team_ranking(html: str, start_year: str, end_year: str) -> list:
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
    start = pd.date_range(start=start_year, end=end_year, freq='YS').tolist()
    end = pd.date_range(start=start_year, end=end_year, freq='Y').tolist()
    return start, end


def get_player_ranking_source(url: str) -> bytes:
    """
    This function reads the html from the , scrolls down the page and returns the source code for that link.
    :param url: url of the page to be scraped
    :return: html of the page
    """

    source = requests.get(url)
    return source.content


def parse_player_ranking(html: bytes):
    """
    This function parses the html of the player ranking page and returns a list of players and other various statistics. For example
    player name, age, rating, K/D ratio, ADR, etc.
    :param html: html of the player ranking page
    :return:
    """
    driver = BeautifulSoup(html, 'html.parser')
    player_list = driver.find('table', class_='stats-table player-ratings-table')
    return player_list
