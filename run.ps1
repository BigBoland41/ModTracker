# Start FastAPI server in a new window
Write-Host "Starting FastAPI server..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000"

# Start React app in a new window
Write-Host "Starting React app..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\WebApp'; npm run dev"
