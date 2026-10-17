# Vehido Translations

Community translations for **Vehido**, the app that tracks your vehicles' maintenance, expenses and budget.
Add your language or improve an existing one by editing a single file and opening a pull request.

Currently available: English (`en`, source), Vietnamese (`vi`).

## Layout

```
arb/
  app_en.arb      # English – the source of truth, do not change keys here
  app_vi.arb      # Vietnamese
  app_<code>.arb  # your language
scripts/
  check_translations.py   # validates a translation file
```

## How to contribute

1. **Fork** [cuongcds/vehido-translations](https://github.com/cuongcds/vehido-translations) and clone your fork.
2. **Copy the English file** to your language code (ISO 639-1, e.g. `th`, `fr`, `es`, `id`; regional variants like `pt_BR` or `zh_TW` are fine):
   ```bash
   cp arb/app_en.arb arb/app_th.arb
   ```
3. Edit `arb/app_th.arb`:
   - Set `"@@locale"` to your code (`"th"`).
   - Translate **only the values** (right side). Never change the keys.
4. **Validate**:
   ```bash
   python scripts/check_translations.py th
   ```
   Requires Python 3.9+. Fix every `ERROR`. `WARN missing key` is allowed (the app falls back to English), but aim for 100%.
5. **Commit and open a pull request** to `main`. Use the PR template and state the language.

Fixing a typo or improving an existing language works the same way: edit the file, run the check, open a PR.

## Translation rules

- **Keep placeholders exactly as they are**: `{appName}`, `{field}`, `{count}`… You may move them within the sentence, but not rename, translate or remove them.
- Entries starting with `@` (e.g. `"@fieldEnterPlaceholder"`) are metadata. Copy them as-is; do not translate them.
- Plural/select syntax such as `{count, plural, one{...} other{...}}`: keep the structure and keywords (`plural`, `one`, `other`), translate only the text inside the braces. Use the plural categories your language needs.
- Do not translate the brand name; it is injected via `{appName}`.
- Keep it short: strings appear on buttons and small screens. Match the tone of the English text (friendly, plain).
- Save as **UTF-8**, valid JSON (double quotes, no trailing commas). Use `\n` for line breaks as the English file does.
- Language names (`languageVietnamese`, `languageEnglish`, …) are translated like any other entry.

## What happens after your PR is merged

The maintainers pull this repo into the app, register the new locale in the app, run `flutter gen-l10n`, then build and publish a new release. Your language shows up in **Settings → Language** in that release, so it may take a little while after the merge.

## Maintainers: syncing with the app

The app's source of truth for new strings is `mobile/lib/l10n/app_en.arb`; keep `arb/app_en.arb` identical.

```bash
# App -> translations (after adding/changing strings in the app)
cp <app>/mobile/lib/l10n/app_en.arb arb/app_en.arb
python scripts/check_translations.py     # lists missing keys per language

# Translations -> app (before a release)
cp arb/app_*.arb <app>/mobile/lib/l10n/
cd <app>/mobile && flutter gen-l10n
```

For each new language also add `Locale('<code>')` to `supportedLocales` in `mobile/lib/app/locale_controller.dart` and a display name for the language picker, then build and submit.

## License

See [LICENSE](LICENSE).

---

## Tiếng Việt (tóm tắt)

1. Fork repo, copy `arb/app_en.arb` thành `arb/app_<mã-ngôn-ngữ>.arb` (ví dụ `app_th.arb`).
2. Đặt `"@@locale"` đúng mã ngôn ngữ, chỉ dịch phần **giá trị**, giữ nguyên key và các `{placeholder}`.
3. Chạy `python scripts/check_translations.py <mã>` cho tới khi không còn `ERROR`.
4. Commit và mở Pull Request. Sau khi merge, đội ngũ sẽ build và phát hành bản app có ngôn ngữ mới.
