import os
import sqlite3
import subprocess
import sys
from datetime import datetime, timedelta, timezone

from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game_scores.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ゲームプロセスを管理するための変数
game_process = None


# ===== データベース関連 =====
def init_database():
    """データベースの初期化"""
    conn = sqlite3.connect("game_scores.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            play_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ===== 既存のルート =====
@app.route("/")
def index():
    """スタート画面を表示"""
    return render_template("start.html")


@app.route("/ranking")
def ranking():
    """ランキング画面を表示"""
    return render_template("ranking.html")


# ===== 新しいAPIルート =====
@app.route("/api/ranking")
def api_ranking():
    """ランキングデータを取得"""
    period = request.args.get("period", "all-time")

    try:
        conn = sqlite3.connect("game_scores.db")
        cursor = conn.cursor()

        # 期間に応じたクエリ
        if period == "today":
            cursor.execute("""
                SELECT player_name, score, play_date
                FROM game_scores
                WHERE DATE(play_date) = DATE('now', 'localtime')
                ORDER BY score DESC
                LIMIT 20
            """)
        elif period == "this-week":
            cursor.execute("""
                SELECT player_name, score, play_date
                FROM game_scores
                WHERE DATE(play_date) >= DATE('now', 'localtime', '-7 days')
                ORDER BY score DESC
                LIMIT 20
            """)
        else:  # all-time
            cursor.execute("""
                SELECT player_name, score, play_date
                FROM game_scores
                ORDER BY score DESC
                LIMIT 20
            """)

        ranking_data = []
        for row in cursor.fetchall():
            ranking_data.append(
                {"player_name": row[0], "score": row[1], "play_date": row[2]}
            )

        conn.close()

        return jsonify({"success": True, "ranking": ranking_data})

    except Exception as e:
        return jsonify({"success": False, "message": f"ランキング取得エラー: {str(e)}"})


@app.route("/api/user-best-score")
def api_user_best_score():
    """ユーザーのベストスコアを取得（今は全体のトップスコア）"""
    try:
        conn = sqlite3.connect("game_scores.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT player_name, score, play_date
            FROM game_scores
            ORDER BY score DESC
            LIMIT 1
        """)

        result = cursor.fetchone()
        conn.close()

        if result:
            return jsonify(
                {
                    "success": True,
                    "best_score": {
                        "player_name": result[0],
                        "score": result[1],
                        "play_date": result[2],
                    },
                }
            )
        else:
            return jsonify({"success": True, "best_score": None})

    except Exception as e:
        return jsonify(
            {"success": False, "message": f"ベストスコア取得エラー: {str(e)}"}
        )


@app.route("/api/save-score", methods=["POST"])
def api_save_score():
    """スコアを保存"""
    try:
        data = request.get_json()
        player_name = data.get("player_name", "Anonymous")
        score = data.get("score", 0)

        # 日本時間で現在時刻を取得
        JST = timezone(timedelta(hours=9))
        now_jst = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect("game_scores.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO game_scores (player_name, score, play_date) VALUES (?, ?, ?)",
            (player_name, score, now_jst),
        )

        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "スコアが保存されました"})

    except Exception as e:
        return jsonify({"success": False, "message": f"スコア保存エラー: {str(e)}"})


# ===== 既存のゲーム制御ルート =====
@app.route("/start_game")
def start_game():
    """シューティングゲームを開始"""
    global game_process

    try:
        # 既にゲームが実行中の場合は終了
        if game_process and game_process.poll() is None:
            game_process.terminate()

        # 新しいゲームプロセスを開始
        player_name = request.args.get("player_name", "Player1")
        game_process = subprocess.Popen(
            [sys.executable, "-m", "game.core.game", player_name]
        )

        return jsonify({"status": "success", "message": "ゲームが開始されました！"})

    except Exception as e:
        return jsonify(
            {"status": "error", "message": f"ゲームの開始に失敗しました: {str(e)}"}
        )


@app.route("/end_game")
def end_game():
    """ゲームを終了"""
    global game_process

    try:
        # ゲームプロセスが実行中の場合は終了
        if game_process and game_process.poll() is None:
            game_process.terminate()
            game_process.wait()

        return jsonify({"status": "success", "message": "ゲームが終了しました"})

    except Exception as e:
        return jsonify(
            {"status": "error", "message": f"ゲームの終了に失敗しました: {str(e)}"}
        )


@app.route("/game_status")
def game_status():
    """ゲームの実行状態を確認"""
    global game_process

    is_running = game_process and game_process.poll() is None

    return jsonify(
        {
            "running": is_running,
            "message": "ゲーム実行中" if is_running else "ゲーム停止中",
        }
    )


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


if __name__ == "__main__":
    print("シューティングゲーム Webサーバーを起動中...")
    print("ブラウザで http://localhost:5000 にアクセスしてください")

    # データベース初期化
    init_database()

    # デバッグモードでFlaskアプリを実行
    app.run(debug=True, host="0.0.0.0", port=5000)
