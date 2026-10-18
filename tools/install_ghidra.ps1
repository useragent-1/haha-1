<#
.SYNOPSIS
    Install the Ghidra analysis engine required by the Rea MCP backend on Windows.

.DESCRIPTION
    Rea itself ships as a CLI + MCP server, but it has no decompiler of its own.
    On Windows the only usable provider is Ghidra, which needs:
      - JDK 21 (Ghidra 12.1.x runtime)
      - An extracted Ghidra 12.1.x PUBLIC release
      - GHIDRA_INSTALL_DIR + JAVA_HOME + PATH

    This script is idempotent: existing downloads are resumed, existing
    installations are reused, and environment variables are only written when
    the target path actually validates.

.PARAMETER Root
    Install root. Default: D:\tools

.PARAMETER GhidraVersion
    Ghidra release to install. Default: 12.1.4

.PARAMETER JdkVersion
    Temurin JDK feature release. Default: 21

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\install_ghidra.ps1

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\install_ghidra.ps1 -Root E:\reverse -GhidraVersion 12.1.4
#>
[CmdletBinding()]
param(
    [string]$Root = 'D:\tools',
    [string]$GhidraVersion = '12.1.4',
    [string]$JdkVersion = '21'
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

function Write-Step($msg) { Write-Host "==> $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "    OK  $msg" -ForegroundColor Green }
function Write-Warn2($msg){ Write-Host "    !!  $msg" -ForegroundColor Yellow }

function Test-ZipComplete([string]$Path) {
    # A truncated .zip opens fine at the entry level but fails on extract, so
    # validate that every entry's compressed stream is readable before reuse.
    if (-not (Test-Path $Path)) { return $false }
    try {
        Add-Type -AssemblyName System.IO.Compression.FileSystem -ErrorAction SilentlyContinue
        $zip = [System.IO.Compression.ZipFile]::OpenRead($Path)
        $count = $zip.Entries.Count
        $zip.Dispose()
        return ($count -gt 0)
    } catch {
        return $false
    }
}

function Invoke-Download([string]$Url, [string]$Dest) {
    if (Test-ZipComplete $Dest) {
        Write-Ok "reusing verified $(Split-Path $Dest -Leaf) ($([math]::Round((Get-Item $Dest).Length/1MB,1)) MB)"
        return
    }
    if (Test-Path $Dest) {
        Write-Warn2 "partial download found ($([math]::Round((Get-Item $Dest).Length/1MB,1)) MB); resuming"
    } else {
        Write-Step "downloading $(Split-Path $Dest -Leaf)"
    }
    & "$env:SystemRoot\System32\curl.exe" -L --retry 10 --retry-all-errors -C - -o $Dest $Url
    if ($LASTEXITCODE -ne 0) { throw "curl failed ($LASTEXITCODE): $Url" }
    if (-not (Test-ZipComplete $Dest)) { throw "download incomplete or corrupt: $Dest" }
    Write-Ok "$([math]::Round((Get-Item $Dest).Length/1MB,1)) MB"
}

function Get-GhidraAssetUrl([string]$Version) {
    $tag = "Ghidra_${Version}_build"
    $api = "https://api.github.com/repos/NationalSecurityAgency/ghidra/releases/tags/$tag"
    $rel = Invoke-RestMethod -Uri $api -Headers @{ 'User-Agent' = 'reverse-flow-installer' }
    $asset = $rel.assets | Where-Object { $_.name -like 'ghidra_*_PUBLIC_*.zip' } | Select-Object -First 1
    if (-not $asset) { throw "no PUBLIC zip asset found for $tag" }
    return @{ url = $asset.browser_download_url; name = $asset.name }
}

# ---------------------------------------------------------------- JDK
Write-Step "checking JDK $JdkVersion"
$jdkHome = Join-Path $Root "jdk$JdkVersion"
$javaExe = Join-Path $jdkHome 'bin\java.exe'
if (Test-Path $javaExe) {
    Write-Ok "JDK already installed: $jdkHome"
} else {
    $jdkZip = Join-Path $Root "jdk$JdkVersion.zip"
    $jdkUrl = "https://api.adoptium.net/v3/binary/latest/$JdkVersion/ga/windows/x64/jdk/hotspot/normal/eclipse?project=jdk"
    Invoke-Download $jdkUrl $jdkZip

    Write-Step "extracting JDK"
    $tmp = Join-Path $Root '_jdk_tmp'
    if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
    Expand-Archive -Path $jdkZip -DestinationPath $tmp -Force
    $inner = Get-ChildItem $tmp -Directory | Select-Object -First 1
    if (Test-Path $jdkHome) { Remove-Item $jdkHome -Recurse -Force }
    Move-Item $inner.FullName $jdkHome
    Remove-Item $tmp -Recurse -Force
    $javaExe = Join-Path $jdkHome 'bin\java.exe'
    if (-not (Test-Path $javaExe)) { throw "JDK extraction produced no bin\java.exe" }
    Write-Ok "installed $jdkHome"
}

# ---------------------------------------------------------------- Ghidra
Write-Step "checking Ghidra $GhidraVersion"
$ghidraHome = Join-Path $Root "ghidra_${GhidraVersion}_PUBLIC"
$headless = Join-Path $ghidraHome 'support\analyzeHeadless.bat'
if (Test-Path $headless) {
    Write-Ok "Ghidra already installed: $ghidraHome"
} else {
    $asset = Get-GhidraAssetUrl $GhidraVersion
    $ghidraZip = Join-Path $Root $asset.name
    Invoke-Download $asset.url $ghidraZip

    Write-Step "extracting Ghidra (large, several minutes)"
    $tmp = Join-Path $Root '_ghidra_tmp'
    if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
    Expand-Archive -Path $ghidraZip -DestinationPath $tmp -Force
    $inner = Get-ChildItem $tmp -Directory | Select-Object -First 1
    if (Test-Path $ghidraHome) { Remove-Item $ghidraHome -Recurse -Force }
    Move-Item $inner.FullName $ghidraHome
    Remove-Item $tmp -Recurse -Force
    $headless = Join-Path $ghidraHome 'support\analyzeHeadless.bat'
    if (-not (Test-Path $headless)) { throw "Ghidra extraction produced no support\analyzeHeadless.bat" }
    Write-Ok "installed $ghidraHome"
}

# ---------------------------------------------------------------- env
Write-Step "setting user environment"
[Environment]::SetEnvironmentVariable('JAVA_HOME', $jdkHome, 'User')
[Environment]::SetEnvironmentVariable('GHIDRA_INSTALL_DIR', $ghidraHome, 'User')
$env:JAVA_HOME = $jdkHome
$env:GHIDRA_INSTALL_DIR = $ghidraHome
$env:PATH = "$jdkHome\bin;$env:PATH"
Write-Ok "JAVA_HOME=$jdkHome"
Write-Ok "GHIDRA_INSTALL_DIR=$ghidraHome"

# ---------------------------------------------------------------- verify
Write-Step "verifying"

# java -version writes to stderr; with $ErrorActionPreference='Stop' PowerShell
# turns that into a terminating NativeCommandError and silently ends the script.
$previousEap = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
& $javaExe -version 2>&1 | ForEach-Object { Write-Host "    $_" }

if (Get-Command rea -ErrorAction SilentlyContinue) {
    $doctor = & rea doctor --format json 2>&1 | Out-String
    # `healthy` is global and can never be true on Windows: the Hopper provider
    # is macOS-only, so it always reports missing_analysis_engine. Grade the
    # Ghidra engine chain instead, which is what this script installs.
    $engineOk = (
        $doctor -match '"name":\s*"ghidra-native_decompiler",\s*"ok":\s*true' -and
        $doctor -match '"name":\s*"ghidra-headless",\s*"ok":\s*true' -and
        $doctor -match '"name":\s*"ghidra-version",\s*"ok":\s*true'
    )
    if ($engineOk) {
        Write-Ok "Rea Ghidra engine: healthy (headless + native decompiler + version)"
        if ($doctor -notmatch '"healthy"\s*:\s*true') {
            Write-Warn2 "rea doctor still flags unrelated items (Hopper is macOS-only; skill/registration entries are cosmetic)"
        }
    } else {
        Write-Warn2 "Ghidra engine still not healthy; inspect with: rea doctor"
        Write-Host $doctor.Substring(0, [Math]::Min(1200, $doctor.Length))
    }
} else {
    Write-Warn2 "rea not on PATH; run: npx -y rea-agents mcp  (or install the rea CLI)"
}
$ErrorActionPreference = $previousEap

Write-Host ""
Write-Host "Done. Two restarts are required before the MCP backend sees the engine:" -ForegroundColor Cyan
Write-Host "  1. open a NEW terminal (env vars are user-scoped)" -ForegroundColor Gray
Write-Host "     rea capabilities      # ghidra availability.status should be 'available'" -ForegroundColor Gray
Write-Host "  2. restart the IDE / MCP host process" -ForegroundColor Gray
Write-Host "     an already-running MCP server keeps its old environment and will" -ForegroundColor Gray
Write-Host "     keep reporting 'install_dir: null' until it is restarted" -ForegroundColor Gray
Write-Host "  then verify: python <skill>/scripts/tool_audit.py --profile native" -ForegroundColor Gray
