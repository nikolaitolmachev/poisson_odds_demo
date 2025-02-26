import Services.consts as consts

import configparser
from requests_html import AsyncHTMLSession
from lxml import html


class ScraperSlight:
    """
    Static class to get an information from web-page which is not protected.
    """

    @staticmethod
    async def get_xg_data_for_all_teams(asession: AsyncHTMLSession, side='home', PROXY='no') -> dict:
        """
        Gets dict {team_name : (xGF, xGA) } with all teams when played at home or away.

        :param asession: current session.
        :param side: depends on venue.
        :param PROXY: use proxy to get xG data or no.
        :return: dict {team_name : (xGF, xGA) }.
        """

        teams = {}

        config = configparser.ConfigParser()
        config.read('settings.ini')
        MINIMAL_MATCHES_TO_COUNT = int(config['COMMON']['MINIMAL_MATCHES_TO_COUNT'])
        # if need to use proxy to get xG data
        if PROXY == 'yes':
            USER_AGENT = config['COMMON']['USER_AGENT']
            header = {'User-agent': USER_AGENT}
            PROXY_ADRRESS = config['COMMON']['PROXY']
            proxy_list = {
                'https': PROXY_ADRRESS
            }
            asession.proxies.update(proxy_list)
        else:
            header = {'User-agent': consts.USER_AGENT_SHORT}

        # get xG data

        url = consts.XG_SITE_NHL + 'H' if side == 'home' else consts.XG_SITE_NHL + 'A'
        request = await asession.get(url, headers=header)
        # await request.html.arender()
        tree = html.fromstring(request.html.html)

        teams_table = tree.xpath('//table[@id="teams"]/tbody/tr')
        for elem in teams_table:
            xGF, xGA = 0.0, 0.0
            team_name = elem.xpath('./td[@class="lh"]/text()')[0]
            games_played = int(elem.xpath('./td[3]/text()')[0])
            if games_played >= MINIMAL_MATCHES_TO_COUNT:
                xGF = float(elem.xpath('./td[23]/text()')[0])
                xGA = float(elem.xpath('./td[24]/text()')[0])
                teams[team_name] = (xGF, xGA)

        return teams