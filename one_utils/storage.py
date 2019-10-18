import pymysql
from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np

def dataframe_to_db(df,table_name,conn):
    DBSession = sessionmaker(conn)
    session = DBSession()
    df.reset_index(drop=True,inplace=True)
    d = df.to_dict(orient='index')
    try:
        for lnum in d.keys():
            line = d[lnum]
            keys = ','.join(list(map(lambda x:'`'+x+'`',list(line.keys()))))
            values = ','.join(map(lambda x:'null' if x=='nan' else x,map(lambda x:str(x) if not isinstance(x,str) else '\''+pymysql.escape_string(x)+'\'',list(line.values()))))
            query = 'REPLACE INTO {} ({}) VALUES ({})'.format(table_name,keys,values)
        #print(query)
            session.execute(query)
        session.commit()
    except TypeError as res:
        print(res)
        session.rollback()
    session.close()


def table_exist(conn,table_name):
    DBSession = sessionmaker(conn)
    session = DBSession()
    tables = list(session.execute('SHOW TABLES LIKE \'{}\''.format(table_name)))
    session.close()
    res = True if len(tables)>0 else False
    return res 
