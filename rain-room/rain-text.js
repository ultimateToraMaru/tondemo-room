// 即時実行関数でローカルスコープを作成（グローバル汚染を防ぐ）
(function(){
    // HTML 上の降らせる領域と、表示テキストを取る入力要素を取得
    const rainArea = document.getElementById('rain-area');
    const textInput = document.getElementById('rain-text-input');

    // ----- 設定（ここを変えると見た目や挙動を調整できます） -----
    const config = {
        spawnInterval: 200, // ミリ秒ごとに新しいドロップを生成する間隔
        minSpeed: 1.2, // 1フレームあたりの最小移動量（px）
        maxSpeed: 3.0, // 1フレームあたりの最大移動量（px）
        minSize: 12, // フォントサイズの最小（px）
        maxSize: 28, // フォントサイズの最大（px）
        color: '#2b9cffff', // テキスト色の既定値
        opacity: 0.7, // テキストの不透明度
        maxDrops: 200 // 同時に表示するドロップの最大数
    };

    // 現在表示中のドロップを管理する集合（削除や更新に使う）
    const drops = new Set();

    // 指定範囲のランダム値を返すヘルパー関数
    function random(min, max){ return Math.random() * (max - min) + min }

    // ----- Drop クラス（1つの降るテキストを表す） -----
    class Drop{
        // コンストラクタ: 要素を作り、初期配置して表示領域に追加する
        constructor(text){
                // ドロップ要素は複数行を含められるように div を使う
                this.el = document.createElement('div');
                this.el.className = 'rain-drop';
            this.el.textContent = text; // 表示する文字列
            this.reset(text); // 位置や速度などを設定
            rainArea.appendChild(this.el); // DOMに追加して見えるようにする
            drops.add(this); // 管理集合に登録
        }

        // reset: 新しく（または再利用時に）位置やサイズ、速度をランダムに設定
        reset(text){
            // ビューポート幅を取り、ランダムなX位置を決める
            const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
            const x = Math.floor(Math.random() * vw);
            const size = Math.floor(random(config.minSize, config.maxSize));
            this.x = x;
            // 画面外上部にスタートさせる（負のY値）
            this.y = -random(10, 100) - (text.split('\n').length * config.maxSize); // 文字数分だけ上からスタート
            // 表示速度もランダム化
            this.speed = random(config.minSpeed, config.maxSpeed);
            // スタイルを当てる
            this.el.style.left = `${this.x}px`;
            this.el.style.top = `${this.y}px`;
            this.el.style.fontSize = `${size}px`;
            this.el.style.color = config.color;
            this.el.style.opacity = config.opacity;
        }

        // update: 毎フレーム呼ばれて位置を更新する
        update(){
            this.y += this.speed; // Y位置を下に移動
            this.el.style.transform = `translateY(${this.y}px)`; // transformで描画
            // 画面下に行ったら要素を削除
            if(this.y > window.innerHeight + 50){
                this.destroy();
            }
        }

        // destroy: DOMから削除して集合からも外す
        destroy(){
            drops.delete(this);
            if(this.el.parentNode) this.el.parentNode.removeChild(this.el);
        }
    }

    // ----- ドロップ生成ループ（必要なら生成する） -----
    // ドロップの総数が上限に達していなければ新規作成する
    function spawnIfNeeded(){
        if(drops.size >= config.maxDrops) return;

        // 入力欄の文字列を使う（なければ既定）
        const text = (textInput && textInput.value) ? textInput.value : '雨';

        // 文字列を一文字ごとに改行する（縦文字として降らせるため）
        const chars = text.split('').join('\n');

        new Drop(chars);
    }

    // ----- アニメーションループ -----
    // すべてのドロップを更新し、再帰的に requestAnimationFrame を呼ぶ
    function animate(){
        drops.forEach(d => d.update());
        requestAnimationFrame(animate);
    }

    // ----- 起動処理 -----
    // 一定間隔でドロップを生成するタイマーを開始し、アニメーションも開始する
    const spawnTimer = setInterval(spawnIfNeeded, config.spawnInterval);
    requestAnimationFrame(animate);

    // ----- 外部からの操作用（デバッグ・カスタマイズ用） -----
    // コンソールから window.rainText.メソッド() でアクセスできます
    window.rainText = {
        setText(t){ if(textInput) textInput.value = t },
        setColor(c){ config.color = c },
        setSpeed(min,max){ config.minSpeed = min; config.maxSpeed = max },
        stop(){ clearInterval(spawnTimer); drops.forEach(d=>d.destroy()) }
    };
})();

// BGMをループ再生
(function(){
    const bg = new Audio('雨が降る1.mp3');
    bg.loop = true;
    bg.volume = 0.5;
    bg.preload = 'auto';

    // 再生を試みる。失敗したらユーザー操作で再生するリスナを登録
    function tryPlay() {
        bg.play().catch(() => {
            const onUser = () => { bg.play().catch(()=>{}); };
            window.addEventListener('click', onUser, { once: true });
            window.addEventListener('touchstart', onUser, { once: true });
            window.addEventListener('keydown', onUser, { once: true });
        });
    }

    tryPlay();

    // 外部から操作したい場合の簡易API
    window.playBgm = () => bg.play().catch(()=>{});
    window.stopBgm = () => bg.pause();
})();
