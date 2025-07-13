// ===== グローバル変数 =====
let currentTab = 'all-time';

// ===== 初期化処理 =====
document.addEventListener('DOMContentLoaded', function () {
    console.log('📊 Ranking Page 読み込み完了');

    // タブイベントリスナーの設定
    setupTabListeners();

    // 初期データの読み込み
    loadRankingData();

    // 自分のベストスコアを読み込み
    loadUserBestScore();
});

// ===== タブ機能 =====
function setupTabListeners() {
    const tabButtons = document.querySelectorAll('.tab-button');

    tabButtons.forEach(button => {
        button.addEventListener('click', function () {
            // アクティブタブの切り替え
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // 選択されたタブの取得
            currentTab = this.getAttribute('data-tab');
            console.log('タブ切り替え:', currentTab);

            // ランキングデータの再読み込み
            loadRankingData();
        });
    });
}

// ===== ランキングデータの読み込み =====
async function loadRankingData() {
    const rankingList = document.getElementById('ranking-list');

    // ローディング表示
    rankingList.innerHTML = `
        <div class="loading-message">
            <div class="loading"></div>
            <span>ランキングを読み込み中...</span>
        </div>
    `;

    try {
        const response = await fetch(`/api/ranking?period=${currentTab}`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('ランキングデータ受信:', data);

        if (data.success) {
            displayRanking(data.ranking);
        } else {
            throw new Error(data.message || 'ランキングデータの取得に失敗しました');
        }

    } catch (error) {
        console.error('ランキング読み込みエラー:', error);
        rankingList.innerHTML = `
            <div class="no-data-message">
                ❌ ランキングデータの読み込みに失敗しました<br>
                <small>${error.message}</small>
            </div>
        `;
    }
}

// ===== ランキング表示 =====
function displayRanking(rankingData) {
    const rankingList = document.getElementById('ranking-list');

    if (!rankingData || rankingData.length === 0) {
        rankingList.innerHTML = `
            <div class="no-data-message">
                📊 まだランキングデータがありません<br>
                <small>ゲームをプレイしてスコアを記録しましょう！</small>
            </div>
        `;
        return;
    }

    const rankingHTML = rankingData.map((item, index) => {
        const rank = index + 1;
        const rankClass = rank <= 3 ? `rank-${rank}` : '';
        const rankEmoji = getRankEmoji(rank);

        return `
            <div class="ranking-item ${rankClass}">
                <div class="rank-info">
                    <div class="rank-number">${rankEmoji}${rank}</div>
                    <div class="player-info">
                        <div class="player-name">${escapeHtml(item.player_name)}</div>
                        <div class="play-date">${formatDate(item.play_date)}</div>
                    </div>
                </div>
                <div class="score-info">
                    <div class="score-value">${item.score.toLocaleString()}</div>
                    <div class="score-unit">pts</div>
                </div>
            </div>
        `;
    }).join('');

    rankingList.innerHTML = rankingHTML;
}

// ===== 自分のベストスコア読み込み =====
async function loadUserBestScore() {
    try {
        const response = await fetch('/api/user-best-score');

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        if (data.success && data.best_score) {
            displayUserBestScore(data.best_score);
        } else {
            displayUserBestScore(null);
        }

    } catch (error) {
        console.error('ベストスコア読み込みエラー:', error);
        displayUserBestScore(null);
    }
}

// ===== 自分のベストスコア表示 =====
function displayUserBestScore(scoreData) {
    const userBest = document.getElementById('user-best');

    if (scoreData) {
        userBest.innerHTML = `
            <span class="score-value">${scoreData.score.toLocaleString()}</span>
            <span class="score-date">${formatDate(scoreData.play_date)}</span>
        `;
    } else {
        userBest.innerHTML = `
            <span class="score-value">-</span>
            <span class="score-date">記録なし</span>
        `;
    }
}

// ===== ユーティリティ関数 =====
function getRankEmoji(rank) {
    // ランクに応じた絵文字を返す
    switch (rank) {
        case 1: return '🥇';
        case 2: return '🥈';
        case 3: return '🥉';
        default: return '';
    }
}

function formatDate(dateString) {
    // 日付文字列をフォーマットして表示
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
        return '今日 ' + date.toLocaleTimeString('ja-JP', {
            hour: '2-digit',
            minute: '2-digit'
        });
    } else if (diffDays === 1) {
        return '昨日';
    } else if (diffDays < 7) {
        return `${diffDays}日前`;
    } else {
        return date.toLocaleDateString('ja-JP');
    }
}

function escapeHtml(text) {
    // HTMLエスケープ処理
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ===== ナビゲーション =====
function goBack() {
    window.location.href = '/';
}

// ===== エラーハンドリング =====
window.addEventListener('error', function (event) {
    console.error('JavaScript エラー:', event.error);
});
