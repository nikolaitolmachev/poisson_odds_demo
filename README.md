# Demonstrating the 'poisson_odds'

![Demo 1](https://github.com/nikolaitolmachev/xgnhl/raw/main/Img/screen_0.jpg)

This console application showcases the [poisson_odds](https://github.com/nikolaitolmachev/poisson_odds) library, which calculates probabilities for NHL matches using the Poisson distribution. The application enables comparison of these probabilities with real-world odds from bookmakers to assess potential betting value. Key features include:
1. **Probability calculations based on xG**: Using the 'poisson_odds' library, probability calculations are performed for moneyline and handicap/total lines for each game based on the expected goals of the teams obtained from a [source](https://www.naturalstattrick.com/teamtable.php?sit=5v5&score=all&rate=y&team=all&loc=). xG serves as a metric for team quality.
2. **Integration with real-world bookmaker odds**: The project allows loading actual bookmaker odds for NHL matches.
3. **Comprasion and Analysis**: Comparing probabilities calculated based on the Poisson distribution with probabilities derived from bookmaker odds. This allows for identifying situations where the model suggests a higher probability of an outcome than assessed by the bookmaker, which may indicate a "value bet."
4. **Console Interface**: A simple and intuitive console interface for input, probability calculation, and result comparison.

![Demo 2](https://github.com/nikolaitolmachev/xgnhl/raw/main/Img/screen_1.jpg)

## How to install ?
Python 3.10 is required to run this application.

Clone the repository:
```
https://github.com/nikolaitolmachev/xgnhl.git
```

Upgrade pip:
```
python -m pip install --upgrade pip
```

Install libs:
```
pip install -r requirements.txt
```

## settings.ini
MINIMAL_MATCHES_TO_COUNT - The minimum number of home or away matches a team must have played for their expected goals (xG) data to be included in the calculations. Default: 3.

MODEL_VALUE_DIFFERENCE - The percentage difference threshold between the model's calculated odds and the bookmaker's odds. Only deviations exceeding this threshold are saved to the stats.txt file. Default: 30.

PROXY - The proxy should be specified in the following format: type://login:password@IP:port

USER_AGENT - The user agent string.

## Note: 
This project is a demonstration, so it cannot guarantee anything. GL!