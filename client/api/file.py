# -*- coding: utf-8 -*-
import json
from operator import itemgetter


from ..api.base import BaseOAAPI


class OAFile(BaseOAAPI):

    def docs_libs(self):
        '''
        获取文档中心目录

        地址：docs/libs
        '''
        result = self._get(
            "docs/libs"
        )
        return result

    def docs_files(self, page_no,  page_size,  doc_id,  fr_type,  pro_type_id, is_share_and_borrow_root, from_biz):
        '''
        获取文档中心目录

        地址：docs/libs
        '''
        result = self._get(
            "docs/files",
            params={
                "pageNo": page_no,  # 默认1
                "pageSize": page_size,  # 默认20
                "docId": doc_id,  # 必填
                "frType": fr_type,  # 必填
                "pro_type_id": pro_type_id,  # 空
                "isShareAndBorrowRoot": is_share_and_borrow_root or 'true',
                "fromBiz": from_biz
            },
        )
        return result

    def docs_create_foleder(self, title, parent_fr_id):
        '''
        创建文件夹

        地址：docs/createFoleder
        '''
        result = self._post(
            "docs/createFoleder",
            data={
                "title": title,
                "parentFrId": parent_fr_id
            },
        )
        return result

    def docs_search(self, archive_id, search):
        '''
        搜索文件夹及文件

        地址：docs/search
        '''
        result = self._post(
            "docs/search",
            data={
                "archiveID": archive_id,
                "pageNo": "1",
                "pageSize": "20",
                "searchType": "1",
                "isShareAndBorrowRoot": "flase",
                "propertyName": "frName",
                "value1": search,
                "value2": "",
                "value3": ""
            },
        )
        return result
    def doc_doc_delete(self, dr_id, dr_ids):
        '''
        删除文件或者文件夹dr_id其实是fr_id,删除一个时dr_id和dr_ids一样，删除多个是，选其中一个作为dr_id，dr_ids逗号分隔
        地址：docs/search
        '''
        result = self._post(
            "doc/docDelete",
            data={
                "drId": dr_id,
                "drIds": dr_ids
            },
        )
        return result
    def docs_files(self, doc_id, page_no=1, page_size=20):
        '''
        获取文件夹信息

        地址：docs/files
        '''
        result = self._get(
            "docs/files",
            params={
                "docId": doc_id,
                "frType":"0",
                "pageNo": page_no,
                "pageSize": page_size
            },
        )
        return result
    def docs_upload_doc_file(self, file_id, doc_lib_id, doc_resource_id, doc_lib_type):
        '''
        上传文件，将上传的文件保存到对应目录

        地址：docs/uploadDocFile
        '''
        result = self._post(
            "docs/uploadDocFile",
            data={
                "fileId": file_id,
                "docLibId": doc_lib_id,
                "docResourceId": doc_resource_id,
                "docLibType": doc_lib_type
            },
        )
        return result

    def attachment_file(self, file_id):
        '''
        下载文件附件

        地址：attachment/file/{file_id}
        '''
        result = self._get(
            f"attachment/file/{file_id}",
        )
        return result

    def attachment(self, file_path):
        '''
        上传文件附件

        地址：attachment
        '''
        files = {'file': (file_path.split('\\')[-1], open(file_path, 'rb'), 'application/octet-stream')}
        result = self._post(
            "attachment",
            files = files
        )
        return result
