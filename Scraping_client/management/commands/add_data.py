from django.core.management.base import BaseCommand
from Scraping_client.models import Project, Property, PropertyHistory
import pandas as pd
import datetime
from sqlalchemy import create_engine
from Scraping_client.scrapper import scrapper

class Command(BaseCommand):
    help = "A command to scrape data and add to database"

    def handle(self, *args, **options):
        ###################################
        ## YIT Developer Scrapper  ########
        ###################################
        data = scrapper.get_apartment_data() # download YIT data
        apartments = scrapper.parse_apartment_data(data) # Parse YIT properties data

        projects = scrapper.get_project_data()
        pr_list = scrapper.parse_project_data(projects)

        ###################################
        ## Zeleznej Studenke Scrapper  ####
        ###################################
        
        html_page = scrapper.get_rendered_html() # render html and save html source code
        listings_url = scrapper.get_listings(html_page) # get listed properties
        properties = scrapper.get_flat_data(listings_url) # parse properties data 
        #properties.head()

        engine = create_engine("sqlite:///db.sqlite3") #connect to database

        # Import projects        
        csv_file = "Scraping_client/scraped_data/projects.csv"
        df = pd.read_csv(csv_file)
        df.loc[-1] = ['2021-11-29',"kZeleznej"]  # adding a row with project Zeleznej just for testing puposes
        df.to_sql(Project._meta.db_table, if_exists="replace", con=engine, index = False)
        #print(df.head())
        print("Sucess, Projects has been updated!")

        # Import property listings
        csv_file_1 = "Scraping_client/scraped_data/apartments.csv"
        csv_file_2 = "Scraping_client/scraped_data/zelezna_studenka.csv"
        df_1 = pd.read_csv(csv_file_1)
        df_2 = pd.read_csv(csv_file_2)
        final_df = df_1.append(df_2)
        final_df = final_df.reset_index(drop=True)
        final_df.drop(["Unnamed: 0"], axis=1, inplace=True)
        #final_df["updateDate"] = pd.to_datetime(final_df["updateDate"])
        final_df.to_csv("Scraping_client/scraped_data/final.csv")
        final_df.to_sql(Property._meta.db_table, if_exists="replace", con=engine, index = True) # write to database
        print(final_df.info())
        print("Sucess, Properties has been updated!")
        

        hist_status = final_df.copy()
        hist_status.rename(columns={"flatNumber":"flatNumber_id"} ,inplace=True)
        hist_status = hist_status[["updateDate","flatNumber_id","propStatus"]]

        if PropertyHistory.objects.exists():

            # Check last update record vs last update date
            all_entries =  PropertyHistory.objects.all()
            last_entry = all_entries.last()
            last_entry_date = last_entry.updateDate
            last_update_date = pd.to_datetime(hist_status["updateDate"][0])
            ts = last_update_date.date()

            if ts != last_entry_date:
                # Import property history status
                hist_status.to_sql(PropertyHistory._meta.db_table, if_exists="append", con=engine, index = False) # write to database
                print("Property historical status UPDATED!")
            else:
                print("Sucess, no updates for property historical status")
                pass 
        
        else:

            # Firs time import property history status
            hist_status.to_sql(PropertyHistory._meta.db_table, if_exists="append", con=engine, index = False) # write to database
            print("Property historical status UPDATED for first time!")   
            

