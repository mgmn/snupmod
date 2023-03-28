# Sn Uploader 改

Sn Uploader (CGI.pm版) \[[archive](https://web.archive.org/web/20140331084142/http://sugachan.dip.jp/obsolete/snup/)\] にサムネイル生成機能とメール通知機能を無理矢理付け足したアップローダスクリプトです。

[動作例](https://v2c.mgmn.jp/up/)

## 追加機能

- ImageMagickによるサムネイル画像作成
- ファイルのアップロード時と削除時に指定アドレスへメール通知送信

## 設置の前に

アップローダの設置にはリスクがともないます。

- [2007-02-24 ひどい目にあった(駄文待避所)](https://onigiri.hatenadiary.org/entries/2007/02/24)
- [2007-02-27 俺ってなんて馬鹿馬鹿馬鹿馬鹿(駄文待避所)](https://onigiri.hatenadiary.org/entries/2007/02/27)
- [放置サーバーにヤバい物が置かれて家宅捜索(スラド)](https://srad.jp/story/07/03/04/0245212)

このスクリプトはメール通知を備えていますが、常に正しく動作するかの保証はできません。 設置する場合は設置場所の法に則った管理をしてください。

## 動作環境

Sn Uploader 改の動作には以下のモジュールが必要になります。

- Encode
- Net::SMTP
- Net::POP3
- ImageMagick (PerlMagick)

Windows + Perl 5.8 (32bit/64bit) と CentOS + Perl 5.10 (64bit) で動作確認しています。 mod_perl でも動くかもしれません。

## 設置方法

zipを解凍し、upload.pl 内の設定変数をテキストエディタで編集します。 各設定変数の説明は同梱のreadmeやスクリプトを参照してください。
設置するディレクトリを作成し、その下にzip内のファイルをアップロードしてください。 doc ディレクトリは削除して構いません。

### 構成例

```text
-- uploader / upload.pl  --- スクリプト本体
    |   index.html --- (自動生成)
    |
    +-- src   --- アップロードファイル保存ディレクトリ
    +-- thumb --- サムネイル保存ディレクトリ
    +-- log   --- ログディレクトリ
    +-- img   --- CSSディレクトリ
```

### chmod 例

```bash
chmod 777 uploader uploader/src uploader/thumb uploader/log uploader/img
chmod 755 uploader/upload.pl
chmod 666 uploader/index.html
```

設置後、uploader/upload.pl にブラウザからアクセスすると index.html が自動生成されます。

## サポート

このスクリプトに関するバグ報告等は 本家Sn Uploaderのサイトではなく、[mgmn](https://github.com/mgmn) までお願いします。

保証はありませんが、出来る限りの範囲で対応すると思います。

## ライセンス

[本家 Sn Uploader の再配布規定](https://github.com/mgmn/snupmod/blob/uploader-kai/sn_saihaifu.txt) に準じます。 当サイトのリンク表示は削除可です。

## Changelog

### mod.1603072206

- メール通知機能を実装しました。
- DLKeyを有効にしているとDLKeyが設定されていないファイルでもサムネイルが作成されない不具合を修正しました。
- \[ALL\]を有効にしていると他のファイルリストが重複して出力される不具合を修正しました。
- DLKeyまたはdummyHTMLのあるファイルでサムネイルのリンク先が404になる不具合を修正しました。
- DLKey付きのファイルアップロード時に Use of uninitialized value 警告が出る不具合を修正しました。

### mod.1403110536

- とりあえず動いた。
