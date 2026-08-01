from pathlib import Path
import hashlib

parts = sorted((Path("ci") / "v007").glob("part-*.txt"))
if len(parts) != 6:
    raise SystemExit(f"Expected 6 Diyse v0.07 patch-source parts, found {len(parts)}")

source = "".join(part.read_text() for part in parts)
expected_sha256 = "98ab3a8773b24fc6e118f93a997770e8aad0215da50ea2936eb6806d6d0a08f8"
actual_sha256 = hashlib.sha256(source.encode()).hexdigest()
if actual_sha256 != expected_sha256:
    raise SystemExit(f"v0.07 patch-source checksum mismatch: {actual_sha256}")

exec(compile(source, "ci/v007/combined-patch.py", "exec"))
