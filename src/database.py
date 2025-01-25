from sqlalchemy import create_engine

def connect_to_database(config):
	"""
	Establishes a connection to the MySQL database using the provided configuration.
	Args:
			config (dict): Configuration dictionary containing connection details.
	Returns:
			sqlalchemy.engine.Engine: A SQLAlchemy connection engine.
	"""
	if config:
		mysql_config = config.get("mysql", {})
		schema = mysql_config.get("schema", "default_schema")
		host = mysql_config.get("host", "localhost")
		user = mysql_config.get("user", "root")
		password = mysql_config.get("password", "")
		port = mysql_config.get("port", 3306)
		connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'
		print("Connection to the database has been established")
		return create_engine(connection_string)
	else:
		raise ValueError("The configuration could not be loaded.")