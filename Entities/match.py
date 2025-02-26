import Services.consts as consts
from Entities.team import Team
from poisson_odds.bookmaker_moneyline import BookmakerMoneyline


class NHLMatch:
    """
    Describes a NHL match.

    :var date: date and time of match starting.
    :var team_a: home team of type Team.
    :var team_b: away team of type Team.
    :var url: URL of a NHL match.
    :var bookmaker_moneyline: type BookmakerMoneyline. Default: None.
    :var bookmaker_handicaps: list of type BookmakerHandicap.
    :var bookmaker_totals: list of type BookmakerTotal.
    """

    def __init__(self, date: str, team_a: Team, team_b: Team, url: str, bookmaker_moneyline: BookmakerMoneyline):
        self.__date = date
        self.__team_a = team_a
        self.__team_b = team_b
        self.__url = url

        self.__bookmaker_moneyline = bookmaker_moneyline  # BookmakerMoneyline
        self.__bookmaker_handicaps = []  # list of BookmakerHandicap
        self.__bookmaker_totals = [] # list of BookmakerTotal

    @property
    def date(self):
        return self.__date
    @property
    def team_a(self):
        return self.__team_a
    @property
    def team_b(self):
        return self.__team_b
    @property
    def url(self):
        return self.__url
    @property
    def bookmaker_moneyline(self) -> BookmakerMoneyline:
        return self.__bookmaker_moneyline

    @property
    def bookmaker_handicaps(self) -> list:
        return self.__bookmaker_handicaps
    @bookmaker_handicaps.setter
    def bookmaker_handicaps(self, bookmaker_handicaps: list):
        self.__bookmaker_handicaps = bookmaker_handicaps

    @property
    def bookmaker_totals(self) -> list:
        return self.__bookmaker_totals
    @bookmaker_totals.setter
    def bookmaker_totals(self, bookmaker_totals: list):
        self.__bookmaker_totals = bookmaker_totals

    def __str__(self):
        return '{} {} - {}.'.format(self.__date, self.__team_a, self.__team_b)

    def save_to_stats(self, message: str):
        """
        Writes info to txt file for statistics.

        :param message: description of value.
        """
        result = self.__str__() + '\n' + message + '\n'

        with open(consts.FILE_STATS, 'a', encoding="utf-8") as f:
            f.write(result)
