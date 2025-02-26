import Services.consts as const


class Quality:
    """
    Static class to calculate quality team_1 by xGF_team_1 and xFA_opponent.
    """

    @staticmethod
    def calculate(xGF_team_1: float, xFA_opponent: float) -> float:
        """
        :param xGF_team_1: team for which calculates quality.
        :param xFA_opponent: opponent of team for which calculates quality.
        :return: quality of a team.
        """

        quality = ((const.XG_DIGRESSION_PREFIX * xGF_team_1 + const.XG_DIGRESSION_SUFFIX) *
                   (const.XG_DIGRESSION_PREFIX * xFA_opponent + const.XG_DIGRESSION_SUFFIX)) -1

        return round(quality, 3)