import yaml
from sqlalchemy.sql import text
from sqlalchemy import create_engine

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

engine_path = f"postgresql://{config['database']['username']}:{config['database']['password']}@localhost/postgres"
engine = create_engine(engine_path)


conn = engine.connect()

try:
    # Assuming `engine` is your SQLAlchemy engine
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        print("Connection Successful: ", result.fetchone())
except Exception as e:
    print("Connection Failed: ", str(e))


# # create users table
# query = text("""
#     CREATE TABLE Users (
#     UserID SERIAL PRIMARY KEY,
#     Username VARCHAR(255) NOT NULL,
#     Email VARCHAR(255) UNIQUE NOT NULL,
#     PasswordHash VARCHAR(255),
#     OTPToken VARCHAR(255),
#     OTPRequestedAt TIMESTAMP,
#     OTPValidTill TIMESTAMP,
#     OTPTokenCount INTEGER DEFAULT 0,
#     CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     UpdatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
# );
# """)
# result = conn.execute(query)
# print(result)
# conn.close()