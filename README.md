# :tophat: Magical Banana :banana:
NEologdとWord2Vecを使った連想ゲーム『マジカルバナナ』のゲームボット

## ルール
「○○といったら××」という形式でプレイヤが順番に発言をします

ただし，××は○○から連想したものでなければいけません

## さっそく遊ぶ
~~下記のリンクから遊べます~~

*現在、サーバ停止中*

- ~~[Chat with Mr. Magical B.](http://k0sk.github.io/magical-banana-front/)~~

## 仕組み
このゲームボットは次のような方法で"連想"しています

- 読みに基づく連想
    - NEologdの辞書データから似た読みの名詞を検索
- 意味に基づく連想
  - Word2Vecのベクトル空間で表現の近い単語を探索
