import os
import subprocess
import sys

from flask import Flask, jsonify, render_template

app = Flask(__name__)

# ゲームプロセスを管理するための変数
game_process = None


@app.route("/")
def index():
    """スタート画面を表示"""
    return render_template("start.html")


@app.route("/start_game")
def start_game():
    """シューティングゲームを開始"""
    global game_process

    try:
        # 既にゲームが実行中の場合は終了
        if game_process and game_process.poll() is None:
            game_process.terminate()

        # 新しいゲームプロセスを開始
        game_script = os.path.join(os.path.dirname(__file__), "game/game.py")
        game_process = subprocess.Popen([sys.executable, game_script])

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


if __name__ == "__main__":
    print("シューティングゲーム Webサーバーを起動中...")
    print("ブラウザで http://localhost:5000 にアクセスしてください")

    # デバッグモードでFlaskアプリを実行
    app.run(debug=True, host="0.0.0.0", port=5000)
