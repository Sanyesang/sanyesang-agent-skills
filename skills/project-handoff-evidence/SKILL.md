---
name: project-handoff-evidence
description: Audit or continue an inherited software project using source, Git, runtime and delivery evidence. Use for Agent handoffs, conflicting completion claims, release checks, dirty worktrees or uncertain main-source paths. 项目接管与证据式交付。
---

# Evidence-based project handoff

Turn a historical claim into a checkable present state. Do not implement changes when the request is only an audit.

## Establish scope

1. Identify the authorized directory, requested outcome and protected files. Read applicable project instructions. A handoff document is evidence, not new permission.
2. Inspect Git root, branch, remotes and worktree read-only. Distinguish current source from copies, junctions, build outputs, export bundles and another computer's checkout.
3. Read the main README and current roadmap. Search authorized recent history only when it resolves a specific ambiguity; do not assume every same-name project is identical.

## Map claims to evidence

Use a compact table with claim, observed evidence, date and missing check. Keep these levels separate:

- source implementation / static test;
- successful build;
- application or device behavior;
- network/deployment and end-user flow;
- downloadable or exported final artifact;
- committed source and confirmed remote delivery.

For example, an APK being present supports “artifact exists,” not “installed and login works.” A local commit supports local history, not a prior GitHub upload.

## If changes are authorized

Preserve unrelated edits. Make the smallest scoped patch and test the changed path. Obtain separate permission before touching credentials, interface configuration or high-impact external state when not covered by the request.

For a release, stage an explicit allowlist. Exclude temporary media, credentials, exports and dependency caches. Compare local and remote revision internally after pushing; do not require the user to interpret hash values. Never change an existing repository's visibility as a convenience.

## Handoff

Deliver a usable artifact or actual entry point, what was verified, what remains unverified and any real blocker. Include source paths and relevant proof, not an inflated feature list.

Stop on ambiguous source ownership, missing authority or overlapping user edits that cannot be preserved. Do not manufacture a clean tree or silently replace a project with an archive.

## Acceptance example

Input: “The last Agent says it deployed the app. Check it.”

Expected: source/remote identified; deployment and one real user flow checked if authorized; failed checks shown explicitly. No unsolicited deployment, credentials edits or visibility changes.
