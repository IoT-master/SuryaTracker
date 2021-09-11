# SuryaTracker

Building an accruate sunrise/sunset event tracker requires precision timing. This script will obtain a year's worth of the Sun's data and store it as a JSON file

`pip install -r requirements.txt` or `pip3 install -r requirements.txt`

create a file called details.py in the Confidential folder and store the value of the city in the following format

`city = '<YOUR CITY>'`

Your city needs to be in the metro area in your region.

run `python SuryaScraper.py` to get the data needed for the sun data.

This data will be stored in Confidential/Sundata.json.