import sys, string
__author__="Olmo S. Zavala Romero"

import psycopg2
import numpy as np
from pathlib import Path

def nicePrint(colnames, rows):
    #for i in range(len(colnames)):
        #print(colnames[i], " - ", rows[0][i])

    print(rows[0][0])
    print(colnames[1], "-", rows[0][1], "   ", colnames[2], "-", rows[0][2]) 
    print("\t P \t N")
    print('PP \t {} \t {}'.format(rows[0][3], rows[0][4]) )
    print("PN \t {} \t {}".format(rows[0][5], rows[0][6]) )

def computeConfussionMatrix():
    #For Posgresql only
    try: 
        conn = psycopg2.connect("dbname='contingencia' user='soloread' host='132.248.8.238' password='SH3<t!4e'")
    except:
        print("Failed to connect to database")


    try:
        cur = conn.cursor();

        print("---------- Computing RMSE ALL --------")
        orig_query = Path('SQL/GetRMSE.sql').read_text()
        cur.execute(orig_query);
        colnames = [desc[0] for desc in cur.description]
        rows = cur.fetchall();
        rmse = np.sqrt(float(rows[0][1])/ float(rows[0][0]))
        print("RMSE = ", rmse)
        print("MAE = ", rows[0][2])

        print("---------- Computing RMSE Good ones--------")
        orig_query = Path('SQL/GetRMSEOnlyGood.sql').read_text()
        cur.execute(orig_query);
        colnames = [desc[0] for desc in cur.description]
        rows = cur.fetchall();
        rmse = np.sqrt(float(rows[0][1])/ float(rows[0][0]))
        print("RMSE = ", rmse)
        print("MAE = ", rows[0][2])
        
        print("Closing connection...")
        conn.close()
        # ----------- ALL ESTATIONS ------------
        text = ['Buena', 'Regular', 'Mala', 'Muy Mala', 'Ext Mala']
        #values = [0, 50, 100, 150, 200, 500]
        values = [0, 70, 95, 154, 204, 404]

        print("---------- ALL stations--------")
        orig_query = Path('SQL/GetDicoAll.sql').read_text()
        for idx in range(0,len(values)-1):
            sqlquery = orig_query.replace('MIN', str(values[idx]))
            sqlquery = sqlquery.replace('MAX', str(values[idx+1]))
            sqlquery = sqlquery.replace('INDEX', text[idx])
            cur.execute(sqlquery);
            colnames = [desc[0] for desc in cur.description]
            rows = cur.fetchall();
            nicePrint(colnames, rows)

        print("---------------- Only GOOD stations--------")
        orig_query = Path('SQL/GetDicoOnlyGood.sql').read_text()
        for idx in range(0,len(values)-1):
            sqlquery = orig_query.replace('MIN', str(values[idx]))
            sqlquery = sqlquery.replace('MAX', str(values[idx+1]))
            sqlquery = sqlquery.replace('INDEX', text[idx])
            cur.execute(sqlquery);
            colnames = [desc[0] for desc in cur.description]
            rows = cur.fetchall();
            nicePrint(colnames, rows)

        # ----------- Single ESTATIONS ------------
        print("By station--------")
        orig_query = Path('SQL/GetDicoByEST.sql').read_text()
        stations = ['ATI', 'BJU','CUA','LPR','MER','PED','TLA','UIZ','XAL']

        for est in stations:
            print("---------", est , "-------")
            for idx in range(0,len(values)-1):
                sqlquery = orig_query.replace('EST', est)
                sqlquery = sqlquery.replace('MIN', str(values[idx]))
                sqlquery = sqlquery.replace('MAX', str(values[idx+1]))
                sqlquery = sqlquery.replace('INDEX', text[idx])
                cur.execute(sqlquery);
                colnames = [desc[0] for desc in cur.description]
                rows = cur.fetchall();

                if idx == 0:
                    print([col.rjust(8) for col in colnames])

                print([str(row).rjust(8) for row in rows[0]])

    except Exception as e:
        print("Something failed!!!!!!!!!", str(e))
        print("Closing connection...")
        conn.close()

    print("Closing connection...")
    conn.close()

if __name__ == "__main__":
    computeConfussionMatrix();

