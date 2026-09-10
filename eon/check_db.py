import psycopg2

conn = psycopg2.connect(
    dbname="ECHO",
    user="admin",
    password="mythadmin",
    host="localhost",
    port="5432",
)
cur = conn.cursor()

print("=== eonapp_butterfly columns ===")
cur.execute("""
    SELECT column_name FROM information_schema.columns
    WHERE table_name = 'eonapp_butterfly'
    ORDER BY column_name;
""")
rows = cur.fetchall()
if not rows:
    print("(table does not exist)")
else:
    for r in rows:
        print(r[0])

print()
print("=== eonapp_flora.Flora_Map_Image ===")
cur.execute("""
    SELECT column_name FROM information_schema.columns
    WHERE table_name = 'eonapp_flora' AND column_name = 'Flora_Map_Image';
""")
rows = cur.fetchall()
print("EXISTS" if rows else "MISSING")

cur.close()
conn.close()
