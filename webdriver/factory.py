# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Factory to create webdriver
import logging
import os

from selenium import webdriver

logger = logging.getLogger(__name__)


WebDriver_Localizers = {
    "chrome": webdriver.Chrome(os.path.join("webdriver", "chrome", "chromedriver")),
    # "edge": webdriver.Edge(os.path.join("webdriver", "edge", "edgedriver")),
    # "firefox": webdriver.Firefox(os.path.join("webdriver", "firefox", "firefoxdriver")),
    # "ie": webdriver.Ie(os.path.join("webdriver", "ie", "iedriver")),
    # "safari": webdriver.Safari(os.path.join("webdriver", "safari", "safaridriver")),
}


def WebDriverFactory(name: str):
    return WebDriver_Localizers[name]
