import json
import re


def analysis_form_metadata(dict_metadata):
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


def analysis_form_data(dict_data, dict_metadata):
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
                    table_data['slave'][key].append(row_data)
    return table_data


def quick_get_field_info_by_display(index, display, table=None):
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


def quick_get_data_by_display(table_info, table_data, parameters, only_values=True):
    '''
    本方法只支持一主一从获取数据，一主多从强制抛出异常
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
                slave[slaveTable] = [{key: value['display'] for key, value in item.items()}for item in slaveTableData]
            else:
                slave[slaveTable] = slaveTableData
    else:
        # 循环查询表类型及表名称，分组
        querys = []
        # 遍历查询属性所属表
        for parameter in parameters:
            if type(parameter) == dict:
                display, column, table_type, table_name = quick_get_field_info_by_display(
                    table_info['index'], parameter['display'], parameter['table'])
                if(display != None):
                    querys.append({'display': display, 'type': table_type, 'table': table_name})
            else:
                display, column, table_type, table_name = quick_get_field_info_by_display(
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
