# -*- coding: utf-8 -*-
import json
from operator import itemgetter


from ..api.base import BaseOAAPI


class OABPM(BaseOAAPI):

    def affairs_pending(self, member_id, page_no, page_size):
        """
        获取代办，该接口文档有一些问题，新版不在有ticket，使用token替换

        详情请参考
        https://open.seeyoncloud.com/seeyonapi/728/748.html

        文档请求：affairs/pending?ticket={loginname}&memberId={memberid}&apps={appsid}
        正确请求：ffairs/pending?token={token}&memberId={memberid}&apps={appsid}&pageNo=1&pageSize=20
        :param memberId: 人员ID
        :return: 代办列表
        """
        result = self._get(
            "affairs/pending",
            params={
                "memberId": member_id,
                "apps": 1,
                "pageNo": page_no or 1,
                "pageSize": page_size or 20,
            },)
        return result

    def pending_affairs(self, subject='', templateName='', page_no=1, page_size=20):
        """
        获取代办,推荐，但返回代办数一直为0

        请求：coll/pendingAffairs
        :param:{"openFrom":"listPending","pageNo":1,"pageSize":20}
        :return: 代办列表
        """
        result = self._post(
            "coll/pendingAffairs",
            data={
                "openFrom": "listPending",
                "subject": subject,
                "templateName": templateName,
                "pageNo": page_no,
                "pageSize": page_size,
            },)
        return result

    def done_affairs(self, subject='', templateName='', page_no=1, page_size=20):
        """
        获取已办,推荐，但返回代办数一直为0

        请求：coll/doneAffairs
        :param:{"openFrom":"listPending","pageNo":1,"pageSize":20}
        :return: 已办列表
        """
        result = self._post(
            "coll/doneAffairs",
            data={
                "openFrom": "listPending",
                "subject": subject,
                "templateName": templateName,
                "pageNo": page_no,
                "pageSize": page_size,
            },)
        return result

    def sent_affairs(self, subject='', templateName='', page_no=1, page_size=20):
        """
        获取已发,推荐，但返回代办数一直为0

        请求：coll/sentAffairs
        :param:{"openFrom":"listPending","pageNo":1,"pageSize":20}
        :return: 已发列表
        """
        result = self._post(
            "coll/sentAffairs",
            data={
                "openFrom": "listPending",
                "subject": subject,
                "templateName": templateName,
                "pageNo": page_no,
                "pageSize": page_size,
            },)
        return result

    def wait_sent_affairs(self,  subject='', templateName='', page_no=1, page_size=20):
        """
        获取待发,推荐，但返回代办数一直为0

        请求：coll/waitSentAffairs
        :param:{"openFrom":"listPending","pageNo":1,"pageSize":20}
        :return: 待发列表
        """
        result = self._post(
            "coll/waitSentAffairs",
            data={
                "openFrom": "listPending",
                "subject": subject,
                "templateName": templateName,
                "pageNo": page_no,
                "pageSize": page_size,
            },)
        return result

    def flow_data(self, object_id, export_type, export_format):
        """
        获取流程（协同）的正文数据

        详情请参考
        https://open.seeyoncloud.com/seeyonapi/728/748.html

        地址：flow/data/{flowId}?exportType=0&exportFormat=json
        :param flowId: 流程的summaryId，列表中的objectId
               exportType 不填写返回的是枚举的enumvalue, 0返回枚举Showvalue，1返回枚举ID
               exportFormat	导出格式：xml，导出XML格式;json，导出JSON格式。since 7.0
        :return: 流程（协同）的正文
        """
        result = self._get(
            f"flow/data/{object_id}",
            params={
                "exportType": export_type or '1',
                "exportFormat": export_format or 'json'
            },)
        return result

    def coll_attachments(self, object_id, att_type):
        """
        获取协同附件列表

        详情请参考
        https://open.seeyoncloud.com/seeyonapi/728/748.html

        地址：coll/attachments/{SummaryID}/{AffairID}/{attType},AffairID取不到任何内容，只需要使用SummaryID
        正确地址：coll/attachments/{SummaryID}/{attType},
        :param summaryId: 流程的summaryId，列表中的objectId
               attType:0代表附件,2代表关联文档,“0,2”代表附件和关联文档
        :return: 协同附件列表
        """
        if att_type == None or att_type == '':
            att_type = '0,2'
        result = self._get(
            f"coll/attachments/{object_id}/{att_type}",
            params={

            },)
        return result

    def flow_state(self, object_id):
        """
        获取流程状态

        详情请参考
        https://open.seeyoncloud.com/seeyonapi/728/748.html

        地址：/flow/state/{flowId}

        :param flowId: 流程的flowId，列表中的objectId
        :return: 获取流程状态
        未发出	待发	1	流程未发出
        处理中	待处理	3	流程发出，无任何人处理/发出后回到待发
        处理中	处理中	4	流程发出，已部分处理
        处理中	回退	6	被退回到上一节点
        处理中	取回	7	被上一节点取回
        非正常结束	撤销	5	被发起者撤销
        非正常结束	终止	15	被终止
        正常结束	结束	0	正常结束
        """
        result = self._get(
            f"flow/state/{object_id}",
            params={

            },)
        return result

    def form_export(self, object_id, member_id):
        """
        获取指定表单HTML信息

        详情请参考
        https://open.seeyoncloud.com/seeyonapi/728/748.html

        地址：/form/export/{affairId}/{memId}

        :param affairId: 流程的affairId，列表中的objectId
               memId: 人员ID
        :return: 指定表单HTML信息

        """
        result = self._get(
            f"form/export/{object_id}/{member_id}",
            params={

            },)
        return result

    def coll_summary(self, affair_id):
        """
         获取代办详情

         地址：/coll/summary/{openFrom}/{affairId}/{summaryId}

         :param openFrom: listPending
                affairId: 流程的affairId，列表中的objectId
                summaryId: 默认-1即可
         :return: 代办详情      
         """
        open_from = "listPending"
        summary_id = -1
        result = self._get(
            f"coll/summary/{open_from}/{affair_id}/{summary_id}",
        )
        return result

    def cap_form_show_form_data(self, module_id, right_id, affair_id, module_type='1'):
        """
       获取表单内容并将内容放到内存中，以待更新

       地址：/capForm/showFormData

       :param
       根据注释从代办详情取对应参数
       最少参数：
       {
          "moduleId": "1268607895909453142",//content.moduleId或者summary.id
          "moduleType": "1",//协同1，公文2
          "rightId": "-3297295598383709150.-5083400289064434275",content.formRightId或者moduleId或者summary.rightId
          "viewState": "1",//默认
          "affairId": "-6950667468869645659",//summary.affairId
          "operateType": "1",//默认
          "cacheKey": "1268607895909453142",content.moduleId或者summary.id
          "templateType": "infopath",//默认
          "openFrom": "listPending"//默认
       }
       全量参数： 
       {
         "containerId": "newInputPosition",
         "moduleId": "1268607895909453142",
         "moduleType": "1",
         "rightId": "-3297295598383709150.-5083400289064434275",
         "viewState": "1",
         "allowQRScan": false,
         "indexParam": "0",
         "affairId": "-6950667468869645659",
         "mappingDataKey": "",
         "sourceType": "",
         "sourceId": "",
         "distributeContentDataId": "-1",
         "distributeContentTemplateId": "-1",
         "distributeAffairId": "-1",
         "signSummaryId": "-1",
         "formId": "-1",
         "operateType": "1",
         "cacheKey": "1268607895909453142",
         "templateType": "infopath",
         "openFrom": "listPending",
         "style": "1"
       }
       :return: 表单内容
       """
        result = self._post(
            "capForm/showFormData",
            data={
                "moduleId": module_id,
                "moduleType": module_type or "1",
                "rightId": right_id,
                "viewState": "1",
                "affairId": affair_id,
                "operateType": "1",
                "cacheKey": module_id,
                "templateType": "infopath",
                "openFrom": "listPending"
            },)
        return result

    def coll_save_or_update(self, content_id, module_id, module_template_id, content_template_id, right_id, content_data_id, form_data, attachment_inputs):
        _json_params = {
            "_currentDiv": {
                "_currentDiv": "0"
            },
            "secretLevelId": {
                "secretLevelId": ""
            },
            "mainbodyDataDiv_0": {
                "id": content_id,
                "moduleType": "1",
                "moduleId": module_id,
                "contentType": "20",
                "moduleTemplateId": module_template_id,
                "contentTemplateId": content_template_id,
                "rightId": right_id,
                "status": "STATUS_RESPONSE_VIEW",
                "viewState": "1",
                "hasHtmlSignature": "0",
                "contentDataId": content_data_id
            },
            **form_data,
            "attachmentInputs": attachment_inputs
        }

        """
        保存表单内容,此方法必须先调用show_form_data将数据加载到内存中
       
        地址：coll/saveOrUpdate

        :param 参数建议从summary或者show_form_data中取,修改的字段只能从show_form_data中metadata取
        必要：
         {
            "_currentDiv": {
                "_currentDiv": "0"
            },
            "secretLevelId": {
                "secretLevelId": ""
            },
            "mainbodyDataDiv_0": {
                "id": "",
                "moduleType": "1",
                "moduleId": "1268607895909453142",
                "contentType": "20",
                "moduleTemplateId": "-426380685737767020",
                "contentTemplateId": "-3620759783523794715",
                "rightId": "-5083400289064434275",
                "status": "STATUS_RESPONSE_VIEW",
                "viewState": "1",
                "contentDataId": "-1254558569434560942"
            },
            "formmain_5036": {
                "field0003": "22222222"
            },
            "attachmentInputs": []
        }
        全量：
        {
            "_currentDiv": {
                "_currentDiv": "0"
            },
            "secretLevelId": {
                "secretLevelId": ""
            },
            "mainbodyDataDiv_0": {
                "id": "",
                "createId": "2381110232683400967",
                "createDate": "2024-04-12 14:42:35.403",
                "modifyId": "-7996962698066704909",
                "modifyDate": "2024-04-12 14:56:26.444",
                "moduleType": "1",
                "moduleId": "1268607895909453142",
                "contentType": "20",
                "moduleTemplateId": "-426380685737767020",
                "contentTemplateId": "-3620759783523794715",
                "sort": "0", 
                "title": "",
                "content": "",
                "rightId": "-5083400289064434275",
                "status": "STATUS_RESPONSE_VIEW",
                "viewState": "1",
                "hasHtmlSignature": "0",
                "contentDataId": "-1254558569434560942"
            },
            "formmain_5036": {
                "field0003": "22222222"
            },
            "attachmentInputs": []
        }
         参数名          summary                   show_form_data
          id            content.id                 contentList[0].id
          createId         不填                       不填
          createDate       不填                       不填 
          modifyId         不填                       不填
          moduleType       1                          1
          moduleId      content.moduleId           contentList[0].moduleId
          contentType   content.contentType        contentList[0].contentType
          moduleTemplateId  summary.templateId     contentList[0].moduleTemplateId
          contentTemplateId  summary.formAppId     contentList[0].contentTemplateId
          rightId          content.rightId         contentList[0].rightId
          contentDataId    content.contentDataId   contentList[0].contentDataId
        根据注释从代办详情取对应参数
        """
        result = self._post(
            "coll/saveOrUpdate",
            data={
                "_json_params": json.dumps(_json_params)
            },)
        return result

    def bpm_template_workfolwId(self, template_code):
        '''
        获取流程模板processId

        地址：bpm/template/workfolwId

        :param templateCode: listPending

        :return: 流程模板processId
        '''
        result = self._get(
            "bpm/template/workfolwId",
            params={
                "templateCode": template_code
            },)
        return result

    def bpm_template_definition(self, template_code):
        '''
        获取流程定义xml

        地址：bpm/template/definition

        :param templateCode: listPending

        :return: 流程定义xml
        '''
        result = self._get(
            "bpm/template/definition",
            params={
                "templateCode": template_code
            },)
        return result

    def cap_form_search_form(self, subject):
        '''
        流程按名字搜索

        地址：capForm/searchForm

        :param subject 搜索名字
        :return
        '''
        '''
        获取表单定义xml

        地址：flow/FromTemplate

        :param templateCode
        :return: 获取表单定义xml
        '''
        result = self._post(
            "capForm/searchForm",
            data={
                "subject": subject
            },
        )
        return result

    def template_templateidlist(self, login_name, module_type=' '):
        '''
        获取登录用户流程，根据cap_form_search_form获取id可以详情

        地址：capForm/searchForm

        :param login_name 登录用户名
        :return
        '''
        '''
        获取表单定义xml

        地址：flow/FromTemplate

        :param login_name
        module_type: 空返回所有
        freeColl(1)
        templete(2)
        plan(3)
        project(4)
        task(5)
        doc(6)
        bbsAndshow(7)
        newsAndbul(8)
        inquiry(9)
        meeting(10)
        :return: 获取登录用户流程
        '''
        login_name = login_name or self._client.login_name
        result = self._get(
            f"template/templateidlist/{login_name}/{module_type}"
        )
        return result

    def coll_find_form_right_id(self, template_id):
        result = self._post(
            "coll/findFormRightId",
            data={
                "template_id": template_id
            },
        )
        return result

    def flow_from_template(self, template_code):
        '''
        获取表单定义xml

        地址：flow/FromTemplate

        :param templateCode
        :return: 获取表单定义xml
        '''
        result = self._get(
            f"flow/FromTemplate{template_code}"
        )
        return result

    def cap_form_load_template(self, form_id, right_id):
        '''
        获取表单定义json

        地址：capForm/loadTemplate

        :param formId: templateidlist 获取formAppId
            rightId: findFormRightId 获取权限
        :return: 表单定义内容
        '''
        result = self._post(
            "capForm/loadTemplate",
            data={

                "formId": form_id,
                "moduleId": "-1",
                "rightId": right_id,
                "templateType": "lightForm"
            },
        )
        return result

    def bpm_process_start(self, app_name, data, draft, login_name, subject, template_code, attachments, relate_doc):
        '''
        发起流程


        地址：bpm/process/start

        :param 
        传入参数说明：

        参数	是否必须	说明
        appName	是	应用类型
        data	是	data参数
        data参数

        参数	是否必须	说明
        templateCode	是	模板编号，参见表单正文流程模板编号
        draft	是	是否为待发：0:新建-发送；1:新建-保存待发
        attachments	否	协同标题区附件，Long型List，值为附件的Id。Id是附件接口响应结果中fileUrl字段的值。
        relateDoc	否	协同公文的id
        subject	否	未设置取模板设置的标题
        data	否	表单data参数
        useNewDataStructure	否	是否使用新的表单数据格式
        doTrigger	否	是否执行触发
        表单data参数

        参数	是否必须	说明
        formmainxxx	是	表单字段数据，json格式：key字段显示名称，value字段值（如果是cap4的附件控件，则value为附件的相关信息）
        formsonxx1	是	数组结构，参考主表
        thirdAttachments	否	CAP4附件参数
        changedFields	否	参与计算的字段
        thirdAttachments参数说明

        参数	是否必须	说明
        subReference	是	对应的附件字段的value值
        fileUrl	是	上传的附件ID
        sort	是	附件排序
        :return: 
        '''
        result = self._post(
            "bpm/process/start",
            data={
                "appName": app_name,
                "data": {
                    "data": data,
                    "draft": draft,
                    "senderLoginName": login_name,
                    "subject": subject,
                    "templateCode": template_code,
                    "attachments": attachments,
                    "relateDoc": relate_doc,
                    "useNewDataStructure": True,
                    "doTrigger": True
                }
            },
        )
        return result

    def bpm_workitem_finish(self, app_name, workitem_id, attitude, content, submit_type='1', base_process_XML='', base_ready_object_JSON=''):
        '''
        协同处理

        地址：bpm/workitem/finish

        :param 
            参数	是否必须	说明
            appName	是	应用类型 collaboration
            workitemId	是	事项ID（wf_workitem_run.id）
            attitude	是	态度（1 已阅， 2 同意， 3 不同意）
            content	否	意见内容
            submitType	否	是否需要提交协同 （1:提交协同，2:暂存待办 默认1）
            baseProcessXML	否	工作流XML。工作流有加签和减签时传入processXML。
            baseReadyObjectJSON	否	当前会签信息， 由后台生成， 加签/知会不传值,该参数可以为null，此时表示没有针对当前流程的Ready状态的节点 如果不为空，并且格式符合BPMProcess的话，在该xml的基础上执行流程修改操作
            messageDataList	否	发送消息用的json格式字符串， 由后台生成
            changeMessageJSON	否	加签/减签等操作数据， 后台生成
        '''
        result = self._post(
            "bpm/workitem/finish",
            data={

                "appName": app_name,
                "workitemId": workitem_id,
                "data": {
                    "comment_deal": {
                        "attitude": attitude,
                        "content": content
                    },
                    "submitType": submit_type,
                    "baseProcessXML": base_process_XML,
                    "baseReadyObjectJSON": base_ready_object_JSON,
                    "messageDataList": '',
                    "changeMessageJSON": ''
                }

            }
            )
        return result

    def bpm_process_stop(self, app_name, workitem_id, content):
        '''
        协同终止

        地址：bpm/process/stop

        :param templateCode: listPending

        :return:
        '''
        result = self._post(
            "bpm/process/stop",
            data={
                "appName": app_name,
                "workitemId": workitem_id,
                "data": {
                    "stopOpinion": content
                }
            },)
        return result

    def bpm_process_repeal(self, app_name, workitem_id, content):
        '''
        协同撤销

        地址：bpm/process/repeal

        :param

        :return:
        '''
        result = self._post(
            "bpm/process/repeal",
            data={
                "appName": app_name,
                "workitemId": workitem_id,
                "data": {
                    "stopOpinion": content
                }

            },)
        return result

    def bpm_workitem_takeback(self, app_name, workitem_id, is_save_opinion='true'):
        '''
        取回接口

        地址：bpm/workitem/takeback

        :param isSaveOpinion: 是否在原意见上修改。 "true"(字符), 保留原意见
        参数说明：

        参数	是否必须	说明
        appName(String)	是	应用类型,协同,表单设置为:collaboration
        workitemId(String)	是	待办事项Id,对应ctp_affair表SUB_OBJECT_ID字段
        dataMap(Map)	是	Key有这些isSaveOpinion:是否在原意见上修改.true:保留原意见。

        :return:
        '''
        result = self._post(
            "bpm/workitem/takeback",
            data={
                "appName": app_name,
                "workitemId": workitem_id,
                "data": {
                    "isSaveOpinion": is_save_opinion
                }

            },)
        return result

    def bpm_workitem_stepBack(self, app_name, workitem_id, content, attitude):
        '''
        协同回退

        地址：bpm/workitem/stepBack

        :param 
        参数说明：

        参数	是否必须	说明
        appName(String)	是	应用类型,协同,表单设置为:collaboration
        workitemId(String)	是	待办事项Id,对应ctp_affair表SUB_OBJECT_ID字段
        dataMap(Map)	是	Key有:isWFTrace:0 流程追溯
        -	是	comment_deal:attitude:1 已阅,2 同意,3 不同意
        -	是	comment_deal:content: 回退意见

        :return:
        '''
        result = self._post(
            "bpm/workitem/stepBack",
            data={
                "appName": app_name,
                "workitemId": workitem_id,
                "data": {
                    "isWFTrace": "0",
                    "comment_deal": {
                        "attitude": attitude,
                        "content": content
                    }
                }

            },)
        return result

    def bpm_workitem_specifyback(self):
        # TODO
        pass

    def bpm_process_addNode(self):
        # TODO
        pass

    def bpm_process_deleteNode(self):
        # TODO
        pass

    def bpm_process_freeReplaceNode(self):
        # TODO
        pass

    def bpm_process_replaceItem(self, app_name, workitem_id, next_member_id):
        '''
        转办

        地址：bpm/process/replaceItem

        :param

        参数说明：

        参数	是否必须	说明
        appName(String)	是	模块ID:("collaboration","edoc")
        workitemId(String)	是	当前流程工作事项id
        nextMemberId(String)	是	替换后的人员id

        :return:
        '''
        result = self._post(
            "bpm/process/repeal",
            data={

                "appName": app_name,
                "workitemId": workitem_id,
                "nextMemberId": next_member_id

            },)
        return result

    def bpm_process_diagramImg(self, appName, workitemId, attitude, content, submitType, baseProcessXML, baseReadyObjectJSON):
        # TODO
        pass
