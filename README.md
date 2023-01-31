# Space100km

- [シェープファイルを使って海より宇宙の方が近い場所を探す](https://zenn.dev/takilog/articles/ddc67c223876a1) のための書き捨てプログラムとデータです
- `data/japan-res-5.pickle` シェープファイルから作ったMultiPolygonのうち面積が上位5個までのPolygonが入ったdictをPickleにしたものです
  - 0が本州、1が北海道、2が九州、3が四国、4が島になってますが、記事では3までしか使っていません。
  - pickleにするときにpickle純正の代わりに`dill`を使っています。
  - `shapely`のversionが2.0.Xじゃないとダメな気がします。
- `data/xy.pickle`
  - 候補地点です
- `output/` が図置き場です。