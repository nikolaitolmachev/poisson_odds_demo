class Team:
    """
    Describes a sport team.

    :var name: name of team.
    :var xGF: xG_for. Default: 0.0.
    :var xGA: xG_against. Default: 0.0.
    """

    def __init__(self, name: str):
        self.__name = name
        self.__xGF = 0.0
        self.__xGA = 0.0


    @property
    def name(self) -> str:
        return self.__name

    @property
    def xGF(self) -> float:
        return self.__xGF
    @xGF.setter
    def xGF(self, xGF: float):
        self.__xGF = xGF

    @property
    def xGA(self) -> float:
        return self.__xGA
    @xGA.setter
    def xGA(self, xGA: float):
        self.__xGA = xGA

    def __str__(self):
        result_with_xG = f'{self.__name} ({self.__xGF}|{self.__xGA})'
        result_without_xG = f'{self.__name}'
        return result_with_xG if self.__xGF and self.__xGA else result_without_xG