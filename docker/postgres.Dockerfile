FROM postgres:15

# Copy init scripts into the correct directory
COPY app/db/init/ /docker-entrypoint-initdb.d/