# audio-notes

トピックを調査し、音声読み上げ用のノートを作って公開するためのリポジトリです。iPhoneのMicrosoft Edge（読み上げ／Immersive Reader）で、その場を耳だけで聞くことを目的としています。

## 仕組み

1. トピックを調査し、TTS向けに最適化したMarkdown原稿（`<slug>.md`）を作成します。
2. `python3 build_note.py <slug>.md "<タイトル>"` で、`note-template.html` を使ってMarkdownをHTML（`<slug>.html`）に変換します。
3. `.md` と `.html` を `main` にpushすると、GitHub Pagesで以下のURLに公開されます。
   ```
   https://soh-arch.github.io/audio-notes/<slug>.html
   ```
4. 公開後、Slackへ通知します（投稿先チャンネルは環境変数 `AUDIO_NOTES_SLACK_CHANNEL_ID` で指定します）。

作業の詳細な手順とルールは [`CLAUDE.md`](./CLAUDE.md) を参照してください。
