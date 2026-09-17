## run docker containers as detached 
docker compose down
docker compose up -d db
sleep 10

# create backend folder with demo publiction library
mkdir backend/data/pdfs/Turing_Way
cp -r backend/data/pdfs/Turing_Way/* backend/data/pdfs/Turing_Way/.
cp backend/data/data_chunks/MyGPT.txt backend/data/data_chunks/.
docker compose up -d mygpt_backend
sleep 60
open http://localhost:8000
sleep 60