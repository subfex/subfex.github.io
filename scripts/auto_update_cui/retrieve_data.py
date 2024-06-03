import urllib.request
import urllib

# direct download of recent csv
url = "https://oceanwatch.pfeg.noaa.gov/products/current_gifs/upwell_122W_36N.txt"
file_path = 'scripts/auto_update_cui/data/upwell_122W_36N.txt'
urllib.request.urlretrieve(url, file_path)

# historical csv from ERDDAP
try:
    hist_url = 'https://coastwatch.pfeg.noaa.gov/erddap/tabledap/erdUI366hr.csv?time%2Cupwelling_index%2Cstation_id%2Clatitude%2Clongitude&time%3E=1996-01-01T00%3A00%3A00Z'
    hist_file_path = 'scripts/auto_update_cui/data/UpwellingIndex_36N_historical_1996-present.csv'
    urllib.request.urlretrieve(hist_url, hist_file_path)
except:
    print('*** could not download historical CUI data from ERDDAP ***')