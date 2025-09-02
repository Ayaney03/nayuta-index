// 無明会 レターページ全体用スクリプト

// ===== グローバル変数 =====
let countdownInterval;
let scrollAnimationObserver;

// ===== カウントダウンタイマー機能 =====
class CountdownTimer {
    constructor(targetId, duration = 3) {
        this.targetId = targetId;
        this.duration = duration; // 日数
        this.startTime = new Date();
        this.endTime = new Date(this.startTime.getTime() + (this.duration * 24 * 60 * 60 * 1000));
        this.interval = null;
        this.init();
    }

    init() {
        this.updateDisplay();
        this.interval = setInterval(() => this.updateDisplay(), 1000);
    }

    updateDisplay() {
        const now = new Date();
        const distance = this.endTime.getTime() - now.getTime();

        if (distance < 0) {
            this.stop();
            this.showExpired();
            return;
        }

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        this.updateElement('days', days);
        this.updateElement('hours', hours);
        this.updateElement('minutes', minutes);
        this.updateElement('seconds', seconds);
    }

    updateElement(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value.toString().padStart(2, '0');
        }
    }

    showExpired() {
        const elements = ['days', 'hours', 'minutes', 'seconds'];
        elements.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = '00';
            }
        });
    }

    stop() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
    }
}

// ===== スクロールアニメーション機能 =====
class ScrollAnimation {
    constructor() {
        this.observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        this.init();
    }

    init() {
        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateElement(entry.target);
                }
            });
        }, this.observerOptions);

        this.observeElements();
    }

    observeElements() {
        const animatedElements = document.querySelectorAll('.fade-in-up, .fade-in-left, .fade-in-right, .fade-in-scale, .speech-bubble');
        animatedElements.forEach(el => {
            this.observer.observe(el);
        });
    }

    animateElement(element) {
        element.classList.add('animate-in');
        
        // 遅延アニメーションの処理
        const delay = element.classList.contains('delay-1') ? 200 :
                     element.classList.contains('delay-2') ? 400 :
                     element.classList.contains('delay-3') ? 600 :
                     element.classList.contains('delay-4') ? 800 :
                     element.classList.contains('delay-5') ? 1000 : 0;

        if (delay > 0) {
            setTimeout(() => {
                element.classList.add('animate-in');
            }, delay);
        }
    }
}

// ===== ページ遷移アニメーション =====
class PageTransition {
    constructor() {
        this.init();
    }

    init() {
        // ページ読み込み時のフェードイン
        document.body.style.opacity = '0';
        document.body.style.transition = 'opacity 0.8s ease-out';
        
        setTimeout(() => {
            document.body.style.opacity = '1';
        }, 100);

        // ページ内リンクのスムーズスクロール
        this.initSmoothScroll();
    }

    initSmoothScroll() {
        const links = document.querySelectorAll('a[href^="#"]');
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
}

// ===== インタラクティブ要素の強化 =====
class InteractiveElements {
    constructor() {
        this.init();
    }

    init() {
        this.initCTAButtons();
        this.initHoverEffects();
        this.initCountdownEmphasis();
    }

    initCTAButtons() {
        const ctaButtons = document.querySelectorAll('.cta-button');
        ctaButtons.forEach(button => {
            button.addEventListener('mouseenter', () => {
                button.style.transform = 'scale(1.05)';
            });
            
            button.addEventListener('mouseleave', () => {
                button.style.transform = 'scale(1)';
            });
        });
    }

    initHoverEffects() {
        const hoverElements = document.querySelectorAll('.hover-lift');
        hoverElements.forEach(element => {
            element.addEventListener('mouseenter', () => {
                element.style.transform = 'translateY(-5px)';
                element.style.boxShadow = '0 10px 25px rgba(0, 0, 0, 0.15)';
            });
            
            element.addEventListener('mouseleave', () => {
                element.style.transform = 'translateY(0)';
                element.style.boxShadow = 'none';
            });
        });
    }

    initCountdownEmphasis() {
        const countdownElements = document.querySelectorAll('.countdown-emphasis');
        countdownElements.forEach(element => {
            element.addEventListener('mouseenter', () => {
                element.style.animation = 'none';
                element.style.transform = 'scale(1.02)';
            });
            
            element.addEventListener('mouseleave', () => {
                element.style.animation = 'pulse 2s ease-in-out infinite';
                element.style.transform = 'scale(1)';
            });
        });
    }
}

// ===== パフォーマンス最適化 =====
class PerformanceOptimizer {
    constructor() {
        this.init();
    }

    init() {
        this.debounceScroll();
        this.lazyLoadImages();
    }

    debounceScroll() {
        let ticking = false;
        
        function updateScroll() {
            ticking = false;
        }

        function requestTick() {
            if (!ticking) {
                requestAnimationFrame(updateScroll);
                ticking = true;
            }
        }

        window.addEventListener('scroll', requestTick);
    }

    lazyLoadImages() {
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }
}

// ===== メイン初期化関数 =====
function initLetterPage() {
    // カウントダウンタイマーの初期化
    const countdownElements = document.querySelectorAll('#countdown-timer, #final-days');
    if (countdownElements.length > 0) {
        new CountdownTimer('countdown-timer', 3);
        
        // 最終ページのカウントダウンも初期化
        if (document.getElementById('final-days')) {
            new CountdownTimer('final-days', 3);
        }
    }

    // スクロールアニメーションの初期化
    new ScrollAnimation();

    // ページ遷移アニメーションの初期化
    new PageTransition();

    // インタラクティブ要素の初期化
    new InteractiveElements();

    // パフォーマンス最適化の初期化
    new PerformanceOptimizer();

    console.log('無明会レターページが初期化されました');
}

// ===== ページ読み込み完了時の実行 =====
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLetterPage);
} else {
    initLetterPage();
}

// ===== ページ表示時の追加処理 =====
window.addEventListener('load', () => {
    // 画像の遅延読み込み完了後の処理
    setTimeout(() => {
        document.body.classList.add('page-loaded');
    }, 500);
});

// ===== エラーハンドリング =====
window.addEventListener('error', (e) => {
    console.error('ページエラーが発生しました:', e.error);
});

// ===== ユーティリティ関数 =====
window.LetterUtils = {
    // 要素の可視性チェック
    isElementInViewport: (el) => {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    },

    // スムーズスクロール
    scrollToElement: (elementId) => {
        const element = document.getElementById(elementId);
        if (element) {
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    },

    // アニメーションクラスの追加
    addAnimationClass: (element, className) => {
        if (element) {
            element.classList.add(className);
        }
    }
};
