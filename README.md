# audio-notes

トピックを調査し、音声読み上げ用のノートを作って公開するためのリポジトリです。Microsoft Edge（読み上げ／Immersive Reader）で、その場を耳だけで聞くことを目的としています。

ブラウザさえあれば、どんな環境からもアクセスできます。これまで試した読み上げアプリやブラウザの中で、読み上げ品質・機能性・読み上げ可能文字数のバランスが最も良かったのがEdgeでした。

## 仕組み

1. トピックを調査し、TTS向けに最適化したMarkdown原稿（`notes/<slug>.md`）を作成します。
2. `python3 build_note.py <slug>.md "<タイトル>"` で、`note-template.html` を使ってMarkdownをHTML（`notes/<slug>.html`）に変換します。
3. `notes/<slug>.md` と `notes/<slug>.html` を `main` にpushすると、GitHub Pagesで以下のURLに公開されます。
   ```
   https://soh-arch.github.io/audio-notes/notes/<slug>.html
   ```
4. 公開後、Slackへ通知します（投稿先チャンネルは環境変数 `AUDIO_NOTES_SLACK_CHANNEL_ID` で指定します）。

## ディレクトリ構成

- `notes/` — 公開済みのノート本体（`<slug>.md` と `<slug>.html` のペア）。
- `build_note.py` / `note-template.html` — Markdown→HTML変換スクリプトとテンプレート。
- `.claude/skills/` — 原稿作成に使うスキル。

作業の詳細な手順とルールは [`CLAUDE.md`](./CLAUDE.md) を参照してください。
