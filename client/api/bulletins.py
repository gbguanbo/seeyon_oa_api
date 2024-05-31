# -*- coding: utf-8 -*-
import json
from operator import itemgetter


from ..api.base  import BaseOAAPI


class OABulletins(BaseOAAPI):
    def cmp_bulletins(self):
        '''
        获取公告类型

        地址：cmpBulletins/type/typeList
        '''
        result = self._get(
            "cmpBulletins/type/typeList"
        )
        return result

    def cmp_bulletins(self, title, cur_tab_id, publish_start_date, publish_end_date, page_no, page_size):
        '''
        获取公告类型
        地址：cmpBulletins/findBulletins4Combo
        '''
        result = self._post(
            "cmpBulletins/findBulletins4Combo",
            data={
                "pageNo": page_no,  # 默认1
                "pageSize": page_size,  # 默认20
                "publishEndDate": publish_end_date,  # 必填
                "publishStartDate": publish_start_date,  # 必填
                "curTabId": cur_tab_id or -1,
                "title": title
            },
        )
        return result

    def cmp_bulletin_detail(self, bul_id, come_from=0, affair_id='false'):
        '''
        获取公告详情
        地址：cmpBulletin/{bulId}/{comeFrom}/{affairId}
        返回值中根据content结合附加下载获取正文
        '''
        result = self._get(
            f"{bul_id}/{come_from}/{affair_id}",
        )
        return result
