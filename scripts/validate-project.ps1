[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$TargetPath
)

$ErrorActionPreference = 'Stop'
$targetRoot = (Resolve-Path $TargetPath).Path
$requiredFiles = @(
    'AGENTS.md',
    'CLAUDE.md',
    '.agent-team/manifest.yaml',
    '.agent-team/routing.yaml',
    '.agent-team/permissions.yaml',
    '.agent-team/commands.yaml',
    '.agent-team/toolkit-version'
)

$errors = @()
foreach ($relativePath in $requiredFiles) {
    if (-not (Test-Path (Join-Path $targetRoot $relativePath))) {
        $errors += "Missing required file: $relativePath"
    }
}

$placeholderPatterns = @('{{', 'UNKNOWN')
foreach ($relativePath in $requiredFiles) {
    $path = Join-Path $targetRoot $relativePath
    if (-not (Test-Path $path)) { continue }
    $content = Get-Content $path -Raw
    foreach ($pattern in $placeholderPatterns) {
        if ($content.Contains($pattern)) {
            $errors += "Unresolved placeholder '$pattern' in $relativePath"
        }
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Host 'Agent toolkit project configuration is structurally valid.'
