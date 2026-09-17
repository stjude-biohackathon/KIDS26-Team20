# Create missing root runtime environment files without overwriting configured values.
[ -f .env_backend ] || cp .env_backend.example .env_backend

# build the docker image
docker compose build db
docker compose build mygpt_backend