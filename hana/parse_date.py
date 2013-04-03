import pandas as pd
from pandas import DataFrame, Series
from datetime import datetime
import sys

def parse_date(dt):
    _dt = None
    try:
        _dt = datetime.strptime(str(dt),"%Y%m%d%H%M%S")
    except ValueError:
        pass
    return _dt

args = sys.argv
df = pd.read_csv(args[1])
df['Closed On'] = df['Closed On'].apply(parse_date)
df['Created On'] = df['Created On'].apply(parse_date)
df['Changed On'] = df['Changed On'].apply(parse_date)

i = df.columns
i = i.map(str.upper)
df.columns = i

df.to_csv('2012_Messages_parsed.csv', index=False)