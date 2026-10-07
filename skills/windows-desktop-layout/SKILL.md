---
name: windows-desktop-layout
description: Design or repair a Windows desktop icon layout using supported Shell identity, measured spacing, corner anchoring and verified rollback. Use when four-corner grouping fails, preview coordinates differ from Explorer, or icons do not reach the intended edge. Windows 桌面图标布局排查。
---

# Windows desktop layout

This is guidance for a layout tool, not permission to open, read, rename or move the files behind icons.

## Measure first

Read the active desktop view, work area, actual icon spacing and positions. Preserve user classification where it already exists. Detect automatic arrangement, DPI, grid snapping, monitor selection and occupied cells. Do not assume pixels are logical units or reuse a fixed 1920×1080 grid on other displays.

Use Shell APIs and stable item identity where supported: `IFolderView`, PIDLs, `GetSpacing`, and batch `SelectAndPositionItems`. Explorer's internal ListView is an implementation detail; a successful message return does not prove final positions changed.

## Plan four anchored regions

- Top-left: first available left/top cell, grow inward.
- Top-right: last valid right/top cell, grow leftward.
- Bottom-left: first left/last bottom cell, grow upward.
- Bottom-right: last right/bottom cell, grow leftward and upward.

Derive the last valid cell from measured work area, the view origin, icon footprint and spacing. “Half of the desktop” is a region boundary, not the starting column for right-hand groups. Do not accidentally reserve an extra full column on the right.

Compute all targets before changing anything. Reject duplicate cells, off-area footprints or insufficient capacity. Show grouping and overflow explicitly; do not silently overlap icons.

## Apply transactionally

1. Snapshot item identity and original coordinates; preserve existing snapshots.
2. Obtain the user's confirmation when the workflow requires it.
3. Apply the full plan by identity, not only display name or volatile list index.
4. Delay for Explorer settlement, reacquire the view and read every actual coordinate. Apply a documented tolerance consistent with measured snapping.
5. On failure, restore by identity and separately verify restoration. Report failed restore items; never claim rollback succeeded solely because the call returned.

Older snapshots with names need occurrence-aware matching for duplicates. Diagnostic snapshots must not displace the most recent user-operation recovery point.

## Validate the real result

Test uneven group sizes, a nearly full region, duplicate display names, changed DPI and non-default icon spacing. Check rightmost/bottommost occupied cells, no overlap and unchanged item count. A screenshot helps, but coordinate readback distinguishes preview from execution.

Stop if Shell discovery fails or the desktop is locked. Do not change OS security settings or force-kill Explorer to conceal a mismatch.

References: [Microsoft positioning sample](https://devblogs.microsoft.com/oldnewthing/20130318-00/?p=4933), [Windows icon-management changes](https://devblogs.microsoft.com/oldnewthing/20211122-00/?p=105948).
