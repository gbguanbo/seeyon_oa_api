from .client import OAClient
import json
import re


class processOA:
    def __init__(self, api_base_url, rest_account, rest_password, login_name):
        self._OAClient = OAClient(api_base_url, rest_account, rest_password, login_name)
        self.process_types()
        self.docs_libs()

    def process_types(self):
        template_types = self._OAClient.bpm.template_templateidlist(self._OAClient.login_name)
        for template in template_types:
            self._OAClient.session.set('template_'+str(template.get('id')), template)

    def docs_libs(self):
        docs_libs = self._OAClient.file.docs_libs()
        for lib in docs_libs:
            self._OAClient.session.set(lib.get('doclib_name'), lib)

    def analysis_affairs(self, affairs):
        details = {}
        affair_id = affairs.get('affairId')
        subject = affairs.get('subject')
        template_id = affairs.get('templateId')
        details['affairId'] = affair_id
        details['subject'] = subject
        details['templateId'] = template_id
        workitem_id = affairs.get('workitemId')
        details['workitemId'] = workitem_id
        process_id = affairs.get('processId')
        details['processId'] = process_id
        case_id = affairs.get('caseId')
        details['caseId'] = case_id
        activity_id = affairs.get('activityId')
        details['activityId'] = activity_id
        template = self._OAClient.session.get('template_'+template_id)
        if(template != None):
            details['templateName'] = template.get('showSubject')
        coll_summary = self._OAClient.bpm.coll_summary(affair_id)
        summary = coll_summary.get('summary')
        module_template_id = summary.get('templateId')
        content_template_id = summary.get('formAppId')
        attachments = summary.get('attachments')
        details['moduleTemplateId'] = module_template_id
        details['contentTemplateId'] = content_template_id
        if attachments:
            file_urls = [
                f"{attachment['fileUrl']}|{attachment['filename']}|{attachment['mimeType']}" for attachment in attachments]
            details['attachments'] = file_urls
        content = coll_summary.get('content')
        content_id = content.get('id')
        module_id = content.get('moduleId')
        right_id = content.get('rightId')
        form_right_id = content.get('formRightId')
        content_data_id = content.get('contentDataId')
        details['contentId'] = content_id
        details['rightId'] = right_id
        details['moduleId'] = module_id
        details['formRightId'] = form_right_id
        details['contentDataId'] = content_data_id
        form_data = self._OAClient.bpm.cap_form_show_form_data(module_id, form_right_id, affair_id)
        results = form_data.get('results')
        if not results:
            details['metadata'] = None
            details['data'] = None
            return details
        details['metadata'] = self.analysis_form_metadata(results.get('metadata'))
        details['data'] = self.analysis_form_data(results.get('data'), results.get('metadata'))
        return details

    def pending_affairs_all_details(self, subject='', templateName='', page_no=1, page_size=20):
        '''
        获取代办列表
        '''
        pending_affairs = self._OAClient.bpm.pending_affairs(subject, templateName, page_no, page_size)
        affairs_data = pending_affairs.get('data')
        self.pending_affairs_details = []
        for affairs in affairs_data:
            self.pending_affairs_details.append(self.analysis_affairs(affairs))
        return self.pending_affairs_details

    def done_affairs_all_details(self, subject='', templateName='', page_no=1, page_size=20):
        '''
        获取已办列表
        '''
        done_affairs = self._OAClient.bpm.done_affairs(subject, templateName, page_no, page_size)
        affairs_data = done_affairs.get('data')
        self.done_affairs_details = []
        for affairs in affairs_data:
            self.done_affairs_details.append(self.analysis_affairs(affairs))
        return self.done_affairs_details

    def sent_affairs_all_details(self, subject='', templateName='', page_no=1, page_size=20):
        '''
        获取已发列表
        '''
        sent_affairs = self._OAClient.bpm.sent_affairs(subject, templateName, page_no, page_size)
        affairs_data = sent_affairs.get('data')
        self.sent_affairs_details = []
        for affairs in affairs_data:
            self.sent_affairs_details.append(self.analysis_affairs(affairs))
        return self.sent_affairs_details

    def wait_sent_affairs_all_details(self, subject='', templateName='', page_no=1, page_size=20):
        '''
        获取代发列表
        '''
        wait_sent_affairs = self._OAClient.bpm.wait_sent_affairs(subject, templateName, page_no, page_size)
        affairs_data = wait_sent_affairs.get('data')
        self.wait_sent_affairs_details = []
        for affairs in affairs_data:
            self.wait_sent_affairs_details.append(self.analysis_affairs(affairs))
        return self.wait_sent_affairs_details

    def finish_affairs(self, workitem_id, attitude, content):
        return self._OAClient.bpm.bpm_workitem_finish('collaboration', workitem_id, attitude, content)

    def stop_affairs(self, workitem_id, content):
        return self._OAClient.bpm.bpm_process_stop('collaboration', workitem_id, content)

    def repeal_affairs(self, workitem_id, content):
        return self._OAClient.bpm.bpm_process_repeal('collaboration', workitem_id, content)

    def takeback_affairs(self, workitem_id, content):
        return self._OAClient.bpm.bpm_workitem_takeback('collaboration', workitem_id, content)

    def stepBack_affairs(self, workitem_id, content, attitude):
        return self._OAClient.bpm.bpm_workitem_stepBack('collaboration', workitem_id, content, attitude)

    def save_or_update_form(self, content_id, module_id, module_template_id, content_template_id, right_id, content_data_id, form_data, attachment_inputs):
        return self._OAClient.bpm.coll_save_or_update(
            content_id, module_id, module_template_id, content_template_id, right_id, content_data_id, form_data, attachment_inputs)

    def download_attachment(self, file_id):
        return self._OAClient.file.attachment_file(file_id)

    def upload_attachment(self, file_paths):
        file_urls = []
        for file_path in file_paths:
            result = self._OAClient.file.attachment(file_path)
            # 支持多个文件上传
            atts = result.get('atts')
            file_urls = file_urls + [att['fileUrl'] for att in atts]
        return file_urls

    def upload_attachment_to_docs(self, file_paths, doclib_name, folder_path, file_name=None):
        '''
        :file_path 要上传文件的物理路径
        :doclib_name 文档中心目录：我的文档等
        :folder_path 数组文件夹路径，如果不存在，创建
        :file_name 如果不为None，将检测遍历之后的根目录是否存在该文件，存在删除
        '''
        # 搜索需要上传的lib
        doc_lib = self._OAClient.session.get(doclib_name)
        doc_lib_id = doc_lib.get('doclib_id')
        doc_lib_type = doc_lib.get('doclib_type')
        # 搜索文件夹
        fr_id = doc_lib_id
        folder_names = folder_path.split('>')
        for folder_name in folder_names:
            docs = self._OAClient.file.docs_search(fr_id, folder_name)
            doc_results = docs.get('data')
            for doc_result in doc_results:
                if(doc_result.get('is_folder')):
                    fr_id = doc_result.get('fr_id')
            if(len(doc_results) == 0):
                self._OAClient.file.docs_create_foleder(folder_name, fr_id)
                docs = self._OAClient.file.docs_search(fr_id, folder_name)
                doc_news = docs.get('data')
                for doc_new in doc_news:
                    if(doc_new.get('is_folder')):
                        fr_id = doc_new.get('fr_id')
        # 获取文件信息
        folder_info = self._OAClient.file.docs_files(fr_id)
        folder_doc_lib_id = folder_info.get('data')[0].get('docLibId')
        if(file_name):
            docs_files_results = folder_info.get('data')[0].get('result')
            for docs_files_result in docs_files_results:
                f_name = docs_files_result.get('file_name')
                if(file_name == f_name):
                    dr_id = docs_files_result.get('fr_id')
                    self._OAClient.file.doc_doc_delete(dr_id, dr_id)
        # 上传附件
        file_urls = self.upload_attachment(file_paths)
        result = self._OAClient.file.docs_upload_doc_file(','.join(file_urls), folder_doc_lib_id, fr_id, doc_lib_type)
        return result

    def analysis_form_metadata(self, dict_metadata):
        master_metadata = dict_metadata.get("fieldInfo")
        table_info = {"masterTable": dict_metadata['tableName'], "slaveTable": []}
        table_info[dict_metadata['tableName']] = {}
        index = ','
        if(master_metadata != None):
            for key, value in master_metadata.items():
                index = index + value['display']+'|' + value['name'] + '|master|' + dict_metadata['tableName'] + ','
                table_info[dict_metadata['tableName']][value['display']] = {
                    'name': value['name'],
                    'inputType': value['inputType']
                }
        slave_metadata = dict_metadata.get("children")
        if(slave_metadata != None):
            for key, value in slave_metadata.items():
                table_info['slaveTable'].append(key)
                table_info[key] = {}
                for field_key, field_value in value.get("fieldInfo").items():
                    index = index + field_value['display']+'|' + field_value['name'] + '|slave|' + key + ','
                    table_info[key][field_value['display']] = {
                        'name': field_value['name'],
                        'inputType': field_value['inputType']
                    }
        table_info['index'] = index
        return table_info

    def analysis_form_data(self, dict_data, dict_metadata):
        master_data = dict_data.get("master")
        master_metadata = dict_metadata.get("fieldInfo")
        table_data = {'master': {dict_metadata['tableName']: {}}, "slave": {}}
        if(master_data != None):
            for key, value in master_data.items():
                info = master_metadata.get(key)
                if(info != None):
                    table_data['master'][dict_metadata['tableName']][info['display']] = {
                        'value': value['value'],
                        'display': value['display'],
                        'fieldName': value['fieldName'],
                        'ownerTableName': value['ownerTableName'],
                        'inputType': info['inputType']
                    }
                    if('attData' in value.keys()):
                        attData = value['attData']
                        if attData:
                            file_urls = [f"{attachment['fileUrl']}|{attachment['filename']}|{attachment['mimeType']}"
                                         for attachment in attData]
                            table_data['master'][dict_metadata['tableName']][info['display']]['value'] = file_urls
                            table_data['master'][dict_metadata['tableName']][info['display']]['display'] = file_urls
        slave_data = dict_data.get("children")
        slave_metadata = dict_metadata.get("children")
        table_data['slave'] = {}
        if(slave_data != None):
            for key, value in slave_data.items():
                table_data['slave'][key] = []
                field_infos = slave_metadata.get(key)['fieldInfo']
                rows = value.get('data')
                for row in rows:
                    row_data = {}
                    if(row != None):
                        for column_key, column in row.items():
                            info = field_infos.get(column_key)
                            if(info != None):
                                row_data[info['display']] = {
                                    'value': column['value'],
                                    'display': column['display'],
                                    'fieldName': column['fieldName'],
                                    'ownerTableName': column['ownerTableName'],
                                    'inputType': info['inputType']
                                }
                                if('attData' in column.keys()):
                                    attData = column['attData']
                                    if attData:
                                        file_urls = [f"{attachment['fileUrl']}|{attachment['filename']}|{attachment['mimeType']}"
                                                     for attachment in attData]
                                        row_data[info['display']]['value'] = file_urls
                                        row_data[info['display']]['display'] = file_urls

                        table_data['slave'][key].append(row_data)
        return table_data

    def quick_get_field_info_by_display(self, index, display, table=None):
        if(table != None):
            pattern = ',('+display+')\|(field\d+)\|(master|slave)\|('+table+'?),'
        else:
            pattern = ',('+display+')\|(field\d+)\|(master|slave)\|(form.*?),'
        match = re.findall(pattern, index)
        if match:
            if(len(match) > 1):
                raise ValueError('匹配到多组', match)
            else:
                return match[0]
        else:
            return None, None, None, None

    def quick_get_data_by_display(self, table_info, table_data, parameters, only_values=True):
        '''
        :parameters 需要获取数据的属性名数组,数组内容可以是字符串（主从无同名字典直接字符串即可）或者字典(处理主表与附表不同表相同字段)，字典结构为{'display':display,'table':table}
        :only_values 去除其他属性（value、fieldName、ownerTableName、inputType），只取值display
        '''
        master = None
        slave = {}
        if(parameters == None or len(parameters) == 0):
            masterTable = table_info.get('masterTable')
            masterTableData = table_data['master'][masterTable]
            if(only_values):
                # 过滤其他属性，只取display
                master = {key: masterTableData[key]['display'] for key in masterTableData}
            else:
                master = masterTableData
            slaveTables = table_info.get('slaveTable')
            for slaveTable in slaveTables:
                slave[slaveTable] = {}
                slaveTableData = table_data['slave'][slaveTable]
                if(only_values):
                    # 过滤其他属性，只取display
                    slave[slaveTable] = [{key: value['display'] for key, value in item.items()}
                                         for item in slaveTableData]
                else:
                    slave[slaveTable] = slaveTableData
        else:
            # 循环查询表类型及表名称，分组
            querys = []
            # 遍历查询属性所属表
            for parameter in parameters:
                if type(parameter) == dict:
                    display, column, table_type, table_name = self.quick_get_field_info_by_display(
                        table_info['index'], parameter['display'], parameter['table'])
                    if(display != None):
                        querys.append({'display': display, 'type': table_type, 'table': table_name})
                else:
                    display, column, table_type, table_name = self.quick_get_field_info_by_display(
                        table_info['index'], parameter)
                    if(display != None):
                        querys.append({'display': display, 'type': table_type, 'table': table_name})
        # 根据表合并数据，合并为[{table:{display:[],type:''}}]
            grouped_querys = {}
            for query in querys:
                if query['table'] not in grouped_querys:
                    grouped_querys[query['table']] = {'display': set(), 'type': set()}
                grouped_querys[query['table']]['display'].add(query['display'])
                grouped_querys[query['table']]['type'].add(query['type'])
        # type一张表只会有一种属性，直接pop就行，返回数组元组[(table,[],type),()]
            results = [
                (group, item_attrs['display'],  item_attrs['type'].pop())
                for group, item_attrs in grouped_querys.items()
            ]

            for result in results:
                table_name = result[0]
                displays = result[1]
                table_type = result[2]
                # 取出表数据
                data = table_data[table_type][table_name]
                # 主从表数据结构不一致，分开处理
                if(table_type == 'master'):
                    if(only_values):
                        # 过滤其他属性，只取display
                        master = {key: data[key]['display'] for key in data if key in displays}
                    else:
                        master = {key: data[key] for key in data if key in displays}
                else:
                    slave[table_name] = {}
                    if(only_values):
                        # 过滤其他属性，只取display
                        slave[table_name] = [{key: value['display'] for key, value in item.items()}for item in data]
                    else:
                        slave[table_name] = data
        if len(slave) == 1:
            slave = next(iter(slave.values()))
        return master, slave
