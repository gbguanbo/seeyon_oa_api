# -*- coding: utf-8 -*-
from enum import Enum, IntEnum, unique



@unique
class OAErrorCode(IntEnum):
   
    # 系统错误
    SYSTEM_ERROR = 1


    # 正常
    SUCCESS = 0
    
    #不合法的 Access Token
    INVALID_ACCESS_TOKEN = 1010
    