# career_dash_board
## Video Link
https://www.youtube.com/watch?v=HaqIjDyaFfk

## Instructions for Getting Data
Before all: 
- We would use selenium in our scraping
- So please download `chrome driver` for your system and put it in a directory
  - use the link: https://chromedriver.chromium.org/downloads
  - here is the instructions for using chrome driver: https://chromedriver.chromium.org/getting-started
- modify the directory in Service() to be the directory of "chrome driver"

1. Run the `alumini_scraping.py` script to get alumni numbers:
   1. Environment Set-up:
      - run `pip install selenium` or `pip3 install selenium` in your terminal to install selenium
      - run `pip install webdriver_manager` or `pip3 install webdriver_manager` in your terminal to install webdriver_manager
      - other packages are the same, just use `pip install pacakge_name` or `pip3 install pacakge_name`
      - Or, if using the IDE, just click on the red underline, and let the ide install it for you
   3. Get Data:
      - Please just click on the run button for this script to get data (scraping takes long time)
        - Note: please enter your credentials in the script as we indicated by **TODO** to login successfully.
      - Or find the `alumni.csv` directly in the `/data_source` folder in the project

2. Run the `salary_scraping.py` script to get company salary:
   1. Environment Set-up:
      - run `pip install selenium` or `pip3 install selenium` in your terminal to install selenium
      - run `pip install webdriver_manager` or `pip3 install webdriver_manager` in your terminal to install webdriver_manager
      - Or, if using the IDE, just click on the red underline, and let the ide install it for you
   2. Get Data:
      - Please just click on the run button for this script to get data (scraping takes long time)
        - Note: please enter your credentials in the script as we indicated by **TODO** to login successfully.
      - Or find the `company_salary_info.csv` directly in the `/data_source` folder in the project
 
3. Run `scraping_google&amazon.py`, `scraping_meta.py`, `scraping_microsoft.py` to get interview questions:
   1. Environment Set-up:
      - download `chrome driver` for your system and put it in a directory
        - use the link: https://chromedriver.chromium.org/downloads
      - modify the directory in Service() to be the directory of "chrome driver"
      - run `pip install selenium` or `pip3 install selenium` in your terminal to install selenium
      - run `pip install webdriver_manager` or `pip3 install webdriver_manager` in your terminal to install webdriver_manager
      - other packages are the same, just use `pip install pacakge_name` or `pip3 install pacakge_name`
      - Or, if using the IDE, just click on the red underline, and let the ide install it for you
   2. Get Data:
      - Please click on the run button for the three files sequentially.
        - Note: Please enter your Glassdoor credentials as we indicated by **TODO** in the script to login successfully.
      - Or find the `google.csv`, `amazon.csv`, `meta.csv` and `microsoft.csv` directly in the `/data_source` folder in the project. 

4. Run the `leetmodel_model.py` to get leet code data from Api:
   1. Get Data:
      - Please click on the run button for the three files sequentially.
        - Note: Please enter your Leet code credentials as we indicated by **TODO** in the script to login successfully.
        - You may have more leet code credentials to get more data than us
      - Or find the `leetcode_data.csv` directly in the `/data_source` folder in the project. 

## Instructions for Running 
1. Use the IDE like pyCharm and click the run for the `main.py`

