from ASOS_Scraper_v2 import ASOS
from Update_ASOS_Cron import Update_ASOS
import os
import pandas as pd

if __name__ == "__main__": 
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
