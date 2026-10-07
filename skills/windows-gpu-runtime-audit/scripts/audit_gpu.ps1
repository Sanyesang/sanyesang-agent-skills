param([string]$PythonPath)
$ErrorActionPreference = 'Stop'
$gpuReport = [ordered]@{ schemaVersion = 1; hardware = $null; driver = $null; runtime = $null; actualApplicationExecution = 'Not observed by this read-only helper' }
try {
    $gpuReport.hardware = @(Get-CimInstance Win32_VideoController | Select-Object Name, DriverVersion, Status, ConfigManagerErrorCode)
} catch {
    $gpuReport.hardware = @{ error = $_.Exception.Message }
}
$nvidiaCommand = Get-Command nvidia-smi -ErrorAction SilentlyContinue
if ($nvidiaCommand) {
    $driverOutput = & $nvidiaCommand.Source '--query-gpu=name,driver_version,memory.total' '--format=csv,noheader' 2>&1
    $gpuReport.driver = @{ available = $true; exitCode = $LASTEXITCODE; output = @($driverOutput | ForEach-Object { "$_" }) }
} else {
    $gpuReport.driver = @{ available = $false; note = 'nvidia-smi not found on PATH; this does not establish that no GPU exists' }
}
if ($PythonPath) {
    $resolvedPython = Get-Item -LiteralPath $PythonPath -ErrorAction Stop
    if ($resolvedPython.PSIsContainer) { throw 'PythonPath must identify an executable, not a directory' }
    $runtimeProbe = @'
import importlib.util, json, sys
result = {'interpreter': sys.executable, 'torch': None, 'onnxruntime': None}
if importlib.util.find_spec('torch'):
    try:
        import torch
        result['torch'] = {'version': str(torch.__version__), 'cuda_build': torch.version.cuda, 'cuda_available': torch.cuda.is_available()}
        if result['torch']['cuda_available']:
            result['torch']['devices'] = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
    except Exception as error:
        result['torch'] = {'error': str(error)}
else:
    result['torch'] = {'installed': False}
if importlib.util.find_spec('onnxruntime'):
    try:
        import onnxruntime
        result['onnxruntime'] = {'version': onnxruntime.__version__, 'providers': onnxruntime.get_available_providers()}
    except Exception as error:
        result['onnxruntime'] = {'error': str(error)}
else:
    result['onnxruntime'] = {'installed': False}
print(json.dumps(result, ensure_ascii=True))
'@
    $runtimeOutput = & $resolvedPython.FullName -c $runtimeProbe 2>&1
    $runtimeExit = $LASTEXITCODE
    if ($runtimeExit -eq 0) {
        try { $gpuReport.runtime = ($runtimeOutput -join "`n") | ConvertFrom-Json }
        catch { $gpuReport.runtime = @{ exitCode = $runtimeExit; error = 'Runtime output was not clean JSON'; output = @($runtimeOutput | ForEach-Object { "$_" }) } }
    } else {
        $gpuReport.runtime = @{ exitCode = $runtimeExit; output = @($runtimeOutput | ForEach-Object { "$_" }) }
    }
} else {
    $gpuReport.runtime = @{ verified = $false; note = 'No project interpreter supplied; framework capability is unknown' }
}
$gpuReport | ConvertTo-Json -Depth 8
