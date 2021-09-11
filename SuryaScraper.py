from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import functools
from Webscraper import CustomChrome
from Confidential import details
from datetime import datetime
import json
from multiprocessing import Pool
from pathlib import Path
from itertools import repeat

def get_padded_month(a_month):
    return datetime.strftime(datetime.strptime(str(a_month), '%m'), '%m')

def get_padded_day(a_day):
    return datetime.strftime(datetime.strptime(str(a_day), '%d'), '%d')


def get_sunrise_sunset_data(city, a_month: int, write_monthly_files=False) -> dict:
    # window.screen.availHeight
    # window.screen.availWidth
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    zero_padded_month = get_padded_month(a_month)
    with CustomChrome(incognito=False) as sun_driver:
        if a_month < current_month:
            current_year += 1
        url = f'https://www.timeanddate.com/sun/usa/{city.lower()}?month={a_month}&year={current_year}'
        sun_driver.browser.get(url)
        if a_month == current_month:
            sun_driver.scroll_and_moves_mouse_to(sun_driver.browser.find_element_by_css_selector('.selected'))
            sun_driver.browser.find_element_by_css_selector('.selected').click()
        sun_driver.browser.find_elements_by_css_selector('tbody tr')
        sun_table = {}
        for idx, each in enumerate(sun_driver.browser.find_elements_by_css_selector('tbody tr')[7:]):        
            raw_row = each.find_elements_by_css_selector('.c')
            if raw_row:
                sunriseset_table = {
                    'Sunrise': raw_row[0].text,
                    'Sunset': raw_row[1].text
                }
                daylength_table = {
                    'Length': raw_row[2].text,
                    'Difference': raw_row[3].text
                }
                astrotw_table = {
                    "Start": raw_row[4].text,
                    "End": raw_row[5].text
                }
                nauttw_table = {
                    "Start": raw_row[6].text,
                    "End": raw_row[7].text
                }
                civtw_table = {
                    "Start": raw_row[8].text,
                    "End": raw_row[9].text
                }            
                solar_noon_table = {
                    'MillionMiles': each.find_elements_by_css_selector(f'.tr.sep')[-1].text,
                    'Time': raw_row[10].text
                }
                sun_table[idx+1] = {
                    'SolarNoon': solar_noon_table,
                    'Sunrise/Sunset': sunriseset_table,
                    'Daylength': daylength_table,
                    'AstronomicalTwilight': astrotw_table,
                    'NauticalTwilight': nauttw_table,
                    'CivilTwilight': civtw_table,
                }
        if write_monthly_files:
            with open(Path.cwd().joinpath(f'Confidential/Sundata-{zero_padded_month}.json'), 'w') as file:
                json.dump(sun_table, file, indent=4)
        return sun_table

def run_with_pool_executor():
    partial_sun = functools.partial(get_sunrise_sunset_data, details.city)
    var = range(1,13)
    with ProcessPoolExecutor() as executor:
        res = list(executor.map(partial_sun, var))
    year_dict = {get_padded_month(each_month): each_month_sun_table for each_month, each_month_sun_table in zip(var, res)}
    with open(Path.cwd().joinpath(f'Confidential/Sundata.json'), 'w') as file:
        json.dump(year_dict, file, indent=4)

def run_with_thread_executor():
    partial_sun = functools.partial(get_sunrise_sunset_data, details.city)
    var = range(1,13)
    with ThreadPoolExecutor() as executor:
        res = list(executor.map(partial_sun, var))
    year_dict = {get_padded_month(each_month): each_month_sun_table for each_month, each_month_sun_table in zip(var, res)}
    with open(Path.cwd().joinpath(f'Confidential/Sundata2.json'), 'w') as file:
        json.dump(year_dict, file, indent=4)        

def run_with_pool():
    my_inputs = [(details.city, x) for x in range(1,13)]
    with Pool() as executor:
        res = list(executor.starmap(get_sunrise_sunset_data, my_inputs))
    year_dict = {get_padded_month(each_month): each_month_sun_table for each_month, each_month_sun_table in zip(my_inputs, res)}
    with open(Path.cwd().joinpath(f'Confidential/Sundata2.json'), 'w') as file:
        json.dump(year_dict, file, indent=4)

def run_with_pool2():
    var = range(1,13)
    with ProcessPoolExecutor() as executor:
        res = list(executor.map(get_sunrise_sunset_data, repeat(details.city), var))
    year_dict = {get_padded_month(each_month): each_month_sun_table for each_month, each_month_sun_table in zip(var, res)}
    with open(Path.cwd().joinpath(f'Confidential/Sundata2.json'), 'w') as file:
        json.dump(year_dict, file, indent=4)

if __name__ == '__main__':
    run_with_pool_executor()




