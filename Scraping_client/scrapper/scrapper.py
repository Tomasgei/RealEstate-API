import requests
import pandas as pd
from datetime import date

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_apartment_data():
    """
    This function scrape data of apartments from website and save it to list
    x = nuber of pages to scrape (paggination)
    """
    url = "https://www.yit.sk/api/v1/productsearch/apartments"

    x = 21 # number of pages to scrape
    flats = []
    for page in range(0,x):
        try: 
            payload = {
                "PageSize": 9,
                "StartPage": page,
                "QueryString": "*",
                "UILanguage": "sk",
                "PageId": 19190,
                "BlockId": 19192,
                "SiteId": "yit.sk",
                "Attrs": ["cmaap"],
                "Fields": None,
                "CacheMaxAge": 0,
                "Filter": {
                    "Field": "Locale",
                    "Value": "sk",
                    "Operator": "Equals",
                    "AndConditions": [
                        {
                            "Field": "ProjectPublish",
                            "Value": True,
                            "Operator": "Equals",
                            "AndConditions": [],
                            "OrConditions": []
                        },
                        {
                            "Field": "IsAvailable",
                            "Value": True,
                            "Operator": "Equals",
                            "AndConditions": [],
                            "OrConditions": []
                        },
                        {
                            "Field": "ProductItemForSale",
                            "Value": True,
                            "Operator": "Equals",
                            "AndConditions": [],
                            "OrConditions": []
                        },
                        {
                            "Field": "AreaIds",
                            "Value": "mksgd37o-p99v-62zn-u28o40qsw92t",
                            "Operator": "Any",
                            "AndConditions": [],
                            "OrConditions": []
                        },
                        {
                            "Field": "BuildingTypeKey",
                            "Value": ["BlockOfFlats", "SemiDetachedHouse", "DetachedHouse", ""],
                            "Operator": "In",
                            "AndConditions": [],
                            "OrConditions": []
                        }
                    ],
                    "OrConditions": []
                },
                "Facet": [],
                "Order": [{"Field": "ReservationStatusIndex"}, {"Field": "CrmId"}]
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
                "Accept": "*/*",
                "Accept-Language": "cs,sk;q=0.8,en-US;q=0.5,en;q=0.3",
                "Referer": "https://www.yit.sk/predaj-bytov?tab=projects",
                "content-type": "application/json",
                "Origin": "https://www.yit.sk",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "same-origin",
                "Sec-Fetch-Site": "same-origin",
                "TE": "trailers"
            }

            response = requests.request("POST", url, json=payload, headers=headers)
            data = response.json()["Hits"]
            flats.append(data)
            print(f"Status code :{response.status_code}, Success!")
            

        except:
        
            print(f"Status code :{response.status_code}, Error, something is wrong!")
            
    
    return flats
def parse_apartment_data(data):
    """
    This function parse and create data frame of apartments 
    from selected data by columns. Save data to .csv file
    """
    # Select columns 
    columns = [
        "UpdateDate",
        "ApartmentNumber",
        "NumberOfRooms",
        "FloorNumber",
        "ApartmentSize",
        "BalconySize",
        "TotalAreaSize",
        "SalesPrice",
        "ReservationStatusKey"
       
    ]

    #rename columns to match Django Model
    new_cols = {"UpdateDate":'updateDate',
        "ApartmentNumber":'flatNumber',
        "NumberOfRooms":'roomsNumber',
        "FloorNumber":'floorsNumber',
        "ApartmentSize":'flatArea',
        "BalconySize":'balconyTerraceArea',
        "TotalAreaSize":'totalArea',
        "SalesPrice":'salesPrice',
        "ReservationStatusKey":'propStatus'
        }

    # define datatypes
    d_types = {'updateDate':"datetime64",
        'flatNumber':"str",
        'roomsNumber':"int64",
        'floorsNumber':"int64",
        'flatArea':"float32",
        'balconyTerraceArea':"float32",
        'totalArea':"float32",
        'salesPrice':"float32",
        'propStatus':"str"}

    features = [] #store flat features
    for index_1 in range(len(data)):
        for index_2 in range(len(data[index_1])):
            
                features_data = data[index_1][index_2]["Fields"]
                filter_none = {k: v for k, v in features_data.items() if v is not None} # delete all None values
                filter_zero = {k: v for k, v in filter_none.items() if v != 0.0} # delete all zero values
                features.append(filter_zero)

        df = pd.json_normalize(features)
        
        today = date.today()    
        df.insert(loc=0, column='UpdateDate', value= today.strftime("%Y-%m-%d"))# add date of update

        clean_data = df.copy()
        clean_data = clean_data[columns]
        clean_data = clean_data.copy()
        clean_data.rename(columns= new_cols, inplace=True)
        clean_data["floorsNumber"] = clean_data["floorsNumber"].str.slice_replace(1, repl="")

        clean_data.astype(dtype=d_types)
        clean_data.to_csv("Scraping_client/scraped_data/apartments.csv",index=False)           

    return clean_data


def get_project_data():
    """
    This function scrape data of developer open projects from website

    """

    url = "https://www.yit.sk/api/v1/productsearch/projects"

    payload = {
        "PageSize": 10,
        "StartPage": 0,
        "QueryString": "*",
        "UILanguage": "sk",
        "PageId": 19190,
        "BlockId": 19192,
        "SiteId": "yit.sk",
        "Attrs": ["cmaap"],
        "Fields": ["_CampaignBadge", "_ConceptBadges", "_ImageUrl", "_NextShowingText", "_Url", "Address", "ApartmentId", "AreaId", "AvailableProductItems", "CoordinatesLatitude", "CoordinatesLongitude", "CrmId", "MarketingArea", "MarketingDescription", "MarketingName", "NameFromCrm", "ProjectAreaMarketingName", "ProjectId", "ProjectShortTitle", "Projects", "ProjectStatusKey", "PromoteProject", "WebProjectStatus", "WebProjectStatusKey", "CmsNumberOfAvailableApartments", "NumberOfApartments", "NumberOfRoomsMin", "NumberOfRoomsMax"],
        "Filter": {
            "Field": "Locale",
            "Value": "sk",
            "Operator": "Equals",
            "AndConditions": [
                {
                    "Field": "ProjectPublish",
                    "Value": True,
                    "Operator": "Equals",
                    "AndConditions": [],
                    "OrConditions": []
                },
                {
                    "Field": "IsAvailable",
                    "Value": True,
                    "Operator": "Equals",
                    "AndConditions": [],
                    "OrConditions": []
                },
                {
                    "Field": "ProductItemForSale",
                    "Value": True,
                    "Operator": "Equals",
                    "AndConditions": [],
                    "OrConditions": []
                },
                {
                    "Field": "AreaIds",
                    "Value": "mksgd37o-p99v-62zn-u28o40qsw92t",
                    "Operator": "Any",
                    "AndConditions": [],
                    "OrConditions": []
                },
                {
                    "Field": "BuildingTypeKey",
                    "Value": ["BlockOfFlats", "SemiDetachedHouse", "DetachedHouse", "", "TownHouse", "Office"],
                    "Operator": "In",
                    "AndConditions": [],
                    "OrConditions": []
                }
            ],
            "OrConditions": []
        },
        "CacheMaxAge": 0,
        "Facet": []
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
        "Accept": "*/*",
        "Accept-Language": "cs,sk;q=0.8,en-US;q=0.5,en;q=0.3",
        "Referer": "https://www.yit.sk/predaj-bytov?tab=apartments&sort=ReservationStatusIndex&order=asc",
        "content-type": "application/json",
        "Origin": "https://www.yit.sk",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "same-origin",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    projects = response.json()["Hits"]
    return projects


def parse_project_data(projects):
    """
    This function parse and create data frame of project
    from selected data by columns. Save data to .csv file
    """
    columns = [
            'UpdateDate',
            'ProjectId',
            ]
    
    project_list = []
    for i in range(len(projects)):
        proj_fields = projects[i]["Fields"]
        project_list.append(proj_fields)
    df = pd.json_normalize(project_list)
    today = date.today()     # get current date 
    df.insert(loc=0, column='UpdateDate', value= today.strftime("%Y-%m-%d"))# add date of update
    clean_data = df.copy()
    clean_data = df[columns]
   
    
    
    clean_data.to_csv("Scraping_client/scraped_data/projects.csv",index=False)
    
    
    return clean_data

def get_rendered_html():
    """
    This function scrap data from dynamic webpage by rendering it 
    and return page source code for next processing
    """
    url = "https://zelezna.sk/ponuka-bytov/"

    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome("C:/Users/tomas/.wdm/drivers/chromedriver/win32/96.0.4664.45/chromedriver.exe")
    driver.get(url) # open url in browser
    html_page = driver.page_source # get rendered page source

    driver.quit() # close browser
    return html_page

def get_listings(html_page):
    """
    This function gets all property listings on homepage
    and return list of urls of all listed properties 
    """

    listings = "elastic-portfolio-item"
    html_soup = BeautifulSoup(html_page, "html.parser") # parse html sources
    flat_listings =  html_soup.find_all("div",listings) # find all "listings class"

    listings_url = []
    # loop trough listings and get listing url
    for flat in flat_listings:
        item = flat.find("a")
        url = item.get("href") 
        listings_url.append(url)
    
    return listings_url

def get_flat_data(listings_url):
    """
    This function collect data for any single property url
    in listings_url list,clean and saves it to csv file and return DataFrame
    """
    property_list = []

    for l in listings_url:

        property_url = l

        r = requests.get(property_url)
        page_source = r.content
        my_soup = BeautifulSoup(page_source, "html.parser")

        # Content CSS classes
        project_title = "row project-title"
        title_2 = "vc_column-inner"
        features_class = "nectar-fancy-ul"
        info_class = "wpb_text_column"


        my_dict = dict()

        # get id 
        project_title = my_soup.find("div",title_2)
        today = date.today()
        my_dict["updateDate"] = today.strftime("%Y-%m-%d")
        try:
            my_dict["flatNumber"] = project_title.h2.text 
        
        except:
            my_dict["flatNumber"] = project_title.h1.text 
            
        # get features, clean and save to dict
        project_features = my_soup.find("div",features_class)
        features = project_features.find_all("li")
        my_dict["roomsNumber"] = int(features[0].text.split(":")[1].replace(" ",""))
        floors_number = str(features[1].text.split(":")[1].replace(" ",""))
        my_dict["floorsNumber"] = int(floors_number.split(".")[0].strip())
        my_dict["flatArea"] = float(features[2].text.split(":")[1].replace(" ","").replace(",","."))
        my_dict["balconyTerraceArea"] = (None if features[3].text.split(":")[1] == "\xa0–" else float(features[3].text.split(":")[1].replace(" ","").replace(",",".")))
        my_dict["totalArea"] = float(features[4].text.split(":")[1].replace(" ","").replace(",","."))
        
        #get status and price for property
        sales_data = my_soup.find_all("div",info_class)
        my_dict["salesPrice"] = (None if len(sales_data[2].h3.text.split(":")[1].replace("€","").strip()) <=1 else float(sales_data[2].h3.text.split(":")[1].replace("\n","").replace("€","").replace(",",".").replace(" ","").strip()))
        my_dict["propStatus"] = sales_data[1].h3.text.split(":")[1].replace("\n","").strip()

        property_list.append(my_dict)

    df = pd.DataFrame.from_dict(property_list)
    df.to_csv("Scraping_client/scraped_data/zelezna_studenka.csv")
    return df