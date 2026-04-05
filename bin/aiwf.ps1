#!/usr/bin/env pwsh
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (Get-Command py -ErrorAction SilentlyContinue) {
  py -3 "$ScriptDir/aiwf.py" @args
} else {
  python "$ScriptDir/aiwf.py" @args
}
