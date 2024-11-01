init:
  uv venv .venv
  uv pip compile --allow-unsafe --generate-hashes --resolver=backtracking requirements.in --output-file requirements.txt
  uv pip install -r requirements.txt


get-data:
  mkdir -p data
  wget https://www.avoindata.fi/data/dataset/941b70c8-3bd4-4b4e-a8fb-0ae29d2647a1/resource/3c277957-9b25-403d-b160-b61fdb47002f/download/finland_addresses_2024-08-14_json.7z -O data/data.7z

extract-data:
  cd data && 7z x data.7z

start:
  docker compose up -d

supabase:
  cd supabase/docker && docker compose up -d
