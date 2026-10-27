#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 -v ro_pass="$DB_RO_PASSWORD" \
     --username "$POSTGRES_USER" --dbname chinook <<'SQL'
CREATE ROLE chatbot_ro LOGIN PASSWORD :'ro_pass';
GRANT CONNECT ON DATABASE chinook TO chatbot_ro;
GRANT USAGE ON SCHEMA public TO chatbot_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO chatbot_ro;
ALTER ROLE chatbot_ro SET default_transaction_read_only = on;
ALTER ROLE chatbot_ro SET statement_timeout = '5s';
SQL