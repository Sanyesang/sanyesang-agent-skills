---
name: windows-gpu-runtime-audit
description: Diagnose Windows applications that use CPU despite a GPU, separating physical device recognition, driver health, framework capability, selected device and observed workload. Use for CUDA, PyTorch, ONNX Runtime, local TTS and rendering questions. Windows GPU 分层核验。
---

# GPU runtime audit

Use read-only checks first. Do not upgrade drivers, install a different framework or modify application/API configuration unless separately authorized.

## Four distinct layers

1. **Hardware:** Windows device inventory and status. Missing NVIDIA utilities do not prove missing hardware.
2. **Driver:** vendor utility/version and error. A functioning device can coexist with a broken or inaccessible utility; retain both observations.
3. **Exact runtime:** the interpreter/process used by this project, framework version, CUDA build and available providers. A CPU-only virtual environment tells you about that environment, not the whole machine.
4. **Actual execution:** selected device, model/tensor placement, application logs and workload evidence. Available CUDA is not proof the app chose it. GPU activity from unrelated processes is not proof of this application's use.

## Helper

Run `scripts/audit_gpu.ps1` with PowerShell 7. Supply `-PythonPath` using the interpreter the project actually launches. Omitting it intentionally leaves framework checks unverified. No dependencies are installed.

The helper reports device/driver checks and Python framework capability as JSON, including nonzero command exits. It does not generate audio, select devices or benchmark the application. A returned provider list needs a separate execution observation.

## Reach a bounded conclusion

Report one of: device absent; device/driver issue; hardware and driver present but current runtime lacks GPU capability; application selected CPU; application observed using GPU; insufficient evidence. Combine labels when needed and cite which observation supports each part.

Recommend the smallest fix only after identifying the failing layer. Shared global dependencies and driver changes can affect other projects; propose the exact environment and verification before editing.

Acceptance example: CPU-only PyTorch in the target venv plus a healthy NVIDIA device is described as an environment issue, not “your computer has no CUDA.” If the interpreter was not supplied, the runtime remains unverified.
