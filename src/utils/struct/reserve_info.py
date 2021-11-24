# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Reserve Information Data Structure
import json
import logging
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from enum import auto
from enum import Enum
from typing import List

logger = logging.getLogger(__name__)


class 禮拜(Enum):
    一 = auto()
    二 = auto()
    三 = auto()
    四 = auto()
    五 = auto()
    六 = auto()
    日 = auto()


class 時段(Enum):
    上午 = auto()
    下午 = auto()


class 狀態(Enum):
    等待預約中 = auto()
    已取消預約 = auto()
    已成功預約 = auto()
    未成功預約 = auto()


@dataclass
class UnitDataStruct:
    """Unit Data Structure"""

    建立日期: str = field(metadata={"help": "建立資料之日期 (yyy.mm.dd)"})
    醫生名稱: str = field(metadata={"help": "預約醫生之名稱"})
    預約日期: str = field(metadata={"help": "預約看病之日期 (yyy.mm.dd)"})
    預約禮拜: 禮拜 = field(metadata={"help": "預約看病之禮拜 (一/二/三/四/五/六/日)"})
    預約時段: 時段 = field(metadata={"help": "預約看病之時段 (上午/下午)"})
    資料狀態: 狀態 = field(metadata={"help": "資料之狀態 (等待預約中/已取消預約/已成功預約/未成功預約)"})

    def __repr__(self) -> str:
        return (
            "\n"
            f"[建立日期]: {self.建立日期}\n"
            f"[醫生名稱]: {self.醫生名稱}\n"
            f"[預約日期]: {self.預約日期}\n"
            f"[預約禮拜]: {self.預約禮拜}\n"
            f"[預約時段]: {self.預約時段}\n"
            f"[資料狀態]: {self.資料狀態}\n"
        )

    def __2json__(self) -> json:
        return json.dumps(
            asdict(self),
            ensure_ascii=False,
            indent=4,
        )

    def __2dict__(self) -> dict:
        return json.loads(self.__2json__())


@dataclass
class RecordInfo_Struct:
    """Record Information Data Structure"""

    掛號紀錄: List[UnitDataStruct] = field(metadata={"help": "掛號紀錄之資料"})

    def __post_init__(self):

        for idx, uds in enumerate(self.掛號紀錄):
            if isinstance(uds, dict):
                self.掛號紀錄[idx] = UnitDataStruct(**uds)

    def __repr__(self) -> str:

        message = f"\n[掛號紀錄]: \n"
        for uds in self.掛號紀錄:
            message += f"{uds}"
        return message

    def __2json__(self) -> json:
        return json.dumps(
            asdict(self),
            ensure_ascii=False,
            indent=4,
        )

    def __2dict__(self) -> dict:
        return json.loads(self.__2json__())


@dataclass
class ReserveInfo_Struct:
    """Reserve Information Data Structure"""

    掛號預約: List[UnitDataStruct] = field(metadata={"help": "掛號預約之資料"})

    def __post_init__(self):

        for idx, uds in enumerate(self.掛號預約):
            if isinstance(uds, dict):
                self.掛號預約[idx] = UnitDataStruct(**uds)

    def __repr__(self) -> str:

        message = f"\n[掛號預約]: \n"
        for uds in self.掛號預約:
            message += f"{uds}"
        return message

    def __2json__(self) -> json:
        return json.dumps(
            asdict(self),
            ensure_ascii=False,
            indent=4,
        )

    def __2dict__(self) -> dict:
        return json.loads(self.__2json__())
