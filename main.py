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
from selenium.webdriver.remote import webelement

import urllib.request
import datetime, time, requests
from pathlib import Path
from dateutil.relativedelta import relativedelta

class Actions(ActionChains):
    def wait(self, time_s: float):
        self._actions.append(lambda: time.sleep(time_s))
        return self

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class DownloadProject():
    def __init__(self, save_path):
        fpath = os.path.join('C:\\', 'Program Files', 'Geckodriver', 'geckodriver.exe')
        cap = DesiredCapabilities().FIREFOX
        cap["marionette"] = True
        opts = Options()
        opts.log.level = "Info"
        opts.set_preference("browser.download.manager.showWhenStarting", False)
        opts.set_preference(f"browser.download.dir","{save_path}")
        opts.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/vnd.ms-excel,image/jpeg,image/jpg")
        self.driver = webdriver.Firefox(capabilities=cap, executable_path=fpath, options=opts, service_log_path=os.path.join(ROOT_DIR, 'logs'))
        self.action = ActionChains(self.driver)

        self.driver.set_window_size(1200, 1200)
        self.driver.implicitly_wait(20) 

        self.save_path = save_path
        self.project_name = None
        self.months_before = None
        self.months_after = None
        self.include_task_list = None
        self.workspace = None

        self.project_config = configparser.ConfigParser()
        self.project_config.read('project_config.ini')

        self.login()

    def set_project(self, project_name):
        self.project_name = project_name
        
        self.months_before = self.project_config[project_name]['months_before']
        self.months_after = self.project_config[project_name]['months_after']
        self.include_task_list = strtobool(self.project_config[project_name]['include_task_list'])
        self.workspace = self.project_config[project_name]['workspace']
        self.filename = '_'.join([self.workspace, self.project_name, datetime.date.today().strftime('%Y-%m-%d')])

    def _get_start_date(self):
        """
        returns formatted string for start date
        """
        today = datetime.date.today()
        result=today - relativedelta(months=int(self.months_before))
        result = result.strftime('%Y-%m-%d')
        return result
    
    def _get_end_date(self):
        """
        returns formatted string for start date
        """
        today = datetime.date.today()
        result = today + relativedelta(months=int(self.months_after))
        result = result.strftime('%Y-%m-%d')
        return result

        
    def login(self):
        self.driver.get("https://app.instagantt.com/")
        try:
            
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
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.NAME, "email"))).send_keys("REDACTED")
        self.driver.find_element(By.NAME, "password").send_keys("REDACTED") 
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
        project_link = self.driver.find_element(By.XPATH, f"//span[contains(text(),'{self.project_name}')]")
        self.action.move_to_element(project_link)
        self.driver.execute_script("arguments[0].click();", project_link)

        
        zoom_out = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div:nth-child(3) > .toolbar-row > .toolbar-row-icon-container")))
        zoom_in = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".toolbar-group-first-item > .toolbar-row-icon-container")))
        actions = ActionChains(self.driver)
        actions.move_to_element(zoom_out)

        try:
            close = WebDriverWait(self.driver, 4).until(self.driver.find_element(By.CSS_SELECTOR, ".close > .fa"))
            close.click()
            print('closing popup')
        except NoSuchElementException as e:
            print('nothing to close')
            pass
        
        for i in range(0,5):
            actions.click(zoom_out)

        
        print(range(0,int(self.project_config[self.project_name]['zoom_level'])))
        for i in range(0,int(self.project_config[self.project_name]['zoom_level'])):
            print('zoom',i)
            actions.click(zoom_in)
        
        actions.perform()
        
        # 21 | click | linkText=Export & Share | 
        self.driver.find_element(By.LINK_TEXT, "Export & Share").click()
        # 22 | click | linkText=Export as Image & PDF | 
        self.driver.find_element(By.LINK_TEXT, "Export as Image & PDF").click()
        # 23 | click | name=export_range_start | 

        ### set include task list
        if self.include_task_list == True:
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/div[2]/div/div/table/tbody/tr[4]/td[2]/div[1]/label/input').click()
            print('including task list')
        elif self.include_task_list == False:
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/div[2]/div/div/table/tbody/tr[4]/td[2]/div[2]/label/input').click()
            print('excluding task list')



        ### set date
        #click date range
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/div[2]/div/div/table/tbody/tr[5]/td[2]/label[2]/input').click()

        send_date = self._get_start_date()
        date_start = self.driver.find_element(By.NAME, "export_range_start")
        date_start.click()
        date_start.send_keys(Keys.CONTROL + 'a')
        date_start.send_keys(send_date)
        
        send_date = self._get_end_date()
        date_end = self.driver.find_element(By.NAME, "export_range_end")
        date_end.click()
        date_end.send_keys(Keys.CONTROL + 'a')
        date_end.send_keys(send_date)
        date_end.send_keys(Keys.ENTER)

        # 30 | click | linkText=Generate | 
        self.driver.find_element(By.LINK_TEXT, "Generate").click()
        self.driver.find_element(By.LINK_TEXT, "Download").click()
        self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
        
        #select image
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//html//body//img')))
        img = self.driver.find_element_by_xpath('//img')
        src = img.get_attribute('src')
        WebDriverWait(self.driver, 0.5)

        #download using requests lib
        all_cookies = self.driver.get_cookies()
        cookies = {}  
        for s_cookie in all_cookies:
            cookies[s_cookie["name"]]=s_cookie["value"]

        r = requests.get(src,cookies=cookies)
        if r.status_code == 200:
            file = open(os.path.join(self.save_path, self.filename+'.jpg'), "wb")
            file.write(r.content)
            file.close()
            print(f'saved {self.filename} successfully')

        #close image tab
        self.driver.close()
        self.driver.switch_to.window(window_name=self.driver.window_handles[0])

        # close download dialog
        self.driver.find_element(By.XPATH,'//html//body//div[1]//div//div[6]//div[1]//a//h3//i').click()

    def quit(self):
        self.driver.quit()
if __name__ == '__main__':
    print(ROOT_DIR)

    program_config=configparser.ConfigParser()
    program_config.read('program_config.ini')

    if program_config['Paths']['save_directory'][0] == '~':
        save_directory=os.path.expanduser(program_config['Paths']['save_directory'])
    else:
        save_directory=program_config['Paths']['save_directory']

    print('save_directory', save_directory)

    #make save directory if needed
    Path(save_directory).mkdir(parents=True, exist_ok=True)


    project_config= configparser.ConfigParser()
    project_config.read('project_config.ini')
    proj = DownloadProject(save_directory)
    
    for project in project_config:
        
        print(project)
        if project == 'DEFAULT':
            continue
        try:
            proj.set_project(project)
            print ("starting:", proj.project_name)
            proj.download_file()
        except:
            proj.quit()
    
    print('done')
    proj.quit()
    



