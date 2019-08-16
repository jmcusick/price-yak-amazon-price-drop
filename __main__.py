import psycopg2
try:
   connection = psycopg2.connect(user="postgres",
                                  password="mysecretpassword",
                                  host="localhost",
                                  port="5432",
                                  database="mytestdb")
   cursor = connection.cursor()
   postgreSQL_select_Query = "select * from mobile"
   cursor.execute(postgreSQL_select_Query)
   print("Selecting rows from mobile table using cursor.fetchall")
   mobile_records = cursor.fetchall()

   print("Print each row and it's columns values")
   for row in mobile_records:
       print("Id = ", row[0], )
       print("Model = ", row[1])
       print("Price  = ", row[2], "\n")
except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)
finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
