    document.addEventListener('DOMContentLoaded', function() {
        // つぶやきファイル名のリスト
        var files = [
            './tweet/20240720.html',
        ];

        // マジカルポン漫画ファイル名のリスト
        var images = [
            './magical-pon-manga/【マジカルポンな日常！】_01.png',
            './magical-pon-manga/【マジカルポンな日常！】_02.png',
            './magical-pon-manga/【マジカルポンな日常！】_03.png',
            './magical-pon-manga/【マジカルポンな日常！】_04.png'
        ];

    // ファイルを読み込む
    function loadFile(file) {
        return new Promise(function(resolve, reject) {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', file, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        resolve(xhr.responseText);
                    } else {
                        reject('Failed to load file: ' + file);
                    }
                }
            };
            xhr.send();
        });

    }

    function loadAllFiles(files) {
        var promises = files.map(function(file) {
            return loadFile(file);
        });

        Promise.all(promises).then(function(contents) {
            var tweetContainer = document.getElementById('tweetContainer');
            contents.forEach(function(content) {
                tweetContainer.innerHTML += content;
            });
        }).catch(function(error) {
            console.error(error);
        });

        // 画像を表示するコンテナ
        var container = document.getElementById('magicalPonMangaContainer');

        // 画像をコンテナに追加
        images.forEach(function(image) {
            var img = document.createElement('img');
            img.src = image;
            img.style.width = '200px';  // 幅を固定
            img.style.height = 'auto';  // 高さは自動調整

            img.onclick = function() {
                window.open(image, '_blank');
            };

            container.appendChild(img);
        });
    }

    loadAllFiles(files);
});
