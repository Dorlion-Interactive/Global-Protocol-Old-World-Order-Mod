# validate_scenario.ps1
# -------------------------------------------------------------------
# Pre-deploy validator for the mod's scenario fragments.
# Each *.json under scenario\ MUST be a JSON object whose top-level
# key matches the ScenarioFragment shape expected by the game.
# A bare JSON array (e.g. ["FRA","PRT"]) will silently break scenario
# load at runtime — Newtonsoft.Json throws and the game falls back to
# vanilla without flags. This script catches that class of bug before
# install.bat copies a broken mod into LOCALAPPDATA.
#
# Exit codes:
#   0  All fragments valid.
#   1  One or more fragments malformed.
# -------------------------------------------------------------------

param(
    [string]$ScenarioDir = (Join-Path $PSScriptRoot "..\scenario")
)

$ErrorActionPreference = 'Stop'

# Map of file name -> required top-level key in the JSON object.
# Header file scenario.json requires scenarioId only; arrays optional.
$FragmentSpec = @{
    'scenario.json'              = @('scenarioId')
    'countries_add.json'         = @('addCountries')
    'countries_remove.json'      = @('removeCountries')
    'countries_state.json'       = @('countryStateOverrides')
    'provinces_ownership.json'   = @('regionOwnerOverrides', 'provinceOwnerOverrides')
    'units_define.json'          = @('unitTypes')
    'units_deploy_armies.json'   = @('initialArmies')
    'units_deploy_fleets.json'   = @('initialFleets')
    'units_deploy_air.json'      = @('initialAirWings')
}

if (-not (Test-Path -LiteralPath $ScenarioDir)) {
    Write-Error "[validate_scenario] Scenario folder not found: $ScenarioDir"
    exit 1
}

$resolvedDir = (Resolve-Path -LiteralPath $ScenarioDir).Path
Write-Host "[validate_scenario] Scanning: $resolvedDir"

$failures = New-Object System.Collections.Generic.List[string]
$checked = 0

Get-ChildItem -LiteralPath $resolvedDir -Filter *.json -File | ForEach-Object {
    $file = $_
    $checked++
    $rel = $file.Name

    # Read raw bytes to detect bare-array shape robustly (works regardless of BOM).
    $raw = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
    $trimmed = $raw.TrimStart([char]0xFEFF, ' ', "`t", "`r", "`n")

    if ($trimmed.Length -eq 0) {
        $failures.Add("$rel : file is empty")
        return
    }

    $firstChar = $trimmed[0]
    if ($firstChar -eq '[') {
        $failures.Add("$rel : root is a JSON array; expected an object like { ""<key>"": [...] }")
        return
    }
    if ($firstChar -ne '{') {
        $failures.Add("$rel : root is not a JSON object (starts with '$firstChar')")
        return
    }

    # Parse and check expected key for known fragment names.
    try {
        $parsed = $raw | ConvertFrom-Json
    } catch {
        $failures.Add("$rel : invalid JSON: $($_.Exception.Message)")
        return
    }

    if ($FragmentSpec.ContainsKey($rel)) {
        $expectedKeys = $FragmentSpec[$rel]
        $hasKey = $false
        foreach ($k in $expectedKeys) {
            if ($null -ne $parsed.PSObject.Properties[$k]) {
                $hasKey = $true
                break
            }
        }
        if (-not $hasKey) {
            $failures.Add("$rel : missing expected top-level key (one of: $($expectedKeys -join ', '))")
            return
        }
    } else {
        Write-Host "  ? $rel (unknown fragment, structural check only)"
    }

    Write-Host "  OK $rel"
}

Write-Host ""
if ($failures.Count -gt 0) {
    Write-Host "[validate_scenario] FAILED ($($failures.Count) of $checked fragment(s) invalid):" -ForegroundColor Red
    foreach ($msg in $failures) {
        Write-Host "  - $msg" -ForegroundColor Red
    }
    exit 1
}

Write-Host "[validate_scenario] OK -- $checked fragment(s) valid." -ForegroundColor Green
exit 0
