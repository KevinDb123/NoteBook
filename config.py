class Config:
    HOSTNAME = "localhost"
    PORT = 'port'#需修改
    USERNAME = "username"#需修改
    PASSWORD = "password"#这里进行了修改
    DATABASE = "online_notebook"

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
