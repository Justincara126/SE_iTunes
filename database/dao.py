from database.DB_connect import DBConnect
from model.album import Album


class DAO:
    @staticmethod
    def get_album(minuti):
        millisecondi=minuti*60*1000
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query=('''select a.id,a.title,a.artist_id,sum(t.milliseconds) as durata
from itunes.album a, itunes.track t
where t.album_id=a.id
        group by a.id,a.title,a.artist_id
        having sum(t.milliseconds) > %s''')
        result={}
        cursor.execute(query,(millisecondi,))
        for row in cursor:
            result[row['id']]=Album(**row)
        cursor.close()
        conn.close()
        return result
    @staticmethod
    def get_edges(lista_id):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result=[]
        placeholders = ",".join(["%s"] * len(lista_id))
        query=f'''  SELECT DISTINCT a1.id as id1, a2.id as id2
                    FROM album a1, album a2, track t1, track t2, playlist_track p1, playlist_track p2
                    WHERE a1.id < a2.id AND 
                          a1.id = t1.album_id AND
                          a2.id = t2.album_id AND 
                          a1.id in ({placeholders}) AND
                          a2.id in ({placeholders}) AND
                          p1.playlist_id = p2.playlist_id  AND 
                          p1.track_id = t1.id AND
                          p2.track_id = t2.id
                    '''
        cursor.execute(query,lista_id+lista_id)
        for row in cursor:
            result.append([row['id1'],row['id2']])
        cursor.close()
        conn.close()
        return result



