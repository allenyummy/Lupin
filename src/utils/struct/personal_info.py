# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Personal Information Data Structure
import json
import logging
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field

logger = logging.getLogger(__name__)


@dataclass
class Birth_Struct:
    """Birth Data Struct"""

    民國年: str = field(metadata={"help": "出生年 (民國)"})
    西元年: str = field(metadata={"help": "出生年 (西元)"})
    月: str = field(metadata={"help": "出生月"})
    日: str = field(metadata={"help": "出生日"})

    def __repr__(self) -> str:
        return (
            f"    [民國年]: {self.民國年}\n"
            f"    [西元年]: {self.西元年}\n"
            f"    [月    ]: {self.月}\n"
            f"    [日    ]: {self.日}\n"
        )

    def __eq__(self, other) -> bool:
        return (
            self.民國年 == other.民國年
            and self.西元年 == other.西元年
            and self.月 == other.月
            and self.日 == other.日
        )


@dataclass
class PersonalInfo_Struct:
    """Personal Information Data Structure"""

    姓名: str = field(metadata={"help": "病人姓名"})
    身分證字號: str = field(metadata={"help": "病人身分證字號"})
    出生年月日: Birth_Struct = field(metadata={"help": "病人出生年月日"})

    def __post_init__(self):
        if isinstance(self.出生年月日, dict):
            self.出生年月日 = Birth_Struct(**self.出生年月日)

    def __repr__(self) -> str:
        return (
            "\n"
            f"[姓名      ]: {self.姓名}\n"
            f"[身分證字號]: {self.身分證字號}\n"
            f"[出生年月日]\n{self.出生年月日}"
        )

    def __eq__(self, other) -> bool:
        return (
            self.姓名 == other.姓名
            and self.身分證字號 == other.身分證字號
            and self.出生年月日 == other.出生年月日
        )

    def __2json__(self) -> json:
        return json.dumps(
            asdict(self),
            ensure_ascii=False,
            indent=4,
        )

    def __2dict__(self) -> dict:
        return json.loads(self.__2json__())
