username = "root"
password = ""
db_name = "mydb"  # name of the schema, it will create table if already not exist

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + username + ':' + password + '@localhost/' + db_name +'?charset=utf8&use_unicode=0'