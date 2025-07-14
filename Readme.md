# ShootingGame（インベーダーゲーム）


## ゲーム概要

* **タイトル**：ShootingGame
* **バージョン**：1.00
* **特徴**： ランキング表示 / アイテム / 時間無制限
* **プレイ時間**：2分程度
* **推奨年齢**：全年齢
* **制作技術**：Python, Flask,
* **制作者**：hayashi, kato, sato

---

## ゲームの起動方法

### ① ローカル起動手順

1. このリポジトリをクローンまたはダウンロードします。

   ```sh
   git clone https://github.com/hayashichiho/ShootingGame
   ```
   ```sh
   cd ShootingGame
   ```

2. Python の依存パッケージをインストールします。

   ```sh
   pip install -r requirements.txt
   ```

3. アプリケーションを起動します。

   ```sh
   python main.py
   ```

4. ブラウザで `http://localhost:5000` にアクセスし、プレイを開始します。

#### ※ データベース初期化方法
   ```sh
   flask db init
   flask db migrate -m "initial"
   flask db upgrade
   ```

### ② Render.com デプロイ手順

1. GitHubとRender.comを連携
2. Webサービスとして設定
3. `requirements.txt`を使用して自動デプロイ

---

## 操作方法（PC）

* **→**：プレイヤーを右へ移動
* **←**：プレイヤーを左へ移動
* **spaceキー**：銃発射

---

## ゲームルール
- **制限時間**：無制限
- **インベーダー回避**：インベーダーを避けて，銃を発射して倒す
- **点数**：敵を倒すと点数加算

#### 敵の種類
- **黄色**：まっすぐ移動する敵
- **紫**：斜めに移動する敵
- **水色**：3回攻撃しないと倒れない敵

#### アイテムの種類
- **2のマーク**：スコア2倍
- **ロケット**：弾の数が増量
- **プレイヤー**：プレイヤーが増量

---

## 攻略のヒント

* アイテムを使うことで敵を倒しやすい
* たくさん発射

---

## 技術スタック

### バックエンド

* Python 3.11
* sqlite3
* Flask

### フロントエンド

* pygame

### デプロイ

* Render.com
* Docker
* Procfile（for Gunicorn）

---

## ディレクトリ構成

```
ShootingGame/
├── main.py                # Webサーバー起動用メインスクリプト
├── requirements.txt       # 依存ライブラリ
├── Readme.md              # このファイル
├── static/
│   ├── resources/
│   │   └── images         # 画像素材
│   ├── css/
│   │   ├── start.css      # スタート画面用デザイン
│   │   └── ranking.css    # ランキング画面用デザイン
│   ├── js/
│   │   ├── start.js       # スタート画面用処理
│   │   └── ranking.js     # ランキング画面用処理
│   └── favicon.ico        # アイコン
├── game/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── game.py        # ゲーム本体（Pygame）
│   │   ├── game_core.py   # ゲームロジック
│   │   └── game_ui.py     # ゲームUI・操作
│   ├── actors/
│   │   ├── __init__.py
│   │   ├── bullet.py      # 弾のクラス
│   │   ├── enemy.py       # 敵のクラス
│   │   ├── item.py        # アイテムのクラス
│   │   ├── player.py      # プレイヤーのクラス
│   │   └── subPlayer.py   # サブプレイヤーのクラス
│   └── utils/
│       ├── __init__.py
│       ├── config.py      # 設定値
│       └── load_files.py  # 画像ロード
├── templates/
│       ├── start.html     # スタート画面HTML
│       └── ranking.html   # ランキング画面HTML
└── Dockerfile             # Docker構成
```

---

## APIエンドポイント一覧

* `POST /api/save-score`：スコア保存
* `GET /api/ranking`：ランキング取得
* `GET /api/user-best-score`：自己ベストスコア取得
* `POST /start_game`：ゲーム開始
* `POST /end_game`：ゲーム終了
* `GET /game_status`：ゲーム状態取得

---

## 動作環境

* **対応OS**：Windows 10/11, Linux
* **推奨ブラウザ**：Chrome, Firefox, Edge, Safari

---

## 利用規約（制定日：2025/07/13）

1. 本ゲームの営利目的での無断使用は禁止です。
2. 二次創作・実況動画は許可しますが、以下の明記が必要です。

   > このゲーム『Shooting Game』の制作者：hayashi, kato, sato
3. 素材の抜き出し・転用・再配布は禁止です（フリー素材は各規約に従ってください）。
4. 規約は予告なく変更される場合があります。

---

## 免責事項

ゲームの使用により発生したいかなる損害についても制作者は責任を負いません。自己責任でご利用ください。

---

## 更新履歴

* 2025/07/13 Ver.1.00 ゲームリリース

---

## クレジット（敬称略）

* hayashi, kato, sato
* Pygame & Flask コミュニティ

---

## 貢献について

バグ報告・機能追加のご提案は Issuesにて歓迎します！
