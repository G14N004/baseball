from unittest import result

from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllAnni():
        conn = DBConnect.get_connection()

        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select distinct t.year
                    from teams t 
                    where t.`year` >=1980 """

        cursor.execute(query)

        for row  in cursor:
            result.append((row["year"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSquadre(anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ select t.ID ,  t.teamCode 
                        from teams t 
                        where t.`year`=%s
        """
        result=[]
        cursor.execute(query,(anno,))
        for row in cursor:
            result.append((row["ID"],row["teamCode"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalario(anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT teamID, SUM(salary) AS totale_salari
                    FROM salaries s 
                    WHERE s.`year`  = %s
                    GROUP BY teamID;
        """
        res={}
        cursor.execute(query,(anno,))
        for row in cursor:
            res[row['teamID']] = row['totale_salari']

        cursor.close()
        conn.close()
        return res
