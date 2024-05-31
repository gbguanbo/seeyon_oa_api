# -*- coding: utf-8 -*-
import json
from operator import itemgetter


from ..api.base  import BaseOAAPI


class OAOrg(BaseOAAPI):

    def org_departments(self, account_id):
        '''
        获取指定单位的所有部门(不包含停用)

        地址：orgDepartments
        参数：account_id 绑定账号登录返回loginAccount
        '''
        result = self._get(
            f"orgDepartments/{account_id}"
        )
        return result

    def org_members_department(self, org_department_id):
        '''
        取得指定单位的所有人员(不包含停用人员)

        地址：orgMembers/department
        org_department_id 部门id
        '''
        result = self._get(
            f"orgMembers/department/{org_department_id}"
        )
        return result

    def org_posts(self, account_id):
        '''
        获取指定单位的所有岗位(不包含停用),其实只能返回全部的

        地址：orgPosts
        参数：account_id 绑定账号登录返回loginAccount
        '''
        result = self._get(
            f"orgPosts/{account_id}"
        )
        return result

    def org_levels(self, account_id):
        '''
        获取指定单位的所有岗位(不包含停用)，其实只能返回全部的

        地址：orgLevels
        参数：account_id 绑定账号登录返回loginAccount
        '''
        result = self._get(
            f"orgLevels/{account_id}"
        )
        return result

    def org_members_post(self, post_id):
        '''
        获取指定单位的所有岗位(不包含停用)，其实只能返回全部的

        地址：/orgMembers/post/
        参数：post_id 岗位id
        '''
        result = self._get(
            f"/orgMembers/post/{post_id}"
        )
        return result

    def org_members_level(self, level_id):
        '''
        获取指定单位的所有岗位(不包含停用)，其实只能返回全部的

        地址：/orgMembers/level/
        参数：level_id职务级别id
        '''
        result = self._get(
            f"/orgMembers/level/{level_id}"
        )
        return result

    def org_department_departmentmanager_info(self, department_id, account_id):
        '''
        获取指定单位的所有岗位(不包含停用)，其实只能返回全部的

        地址：orgDepartment/departmentmanagerinfo/{departmentid}/{accountid}
        参数：department_id ,account_id
        返回 deptrole0部门负责人 deptrole1分管，其他deptrole未知
        '''
        result = self._get(
            f"orgDepartment/departmentmanagerinfo/{department_id}/{account_id}"
        )
        return result
