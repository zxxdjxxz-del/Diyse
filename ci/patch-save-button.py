from pathlib import Path

root = Path("source")

state_path = root / "core/src/main/java/com/dj/diyse/model/GameState.java"
state = state_path.read_text()
old_save = '''    public void save() {
        Preferences preferences = Gdx.app.getPreferences(PREFS);
        preferences.putBoolean("save_exists", true);
        preferences.putFloat("player_x", playerX);
        preferences.putFloat("player_y", playerY);
        preferences.putInteger("healing_draughts", healingDraughts);
        preferences.putBoolean("encounter_cleared", prototypeEncounterCleared);
        for (int i = 0; i < party.size; i++) {
            CharacterState member = party.get(i);
            String prefix = "party_" + i + "_";
            preferences.putInteger(prefix + "level", member.level);
            preferences.putInteger(prefix + "xp", member.xp);
            preferences.putInteger(prefix + "hp", member.hp);
            preferences.putInteger(prefix + "max_hp", member.maxHp);
            preferences.putInteger(prefix + "resource", member.resource);
            preferences.putInteger(prefix + "max_resource", member.maxResource);
            preferences.putInteger(prefix + "attack", member.attack);
            preferences.putInteger(prefix + "defense", member.defense);
            preferences.putInteger(prefix + "magic", member.magic);
            preferences.putInteger(prefix + "resistance", member.resistance);
            preferences.putInteger(prefix + "speed", member.speed);
        }
        preferences.flush();
        hasSave = true;
    }
'''
new_save = '''    public boolean save() {
        try {
            Preferences preferences = Gdx.app.getPreferences(PREFS);
            preferences.putBoolean("save_exists", true);
            preferences.putFloat("player_x", playerX);
            preferences.putFloat("player_y", playerY);
            preferences.putInteger("healing_draughts", healingDraughts);
            preferences.putBoolean("encounter_cleared", prototypeEncounterCleared);
            for (int i = 0; i < party.size; i++) {
                CharacterState member = party.get(i);
                String prefix = "party_" + i + "_";
                preferences.putInteger(prefix + "level", member.level);
                preferences.putInteger(prefix + "xp", member.xp);
                preferences.putInteger(prefix + "hp", member.hp);
                preferences.putInteger(prefix + "max_hp", member.maxHp);
                preferences.putInteger(prefix + "resource", member.resource);
                preferences.putInteger(prefix + "max_resource", member.maxResource);
                preferences.putInteger(prefix + "attack", member.attack);
                preferences.putInteger(prefix + "defense", member.defense);
                preferences.putInteger(prefix + "magic", member.magic);
                preferences.putInteger(prefix + "resistance", member.resistance);
                preferences.putInteger(prefix + "speed", member.speed);
            }
            preferences.flush();

            Preferences verification = Gdx.app.getPreferences(PREFS);
            boolean verified = verification.getBoolean("save_exists", false)
                && Math.abs(verification.getFloat("player_x", Float.NaN) - playerX) < 0.01f
                && Math.abs(verification.getFloat("player_y", Float.NaN) - playerY) < 0.01f
                && verification.getInteger("healing_draughts", -1) == healingDraughts
                && verification.getBoolean("encounter_cleared", !prototypeEncounterCleared) == prototypeEncounterCleared;
            for (int i = 0; i < party.size && verified; i++) {
                CharacterState member = party.get(i);
                String prefix = "party_" + i + "_";
                verified = verification.getInteger(prefix + "level", -1) == member.level
                    && verification.getInteger(prefix + "xp", -1) == member.xp
                    && verification.getInteger(prefix + "hp", -1) == member.hp
                    && verification.getInteger(prefix + "resource", -1) == member.resource;
            }

            hasSave = verified;
            if (!verified) {
                Gdx.app.error("Diyse", "Save verification failed after Preferences.flush().");
            }
            return verified;
        } catch (RuntimeException exception) {
            Gdx.app.error("Diyse", "Unable to save the current game state.", exception);
            return false;
        }
    }
'''
if old_save not in state:
    raise SystemExit("Expected GameState.save implementation was not found.")
state_path.write_text(state.replace(old_save, new_save, 1))

screen_path = root / "core/src/main/java/com/dj/diyse/screens/CourtyardScreen.java"
screen = screen_path.read_text()
replacements = [
    (
        "    private final Label status;\n",
        "    private final Label status;\n    private final Label saveNotice;\n    private final TextButton saveButton;\n",
    ),
    (
        "    private boolean down;\n",
        "    private boolean down;\n    private float saveFeedbackSeconds;\n",
    ),
    (
        '''        TextButton save = new TextButton("Save", game.skin());
        save.setBounds(1080, 650, 150, 48);
        save.addListener(new com.badlogic.gdx.scenes.scene2d.utils.ClickListener() {
            @Override
            public void clicked(InputEvent event, float x, float y) {
                persistPosition();
                status.setText("Game saved. Individual levels and XP are stored.");
            }
        });
        stage.addActor(save);
''',
        '''        saveNotice = new Label("", game.skin(), "gold");
        saveNotice.setAlignment(Align.center);
        saveNotice.setBounds(965, 540, 300, 28);
        stage.addActor(saveNotice);

        saveButton = new TextButton("Save Game", game.skin());
        saveButton.setBounds(1000, 575, 230, 70);
        saveButton.getLabel().setFontScale(1.15f);
        saveButton.addListener(new com.badlogic.gdx.scenes.scene2d.utils.ClickListener() {
            @Override
            public void clicked(InputEvent event, float x, float y) {
                boolean saved = persistPosition();
                saveFeedbackSeconds = 2.5f;
                if (saved) {
                    saveButton.setText("SAVED");
                    saveNotice.setText("Progress saved successfully");
                    status.setText("Game saved. Position, items, HP, levels, and individual XP are stored.");
                } else {
                    saveButton.setText("SAVE FAILED");
                    saveNotice.setText("Could not verify the save");
                    status.setText("Save failed. Please try again before leaving the courtyard.");
                }
            }
        });
        stage.addActor(saveButton);
''',
    ),
    (
        '''    private void persistPosition() {
        game.state().setPlayerPosition(playerX, playerY);
        game.state().save();
    }
''',
        '''    private boolean persistPosition() {
        game.state().setPlayerPosition(playerX, playerY);
        return game.state().save();
    }
''',
    ),
    (
        '''        stage.act(Math.min(delta, 1f / 30f));
        stage.draw();
    }

    @Override
    public void hide() {
        persistPosition();
    }
''',
        '''        if (saveFeedbackSeconds > 0f) {
            saveFeedbackSeconds -= delta;
            if (saveFeedbackSeconds <= 0f) {
                saveButton.setText("Save Game");
                saveNotice.setText("");
            }
        }

        stage.act(Math.min(delta, 1f / 30f));
        stage.draw();
    }

    @Override
    public void pause() {
        persistPosition();
    }

    @Override
    public void hide() {
        persistPosition();
    }
''',
    ),
]
for old, new in replacements:
    if old not in screen:
        raise SystemExit("Expected CourtyardScreen save-button block was not found.")
    screen = screen.replace(old, new, 1)
screen_path.write_text(screen)
