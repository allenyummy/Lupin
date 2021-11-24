# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Auto booking
import argparse
import logging
import os

from selenium.webdriver.support.ui import Select

from config.ntuh import NTUH_Check_URL
from src.utils.action.usr import action_lookup
from src.utils.captcha import resolve_captcha_from_bytes
from webdriver.factory import WebDriver_Localizers
from webdriver.factory import WebDriverFactory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M",
)
logger = logging.getLogger(__name__)


def parse_args():

    parser = argparse.ArgumentParser(
        description="Confirm whether the appointment is successful",
    )
    parser.add_argument(
        "-pi",
        "--personal_info_filepath",
        type=str,
        help="User personal information filepath",
    )
    parser.add_argument(
        "-wd",
        "--webdriver",
        type=str,
        default="chrome",
        choices=list(WebDriver_Localizers.keys()),
        help=f"Determine which web driver would be instantiated. {list(WebDriver_Localizers.keys())}",
    )

    # parser.add_argument(
    #     "-o",
    #     "--output_file",
    #     type=str,
    #     help="store data into output file.",
    # )
    # parser.add_argument(
    #     "-c",
    #     "--cache_file",
    #     type=str,
    #     help="get data from a cache file.",
    # )
    args = parser.parse_args()
    return args


def main():

    """Args"""
    args = parse_args()
    logger.info(f"ARGS: {args}\n")

    """Usr Data"""
    pis = action_lookup(args.personal_info_filepath)

    """Init Webdriver"""
    browser = WebDriverFactory(args.webdriver)

    """Get Entrance of Webpage"""
    browser.get(NTUH_Check_URL)

    """Find Element and Send Information"""
    勾選身分證字號 = browser.find_element_by_xpath("//*[@id='UclQueryInput_radInputNum_1']")
    勾選身分證字號.click()

    身分證字號 = browser.find_element_by_xpath("//*[@id='UclQueryInput_txtIdno']")
    身分證字號.send_keys(pis.身分證字號)

    年 = Select(browser.find_element_by_xpath("//*[@id='UclQueryInput_ddlBirthYear']"))
    年.select_by_visible_text(pis.出生年月日.民國年)

    月 = Select(browser.find_element_by_xpath("//*[@id='UclQueryInput_ddlBirthMonth']"))
    月.select_by_visible_text(pis.出生年月日.月)

    日 = Select(browser.find_element_by_xpath("//*[@id='UclQueryInput_ddlBirthDay']"))
    日.select_by_visible_text(pis.出生年月日.日)

    驗證碼圖片 = browser.find_element_by_xpath(
        "//*[@id='UclQueryInput_imgVlid']"
    ).screenshot_as_png
    驗證碼格子 = browser.find_element_by_xpath("//*[@id='UclQueryInput_txtVerifyCode']")
    驗證碼結果 = resolve_captcha_from_bytes(驗證碼圖片)
    驗證碼格子.send_keys(驗證碼結果)

    """Submit"""
    查詢 = browser.find_element_by_xpath("//*[@id='UclQueryInput_btnQuery']")
    查詢.click()

    """Save Captcha Image"""
    驗證碼位址 = f"img/{驗證碼結果}.png"
    with open(驗證碼位址, "wb") as f:
        f.write(驗證碼圖片)
        f.close()

    """Save Screen Shot"""
    browser.get_screenshot_as_file(
        os.path.join(os.path.dirname(args.personal_info_filepath), "screen_shot.png")
    )

    browser.close()


if __name__ == "__main__":
    main()
