import pyodbc
import pandas as pd
pyodbc.pooling = False
conn = pyodbc.connect(
    r'DRIVER={Teradata};'
    r'DBCName=idwprd.card.xxxx;'
    r'Database=ICDW_CB_PRSN_V;'
    r'Authentication=ldap;'
    r'UID=xxxxxx;'
    r'PWD=xxxxxx',
    autocommit=True,
    ansi=True)
cursor = conn.cursor()
statement = '''
    select
        ACCT_TP_CD,
        ACCT_TP_TX,
        count(distinct ACCT_DIM_NB) as counts
    from ICDW_CB_PRSN_V.DCM_OLM_DIM_ACCT
    group by 1, 2
    '''
df = pd.read_sql(statement, conn)
conn.close()
df
