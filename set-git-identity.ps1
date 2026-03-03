<#
PowerShell helper to set Git identity.
Usage:
  # Set global identity (default)
  .\set-git-identity.ps1

  # Set local repo identity only
  .\set-git-identity.ps1 -Local
#>
param(
    [switch]$Local
)

$Name = 'Willian'
$Email = 'digitalprobr1@gmail.com'

if ($Local) {
    git config user.name "$Name"
    git config user.email "$Email"
    Write-Output "Set local git user.name and user.email in this repository."
} else {
    git config --global user.name "$Name"
    git config --global user.email "$Email"
    Write-Output "Set global git user.name and user.email for the current user."
}

Write-Output "To verify:"
Write-Output "  git config user.name"
Write-Output "  git config user.email"
Write-Output "  git config --global user.name"
Write-Output "  git config --global user.email"