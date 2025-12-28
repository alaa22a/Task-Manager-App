$base = "http://localhost:5000/api"
$email = "testUser_$(Get-Random)@example.com"
$s = ConvertTo-Json @{name="Test User"; email=$email; password="password"}

Write-Host "Registering $email..."
Invoke-RestMethod -Uri "$base/auth/register" -Method Post -Body $s -ContentType "application/json"

Write-Host "Logging in..."
$login = Invoke-RestMethod -Uri "$base/auth/login" -Method Post -Body $s -ContentType "application/json"
$token = $login.access_token
Write-Host "Token received: $($token.Substring(0, 10))..."

Write-Host "Creating Task..."
$taskBody = ConvertTo-Json @{title="Test Task via Script"}
$headers = @{Authorization="Bearer $token"}
try {
    $task = Invoke-RestMethod -Uri "$base/tasks" -Method Post -Body $taskBody -ContentType "application/json" -Headers $headers
    Write-Host "Task Created: $($task.title)"
} catch {
    Write-Host "Error creating task: $_"
    $_.Exception.Response
}
