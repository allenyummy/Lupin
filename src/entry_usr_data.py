# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Entry
import logging

import src.utils.action.usr as ac_usr

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M",
)
logger = logging.getLogger(__name__)


def main():

    logger.info("Welcome to Lupin !!")

    """Get Personal Info"""
    pis = ac_usr.action_input_personal_info()
    logger.info("您輸入的個人資料如下:")
    logger.info(f"{pis}")

    """Init Action Processor"""
    ap = ac_usr.ActionProcessor(pis=pis)

    """Check Personal Info"""
    while ap.檢查個人資料():
        logger.info("Wrong personal info. Please type in again.")
        pis = ac_usr.action_input_personal_info()
        logger.info("您輸入的個人資料如下:")
        logger.info(f"{pis}")
        ap.pis = pis

    while True:

        """Action Input"""
        action = input(
            f"******************\n"
            f"今日預辦業務為: \n"
            f"{ac_usr.Action.新增預約.value}-{ac_usr.Action.新增預約.name}\n"
            f"{ac_usr.Action.刪除預約.value}-{ac_usr.Action.刪除預約.name}\n"
            f"{ac_usr.Action.查看預約.value}-{ac_usr.Action.查看預約.name}\n"
            f"{ac_usr.Action.查看紀錄.value}-{ac_usr.Action.查看紀錄.name}\n"
            f"{ac_usr.Action.移除資料.value}-{ac_usr.Action.移除資料.name}\n"
            f"{ac_usr.Action.離開.value}-{ac_usr.Action.離開.name}\n"
            f"******************\n"
            "請輸入數字: "
        )

        """ Process Action """
        ap.分配器(action)


if __name__ == "__main__":
    main()
