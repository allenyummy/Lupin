# encoding=utf-8
# Author: Yu-Lun Chiang
# Description:
import logging
from enum import auto
from enum import Enum

from selenium.webdriver.support.ui import Select

from webdriver.factory import WebDriver_Localizers
from webdriver.factory import WebDriverFactory

logger = logging.getLogger(__name__)


class SeAction(Enum):
    註冊 = auto()
    查詢 = auto()


class NTUH:

    """註冊相關"""

    註冊頁面_網址 = "https://reg.ntuh.gov.tw/webadministration/DoctorServiceQueryByDrName.aspx?HospCode=T0&QueryName="
    支援醫生 = ["陳美州", "周文堅", "周博敏"]

    註冊頁面_掛號鈕_XPATH = f"//*[@id='DoctorServiceListInSeveralDaysInput_GridViewDoctorServiceList{ctl}AdminTextShow']"
    註冊頁面_身分證字號_XPATH = "//*[@id='txtIuputID']"
    註冊頁面_勾選身分證字號_XPATH = "//*[@id='radInputNum_0']"
    註冊頁面_出生年月日_年_XPATH = "//*[@id='ddlBirthYear']"
    註冊頁面_出生年月日_月_XPATH = "//*[@id='ddlBirthMonth']"
    註冊頁面_出生年月日_日_XPATH = "//*[@id='ddlBirthDay']"
    註冊頁面_驗證碼圖片_XPATH = "//*[@id='imgVlid']"
    註冊頁面_驗證碼格子_XPATH = "//*[@id='txtVerifyCode']"
    註冊頁面_確認鈕_XPATH = "//*[@id='btnOK']"

    """查詢相關"""

    查詢頁面_網址 = "https://reg.ntuh.gov.tw/webadministration/Query.aspx"

    查詢頁面_勾選身分證字號_XPATH = "//*[@id='UclQueryInput_radInputNum_1']"
    查詢頁面_身分證字號_XPATH = "//*[@id='UclQueryInput_txtIdno']"
    查詢頁面_出生年月日_年_XPATH = "//*[@id='UclQueryInput_ddlBirthYear']"
    查詢頁面_出生年月日_月_XPATH = "//*[@id='UclQueryInput_ddlBirthMonth']"
    查詢頁面_出生年月日_日_XPATH = "//*[@id='UclQueryInput_ddlBirthDay']"
    查詢頁面_驗證碼圖片_XPATH = "//*[@id='UclQueryInput_imgVlid']"
    查詢頁面_驗證碼格子_XPATH = "//*[@id='UclQueryInput_txtVerifyCode']"

    def __init__(self, webdriver: str):

        """Init Webdriver"""
        self.browser = WebDriverFactory(webdriver)

    def get_entrance_of_webpage(self, action: str, pis, ris, rec):

        if action == SeAction.註冊.name:
            pass
        elif action == SeAction.查詢.name:
            pass
        else:
            raise ValueError("Unknown action.")
