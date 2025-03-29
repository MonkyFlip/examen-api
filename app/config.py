class Config:
    # Configuración de la conexión a RDS con tus credenciales
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://miguel:miguel-1234@database-1.cto6isqgsi2s.us-east-2.rds.amazonaws.com/examen"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
