import re
from datetime import datetime
from functions.regexPatterns import DATE_FIND_PATTERN, DATE_FORMAT_PATTERNS, DATE_CLEAN_PATTERN, SPORT_SEPARATOR_PATTERN, WHITESPACE_PATTERN

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
    if not year:
        return None
    if isinstance(year, str):
        year = year.split("-")[0]
    if year and year != "None":
        return int(year)

def cleanDate(date_str: str | None) -> str | None:
    """
    Extracts and returns a standardized date (YYYY.MM.DD) from various formats,
    automatically resolving ambiguous day/month orders (US-style by default).
    """
    if not date_str:
        return None

    cleaned = str(date_str).strip()
    if not cleaned:
        return None

    for pattern, format_type in DATE_FORMAT_PATTERNS:
        match = pattern.fullmatch(cleaned)
        if not match:
            continue

        groups = match.groups()
        year = month = day = None

        try:
            if format_type in ('DD.MM.YYYY', 'DD-MM-YYYY', 'DD/MM/YYYY'):
                day, month, year = map(int, groups)
            elif format_type in ('MM.DD.YYYY', 'MM/DD/YYYY', 'MM-DD-YYYY'):
                month, day, year = map(int, groups)
            elif format_type in ('YYYY-MM-DD', 'YYYY/MM/DD', 'YYYY.MM.DD'):
                year, month, day = map(int, groups)

            # Automatic ambiguity resolution (US-style default)
            if format_type in ('DD.MM.YYYY', 'DD/MM/YYYY', 'DD-MM-YYYY', 
                               'MM.DD.YYYY', 'MM/DD/YYYY', 'MM-DD-YYYY'):
                if day <= 12 and month <= 12:
                    # Try both interpretations
                    try:
                        dt_us = datetime(year, month, day)      # US-style
                        dt_eu = datetime(year, day, month)      # European-style
                        dt = dt_us  # Pick US-style by default
                    except ValueError:
                        # If one fails, fallback to the other
                        try:
                            dt = datetime(year, day, month)
                        except ValueError:
                            continue
                else:
                    dt = datetime(year, month, day)
            else:
                dt = datetime(year, month, day)

            return dt.strftime('%Y.%m.%d')

        except (ValueError, TypeError):
            continue

    return None

def detectSports(file_name_no_ext: str):
    file_name_no_ext = file_name_no_ext.strip()

    # Step 1: Extract ANY date in the string (start, middle, end)
    date_match = DATE_FIND_PATTERN.search(file_name_no_ext)
    if not date_match:
        return None
    potential_date = date_match.group(1)
    cleaned_date = cleanDate(potential_date)
    if not cleaned_date:
        return None

    # Step 2: Remove the date from the string
    file_no_date = DATE_FIND_PATTERN.sub('', file_name_no_ext).strip()
    # Clean extra whitespace
    file_no_date = WHITESPACE_PATTERN.sub(' ', file_no_date).strip()

    # Step 3: Find the separator
    separator_match = SPORT_SEPARATOR_PATTERN.search(file_no_date)
    if not separator_match:
        return None

    sport_separator = separator_match.group(0).strip()

    # Split on separator
    parts = SPORT_SEPARATOR_PATTERN.split(file_no_date, maxsplit=1)
    if len(parts) != 3:
        return None

    team_1 = parts[0].strip()
    team_2 = parts[2].strip()  # parts[1] is the separator

    if not team_1 or not team_2:
        return None

    return {
        "type": "sports",
        "date": cleaned_date,
        "sport_separator": sport_separator,
        "team_1": team_1,
        "team_2": team_2
    }