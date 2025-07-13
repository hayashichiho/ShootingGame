// ===== グローバル変数 =====
let statusCheckInterval = null;
let lastGameStatus = undefined;

// ===== ゲーム制御関数 =====
async function startGame() {
    // ゲーム開始
    const startBtn = document.getElementById('startBtn');
    const buttonText = startBtn.querySelector('.button-text');
    const loading = startBtn.querySelector('.loading');

    try {
        // ローディング表示
        startBtn.disabled = true;
        buttonText.style.opacity = '0.7';
        loading.classList.remove('hidden');
        addButtonClickEffect(startBtn);

        const response = await fetch('/start_game');

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        if (data.status === 'success') {
            console.log('ゲーム開始成功:', data);
            buttonText.textContent = 'ゲーム起動中...';
            loading.classList.add('hidden');
        } else {
            console.error('ゲーム開始失敗:', data);
        }
    } catch (error) {
        console.error('ゲーム開始エラー:', error);
    }
}

async function endGame() {
    // ゲーム終了
    try {
        const response = await fetch('/end_game');

        // レスポンス確認
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        // レスポンスデータの取得
        const data = await response.json();
        if (data.status === 'success') {
            console.log('ゲーム終了成功:', data);
        } else {
            console.error('ゲーム終了失敗:', data);
        }
    } catch (error) {
        console.error('ゲーム終了エラー:', error);
    }
}


async function checkStatus() {
    // ゲーム状態確認
    try {
        const data = await fetchGameStatus();
        console.log('状態確認結果:', data);
    } catch (error) {
        console.error('状態確認エラー:', error);
    }
}



// ===== 共通のAPI呼び出し関数 =====
async function fetchGameStatus() {
    const response = await fetch('/game_status');
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return await response.json();
}



// ===== ボタンクリック効果 =====
function addButtonClickEffect(button) {
    // ボタン加工
    button.style.transform = 'scale(0.95)';
    setTimeout(() => {
        button.style.transform = '';
    }, 150);
}


function initializeButtons() {
    // 全てのボタンにクリック効果を追加
    const buttons = document.querySelectorAll('.menu-button, .start-button');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            addButtonClickEffect(button);
        });

        // ホバー効果
        button.addEventListener('mouseenter', () => {
            button.style.transform = 'translateY(-2px)';
        });
        button.addEventListener('mouseleave', () => {
            button.style.transform = '';
        });
    });
}

// ===== モーダル制御 =====
function showInstructions() {
    // 説明書表示
    const modal = document.getElementById('instructionsModal');
    modal.classList.remove('hidden');

    // フェードイン効果
    setTimeout(() => {
        modal.style.opacity = '1';
    }, 10);

    console.log('説明モーダルを表示');
}

function hideInstructions() {
    // 説明書非表示
    const modal = document.getElementById('instructionsModal');
    modal.style.opacity = '0';

    setTimeout(() => {
        modal.classList.add('hidden');
    }, 300);

    console.log('説明モーダルを非表示');
}

document.getElementById('instructionsModal')?.addEventListener('click', function (event) {
    if (event.target === this) {
        // モーダルの外側クリックで閉じる
        hideInstructions();
    }
});

// ===== キーボードショートカット =====
document.addEventListener('keydown', function (event) {
    // モーダルが開いている時の処理
    const modal = document.getElementById('instructionsModal');
    const isModalOpen = !modal.classList.contains('hidden');

    if (isModalOpen) {
        if (event.code === 'Escape') {
            event.preventDefault();
            hideInstructions();
        }
        return; // モーダルが開いている時は他のショートカットを無効化
    }
});

// ===== ゲーム状態表示更新 =====
function updateGameStatusDisplay(isRunning) {
    console.log('UI状態更新:', isRunning);

    const startBtn = document.getElementById('startBtn');
    if (!startBtn) {
        console.error('startBtnが見つかりません');
        return;
    }

    const buttonText = startBtn.querySelector('.button-text');
    if (!buttonText) {
        console.error('.button-textが見つかりません');
        return;
    }

    // boolean値で正しく判定
    if (isRunning === true) {
        startBtn.disabled = true;
        buttonText.textContent = 'ゲーム実行中';
        buttonText.style.opacity = '0.7';
        console.log('ボタンを「ゲーム実行中」に変更しました');
    } else {
        startBtn.disabled = false;
        buttonText.textContent = 'ゲーム開始';
        buttonText.style.opacity = '1';
        console.log('ボタンを「ゲーム開始」に変更しました');
    }
}
// ===== 自動監視 =====
function startStatusMonitoring() {
    // 定期的なゲーム状態監視を開始
    if (statusCheckInterval) return; // 既に開始されている場合は何もしない

    statusCheckInterval = setInterval(async () => {
        try {
            const data = await fetchGameStatus();

            // 状態が変更された場合のみ通知
            if (lastGameStatus !== undefined && lastGameStatus !== data.running) {
                const statusText = data.running ? 'ゲームが開始されました' : 'ゲームが終了しました';
                console.log('状態変更検知:', statusText);

                // UI状態を更新
                updateGameStatusDisplay(data.running);
            }
            lastGameStatus = data.running;

        } catch (error) {
            console.debug('定期監視エラー:', error);
        }
    }, 3000); // 3秒間隔

    console.log('自動状態監視を開始しました');
}

// 定期監視を停止
function stopStatusMonitoring() {
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
        statusCheckInterval = null;
        console.log('自動状態監視を停止しました');
    }
}

// ===== エラーハンドリング =====
window.addEventListener('error', function (event) {
    console.error('JavaScript エラー:', event.error);
});

window.addEventListener('online', function () {
    console.log('ネットワーク接続復旧');
});

window.addEventListener('offline', function () {
    console.log('ネットワーク接続切断');
});


// ===== 初期化処理 =====
document.addEventListener('DOMContentLoaded', function () {
    // ページ読み込み完了時の初期化
    console.log('🎮 Shooting Game Web Interface 読み込み完了');

    // 初期化処理
    initializeButtons();

    // 初期状態確認（少し遅らせて実行）
    setTimeout(() => {
        checkStatus();
    }, 500);

    // 定期監視開始
    startStatusMonitoring();

    // ページ離脱時のクリーンアップ
    window.addEventListener('beforeunload', function () {
        stopStatusMonitoring();
    });

    // キーボードショートカットの説明をコンソールに出力
    console.log('利用可能なキーボードショートカット:');
    console.log('Escape: モーダル閉じる / ゲーム終了');
});

// ===== ランキング表示 =====
function showRanking() {
    console.log('ランキングページに移動');
    window.location.href = '/ranking';
}
