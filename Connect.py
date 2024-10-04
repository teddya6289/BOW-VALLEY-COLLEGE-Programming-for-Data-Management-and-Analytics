import oracledb
import getpass
import tabulate
user=   'hr'
service=    'localhost/orclpdb'
port=   1521
pw= 'Samteh5020'

with  oracledb.connect(user=user, password=pw, dsn=service, port=port) as connection:
  with connection.cursor() as cursor:
     cursor.execute("select employee_id,first_name||' '||last_name,hire_date,salary from employees1")
     max=20
     rows=cursor.fetchmany(max)
print(tabulate.tabulate(rows,headers=['employee_id','full_name','hire_date','salary'],tablefmt='orgtbl'))


from sqlalchemy import create_engine
from sqlalchemy import text
import pyodbc
import pandas as pd

#preparing connection parameters
server= 'localhost'
database = 'AdventureWorks2022'
Driver = 'odbc driver 17 for sql server'
user = "Balli"

#connection string

connection_string = f'mssql+pyodbc://{user}@{server}/{database}?Trusted_Connection=Yes&driver={Driver}'

#connecting to Mssql server and fetching data Sales data from the AdventureWorks2022 data base

engine = create_engine(connection_string)
with engine.connect() as conn:
  result = conn.execute(text('select * from Sales.Store'))
  df = pd.DataFrame(result, columns=result.keys())
  print(df.head(101))

#RUNNING AN SQL SELECT STATEMENT ON ADVENTUREWORKS2022 DATABASE

#Creating a function to handle our connection


def create_conn_sqlserver(string_conn):
  engine = None
  try:
    engine = create_engine(string_conn)
    print('Sql server connection successful')
  except:
    print('fail connection attempt')
  return engine

#calling the create_conn_sqlserver function
string_conn =f'mssql+pyodbc://{user}@{server}/{database}?Trusted_Connection=Yes&driver={Driver}'
engine = create_conn_sqlserver(string_conn)

#Using function to fetch data from the AdventureWorks2022 database

def fetchsales_data(engine,querry):
  result = None
  try:
      with engine.connect() as conn:
         Data = conn.execute(text(querry))
         result =(Data.fetchall())
         print('Querry executed successfully')
         return result
  except:
      print('failed querry error')
#Calling the fetchsales_data
fetch_data_sqlstatement="select * from Sales.Store where BusinessEntityID between 400 and 1900;"

data=fetchsales_data(engine,fetch_data_sqlstatement)

#creating a list to store data fetched from the AdventureWorks2022 database
Fr_db_query=[]
#using the for loop to iterate over the sales data while using pandas dataframe to present it
for rows in data:
  result =list((rows))
  Fr_db_query.append(result)
  df = pd.DataFrame(Fr_db_query)
print(df.head(31))




#Running and insert sql statement using functions

def createtable_insert(engine):
   try:
      with engine.connect() as conn:
         conn.execute(text("""create table payroll(ID int identity (2,3) primary key,
                                                  first_name varchar(50) not null,
                                                  last_name varchar(50) not null,
                                                  basic_salary Dec(10,2) not null);"""))
         conn.execute(text("""insert into payroll values('Alexander',	'Hunold',158670),
                                                        ('David','Austin',219000.25),
                                                        ('Nancy','Greenberg',115900.68),
                                                        ('Den','Raphaely',32800),
                                                        ('Sigal','Tobias',200100);"""))
         data = conn.execute(text("select * from payroll;"))
         result =(data.fetchall())
         df = pd.DataFrame(result,columns=['ID','First Name','Last Name','Basic Salary'])
         print('table payroll created\nvalues inserted successfully')
         conn.commit()
         return df
      
   except Exception as e:
      print(f'Sql statement failed to execute:{e}')

with engine.connect() as conn:
   data = conn.execute(text("select * from payroll;"))
   df = pd.DataFrame(data,columns=['ID','First Name','Last Name','Updated Salary Column'])
   print(df)

string_conn =f'mssql+pyodbc://{user}@{server}/{database}?Trusted_Connection=Yes&driver={Driver}'
engine = create_conn_sqlserver(string_conn)
createtable_insert(engine)


#performing and update sql statement on the dummy payroll table
string_conn =f'mssql+pyodbc://{user}@{server}/{database}?Trusted_Connection=Yes&driver={Driver}'
engine = create_conn_sqlserver(string_conn)
with engine.connect() as conn:
   conn.execute(text("update payroll set basic_salary = 0 where basic_salary > 200000"))
   data = conn.execute(text("select * from payroll;"))
   df = pd.DataFrame(data,columns=['ID','First Name','Last Name','Updated Salary Column'])
   print(df)


#performing Sql delete statement on the dummy payroll table

with engine.connect() as conn:
   conn.execute(text("delete from payroll where ID =14;"))
   data = conn.execute(text("select * from payroll;"))
   df = pd.DataFrame(data,columns=['ID','First Name','Last Name','Updated Salary Column'])
   print(df)

