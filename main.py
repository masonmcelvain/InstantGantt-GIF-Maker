import configparser, os
from distutils.util import strtobool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException

import urllib.request
import datetime
from dateutil.relativedelta import relativedelta

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class DownloadProject():
    def __init__(self, save_path):
        fpath = os.path.join('C:\\', 'Program Files', 'Geckodriver', 'geckodriver.exe')
        cap = DesiredCapabilities().FIREFOX
        cap["marionette"] = True
        opts = Options()
        opts.log.level = "debug"
        opts.set_preference("browser.download.manager.showWhenStarting", False)
        opts.set_preference("browser.download.dir","/Data")
        opts.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/vnd.ms-excel")
        self.driver = webdriver.Firefox(capabilities=cap, executable_path=fpath, options=opts, service_log_path=os.path.join(ROOT_DIR, 'logs'))
        self.action = ActionChains(self.driver)

        self.driver.set_window_size(3456, 1416)
        self.driver.implicitly_wait(20) 

        self.save_path = save_path
        self.project_name = None
        self.months_before = None
        self.months_after = None
        self.include_task_list = None
        self.workspace = None

        self.login()

    def set_project(self, project_name):
        self.project_name = project_name
        config= configparser.ConfigParser()

        config.read('project_config.ini')
        self.months_before = config[project_name]['months_before']
        self.months_after = config[project_name]['months_after']
        self.include_task_list = strtobool(config[project_name]['include_task_list'])
        self.workspace = config[project_name]['workspace']
        self.filename = '_'.join([self.workspace, self.project_name, datetime.date.today().strftime('%Y-%m-%d')])

    def _get_start_date(self):
        """
        returns formatted string for start date
        """
        today = datetime.date.today()
        result=today - relativedelta(months=self.months_before)
        result = result.strftime('%Y-%m-%d')
        print(result)
        return result
    
    def _get_end_date(self):
        """
        returns formatted string for start date
        """
        today = datetime.date.today()
        result = today + relativedelta(months=self.months_after)
        result = result.strftime('%Y-%m-%d')
        print(result)
        return result

        
    def login(self):
        self.driver.get("https://app.instagantt.com/")
        try:
            self.driver.set_window_size(1456, 1416)
            
            self.driver.execute_script("scroll(0, 250);")
            login_button = self.driver.find_element_by_css_selector(".line-button-blue")
            WebDriverWait(self.driver, 2)
            self.driver.execute_script("scroll(0, 0);")
            WebDriverWait(self.driver, 2)
            self.action.move_to_element(login_button)
            self.driver.execute_script("arguments[0].click();", login_button)

            # element.click()
        except NoSuchElementException:
            print('login not found!')
            pass
        # 4 | click | css=.solid-button-blue:nth-child(4) |
        
        #go to login from home
        login_button = self.driver.find_element(By.CSS_SELECTOR, ".solid-button-blue:nth-child(4)")
        WebDriverWait(self.driver, 20)
        self.driver.execute_script("arguments[0].click();", login_button)

        #log in page
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.NAME, "email"))).send_keys("***REMOVED***")
        self.driver.find_element(By.NAME, "password").send_keys("***REMOVED***") 
        self.driver.find_element(By.CSS_SELECTOR, ".auth0-label-submit").click()

    def download_file(self):
        # open workspace drop down
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div:nth-child(1) > .fa-caret-down:nth-child(1)")))
        workspace_dropdown = self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .fa-caret-down:nth-child(1)")
        self.driver.execute_script("arguments[0].click();", workspace_dropdown)
        
        # select workspace
        workspace_link = self.driver.find_element(By.XPATH, f"//div[contains(text(),'{self.workspace}')]")
        self.action.move_to_element(workspace_link)

        self.driver.execute_script("arguments[0].click();", workspace_link)

        # select project
        print('project:', self.project_name)
        project_link = self.driver.find_element(By.XPATH, f"//html//body//div[1]//div//div[4]//div[2]//ul//li[5]//div[3]//div//span[contains(text(),'{self.project_name}')]")
        self.action.move_to_element(project_link)
        self.driver.execute_script("arguments[0].click();", project_link)

        # 10 | click | css=.\_32AWpOHuVapfx2jS2omul_:nth-child(5) span | 
        self.driver.find_element(By.CSS_SELECTOR, ".\\_32AWpOHuVapfx2jS2omul_:nth-child(5) span").click()
        # 11 | runScript | window.scrollTo(0,0) | 
        self.driver.execute_script("window.scrollTo(0,0)")
        # 12 | click | css=div:nth-child(3) > .toolbar-row > .toolbar-row-icon-container | 
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) > .toolbar-row > .toolbar-row-icon-container").click()
        # 13 | click | css=div:nth-child(3) > .toolbar-row > .toolbar-row-icon-container | 
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) > .toolbar-row > .toolbar-row-icon-container").click()
        # 14 | click | css=.toolbar-row:nth-child(2) > .toolbar-row-icon-container | 
        self.driver.find_element(By.CSS_SELECTOR, ".toolbar-row:nth-child(2) > .toolbar-row-icon-container").click()
        # 15 | click | css=.toolbar-group-first-item > .toolbar-row-icon-container | 
        self.driver.find_element(By.CSS_SELECTOR, ".toolbar-group-first-item > .toolbar-row-icon-container").click()
        # 16 | runScript | window.scrollTo(0,0) | 
        self.driver.execute_script("window.scrollTo(0,0)")
        # 17 | click | css=div:nth-child(3) > .toolbar-row > .toolbar-row-icon-container | 
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) > .toolbar-row > .toolbar-row-icon-container").click()
        # 18 | click | css=div:nth-child(3) > .toolbar-row > .toolbar-row-icon-container | 
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) > .toolbar-row > .toolbar-row-icon-container").click()
        # 19 | click | css=div:nth-child(3) > .toolbar-row > .toolbar-row-icon-container | 
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) > .toolbar-row > .toolbar-row-icon-container").click()
        # 20 | doubleClick | css=div:nth-child(3) > .toolbar-row > .toolbar-row-icon-container | 
        element = self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) > .toolbar-row > .toolbar-row-icon-container")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        # 21 | click | linkText=Export & Share | 
        self.driver.find_element(By.LINK_TEXT, "Export & Share").click()
        # 22 | click | linkText=Export as Image & PDF | 
        self.driver.find_element(By.LINK_TEXT, "Export as Image & PDF").click()
        # 23 | click | name=export_range_start | 
        self.driver.find_element(By.NAME, "export_range_start").click()
        # 24 | click | name=export_range_start |  
        self.driver.find_element(By.NAME, "export_range_start").click()
        # 26 | type | name=export_range_start | 2021/07/06
        send_date = self._get_start_date()
        self.driver.find_element(By.NAME, "export_range_start").send_keys(str(send_date))
        # 27 | click | name=export_range_end | 
        self.driver.find_element(By.NAME, "export_range_end").click()
        # 28 | type | name=export_range_end | 2021-11-06
        send_date = self._get_end_date()
        self.driver.find_element(By.NAME, "export_range_end").send_keys(str(send_date))
        # 29 | sendKeys | name=export_range_end | ${KEY_ENTER}
        self.driver.find_element(By.NAME, "export_range_end").send_keys(Keys.ENTER)
        # 30 | click | linkText=Generate | 
        self.driver.find_element(By.LINK_TEXT, "Generate").click()
        # 31 | click | linkText=Download | 
        self.driver.find_element(By.LINK_TEXT, "Download").click()
        self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
        
        #select image
        img = self.driver.find_element_by_xpath('//html//body//img')
        src = img.get_attribute('src')
        actions.context_click(img).send_keys('v').perform()


if __name__ == '__main__':
    print(ROOT_DIR)

    program_config=configparser.ConfigParser()
    program_config.read('program_config.ini')

    if program_config['Paths']['save_directory'][0] == '~':
        save_directory=os.path.expanduser(program_config['Paths']['save_directory'])
    else:
        save_directory=program_config['Paths']['save_directory']

    print('save_directory', save_directory)


    project_config= configparser.ConfigParser()
    project_config.read('project_config.ini')
    proj = DownloadProject(save_directory)
    
    for project in project_config:
        
        print(project)
        if project == 'DEFAULT':
            continue
        
        proj.set_project(project)
        print ("starting:", proj.project_name)
        proj.download_file()

