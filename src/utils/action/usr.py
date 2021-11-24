# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Action for manipulating user data
import logging
import os
import sys
from enum import Enum

import src.utils.struct.personal_info as pi
import src.utils.struct.reserve_info as ri
import src.utils.utility as ut

logger = logging.getLogger(__name__)


class Action(Enum):
    新增預約 = "1"
    刪除預約 = "2"
    查看預約 = "3"
    查看紀錄 = "4"
    移除資料 = "5"
    離開 = "e"


def action_input_personal_info():
    姓名 = input("病人名稱: ")
    身分證字號 = input("病人身分證字號: ")
    民國年 = input("請輸入出生年 (民國): ")
    西元年 = input("請輸入出生年 (西元): ")
    月 = input("請輸入出生月 (mm): ")
    日 = input("請輸入出生日 (dd): ")

    pis = pi.PersonalInfo_Struct(
        姓名=姓名,
        身分證字號=身分證字號,
        出生年月日=pi.Birth_Struct(
            民國年=民國年,
            西元年=西元年,
            月=月,
            日=日,
        ),
    )
    return pis


def action_check_if_file_exists(path: str) -> bool:
    if os.path.exists(path):
        return True
    return False


def action_check_personal_info(pis, path: str) -> bool:
    real_pis_dict = ut.readYaml(path)
    real_pis = pi.PersonalInfo_Struct(**real_pis_dict)
    return pis == real_pis


def action_add():
    建立日期 = input("請輸入今日日期 (yyy.mm.dd): ")
    醫生名稱 = input("請輸入預約醫生之名稱: ")
    預約日期 = input("請輸入預約看病之日期 (yyy.mm.dd): ")
    預約禮拜 = input("請輸入預約看病之禮拜 (一/二/三/四/五/六/日): ")
    預約時段 = input("請輸入預約看病之時段 (上午/下午): ")

    uds = ri.UnitDataStruct(
        建立日期=建立日期,
        醫生名稱=醫生名稱,
        預約日期=預約日期,
        預約禮拜=預約禮拜,
        預約時段=預約時段,
        資料狀態=ri.狀態.等待預約中.name,
    )
    return uds


def action_delete(ris_filepath: str):
    ris_dict = ut.readYaml(ris_filepath)
    ris = ri.ReserveInfo_Struct(**ris_dict)

    for idx, d in enumerate(ris.掛號預約):
        logger.info(f"idx: {idx}")
        logger.info(d)

    delete_idx = input("請輸入欲刪除之預約編號: ")
    uds = ris.掛號預約[int(delete_idx)]
    uds.資料狀態 = ri.狀態.已取消預約.name

    del ris.掛號預約[int(delete_idx)]

    return ris, uds


def action_lookup(filepath: str):

    if "個人資料" in filepath:
        return ut.yaml2PersonalInfo(filepath)

    if "掛號預約" in filepath:
        return ut.yaml2ReserveInfo(filepath)

    if "掛號紀錄" in filepath:
        return ut.yaml2RecordInfo(filepath)


class ActionProcessor:
    def __init__(self, pis: pi.PersonalInfo_Struct):

        self.pis = pis
        self.usr_dir = os.path.join("usr", pis.姓名)

        self.pis_filepath = os.path.join(self.usr_dir, "個人資料.yaml")
        self.ris_filepath = os.path.join(self.usr_dir, "掛號預約.yaml")
        self.rec_filepath = os.path.join(self.usr_dir, "掛號紀錄.yaml")

        self.mkdirs()
        self.update_status()

    def update_status(self):
        self.pis_status = action_check_if_file_exists(self.pis_filepath)
        self.ris_status = action_check_if_file_exists(self.ris_filepath)
        self.rec_status = action_check_if_file_exists(self.rec_filepath)

    def mkdirs(self):
        os.makedirs(self.usr_dir, exist_ok=True)

    def 檢查個人資料(self):
        if not self.pis_status:
            return False
        return self.pis != action_lookup(self.pis_filepath)

    def 分配器(self, action: str):

        if action == Action.新增預約.value:
            self.新增預約()

        # 2-刪除預約
        elif action == Action.刪除預約.value:
            self.刪除預約()

        # 3-查看預約
        elif action == Action.查看預約.value:
            self.查看預約()

        # 4-查看紀錄
        elif action == Action.查看紀錄.value:
            self.查看紀錄()

        # 5-移除資料
        elif action == Action.移除資料.value:
            self.移除資料()

        # e-離開
        elif action == Action.離開.value:
            self.離開()

        # Unknown Action
        else:
            logger.error(f"未知指令！")

    def 新增預約(self):

        logger.info(f"您選擇 {Action.新增預約.value}-{Action.新增預約.name}")

        # 建立新客人的個人資料
        if not self.pis_status:
            logger.info("未在資料庫中找到您的個人資料，在資料庫建立檔案中...")
            ut.writeYaml(data=self.pis.__2dict__(), outfile=self.pis_filepath)
            logger.info(f"已建立個人資料於 {self.pis_filepath}")

        # 新增的掛號預約資料
        uds = action_add()
        logger.info("您輸入的預約資料如下:")
        logger.info(f"{uds}")

        # 建立新客人的掛號預約資料
        if not self.ris_status:
            logger.info("未在資料庫中找到您的掛號預約資料，在資料庫建立檔案中...")
            ris = ri.ReserveInfo_Struct(掛號預約=[uds])
            ut.writeYaml(data=ris.__2dict__(), outfile=self.ris_filepath)
            logger.info(f"已建立掛號預約資料於 {self.ris_filepath}")

        # 舊客人在線等的預約
        else:
            logger.info("在資料庫中找到您的掛號預約資料，讀取資料中...")
            ris = action_lookup(self.ris_filepath)
            ris.掛號預約.append(uds)
            ut.writeYaml(data=ris.__2dict__(), outfile=self.ris_filepath)
            logger.info(f"已新增掛號預約資料於 {self.ris_filepath}")

        # 更新狀態
        self.update_status()

    def 刪除預約(self):

        logger.info(f"您選擇 {Action.刪除預約.value}-{Action.刪除預約.name}")

        # 建立新客人的個人資料
        if not self.pis_status:
            logger.info("未在資料庫中找到您的個人資料，在資料庫建立檔案中...")
            ut.writeYaml(data=self.pis.__2dict__(), outfile=self.pis_filepath)
            logger.info(f"已建立個人資料於 {self.pis_filepath}")

        # 新客人無掛號預約資料
        if not self.ris_status:
            logger.info(f"未在資料庫中找到您的掛號預約資料，請選擇 {Action.新增預約.value}-{Action.新增預約.name}")

        # 舊客人刪除掛號預約
        else:

            ris, uds = action_delete(self.ris_filepath)

            # 刪除後，尚有掛號預約資料
            if ris.掛號預約:
                ut.writeYaml(data=ris.__2dict__(), outfile=self.ris_filepath)

            # 刪除後，無掛號預約資料
            else:
                os.remove(self.ris_filepath)

            # 沒有掛號紀錄資料
            if not self.rec_status:
                logger.info("未在資料庫中找到您的掛號紀錄資料，在資料庫建立檔案中...")
                rec = ri.RecordInfo_Struct(掛號紀錄=[uds])
                ut.writeYaml(data=rec.__2dict__(), outfile=self.rec_filepath)
                logger.info(f"已建立掛號紀錄資料於 {self.rec_filepath}")

            # 有掛號紀錄資料
            else:
                logger.info("在資料庫中找到您的掛號紀錄資料，讀取檔案中...")
                rec = action_lookup(self.rec_filepath)
                rec.掛號紀錄.append(uds)
                ut.writeYaml(data=rec.__2dict__(), outfile=self.rec_filepath)
                logger.info(f"已新增掛號紀錄資料於 {self.rec_filepath}")

        # 更新狀態
        self.update_status()

    def 查看預約(self):

        logger.info(f"您選擇 {Action.查看預約.value}-{Action.查看預約.name}")

        # 建立新客人的個人資料
        if not self.pis_status:
            logger.info("未在資料庫中找到您的個人資料，在資料庫建立檔案中...")
            ut.writeYaml(data=self.pis.__2dict__(), outfile=self.pis_filepath)
            logger.info(f"已建立個人資料於 {self.pis_filepath}")

        # 新客人無掛號預約資料
        if not self.ris_status:
            logger.info(f"未在資料庫中找到您的掛號預約資料，請選擇 {Action.新增預約.value}-{Action.新增預約.name}")

        # 舊客人的掛號預約
        else:
            logger.info("在資料庫中找到您的掛號預約資料，讀取資料中...")
            ris = action_lookup(self.ris_filepath)
            logger.info("您的預約記錄如下:")
            logger.info(ris)

        # 更新狀態
        self.update_status()

    def 查看紀錄(self):

        logger.info(f"您選擇 {Action.查看紀錄.value}-{Action.查看紀錄.name}")

        # 建立新客人的個人資料
        if not self.pis_status:
            logger.info("未在資料庫中找到您的個人資料，在資料庫建立檔案中...")
            ut.writeYaml(data=self.pis.__2dict__(), outfile=self.pis_filepath)
            logger.info(f"已建立個人資料於 {self.pis_filepath}")

        # 新客人無掛號紀錄資料
        if not self.rec_status:
            logger.info(f"未在資料庫中找到您的掛號紀錄資料，請選擇 {Action.新增預約.value}-{Action.新增預約.name}")

        # 舊客人的掛號紀錄
        else:
            logger.info("在資料庫中找到您的掛號紀錄資料，讀取資料中...")
            rec = action_lookup(self.rec_filepath)
            logger.info("您的預約記錄如下:")
            logger.info(rec)

        # 更新狀態
        self.update_status()

    def 移除資料(self):

        logger.info(f"您選擇 {Action.移除資料.value}-{Action.移除資料.name}")
        if self.pis_status:
            os.remove(self.pis_filepath)
        if self.ris_status:
            os.remove(self.ris_filepath)
        if self.rec_status:
            os.remove(self.rec_filepath)

        # 更新狀態
        self.update_status()

    def 離開(self):
        logger.info(f"您選擇 {Action.離開.value}-{Action.離開.name}")

        if not self.pis_status and not self.ris_status and not self.rec_status:
            os.rmdir(self.usr_dir)

        sys.exit()
