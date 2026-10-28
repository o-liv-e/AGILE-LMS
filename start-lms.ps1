
$ErrorActionPreference = "Stop"

$forwards = @(
    @{ Name = "LMS v1"; Service = "lms-v1-service"; Port = 8501 },
    @{ Name = "LMS v2"; Service = "lms-v2-service"; Port = 8502 },
    @{ Name = "LMS v3"; Service = "lms-v3-service"; Port = 8503 }
)

foreach ($item in $forwards) {
    Start-Process -FilePath "powershell.exe" -ArgumentList @(
        "-NoExit",
        "-Command",
        "kubectl port-forward service/$($item.Service) $($item.Port):5000"
    )
}

Write-Host ""
Write-Host "LMS startup commands launched."
Write-Host "V1: http://localhost:8501"
Write-Host "V2: http://localhost:8502"
Write-Host "V3: http://localhost:8503"
