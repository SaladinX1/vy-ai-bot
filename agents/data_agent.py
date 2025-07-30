# Fichier : agents/data_agent.py

from pytrends.request import TrendReq

def get_trending_niches():
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(["AI", "crypto", "fitness"], timeframe='now 1-d')
    return pytrends.interest_over_time().to_dict()