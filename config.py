class Config:
    HOSTNAME = "localhost"
    PORT = '3306'
    USERNAME = "root"
    PASSWORD = "Tmz_20200212_zmT"
    DATABASE = "online_notebook"

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
