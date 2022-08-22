"""
This file contain functions used to create the dataset for the analysis and model.
"""

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re


def get_monday(start_year: str, end_year: str) -> list:
    """
    This function returns a list of monday dates between the start_year and end_year. Since HLTV team rankings are updated
    every week on monday. The first ever recorded ranking is on 2015-10-26.
    :param start_year: start year of the dataset
    :param end_year: end year of the dataset
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


def get_html(url) -> str:
    """"
    This function receives the html from the url, scrolls down the page and returns the html.
    :param url: url of the page to be scraped
    :return: html of the page
    """

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    return driver.page_source


def parse_team_ranking(html: str, start_date: str, end_date: str) -> list:
    """
    This function receives the html and parses it to return a list of teams and their respective rankings.
    :param html: html of the page
    :return: list of teams and their respective rankings
    """
    soup = BeautifulSoup(html, 'html.parser')
    team_list = soup.findAll("div", class_="ranked-team standard-box")
    pattern = re.compile('\#(\d+)')
    team_ranking = []
    for team in team_list:
        rank = pattern.match(
            team.find("span", class_="position").text).groups(1)[0]
        team_name = team.find("span", class_="name").text
        players = team.findAll("div", class_="rankingNicknames")
        playernames = [names.text for names in players]
        date_range = pd.date_range(start=start_date, end=end_date)
        for date in date_range:
            if pd.to_datetime(pd.Timestamp(year=2015, month=10, day=26)) <= date < pd.to_datetime(pd.Timestamp.now()):
                team_ranking.append([date.strftime('%Y-%m-%d'), team_name, rank, playernames])
    return team_ranking
