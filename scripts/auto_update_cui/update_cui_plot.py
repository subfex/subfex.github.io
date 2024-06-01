# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %% historical csv file
csv_file = 'scripts/auto_update_cui/data/UpwellingIndex_36N_historical_1996-present.csv'
dfh = pd.read_csv(csv_file, skiprows=[1], parse_dates=[0])

# %% recent csv file
recent_csv_file = 'scripts/auto_update_cui/data/upwell_122W_36N.txt'
with open(recent_csv_file) as f:
    flines = f.readlines()
headeri = [i for i, line in enumerate(flines) if 'VARIABLE : UPWELLING_INDEX' in line]

nskip = headeri[-1] + 8
dfr = pd.read_csv(recent_csv_file, skiprows=nskip, delim_whitespace=True, 
                  skipinitialspace=True, names=['date', 'time', '/', 'count', 'upwelling_index'],
                  parse_dates=[[0,1]], date_parser=lambda x: pd.to_datetime(x, utc=True))

dfr = dfr.rename(columns={'date_time':'time'})
dfr = dfr.drop(columns = ['/', 'count'])

# %% Concatenate historical and recent

df = pd.concat([dfh, dfr], ignore_index=True)
pd.to_datetime(df['time'])

# %% Loop through years and add CUI to dataframe

df['year'] = df['time'].dt.year
df['yearday'] = df['time'].dt.dayofyear
df['cui'] = np.nan*df['upwelling_index'].copy()

allyears = np.unique(df['year'])
for i, year in enumerate(allyears):
    yearstart = np.datetime64(str(year)+'-01-01')
    tstart = np.datetime64(str(year)+'-01-15')
    tend = np.datetime64(str(year+1)+'-01-01')

    yi = (df['time'].dt.date >= yearstart) & (df['time'].dt.date < tend)
    ii = (df['time'].dt.date >= tstart) & (df['time'].dt.date < tend)
    dfsub = df[ii]
    
    dfsub['upwelling_index']
    # t = dfsub['time'] - dfsub.iloc[0]['time']

    cuisub = dfsub['upwelling_index'].interpolate().cumsum()
    df.loc[cuisub.index, 'cui'] = cuisub

# %% Make plot
plt.figure(figsize=(6,3))

n = len(allyears)
colors = plt.cm.Greys(np.linspace(0,1,n+6))

for i, year in enumerate(allyears):
    dfp = df[df['year'] == year]
    plt.plot(dfp['yearday'], dfp['cui'], '-', color=colors[i+6])
    plt.xlim([0,366])

plt.plot(dfp['yearday'], dfp['cui'], '-', color='r', label=str(year))
plt.xlabel('yearday')
plt.ylabel('CUI [m$^2$/s/100m]')
plt.title('cumulative upwelling index - 36N\n'+
            str(allyears[0])+'-'+str(allyears[-1])+', darker = more recent')
plt.tight_layout()
plt.savefig('scripts/auto_update_cui/figures/cui_36N_updated.png', dpi=1000)
