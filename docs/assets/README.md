# Diyse Asset Library

**Status:** Authoritative repository routing for the project asset inventory  
**Added:** 2026-08-31

This directory preserves the consolidated Diyse asset-library work created during the August 30–31, 2026 asset pass.

## Current authority

The current consolidated inventory is **DIYSE Asset Library Master v5**.

Repository preservation is split into exact UTF-8 parts under:

`docs/assets/archive/DIYSE_ASSET_LIBRARY_MASTER_2026-08-30_v5/`

Concatenating `part_01.txt` through `part_10.txt` in numeric order reconstructs the original master file byte-for-byte as UTF-8 text.

- Original master SHA-256: `17648aadd7ad28570b9a017a03362041875e6fa10df173315871dfcb89d57246`
- Original master character count: `175133`
- Original master version: `v5`
- Original master date: `2026-08-30`

The exact source-archive names, sizes, member counts, and SHA-256 hashes are recorded in `SOURCE_ARCHIVE_MANIFEST.md`.

## Current inventory totals

- **3,214** canonical extracted map/environment TGA records.
- **2,878** exact-unique extracted TGAs after byte-level deduplication.
- **107** represented source map families across Maps 001–116.
- Missing map numbers through 116: **015, 033, 042, 085, 097, 098, 099, 101, 102**.
- **94** verified-CC0 Quaternius Fantasy Props MegaKit models.
- **86** verified-CC0 Quaternius humanoid animation clips across Universal Animation Library 1 and 2.

## Provenance separation

The extracted Map001–Map116 texture material is **license-unverified extracted source material**. It must not be relabeled as CC0 or freely redistributable material. Keep it segregated from verified-open assets and treat it as private/reference/prototyping material unless rights are separately confirmed.

The Quaternius Fantasy Props MegaKit and both Universal Animation Libraries are verified **CC0 1.0 Universal / Public Domain Dedication** and may be modified and used directly.

## Project-use rule

These extracted map textures are a **parts/reference library for building original Diyse maps**, not a target for reconstructing the source maps. Diyse layouts, collision, traversal, encounter placement, treasure placement, camera design, landmarks, faction identity, and final environment composition remain original project work.

## Raw binary storage

The authoritative source ZIP set represented by the manifest is approximately **2.25 GB**. Those binaries are not ordinary documentation and are not embedded into this Git repository by this preservation commit. Use the manifest hashes to verify any binary-source storage or future Git LFS/external archive import before treating it as authoritative.
