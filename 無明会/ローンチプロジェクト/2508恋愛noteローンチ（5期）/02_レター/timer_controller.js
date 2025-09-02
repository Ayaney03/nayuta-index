// 無明会 タイマー制御専用スクリプト
// Utageの管理画面とユーザー向けページを区別してタイマー機能を実装

(function() {
    'use strict';

    // ===== 環境判定機能 =====
    class EnvironmentDetector {
        constructor() {
            this.isAdminPanel = this.detectAdminPanel();
            this.isUserPage = !this.isAdminPanel;
        }

        detectAdminPanel() {
            // Utageの管理画面を判定する複数の方法
            const adminIndicators = [
                // URLパスでの判定
                window.location.pathname.includes('/admin'),
                window.location.pathname.includes('/manage'),
                window.location.pathname.includes('/edit'),
                window.location.pathname.includes('/dashboard'),
                
                // ドメインでの判定
                window.location.hostname.includes('admin'),
                window.location.hostname.includes('manage'),
                
                // クエリパラメータでの判定
                window.location.search.includes('admin='),
                window.location.search.includes('edit='),
                window.location.search.includes('preview='),
                
                // 特定の要素の存在での判定
                document.querySelector('.admin-panel'),
                document.querySelector('.utage-admin'),
                document.querySelector('#admin-toolbar'),
                
                // iframe内での実行判定
                window.self !== window.top,
                
                // 特定のクラスやIDの存在
                document.body.classList.contains('admin'),
                document.body.classList.contains('editor'),
                document.body.id === 'admin-body'
            ];

            return adminIndicators.some(indicator => indicator);
        }

        isUserEnvironment() {
            return this.isUserPage;
        }

        isAdminEnvironment() {
            return this.isAdminPanel;
        }
    }

    // ===== ユーザー専用タイマー機能 =====
    class UserTimerController {
        constructor(duration = 3) {
            this.storageKey = 'mumyokai_timer_start';
            this.duration = duration; // デフォルト3日間、カスタマイズ可能
            this.init();
        }

        init() {
            // 初回訪問時刻を記録
            this.recordFirstVisit();
            
            // タイマー開始
            this.startTimer();
            
            // 期限チェック
            this.checkExpiration();
        }

        recordFirstVisit() {
            const existingStart = localStorage.getItem(this.storageKey);
            if (!existingStart) {
                const now = new Date().getTime();
                localStorage.setItem(this.storageKey, now.toString());
                console.log('初回訪問を記録しました:', new Date(now));
            }
        }

        getStartTime() {
            const startTime = localStorage.getItem(this.storageKey);
            return startTime ? parseInt(startTime) : new Date().getTime();
        }

        getEndTime() {
            const startTime = this.getStartTime();
            return startTime + (this.duration * 24 * 60 * 60 * 1000);
        }

        startTimer() {
            this.updateDisplay();
            this.interval = setInterval(() => {
                this.updateDisplay();
            }, 1000);
        }

        updateDisplay() {
            const now = new Date().getTime();
            const endTime = this.getEndTime();
            const distance = endTime - now;

            if (distance < 0) {
                this.handleExpiration();
                return;
            }

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            // 複数のタイマー要素を更新
            this.updateTimerElements('days', days);
            this.updateTimerElements('hours', hours);
            this.updateTimerElements('minutes', minutes);
            this.updateTimerElements('seconds', seconds);

            // 最終カウントダウンも更新
            this.updateTimerElements('final-days', days);
            this.updateTimerElements('final-hours', hours);
            this.updateTimerElements('final-minutes', minutes);
            this.updateTimerElements('final-seconds', seconds);
        }

        updateTimerElements(id, value) {
            const elements = document.querySelectorAll(`#${id}`);
            elements.forEach(element => {
                if (element) {
                    element.textContent = value.toString().padStart(2, '0');
                }
            });
        }

        handleExpiration() {
            // タイマー停止
            if (this.interval) {
                clearInterval(this.interval);
            }

            // 全てのタイマー表示を00にする
            const timerIds = ['days', 'hours', 'minutes', 'seconds', 'final-days', 'final-hours', 'final-minutes', 'final-seconds'];
            timerIds.forEach(id => {
                this.updateTimerElements(id, 0);
            });

            // 期限切れページに遷移
            this.showExpiredPage();
        }

        showExpiredPage() {
            // ページ全体を期限切れ表示に置き換え
            document.body.innerHTML = this.getExpiredPageHTML();
            
            // 期限切れをローカルストレージに記録
            localStorage.setItem('mumyokai_expired', 'true');
        }

        getExpiredPageHTML() {
            return `
                <div style="
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    background: linear-gradient(135deg, #f5e6a3 0%, #d4af37 50%, #b8860b 100%);
                    font-family: 'Hiragino Mincho ProN', serif;
                    text-align: center;
                    padding: 20px;
                ">
                    <div style="
                        max-width: 600px;
                        background: rgba(255, 255, 255, 0.95);
                        padding: 60px 40px;
                        border-radius: 20px;
                        box-shadow: 0 20px 40px rgba(139, 105, 20, 0.3);
                        border: 2px solid #d4af37;
                    ">
                        <h1 style="
                            font-size: 48px;
                            color: #8b6914;
                            margin-bottom: 30px;
                            font-weight: 700;
                        ">募集終了</h1>
                        
                        <p style="
                            font-size: 24px;
                            color: #2d3748;
                            margin-bottom: 30px;
                            line-height: 1.6;
                        ">
                            無明会の特別なご案内は<br>
                            終了いたしました
                        </p>
                        
                        <div style="
                            background: rgba(139, 105, 20, 0.1);
                            padding: 30px;
                            border-radius: 12px;
                            margin-bottom: 40px;
                        ">
                            <p style="
                                font-size: 18px;
                                color: #8b6914;
                                margin: 0;
                                line-height: 1.8;
                            ">
                                次回の募集については<br>
                                公式アカウントにてお知らせいたします
                            </p>
                        </div>
                        
                        <a href="https://x.com/mumyokai0201" 
                           target="_blank"
                           style="
                               display: inline-block;
                               background: linear-gradient(135deg, #8b6914 0%, #d4af37 100%);
                               color: #ffffff;
                               padding: 20px 40px;
                               border-radius: 12px;
                               text-decoration: none;
                               font-size: 18px;
                               font-weight: 600;
                               box-shadow: 0 6px 16px rgba(139, 105, 20, 0.4);
                               transition: transform 0.3s ease;
                           "
                           onmouseover="this.style.transform='scale(1.05)'"
                           onmouseout="this.style.transform='scale(1)'">
                            公式アカウントをフォロー
                        </a>
                        
                        <p style="
                            font-size: 14px;
                            color: #666;
                            margin-top: 30px;
                            font-style: italic;
                        ">
                            ありがとうございました
                        </p>
                    </div>
                </div>
            `;
        }

        checkExpiration() {
            // ページ読み込み時に既に期限切れかチェック
            const isExpired = localStorage.getItem('mumyokai_expired');
            if (isExpired === 'true') {
                this.showExpiredPage();
                return;
            }

            const now = new Date().getTime();
            const endTime = this.getEndTime();
            
            if (now >= endTime) {
                this.handleExpiration();
            }
        }

        // デバッグ用メソッド
        resetTimer() {
            localStorage.removeItem(this.storageKey);
            localStorage.removeItem('mumyokai_expired');
            location.reload();
        }

        // 残り時間を取得（デバッグ用）
        getRemainingTime() {
            const now = new Date().getTime();
            const endTime = this.getEndTime();
            const distance = endTime - now;
            
            if (distance < 0) return null;
            
            return {
                days: Math.floor(distance / (1000 * 60 * 60 * 24)),
                hours: Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
                minutes: Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)),
                seconds: Math.floor((distance % (1000 * 60)) / 1000),
                total: distance
            };
        }
    }

    // ===== メイン初期化処理 =====
    function initTimerController() {
        const detector = new EnvironmentDetector();
        
        console.log('環境判定結果:', {
            isAdmin: detector.isAdminEnvironment(),
            isUser: detector.isUserEnvironment(),
            url: window.location.href
        });

        // ユーザー環境でのみタイマーを実行
        if (detector.isUserEnvironment()) {
            console.log('ユーザー環境を検出 - タイマーを開始します');
            
            // カスタム期間の設定（グローバル変数 TIMER_DURATION_HOURS で指定可能）
            let duration = 3; // デフォルト3日間
            if (typeof window.TIMER_DURATION_HOURS !== 'undefined') {
                duration = window.TIMER_DURATION_HOURS / 24; // 時間を日数に変換
            }
            
            window.mumyokaiTimer = new UserTimerController(duration);
            
            // デバッグ用にグローバルに公開
            window.resetMumyokaiTimer = () => {
                if (window.mumyokaiTimer) {
                    window.mumyokaiTimer.resetTimer();
                }
            };
            
            window.getMumyokaiRemainingTime = () => {
                if (window.mumyokaiTimer) {
                    return window.mumyokaiTimer.getRemainingTime();
                }
                return null;
            };
        } else {
            console.log('管理環境を検出 - タイマーをスキップします');
        }
    }

    // ===== 実行タイミングの制御 =====
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTimerController);
    } else {
        initTimerController();
    }

})();
