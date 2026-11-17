# Copy the skills into ~/.claude/skills. Use -Force to overwrite skills you already have.
param([switch]$Force)
$dest = Join-Path $HOME ".claude\skills"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Get-ChildItem -Directory (Join-Path $here "skills") | ForEach-Object {
  $target = Join-Path $dest $_.Name
  if ((Test-Path $target) -and -not $Force) { Write-Host "skip   $($_.Name) (already installed, use -Force to overwrite)" }
  else { if (Test-Path $target) { Remove-Item -Recurse -Force $target }; Copy-Item -Recurse $_.FullName $target; Write-Host "added  $($_.Name)" }
}
Write-Host "Done. Restart Claude Code."
