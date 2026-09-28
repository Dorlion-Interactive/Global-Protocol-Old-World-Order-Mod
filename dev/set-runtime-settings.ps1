param(
    [Parameter(Mandatory = $true)]
    [string]$ModJsonPath,

    [Parameter(Mandatory = $true)]
    [ValidateSet("sdk", "csharp", "as", "dotnet")]
    [string]$BuildVariant
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $ModJsonPath)) {
    throw "mod.json not found: $ModJsonPath"
}

$variant = $BuildVariant.ToLowerInvariant()
$desiredPolicy = "csharp_only"
$desiredComponentRuntime = $false

switch ($variant) {
    "dotnet" {
        $desiredPolicy = "wasm_only"
        $desiredComponentRuntime = $true
    }
    "as" {
        $desiredPolicy = "wasm_only"
        $desiredComponentRuntime = $false
    }
    default {
        $desiredPolicy = "csharp_only"
        $desiredComponentRuntime = $false
    }
}

$json = Get-Content $ModJsonPath -Raw | ConvertFrom-Json
$json.runtimePolicy = $desiredPolicy
$json.enableComponentRuntime = $desiredComponentRuntime

if (-not $json.PSObject.Properties.Name.Contains("entrypoints") -or $null -eq $json.entrypoints) {
    $json | Add-Member -NotePropertyName "entrypoints" -NotePropertyValue ([pscustomobject]@{})
}

if ($desiredPolicy -eq "csharp_only") {
    $json.entrypoints.PSObject.Properties.Remove("wasm")
} else {
    if ($json.entrypoints.PSObject.Properties.Name.Contains("wasm")) {
        $json.entrypoints.wasm = "Content/mod.wasm"
    } else {
        $json.entrypoints | Add-Member -NotePropertyName "wasm" -NotePropertyValue "Content/mod.wasm"
    }
}

$json | ConvertTo-Json -Depth 20 | Set-Content $ModJsonPath -Encoding UTF8

Write-Host ("runtimePolicy=" + $desiredPolicy)
Write-Host ("enableComponentRuntime=" + $desiredComponentRuntime)
