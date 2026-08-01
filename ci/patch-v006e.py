from pathlib import Path

root = Path("source")

def replace_once(relative, old, new):
    path = root / relative
    text = path.read_text()
    if old not in text:
        raise SystemExit(f"v0.06E expected marker missing in {relative}: {old[:80]}")
    path.write_text(text.replace(old, new, 1))

replace_once("core/src/main/java/com/dj/diyse/DiyseGame.java", 'VERSION = "0.06D"', 'VERSION = "0.06E"')
replace_once("core/src/main/java/com/dj/diyse/model/GameState.java", 'putString("save_build", "0.06D")', 'putString("save_build", "0.06E")')
replace_once("android/build.gradle", "versionCode 9", "versionCode 10")
replace_once("android/build.gradle", "versionName '0.06D'", "versionName '0.06E'")
replace_once("core/src/test/java/com/dj/diyse/VersionContractTest.java", 'assertEquals("0.06D", DiyseGame.VERSION);', 'assertEquals("0.06E", DiyseGame.VERSION);')

battle_path = root / "core/src/main/java/com/dj/diyse/screens/BattleScreen.java"
battle = battle_path.read_text()
import_old = "import com.dj.diyse.combat.BattleAction;\n"
import_new = "import com.dj.diyse.combat.BattleAction;\nimport com.dj.diyse.combat.BattleArenaOrientation;\n"
if import_old not in battle:
    raise SystemExit("v0.06E BattleScreen import marker missing")
battle = battle.replace(import_old, import_new, 1)
old_draw = '''        float shake = activeAction == null ? 0f : presentation.shakeX();
        game.batch().draw(arenaBackground, shake, 0, DiyseGame.WORLD_WIDTH, DiyseGame.WORLD_HEIGHT);
        game.batch().setColor(1f, 1f, 1f, 0.72f);
        game.batch().draw(arenaAtmosphere, (float)Math.sin(visualClock * 0.45f) * 5f, 0,
            DiyseGame.WORLD_WIDTH, DiyseGame.WORLD_HEIGHT);
        game.batch().setColor(1f, 1f, 1f, 1f);

        drawSelectionRings();
        drawPartyModels();
        drawEnemyModels();
        drawActionEffect();
        game.batch().draw(arenaForeground, shake * 0.35f, 0, DiyseGame.WORLD_WIDTH, DiyseGame.WORLD_HEIGHT);
'''
new_draw = '''        float shake = activeAction == null ? 0f : presentation.shakeX();
        float[] backgroundDraw = BattleArenaOrientation.upright(
            shake, 0f, DiyseGame.WORLD_WIDTH, DiyseGame.WORLD_HEIGHT);
        game.batch().draw(arenaBackground, backgroundDraw[0], backgroundDraw[1], backgroundDraw[2], backgroundDraw[3]);
        game.batch().setColor(1f, 1f, 1f, 0.72f);
        float[] atmosphereDraw = BattleArenaOrientation.upright(
            (float)Math.sin(visualClock * 0.45f) * 5f, 0f, DiyseGame.WORLD_WIDTH, DiyseGame.WORLD_HEIGHT);
        game.batch().draw(arenaAtmosphere, atmosphereDraw[0], atmosphereDraw[1], atmosphereDraw[2], atmosphereDraw[3]);
        game.batch().setColor(1f, 1f, 1f, 1f);

        drawSelectionRings();
        drawPartyModels();
        drawEnemyModels();
        drawActionEffect();
        float[] foregroundDraw = BattleArenaOrientation.upright(
            shake * 0.35f, 0f, DiyseGame.WORLD_WIDTH, DiyseGame.WORLD_HEIGHT);
        game.batch().draw(arenaForeground, foregroundDraw[0], foregroundDraw[1], foregroundDraw[2], foregroundDraw[3]);
'''
if old_draw not in battle:
    raise SystemExit("v0.06E BattleScreen arena draw block missing")
battle_path.write_text(battle.replace(old_draw, new_draw, 1))

(root / "core/src/main/java/com/dj/diyse/combat/BattleArenaOrientation.java").write_text('''package com.dj.diyse.combat;

/**
 * Converts full-screen Pixmap-authored battle arena layers into upright SpriteBatch draw rectangles.
 * This transform is intentionally separate from battle-model orientation so arena and character
 * regression tests can fail independently.
 */
public final class BattleArenaOrientation {
    private BattleArenaOrientation() { }

    public static float[] upright(float x, float y, float width, float height) {
        return new float[] { x, y + height, width, -height };
    }
}
''')

(root / "core/src/test/java/com/dj/diyse/combat/BattleArenaOrientationTest.java").write_text('''package com.dj.diyse.combat;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;

public final class BattleArenaOrientationTest {
    @Test
    void fullScreenArenaUsesOneVerticalCorrection() {
        assertArrayEquals(new float[] { 0f, 720f, 1280f, -720f },
            BattleArenaOrientation.upright(0f, 0f, 1280f, 720f));
    }

    @Test
    void screenShakeOffsetDoesNotChangeOrientation() {
        assertArrayEquals(new float[] { 7f, 720f, 1280f, -720f },
            BattleArenaOrientation.upright(7f, 0f, 1280f, 720f));
    }
}
''')

(root / "docs/CHANGELOG_v0.06E.md").write_text('''# Diyse Prototype v0.06E — Battle Background Orientation Correction

- Corrects the device-confirmed vertical inversion of the layered battle arena.
- Applies exactly one vertical correction to the background, atmosphere, and foreground layers.
- Keeps the v0.06D upright party and mirrored-upright Black Host model transforms unchanged.
- Adds independent arena-orientation tests so model and background regressions cannot mask one another.
- Preserves Item → Defend → Speed resolution, enemy action locking, targeting, damage formulas, MP costs, one-impact presentation timing, encounter XP, progression, victory/defeat behavior, and Save schema 3.
- Uses the current v0.80 active master canon authority.
- The exact Crest of Yahtrea is not approximated.
- Arena art, models, effects, and timing remain provisional test presentation.
''')

checklist_path = root / "docs/TEST_CHECKLIST.md"
checklist = checklist_path.read_text()
section = '''
## v0.06E Battle Background Orientation
- [ ] Battle arena wall, arches, floor, central inlay, breach glow, and torchlight are upright.
- [ ] Background, atmosphere, and foreground remain aligned during screen shake.
- [ ] Party models remain upright.
- [ ] Black Host models remain upright and horizontally mirrored toward the party.
- [ ] Attack, cast, guard, hurt, down, and victory poses remain upright.
- [ ] Combat order, damage, targeting, saving, and progression remain unchanged.
'''
if "## v0.06E Battle Background Orientation" in checklist:
    raise SystemExit("v0.06E checklist section already exists")
checklist_path.write_text(checklist + section)

battle = battle_path.read_text()
for marker in (
    "BattleArenaOrientation.upright", "backgroundDraw", "atmosphereDraw", "foregroundDraw",
    "BattleModelOrientation.upright(x, y, p[2], p[3], false)",
    "BattleModelOrientation.upright(x, y, p[2], p[3], true)",
    "Items → Defend → Speed.", "EnemyBehavior.lockActions", "ENCOUNTER_XP = 40",
    "attack + power - defense / 2", "magic + power - resistance / 2", "presentation.consumeImpact",
):
    if marker not in battle:
        raise SystemExit(f"v0.06E verification failed for {marker}")
if battle.count("BattleArenaOrientation.upright") != 3 or battle.count("BattleModelOrientation.upright") != 2:
    raise SystemExit("v0.06E orientation call-count verification failed")

android_gradle = (root / "android/build.gradle").read_text()
for marker in ("versionCode 10", "versionName '0.06E'", "diyse-prototype.keystore", "signingConfig signingConfigs.prototype"):
    if marker not in android_gradle:
        raise SystemExit(f"v0.06E Android verification failed for {marker}")
if 'SAVE_SCHEMA_VERSION = 3' not in (root / "core/src/main/java/com/dj/diyse/model/GameState.java").read_text():
    raise SystemExit("v0.06E changed save schema")
if (root / "android/prototype-signing/diyse-prototype.keystore").stat().st_size < 1000:
    raise SystemExit("v0.06E permanent prototype keystore is missing or truncated")

print("Applied Diyse Prototype v0.06E battle background orientation correction.")
