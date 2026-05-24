$ErrorActionPreference = "Stop"

$dockerConfig = Join-Path $PSScriptRoot ".docker-cli"
New-Item -ItemType Directory -Force -Path $dockerConfig | Out-Null

$env:DOCKER_CONFIG = $dockerConfig

Write-Host "DOCKER_CONFIG set to $dockerConfig"
Write-Host "Use Docker commands in this PowerShell session, for example:"
Write-Host "  docker compose up -d --build"
Write-Host "  docker exec -it spark-practice-dev bash"
