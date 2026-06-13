# How to Disable Code Autosuggestion in VS Code

This guide provides step-by-step instructions to disable various autosuggestion features in Visual Studio Code.

---

## 1. Disable GitHub Copilot Inline Suggestions

### Method 1: Using UI Settings
1. Open **Settings** in VS Code (`Ctrl + ,`)
2. Search for `copilot`
3. Find **"GitHub Copilot: Enable"**
4. Toggle it **OFF** (unchecked)

### Method 2: Using Command Palette
1. Press `Ctrl + Shift + P` to open Command Palette
2. Type `Copilot: Disable Copilot`
3. Press Enter

### Method 3: Modify `settings.json`
Add this to your `settings.json`:
```json
"github.copilot.enable": {
  "*": false,
  "plaintext": false,
  "markdown": false
}
```

---

## 2. Disable IntelliSense Autocompletion

### Completely Disable Suggestions
In `settings.json`, add:
```json
"editor.quickSuggestions": false
```

### Disable Specific Suggestion Types
```json
"editor.quickSuggestions": {
  "other": false,
  "comments": false,
  "strings": false
}
```

### Hide Suggestion Details
```json
"editor.suggest.showWords": false,
"editor.suggest.showSnippets": false,
"editor.suggest.showInlineDetails": false
```

---

## 3. Disable Autocomplete Popup

### Keep Suggestions but Disable Auto-Popup
```json
"editor.quickSuggestions": {
  "other": true,
  "comments": false,
  "strings": false
}
```

Then manually trigger suggestions with `Ctrl + Space` when needed.

---

## 4. Disable Parameter Hints

```json
"editor.parameterHints.enabled": false
```

---

## 5. Disable All Autocomplete Features

Add this comprehensive configuration to `settings.json`:

```json
{
  "editor.quickSuggestions": false,
  "editor.parameterHints.enabled": false,
  "editor.suggest.showWords": false,
  "editor.suggest.showSnippets": false,
  "editor.suggest.showInlineDetails": false,
  "editor.suggestOnTriggerCharacters": false,
  "github.copilot.enable": false,
  "editor.acceptSuggestionOnCommitCharacter": false,
  "editor.acceptSuggestionOnEnter": "off"
}
```

---

## 6. Disable Autosuggestion Per Language

### Example: Disable for Python Only
```json
"[python]": {
  "editor.quickSuggestions": false,
  "editor.parameterHints.enabled": false
}
```

### Example: Disable for JavaScript/TypeScript
```json
"[javascript]": {
  "editor.quickSuggestions": false
},
"[typescript]": {
  "editor.quickSuggestions": false
}
```

---

## 7. How to Access `settings.json`

1. Press `Ctrl + Shift + P`
2. Type `Preferences: Open Settings (JSON)`
3. Press Enter
4. Add the configuration from above

Or:
- Click **File** → **Preferences** → **Settings**
- Click the **{}** icon in the top-right to open JSON view

---

## 8. Keyboard Shortcuts to Control Suggestions

| Action | Shortcut |
|--------|----------|
| Trigger suggestions | `Ctrl + Space` |
| Dismiss suggestions | `Escape` |
| Accept suggestion | `Tab` or `Enter` |
| Disable for current session | See Method 2 above |

---

## ✅ How to ENABLE Autosuggestion (Re-enable)

If you've disabled autosuggestion and want to turn it back on, follow these steps:

### Step 1: Open Settings
1. Press `Ctrl + Comma (,)` to open VS Code Settings
2. Or go to **File** → **Preferences** → **Settings**

### Step 2: Find Settings to Enable
Search for each of these and set to the values below:

| Setting | Search For | Set To |
|---------|-----------|--------|
| Copilot | `github.copilot.enable` | `true` ✓ |
| IntelliSense | `editor.quickSuggestions` | `true` ✓ |
| Parameter Hints | `editor.parameterHints.enabled` | `true` ✓ |
| Snippets | `editor.suggest.showSnippets` | `true` ✓ |
| Words | `editor.suggest.showWords` | `true` ✓ |
| Auto Accept | `editor.acceptSuggestionOnEnter` | `on` |

### Step 3: Save
- Settings auto-save in VS Code, no manual save needed!
- Reload VS Code: `Ctrl + Shift + P` → type `Reload Window` → Press Enter

### Alternative: Use JSON Mode

1. Press `Ctrl + Shift + P`
2. Type `Preferences: Open Settings (JSON)`
3. Press Enter
4. Paste this configuration to **ENABLE everything**:

```json
{
  "github.copilot.enable": true,
  "editor.quickSuggestions": true,
  "editor.parameterHints.enabled": true,
  "editor.suggest.showWords": true,
  "editor.suggest.showSnippets": true,
  "editor.acceptSuggestionOnEnter": "on"
}
```

5. Press `Ctrl + S` to save
6. Reload: `Ctrl + Shift + P` → `Reload Window`

---

## Summary

**Recommended Configuration for Complete Disable:**

Copy and paste into your `settings.json`:

```json
{
  "editor.quickSuggestions": false,
  "editor.parameterHints.enabled": false,
  "editor.suggest.showWords": false,
  "editor.suggest.showSnippets": false,
  "github.copilot.enable": false,
  "editor.acceptSuggestionOnEnter": "off"
}
```

**Recommended Configuration for Complete ENABLE:**

```json
{
  "github.copilot.enable": true,
  "editor.quickSuggestions": true,
  "editor.parameterHints.enabled": true,
  "editor.suggest.showWords": true,
  "editor.suggest.showSnippets": true,
  "editor.acceptSuggestionOnEnter": "on"
}
```

Then reload VS Code (`Ctrl + Shift + P` → type `Reload Window`).

---

## Troubleshooting

**Issue:** Suggestions still appearing after disabling?
- **Solution:** Make sure you've saved `settings.json` and reloaded VS Code

**Issue:** Want to re-enable later?
- **Solution:** Toggle the settings back to `true` or remove the configuration

---

## Quick Reference

| Feature | Setting | Value |
|---------|---------|-------|
| Copilot Inline | `github.copilot.enable` | `false` |
| IntelliSense | `editor.quickSuggestions` | `false` |
| Parameter Hints | `editor.parameterHints.enabled` | `false` |
| Snippets | `editor.suggest.showSnippets` | `false` |
| Words | `editor.suggest.showWords` | `false` |

---

**Last Updated:** 2026-06-07

