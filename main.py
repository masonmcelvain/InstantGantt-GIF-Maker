import configparser, os
from distutils.util import strtobool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class DownloadProject():
    def __init__(self, project_name):
        self.driver = webdriver.Firefox()
        self.project_name = project_name
        config= configparser.ConfigParser()

        config.read('project_config.ini')
        self.months_before = config[project_name]['months_before']
        self.months_after = config[project_name]['months_after']
        self.include_task_list = strtobool(config[project_name]['include_task_list'])
        self.workspace = config[project_name]['workspace']

    # def download_file


if __name__ == '__main__':
    config= configparser.ConfigParser()
    config.read('project_config.ini')
    
    for project in config:
        proj = DownloadProject(project)
        print (proj.project_name)
