# Diyse Asset Source Archive Manifest

**Status:** Authoritative checksum manifest for the source archives represented by Asset Library Master v5  
**Generated:** 2026-08-31  
**Total source ZIP bytes:** **2,245,575,854**

This manifest records the exact source archives used to build the current consolidated asset inventory. It does **not** assert that every archive is legally redistributable. Provenance and license handling remain controlled by `docs/assets/README.md` and the v5 master inventory.

| Archive | Bytes | Files | SHA-256 |
|---|---:|---:|---|
| `1-6.zip` | 99317080 | 224 | `82405cf5556c7f655d10ed34aade763379cbb5bf7a18e0c2ff5974fab91ad86f` |
| `7-9.zip` | 108300708 | 175 | `295be5fc8ecf7d0775391af8372b90b941a153c1aabae523a9aff8fe8800bd1d` |
| `10-13.zip` | 74401884 | 157 | `02eda36dbef067ce01cb857ea44dacd22c779e7a1e28ce37a8ae5585ab793e41` |
| `14-18.zip` | 65700997 | 98 | `1789257a34f2a91b3695f23ea689acaba777f22b05ae54474fce3ef05622feaa` |
| `19-22.zip` | 42401449 | 92 | `c2e15b486f7d27190fe40edb5780228edc2da2b294d134468b435f6057109789` |
| `23-27.zip` | 57912991 | 108 | `a89c80ce13488f03f8c76af671d19040b9ac9935c03afededbbc8da0796cc135` |
| `28-31.zip` | 47834424 | 26 | `aca9bf6240841e40fae26814dbc29cebe900d47f8a58c99709496cf3c89d6b81` |
| `32-39.zip` | 66343254 | 122 | `9569dc413ebdfde10781dd22445d129113861adecc424b0438f16add80e214bd` |
| `40-45.zip` | 61846258 | 110 | `43fdac3c70eedb9b4970d94b5e2a97df48780ba241dad70dff4d0f0d059d7d71` |
| `46-50.zip` | 51013995 | 154 | `e37eafd79df7e2516fa98108bb19a95157270e655315d66dc16f46b8cdc3cace` |
| `51-60.zip` | 178052699 | 205 | `cf2befa7ccdb3224f47d95c96ca10a096fe58339f690ee825194d2d4f93534df` |
| `61-67.zip` | 111050115 | 405 | `05c72be68447f8b9f6e1e31306aba2de927cb9c3e8e58affca18d048ecb7c887` |
| `68-72.zip` | 122929170 | 201 | `e761ff3424fc3c2c02870d9e8caab7d14835fbb752566cc6ee0f4d21e121fdad` |
| `73-75.zip` | 91634544 | 185 | `55513e0f1271f221826c22f4cc95060b631e459f2d404e64820f61aef28a2b91` |
| `76-79.zip` | 189768960 | 166 | `f587d1ed1b78bff8f0f921067c4d722984fde4e5c72888cc96372e3945834fd6` |
| `080.zip` | 50055152 | 17 | `e2e2031ddcbd319e27c03be770a2552d3cd650f20e1186513775dcbb777916f0` |
| `81-84.zip` | 175652022 | 219 | `05173e63b09f45cce9654672a80f2c27e961739761811da79b97ad9c4a50a5e3` |
| `85-90.zip` | 177490415 | 234 | `0883c43d26602fa0d3797fe7d31f21b2848a978637e1c36bbb076e28c852b86a` |
| `91-95.zip` | 77839592 | 149 | `ffb001e2ec67afc86ad7a6fc9e22235f9e47729da8d2cdba4fe7a5749af8e2e5` |
| `96-105.zip` | 84193870 | 103 | `e0b37e17a4ef94facf78f4f65bf5cd30b3f5970dc6e2856aad63df8369aea86b` |
| `106-111.zip` | 75330367 | 70 | `89c5b5f030afc7462df960d4b2743ffc6f6175459be5499e4bc98787419d0063` |
| `112-116.zip` | 51652612 | 11 | `8892990dac8e05b9757562121a26553c5cf916bde37332894ca280426f4ac14e` |
| `Fantasy Props MegaKit[Standard].zip` | 150213360 | 517 | `8b6f7e806d222e585478f0e1bdc6b271bbc7bc6f84dd6af8ca703a7c64f0cb1e` |
| `Universal Animation Library[Standard].zip` | 15904933 | 9 | `cc73fc4e495b82958207316596317a3f40b9fa38065bde1027937452da537724` |
| `Universal Animation Library 2[Standard].zip` | 18735003 | 13 | `4008ea208a604773a2b2177d965f0f5d3195498b5bf838c3f5785d68e95f2a68` |

## Canonicalization notes

- `080.zip` and `81-84.zip` contain the same 17 Map080 files byte-for-byte. The master inventory counts that Map080 set only once canonically.
- Earlier `10-12.zip`, `13-19.zip`, and `20-28.zip` uploads were diagnostic/superseded because many later files were zero-byte. They are intentionally **not** part of this authoritative source manifest.
- Map093 is present despite its unusual `map_093` filename convention.
- The current missing map numbers through 116 are 015, 033, 042, 085, 097, 098, 099, 101, and 102.

## Verification rule

Before a raw source archive is accepted into future Git LFS, external object storage, or another archival location, verify its SHA-256 against this manifest. A mismatch means it is not the same source archive used for Asset Library Master v5 and must be investigated before replacing the authority copy.
