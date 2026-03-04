$content = Get-Content 'data.js' -Raw -Encoding UTF8
if ($content.StartsWith('let RAW_DATA')) {
    $content = 'var RAW_DATA' + $content.Substring('let RAW_DATA'.Length)
    Set-Content 'data.js' -Value $content -Encoding UTF8 -NoNewline
    Write-Host 'DONE: changed let -> var in data.js'
} else {
    Write-Host 'First chars:' $content.Substring(0, 50)
    Write-Host 'Trying regex replace...'
    $newContent = $content -replace 'let RAW_DATA\s*=', 'var RAW_DATA ='
    if ($newContent -ne $content) {
        Set-Content 'data.js' -Value $newContent -Encoding UTF8 -NoNewline
        Write-Host 'DONE via regex replace'
    } else {
        Write-Host 'No change made - searching for RAW_DATA declaration...'
        $idx = $content.IndexOf('RAW_DATA')
        Write-Host 'Context:' $content.Substring([Math]::Max(0,$idx-10), 100)
    }
}
