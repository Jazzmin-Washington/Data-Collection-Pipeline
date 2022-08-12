from ASOS_Scraper_v2 import ASOS
from Update_ASOS_Cron import Update_ASOS
import os
import pandas as pd

if __name__ == "__main__": 
    try:
        ASOS._check_for_previous_scrapes()
        ASOS._choose_gender_and_pages()
        ASOS._user_select_amt_products()
        print("\n Let's do some Set Up for the Scraper...\n")
        print('\n Please enter your aws information when prompted \n')
        ASOS._get_aws_info()
        print('\n Please enter your sql database information when prompted \n')
        ASOS._get_sql_info()

        if ASOS.previous == False:
            ASOS._scrape_website()
            ASOS._s3_data_dump()
            ASOS._postgres_dump() 
        
        else:
            
            ASOS._prev_data_retrieve()
            ASOS._previously_scraped()
            ASOS._scrape_website()
            ASOS._prev_data_append()
            ASOS._s3_data_dump()
            ASOS._postgres_dump() 
    except:
        gender_list = ['M', 'W']
        cred=os.getcwd()
        credentials = pd.read_json(f'{cred}/scrapers/credentials.json', typ='dictionary')
        Update_ASOS._get_credentials()
        os.chdir(Update_ASOS.data_dir)
        for genders in gender_list:
            Update_ASOS.full_item_list = []
            gender = genders
            print(gender)
            Update_ASOS._choose_gender_and_pages()
            print(Update_ASOS.gender)
            Update_ASOS._prev_data_retrieve()
            Update_ASOS._previously_scraped()
            Update_ASOS._scrape_website()
            Update_ASOS._prev_data_append()
            Update_ASOS._s3_data_dump()
            Update_ASOS._postgres_dump()
