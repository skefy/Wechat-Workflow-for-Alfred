# encoding: utf-8
import os
import sys
from workflow import Workflow
from workflow import Variables
from workflow.workflow import uninterruptible
import logging

def update_wx_group_db(wf):
    args = wf.args
    DB_PATH = args[0].strip()
    DB_KEY = args[1].strip()

    wechat_group_db_file = DB_PATH + "/Group/group_new.db"
    decrypted_file = wf.datadir + "/groupdecrypted.db"
    
    if not os.path.exists(wechat_group_db_file):
        logging.error("wechat db file not exists!")
        return 1

    if os.path.exists(decrypted_file):
        os.remove(decrypted_file)

    conn = sqlite.connect(wechat_group_db_file)
    c = conn.cursor()
    c.execute( "PRAGMA cipher_page_size = 1024;" )
    c.execute( "PRAGMA cipher_use_hmac = OFF;" )
    c.execute( "PRAGMA kdf_iter = 4000;" )
    c.execute( "PRAGMA key = " + DB_KEY + ";" )
    try:
        c.execute( "ATTACH DATABASE \'" + decrypted_file + "\' AS groupdecrypted KEY '';" )
        c.execute( "SELECT sqlcipher_export('groupdecrypted');" )
        c.execute( "DETACH DATABASE groupdecrypted;" )
        c.close()
        return 0
    except:
        c.close()
        logging.error("wechat db export fail!")
        return 1


def update_wx_contact_db(wf):
    args = wf.args
    if len(args) != 2:
        return 1

    DB_PATH = args[0].strip()
    DB_KEY = args[1].strip()

    wechat_contect_db_file = DB_PATH + "/Contact/wccontact_new2.db"
    decrypted_file = wf.datadir + "/wechatdecrypted.db"
    
    if not os.path.exists(wechat_contect_db_file):
        logging.error("wechat db file not exists!")
        return 1

    if os.path.exists(decrypted_file):
        os.remove(decrypted_file)
        
    conn = sqlite.connect(wechat_contect_db_file)
    c = conn.cursor()
    c.execute( "PRAGMA cipher_page_size = 1024;" )
    c.execute( "PRAGMA cipher_use_hmac = OFF;" )
    c.execute( "PRAGMA kdf_iter = 4000;" )
    c.execute( "PRAGMA key = " + DB_KEY + ";" )
    try:
        c.execute( "ATTACH DATABASE \'" + decrypted_file + "\' AS wechatdecrypted KEY '';" )
        c.execute( "SELECT sqlcipher_export('wechatdecrypted');" )
        c.execute( "DETACH DATABASE wechatdecrypted;" )
        c.close()
        return 0
    except:
        c.close()
        logging.error("wechat db export fail!")
        return 1

def return_for_flow(result):
    v = Variables(result)
    print(v)

def sync_db_data(wf):
    if  update_wx_contact_db(wf) == 0 and update_wx_group_db(wf) == 0:
        return_for_flow("sucess")
    else:
        return_for_flow("fail")
   
    
if __name__ == '__main__':
    wf = Workflow(libraries=['./lib'])
    from pysqlcipher import dbapi2 as sqlite
    
    sys.exit(wf.run(sync_db_data))