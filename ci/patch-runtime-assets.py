from pathlib import Path

root = Path("source")


def replace_required(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if old not in text:
        raise SystemExit(f"Expected text not found in {path}: {old}")
    path.write_text(text.replace(old, new, 1))


def insert_import(path: Path, anchor: str, import_line: str) -> None:
    text = path.read_text()
    if import_line in text:
        return
    if anchor not in text:
        raise SystemExit(f"Import anchor not found in {path}: {anchor}")
    path.write_text(text.replace(anchor, anchor + import_line, 1))


title = root / "core/src/main/java/com/dj/diyse/screens/TitleScreen.java"
insert_import(title, "import com.dj.diyse.DiyseGame;\n", "import com.dj.diyse.ui.PrototypeArt;\n")
replace_required(
    title,
    '        background = new Texture("environments/title_background.png");',
    '        background = PrototypeArt.titleBackground();',
)

courtyard = root / "core/src/main/java/com/dj/diyse/screens/CourtyardScreen.java"
insert_import(courtyard, "import com.dj.diyse.DiyseGame;\n", "import com.dj.diyse.ui.PrototypeArt;\n")
replace_required(
    courtyard,
    '''        background = new Texture("environments/courtyard_background.png");
        foreground = new Texture("environments/courtyard_foreground.png");
        player = new Texture("characters/vanguard.png");''',
    '''        background = PrototypeArt.courtyardBackground();
        foreground = PrototypeArt.courtyardForeground();
        player = PrototypeArt.character(
            new Color(0.10f, 0.32f, 0.20f, 1f),
            new Color(0.88f, 0.72f, 0.26f, 1f),
            false);''',
)

battle = root / "core/src/main/java/com/dj/diyse/screens/BattleScreen.java"
insert_import(battle, "import com.badlogic.gdx.graphics.Texture;\n", "import com.badlogic.gdx.graphics.Color;\n")
insert_import(battle, "import com.dj.diyse.model.PrototypeData;\n", "import com.dj.diyse.ui.PrototypeArt;\n")
replace_required(
    battle,
    '''        background = new Texture("environments/battle_background.png");
        vanguard = new Texture("characters/vanguard.png");
        wardMage = new Texture("characters/ward_mage.png");
        guardian = new Texture("characters/guardian.png");
        ironCohort = new Texture("enemies/iron_cohort.png");
        warSorcerer = new Texture("enemies/war_sorcerer.png");''',
    '''        background = PrototypeArt.battleBackground();
        vanguard = PrototypeArt.character(
            new Color(0.10f, 0.34f, 0.20f, 1f),
            new Color(0.91f, 0.74f, 0.27f, 1f),
            false);
        wardMage = PrototypeArt.character(
            new Color(0.17f, 0.31f, 0.49f, 1f),
            new Color(0.86f, 0.82f, 0.68f, 1f),
            false);
        guardian = PrototypeArt.character(
            new Color(0.36f, 0.38f, 0.40f, 1f),
            new Color(0.88f, 0.72f, 0.26f, 1f),
            false);
        ironCohort = PrototypeArt.character(
            new Color(0.08f, 0.07f, 0.08f, 1f),
            new Color(0.62f, 0.04f, 0.03f, 1f),
            true);
        warSorcerer = PrototypeArt.character(
            new Color(0.07f, 0.04f, 0.09f, 1f),
            new Color(0.48f, 0.12f, 0.64f, 1f),
            true);''',
)

for screen in (title, courtyard, battle):
    text = screen.read_text()
    forbidden = (
        'environments/title_background.png',
        'environments/courtyard_background.png',
        'environments/courtyard_foreground.png',
        'environments/battle_background.png',
        'characters/vanguard.png',
        'characters/ward_mage.png',
        'characters/guardian.png',
        'enemies/iron_cohort.png',
        'enemies/war_sorcerer.png',
    )
    remaining = [value for value in forbidden if value in text]
    if remaining:
        raise SystemExit(f"Missing runtime asset references remain in {screen}: {remaining}")

print("Replaced missing image-file loads with generated runtime artwork.")
