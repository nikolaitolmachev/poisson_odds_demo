import asyncio
from requests_html import AsyncHTMLSession
from poisson_odds.poisson import Poisson

import Services.consts as consts
from Value.quality import Quality
from Services.scraper_slight import ScraperSlight
from Services.scraper import Scraper
from Value.value import Value


XG_ALL_HOME, XG_ALL_AWAY = None, None

def set_xGs(PROXY='no') -> tuple:
    """
    Sets xGs.

    :param PROXY: use proxy to get xG data or no.
    """

    # get xG data for all teams at home
    # get xG data for all teams in away
    asession = AsyncHTMLSession()
    loop = asyncio.get_event_loop()
    futures = [
        loop.create_task(ScraperSlight.get_xg_data_for_all_teams(asession, PROXY=PROXY)),
        loop.create_task(ScraperSlight.get_xg_data_for_all_teams(asession, side='away', PROXY=PROXY)),
    ]
    results = loop.run_until_complete(asyncio.gather(*futures))
    global XG_ALL_HOME, XG_ALL_AWAY
    XG_ALL_HOME = results[0]
    XG_ALL_AWAY = results[1]

def analyze_all_matches():
    """
    Analyzes all available NHL matches.
    """

    print('=' * 100)

    all_urls_matches = Scraper.get_urls_all_upcoming_matches()

    if all_urls_matches:
        how_many_matches = '1 match was' if len(all_urls_matches) == 1 else f'{len(all_urls_matches)} matches were'
        print(f'Succesfull, {how_many_matches} founded.')
        print('=' * 100)

        # analyze every match by URL
        for url in all_urls_matches:
            analyze_single_match(url)
            print('=' * 100)
    else:
        print(consts.ERROR_NO_UPCOMING_MATCHES_ALL)
        print('=' * 100)

def analyze_single_match(url: str):
    """
    Analyzes a single NHL match.

    :param url: url of a match which need to analyze.
    """

    print('Scraping...')

    nhl_match = Scraper.get_main_data_for_match(url)
    print(nhl_match)

    if nhl_match is not None:
        # if there is some odds (or moneyline, or handicaps, or totals) then work
        # otherwise no sense
        if nhl_match.bookmaker_moneyline is not None or nhl_match.bookmaker_handicaps or nhl_match.bookmaker_totals:

            # set xGs for both
            global XG_ALL_HOME, XG_ALL_AWAY
            xg_home = XG_ALL_HOME.get(nhl_match.team_a.name, (0.0, 0.0))
            xg_away = XG_ALL_AWAY.get(nhl_match.team_b.name, (0.0, 0.0))
            nhl_match.team_a.xGF = xg_home[0]
            nhl_match.team_a.xGA = xg_home[1]
            nhl_match.team_b.xGF = xg_away[0]
            nhl_match.team_b.xGA = xg_away[1]

            # if there are xG data for both teams then work
            # otherwise no sense
            if (nhl_match.team_a.xGF > 0.0 and nhl_match.team_a.xGA > 0.0
                    and nhl_match.team_b.xGA > 0.0 and nhl_match.team_b.xGF > 0.0):

                print('Calculating...')

                # calculate quality of both teams
                quality_home = Quality.calculate(nhl_match.team_a.xGF, nhl_match.team_b.xGA)
                quality_away = Quality.calculate(nhl_match.team_b.xGF, nhl_match.team_a.xGA)
                print(f'Team quality: {quality_home} - {quality_away}')

                # calculate line/odds by user model (Poisson) by team qualities
                poisson = Poisson(quality_home, quality_away)

                # looking for a value
                Value.looking_for_value(nhl_match, poisson)
            else:
                if not nhl_match.team_a.xGF and not nhl_match.team_a.xGA:
                    print(consts.ERROR_NO_XG_DATA_FOR_HOME)
                if not nhl_match.team_b.xGA and not nhl_match.team_b.xGF:
                    print(consts.ERROR_NO_XG_DATA_FOR_AWAY)
        else:
            print(consts.ERROR_NO_ANY_LINES_ODDS_FOR_MATCH)
    else:
        print(consts.EXCEPTION_WITH_SCRAPING_WEB_PAGE)

def main():
    """
    Main function of application.
    """
    print("Welcome to poisson_odds Demo!")

    print("=" * 100)
    proxy = input('Do you want to use proxy to get xG data? Y/N: ')
    proxy = 'yes' if proxy.lower() == 'y' else 'no'

    while True:
        print("=" * 100)
        print("""Choose the next:        
        1 - To analyze all upcoming matches.                          
        2 - To analyze a single match by a URL.
        or another symbol to exit.""")

        choice = input("Your choice = ")

        if choice in ('1', '2'):
            # set xGs
            global XG_ALL_HOME, XG_ALL_AWAY
            if XG_ALL_HOME is None and XG_ALL_AWAY is None:
                try:
                    set_xGs(proxy)
                except requests.exceptions.ConnectionError:
                    print(consts.EXCEPTION_WITH_SCRAPING_WEB_PAGE)
                    return
                except KeyError:
                    print(consts.EXCEPTION_SETTINGS_ERROR)
                    return
            if XG_ALL_HOME is None and XG_ALL_AWAY is None:
                # then banned
                print(consts.EXCEPTION_WITH_SCRAPING_XG_PAGE)
                return

        if choice == '1':
            analyze_all_matches()

        elif choice == '2':
            print('=' * 100)
            url = input("Write a URL of match: ")
            print('=' * 100)
            # check that url is correct
            if consts.NHL_LEAGUE in url:
                analyze_single_match(url)
            else:
                print(consts.ERROR_WRONG_URL)
            print("=" * 100)

        else:
            print("=" * 100)
            print("Bye Bye!")
            break


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print('Something is going wrong: ' + str(ex))