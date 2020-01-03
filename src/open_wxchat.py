# encoding: utf-8
import os
import sys
from workflow import Workflow
import logging
import sqlite3


def open_new_chat(wf):
    args = wf.args
    keyword = args[0].strip()

    if not keyword:
        wf.add_item(u'快捷微信对话',
                    u"输入联系人",
                    arg='',
                    valid=True)
        wf.send_feedback()
        return
    
    keyword = wf.decode(keyword)
    result = search_friend(keyword)
    if result == None or len(result) == 0:
        wf.add_item(keyword,
                    u"打开微信对话",
                    arg=keyword,
                    autocomplete=' '+keyword,
                    valid=True)
    else:
        for item in result:
            # logging.info("== "+item[0]+" / " + item[0])
            dis_name = item[1]
            if dis_name == None or dis_name == "":
                dis_name = item[0]
            wf.add_item(dis_name,
                        u"打开微信对话",
                        arg=dis_name,
                        autocomplete=' '+dis_name,
                        valid=True)
    result = search_group(keyword)
    if result != None and len(result) != 0:
        for item in result:
            dis_name = item[0]
            wf.add_item(u"【群】"+dis_name,
                        u"打开微信对话",
                        arg=dis_name,
                        autocomplete=' '+dis_name,
                        valid=True)

    wf.send_feedback()


def search_friend(keyword):
    contact_db = wf.datadir + "/wechatdecrypted.db"
    if not os.path.exists(contact_db):
        return None

    searchName = '\'%%%s%%\'' % keyword
    msql = 'select nickname, m_nsRemark from WCContact where (nickname like {search}) or (m_nsRemark like {search}) or (m_nsFullPY like {search}) or (m_nsRemarkPYFull like {search})  or (m_nsRemarkPYShort like {search}) or (m_nsAliasName like {search}) limit 30'
    sql_code = msql.format(search=searchName.encode('utf-8'))
    # logging.info(sql_code)
    conn = sqlite3.connect(contact_db)
    c = conn.cursor()
    cursor = conn.execute(sql_code)
    result = cursor.fetchall()
    conn.close()
    return result


def search_group(keyword):
    group_db = wf.datadir + "/groupdecrypted.db"
    if not os.path.exists(group_db):
        return None

    searchName = '\'%%%s%%\'' % keyword
    msql = 'select nickname from GroupContact where (nickname like {search} ) or (m_nsFullPY like {search}) limit 30'
    sql_code = msql.format(search=searchName.encode('utf-8'))
    conn = sqlite3.connect(group_db)
    c = conn.cursor()
    cursor = conn.execute(sql_code)
    result = cursor.fetchall()
    conn.close()
    return result


if __name__ == '__main__':
    wf = Workflow(libraries=['./lib'])
    sys.exit(wf.run(open_new_chat))
