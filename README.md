# audio-notes

トピックを調査し、音声読み上げ用のノートを作って公開するためのリポジトリです。Microsoft Edge（読み上げ／Immersive Reader）で、その場を耳だけで聞くことを目的としています。

ブラウザさえあれば、どんな環境からもアクセスできます。これまで試した読み上げアプリやブラウザの中で、読み上げ品質・機能性・読み上げ可能文字数のバランスが最も良かったのがEdgeでした。

## ノートを聞く

公開済みのノートは、GitHub Pagesで以下のURLから読めます。

```
https://soh-arch.github.io/audio-notes/notes/<slug>.html
```

Edgeでページを開き、読み上げ（Immersive Reader）を起動すると、そのまま本文が読み上げられます。ページは装飾の少ない静的HTMLなので、本文以外のUIが読み上げに混ざりません。

## ノートを作る

通常はClaude Codeに「〇〇について調査してください」と依頼すると、調査から公開・Slack通知までを一通り実行します。エージェントが従う手順は [`CLAUDE.md`](./CLAUDE.md) に書かれています。

手作業で変換だけを行う場合は、`notes/` に原稿（`<slug>.md`）を置いた上で、次のコマンドを実行します。

```
python3 build_note.py <slug>.md "<記事タイトル>"
```

`notes/<slug>.html` が生成されます。実行にはPython 3と `pandoc` が必要です。

## 原稿の書き方

原稿は「読む」ためではなく「聞く」ために書きます。箇条書きや記号を地の文に開き、参照は代名詞ではなく名詞で繰り返し、数値や単位は読み上げて意味が通る形にします。この方針は `.claude/skills/topic-to-audio-script/SKILL.md` にスキルとしてまとめてあり、Claude Codeが原稿を書くときに参照します。

## なぜこの構成なのか

読み上げを確実に動かせる配信形式が、実際に試すとかなり限られていたためです。

- GitHubの `raw.githubusercontent.com` は `Content-Security-Policy: sandbox` を付与するため、Edgeの読み上げが信頼できない文書とみなして動きません。
- GitHubのファイルプレビュー画面（blobページ）はUIノイズが多く、Edgeの本文抽出が本文を確信して拾えません。
- JavaScriptで後から本文を差し込むページも、Edgeの読み上げはページ読み込み直後の静的HTMLしか見ないため機能しません。

唯一確実に動くのが、**本文が最初からHTMLソースに書き込まれた、装飾の少ない静的ページ**をGitHub Pagesで配信する形でした。`build_note.py` と `note-template.html` は、この形式を実機（iPhone版Edge）で検証した上で固定しています。そのため、テンプレートのDOM構造と変換方針は変更しない前提で運用しています。

## ディレクトリ構成

- `notes/` — 公開済みのノート本体（`<slug>.md` と `<slug>.html` のペア）。
- `build_note.py` — Markdown→HTML変換スクリプト（pandoc経由）。
- `note-template.html` — 生成されるページのテンプレート。
- `CLAUDE.md` — Claude Codeが従う作業手順とルール（エージェント向け）。
- `.claude/skills/` — 原稿作成に使うスキル（エージェント向け）。

## Slack通知

ノートを公開すると、URLがSlackへ投稿されます。投稿先チャンネルは環境変数 `AUDIO_NOTES_SLACK_CHANNEL_ID` で指定します。ワークスペース固有の値なので、このリポジトリにはコミットせず、実行環境（Claude Codeの環境設定やCI）の環境変数として渡してください。設定されていない場合、通知はスキップされ、公開URLだけが報告されます。
