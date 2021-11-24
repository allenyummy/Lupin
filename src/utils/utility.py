# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Utility function
import logging

import yaml

import src.utils.struct.personal_info as pi
import src.utils.struct.reserve_info as ri

logger = logging.getLogger(__name__)


def writeYaml(data, outfile):

    with open(outfile, "w", encoding="utf-8") as f:
        yaml.dump(
            data,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            indent=4,
        )
        f.close()


def readYaml(infile: str) -> dict:

    with open(infile, "r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        f.close()
    return data


def yaml2PersonalInfo(infile: str) -> pi.PersonalInfo_Struct:

    pis_dict = readYaml(infile)
    pis = pi.PersonalInfo_Struct(**pis_dict)
    return pis


def yaml2ReserveInfo(infile: str) -> ri.ReserveInfo_Struct:

    ris_dict = readYaml(infile)
    ris = ri.ReserveInfo_Struct(**ris_dict)
    return ris


def yaml2RecordInfo(infile: str) -> ri.RecordInfo_Struct:

    rec_dict = readYaml(infile)
    rec = ri.RecordInfo_Struct(**rec_dict)
    return rec
