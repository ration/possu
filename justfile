init:
  uv venv .venv
  uv pip compile --allow-unsafe --generate-hashes --resolver=backtracking requirements.in --output-file requirements.txt
  uv pip install -r requirements.txt

start:
  docker compose up -d

supabase:
  cd supabase/docker && docker compose up -d
