## Summary

<!-- What changed and why -->

## Asset changes (if applicable)

<!-- List each sm_*.py file modified and the concept art it targets -->

| Script | Concept reference | Change summary |
|---|---|---|
| `sm_xxx.py` | AD-001 | Rewrote geometry to match ... |

## Visual acceptance checklist

For every changed asset script, confirm:

- [ ] CI passes (all 16 checks green)
- [ ] Render artifact (`*_preview.png`) downloaded and reviewed from Actions artifacts
- [ ] Comparison composite (`*_vs_concept.png`) shows a clear correspondence in silhouette shape, scale, and mass distribution
- [ ] Asset passes the silhouette language rules for its biome (`Docs/ASSET_QUALITY_STANDARDS.md`)
- [ ] No geometry anti-patterns visible (floating points, icosphere blob chains, zero-thickness planes)

## UE5 handoff checks (if exporting)

- [ ] Origin at base (set_origin_to_base called)
- [ ] Material slots named correctly (mat_*)
- [ ] FBX exported to Content/ArtSourceExports/<Category>/
- [ ] ASSET_NOTES.md updated

## Concept art comparison

<!-- Attach or link to the *_vs_concept.png images from the CI artifacts -->
<!-- These images are the primary acceptance gate — do not merge without reviewing them -->
