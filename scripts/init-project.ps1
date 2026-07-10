[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$TargetPath,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$toolkitRoot = Split-Path -Parent $PSScriptRoot
$templateRoot = Join-Path $toolkitRoot 'templates'
$targetRoot = (Resolve-Path $TargetPath).Path

if (-not (Test-Path (Join-Path $targetRoot '.git'))) {
    throw "TargetPath must be the root of a Git repository: $targetRoot"
}

$files = @(
    @{ Source = 'AGENTS.md'; Destination = 'AGENTS.md' },
    @{ Source = 'CLAUDE.md'; Destination = 'CLAUDE.md' },
    @{ Source = '.agent-team/manifest.yaml'; Destination = '.agent-team/manifest.yaml' },
    @{ Source = '.agent-team/routing.yaml'; Destination = '.agent-team/routing.yaml' },
    @{ Source = '.agent-team/permissions.yaml'; Destination = '.agent-team/permissions.yaml' },
    @{ Source = '.agent-team/commands.yaml'; Destination = '.agent-team/commands.yaml' },
    @{ Source = '.agent-team/observability.yaml'; Destination = '.agent-team/observability.yaml' },
    @{ Source = '.agent-team/metrics/model-usage.csv'; Destination = '.agent-team/metrics/model-usage.csv' },
    @{ Source = '.agent-team/metrics/README.md'; Destination = '.agent-team/metrics/README.md' },
    @{ Source = 'task-contract.yaml'; Destination = '.agent-team/tasks/TASK-TEMPLATE.yaml' }
)

foreach ($file in $files) {
    $source = Join-Path $templateRoot $file.Source
    $destination = Join-Path $targetRoot $file.Destination
    $destinationDirectory = Split-Path -Parent $destination
    New-Item -ItemType Directory -Path $destinationDirectory -Force | Out-Null

    if ((Test-Path $destination) -and -not $Force) {
        Write-Warning "Skipped existing file: $($file.Destination)"
        continue
    }

    Copy-Item $source $destination -Force
    Write-Host "Installed $($file.Destination)"
}

$version = (Get-Content (Join-Path $toolkitRoot 'VERSION') -Raw).Trim()
Set-Content -Path (Join-Path $targetRoot '.agent-team/toolkit-version') -Value $version -NoNewline
New-Item -ItemType Directory -Path (Join-Path $targetRoot '.agent-team/reviews') -Force | Out-Null
New-Item -ItemType File -Path (Join-Path $targetRoot '.agent-team/reviews/.gitkeep') -Force | Out-Null

Write-Host "Toolkit $version installed. Replace all template placeholders using verified repository evidence before committing."
Write-Host "Codex must now ask the human whether local model-usage telemetry may be recorded and persist the answer in .agent-team/observability.yaml."
