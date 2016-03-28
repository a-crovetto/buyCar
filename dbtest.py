import sqlite3

conn = sqlite3.connect('cars.db')

c = conn.cursor()
c.execute("select id from cars where link = 'htt://auto.mercadolibre.com.uy/MLU-433803497-nissan-maxima-30-automatico-ano-2000-chocado-_JM'")

id = c.fetchone()

if id is not None:
    print id[0]
else:
    print 'no hay'

conn.close()
