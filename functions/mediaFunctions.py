import re
import logging

def constructSeriesTitle(season = None, episode = None, folder: bool = False):
    """
    Constructs a proper title for a series based on the season and episode.

    :param season: The season number or a list of season numbers.
    :param episode: The episode number or a list of episode numbers.
    :param folder: If True, the title will be formatted for a folder name.
    """


    title_season = None
    title_episode = None

    if isinstance(season, list):
        # get first and last season
        title_season = f"S{season[0]:02}-S{season[-1]:02}"
    elif isinstance(season, int) or season is not None:
        if folder:
            title_season = f"Season {season}"
        else:
            title_season = f"S{season:02}"
    
    if isinstance(episode, list):
        # get first and last episode
        title_episode = f"E{episode[0]:02}-E{episode[-1]:02}"
    elif isinstance(episode, int) or episode is not None:
        title_episode = f"E{episode:02}"

    if title_season and title_episode:
        return f"{title_season}{title_episode}"
    elif title_season:
        return title_season
    elif title_episode:
        return title_episode
    else:
        return None
    
def cleanTitle(title: str):
    """
    Removes invalid characters from the title.
    """
    title = re.sub(r"[\/\\\:\*\?\"\<\>\|]", "", title)
    return title

def cleanYear(year: str | int):
    """
    Cleans the year listing which can be a string (2023-2024) or an int (2023).
    """
    try:
        if not year:
            return None
        if isinstance(year, str):
            year = year.split("-")[0]
        if type(year) is int:
            return year
        if year and year != "None":
            if isinstance(year, str):
                year = year.replace("-", "")
                year = year.strip()
                return int(year)
            else:
                return int(year)
        else:
            return None
    except Exception as e:
        logging.error(f"Error cleaning year: {e}")
        return None
