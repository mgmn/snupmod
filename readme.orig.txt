21:05 2005/10/10
suga@snpn.net

Sn Uploader

普通の(何
汎用ファイルアップローダです
思うようなのが無かったので
この際作ってみました

スクリプト本体は
/uploader/          NoCGI.pm版
/uploader+cgipm/    CGI.pm版
のディレクトリに格納されています

適当に作ったもんなので
タイトルの設定項目などはありません
デザイン等変えたい場合はそれほど難しくないと思いますので
ソースそのままいぢってください

基本的な動作はCGI.pm版/NoCGI.pm版共に変わりませんが
NoCGI.pm版の方がパフォーマンスがよい思います
扱うサイズがあんまり容量が大きくない場合はどちらでもかまわないかと
なおIISではアップロードできないこともないと思いますが
動作が不審になる傾向があるので出来れば避けた方がよさそうです

アーカイブに添付されているスクリプトの
漢字コードはShift-JIS/改行コードはCRLFになっています

※
このスクリプトの著作権は作者に帰属しますが
利用者の責任において自由に改変,運用することができます
また利用したことによって発生した損害に対して
作者は一切の責務を負わないものとします

//////
設置方法
1. 設置するディレクトリを作成します
   なおこのディレクトリはCGI実行権限で書き込めるように
 　suEXEC環境ならば701 その他なら 777のようにパーミッションを設定する
   suEXEC環境で 777などにした場合スクリプトにアクセスすると 500 Internal Server Error が出ることがあります
2. upload.cgiをエディタ等で開きはじめの方のパラメータを設定する
　 基本的には$set{'admin_pass'}の変更とPerlのPATHの確認だけでいいと思います
3. サーバにアップロードし適度にパーミッションex.(suEXEC:700 other:755)を設定する
4. ブラウザで upload.cgiに直接アクセスするとログファイル/ディレクトリを自動的に作成します
   アップローダへのリンクはupload.cgiではなく upload.html(1ページ目のアドレス)にしてください
   ＃upload.cgiにアクセスされた場合は無駄にプロセスを起動してupload.htmlに転送するだけです

   * 初めてアクセスした際に「メインログの作成に失敗しました」などの表示が出た場合は
     1.のディレクトリのパーミッション設定を見直してください

あとは適当に設定とか変えてみてください
なお1ページ目をindex.html等にするとURLがちょっと短くなるかもしれません
＃設置したディレクトリにはindex.htmlを作成しないので
  インデックスリストが表示される環境の方は上記のように設定するか
  空のindex.htmlでもアップロードしてください

suEXEC時の構成例
-- upload [701] / upload.cgi [700]
　　|             log.cgi    [600] --- 自動作成
　　|             upload.html[604] --- 自動作成
    |
　　+-- src [701] --- 自動作成

その他一般的な構成
-- upload [777] / upload.cgi [755]
　　|             log.cgi    [666] --- 自動作成
　　|             upload.html[666] --- 自動作成
    |
　　+-- src [777] --- 自動作成
//////

ファイルの削除方法
  1.ファイルNoの欄にNoを入れます
    up0001.jpg -> 1, 0001 , up0001 , up0001.jpg 等 数値が検出できれば(hoge001.pngでも)OKです
    JavaScriptが有効な場合 "D" と言う文字がファイル名の左側に出てきますのでそれをクリックされても結構です
  2.削除キーが必要なときは入力する
    管理者PASSを入れると全てのファイルが削除可能です
    また削除時のIPアドレスが投稿時IPアドレスの第3オクテット(192.168.0.9 の 192.168.0.)まで
    一致する場合又はユーザー固有IDが一致する場合に限っては削除キーは必要ではありません
  3.delを押す
  又,管理者はSUSS(Sn Uploader Support Script)にログインすることにより選択/一括削除ができます

HTMLを更新したい場合
  スクリプト改変/POSTKey有無等でフォームデザインが変わって更新したい場合は
  削除フォームにNoを入れずKeyの欄に管理者PASS($set{'admin_pass'})の値を入れてdelを押してください
  又はSUSS(Sn Uploader Support Script)にログインして作業をしてください

SUSS(Sn Uploader Support Script)
  要するに管理画面です 元々別スクリプトでしたが統合されました
  SUSSにログインするためには 削除フォームの Del欄に設定した管理者ログインID
  Key欄に管理者パスワード を入力してdelを押します
  ログインすると管理者画面に切り替わり ログの一括削除/エラーログ表示/設定表示などを見ることができます

Cookieについて
  このスクリプトではCookieを使用しています 主に削除補助として使います
  SN_UPLOAD(JavaScript) 投稿フォームのDelKey/PostKeyを記憶します
  SN_DEL   (JavaScript) 削除フォームのKeyを記憶します 値がない場合SN_UPLOADのDelKeyをコピーします
  SN_USER  (HTML_META)  ユーザー固有IDを記憶します
  Cookieの保存の期限とかは特に制限していないので気に食わなかったら該当部分を修正してください
  管理者はまず削除フォームに管理者PASSを入れ[del]を押し記憶させると
  ファイル削除やSUSSに入ったりする際にいくらか楽になると思います

バグを見つけたら…
  直す保証はありませんが掲示板等に報告もらえたら善処したいと思います

あんまり大したことではないこと
  稀に設置されたアップローダにあるファイルの削除依頼などが下部のリンクを辿って
  こちらに来ることがあるので デフォルトでは省略されていますが
  できれば $set{'home_url'}([HOME]のリンク先の値) は埋めてほしいかもしれません
  なおこの値は ../ や http://example.org/~user/ など相対パスでも絶対パスでも構いません

さらに大したことではないこと
  配布アーカイブの中にあるスクリプトファイルは標準的なエディタでも
  編集しやすいように文字コードにShift-JISを使用しています
  そのためバグというかShift-JISの一部の文字コードが\と重なっている影響で
  ファイル名に"表,予,ソ,ー"などが含まれているとファイル名が途中で切れます
  デザイン変更等で文字を追加挿入した場合 場所によっては500エラーがでることもあります
  別にバイナリが化けたりするわけではないのですが気になる人は
  エディタ等でスクリプト全体をEUCに変換するのがよいかと思います
  設定項目の終わりの方に $set{'html_head'} という項目があるのでcharsetを euc-jp にすると
  排出HTMLのMETAタグ部分は書き換わります
  ＃途中からEUCに切り替えるときはログファイルの変換もお忘れずに...

本当に大したことではないこと
  このスクリプトのデフォルトでは生成するHTMLの右下に配布ページへのリンクが張ってありますが
  デザインの変更や都合上削除したい場合は(もちろん残して頂ければ嬉しいのですが)
  リンク及び表示を削除して頂いても一向に構いません
  但しこれはスクリプトの著作権を放棄するということではありません


補足事項
  スクリプト内の説明で少々説明が足りないところがあるかもしれませんので補足しておきます

$set{'interval'}
  同一IPからの連続投稿を指定した秒数の間拒否します
  デフォルトは0秒になっていますが 例えば10分ならば 60*10 と表記しても問題ありません
  なお最終投稿のIP/時間でしか判断していないので上記の例ですと
  10分以内に他の人がアップロードをした場合は解除されてしまいます

$set{'max_all_flag'}
  この値を有効にすると投稿数以外にファイルの容量でもログ落ちを判定するようになります
  レンタルサーバなど容量が限られている場合役に立つのではないでしょうか？
  注意としては 例えば 1ファイルの最大容量が10MB($set{'max_size'} = 10*1024),
  総容量50MB($set{'max_all_size'}= 50*1024) に設定した場合
  サーバに既に50MBある状態で  10MBのファイルをアップロードされると
  一時的に 50MB+10MB = 60MB が消費されます また複数同時アップロード時にも同様のことが言えますので
  少し余裕を持って(サーバ制限量よりは少なめに)設定したほうがよさそうです
  また保持件数制限時もそうですが パーミッション設定,アクセス権などの関係で
  ファイルが削除できなかった場合は(ファイルが実際に残っているので)メインログからは削除していません
  よって設定ログ数/容量より実際のログ数/容量が多くなることがあります

$set{'up_all'}
  この値を有効にすると$set{'up_ext'}に登録されているもの以外でもアップロードを受け付けます
  $set{'ext_org'}が無効になっている場合(=0)は拡張子'.bin'で登録されます
  $set{'ext_org'}が有効になっている場合(=1)は投稿時の拡張子になります
  $set{'ext_org'}を有効にする場合(=1)は
  スクリプト言語など予期せぬ動作をする場合がありますので
  セキュリティーには十分気をつけて下さい

$set{'find_crypt'}
  この値が有効になっているとアップロードされたアーカイブが暗号化されているか調べます(ZIPのみ)
  暗号化されている場合はCOMMENTの最初に赤の"*"が付きます
  大体検出出来てるナ と思われる場合には排出HTMLのどこかに*はPASS付だ と書いておけば
  ダウンロードする側にも多少はメリット!?があるかなと思います

$set{'binary_compare'}
  この値が有効になっていると既にアップロードされているファイルとバイナリ比較をします
  一致したらファイルをアップロードさせません

$set{'post_key'}
  $set{'post_flag'}が有効になっている場合(=1)はこの値をフォームに入力しないと
  アップロードできなくなります PostKeyは,で区切ることで複数発行することができ
  メインログには備考として投稿された際のPostKeyが記録されます
  途中からPostKeyを有効にする場合は投稿フォームにPostKeyの項目がありませんので
  スクリプトを設定したら上記の「HTMLを更新したい場合」を参考にHTMLを更新してください

$set{'dlkey'}
  DLKeyの使用の有無
  アップロードされたファイルを ./src/up****.*** から ./src/up****.***_[a-zA-Z0-9]{20}/up****.***
  にリネームすることによって作成されるファイルリストのリンクより辿れなくします
  実URLは投稿時設定したDLKeyにて認証することによって参照できます
  perlを無駄に起動したくない場合は $set{'dummy_html'} の値を 2以上にすると、
  認証時のHTMLを静的HTMLで吐き出すようになります。
  無駄なCGIの起動が減りますので問題がなければ静的HTMLを吐き出すようにすることをお勧めします。

$set{'zero_clear'}
  FTPなどCGI以外からの操作でファイルを削除した場合
  メインログには情報が残っているがリンク先のファイルがないということがあります
  この値が有効な場合次回ファイルアップロード時に該当ファイル情報をメインログから削除します
  有効にしなかった場合は次回更新時からも0バイトのファイルとしてHTMLファイルリストに記載されます

$set{'http_src_path'}
  稀にファイルリストのリンクに相対PATHを使えないケースがありますので
  そのような場合はこの値を設定する事によって明示的にファイルの位置を指定できます
  尚指定した場合は ファイル保存ディレクトリ $set{'src_dir'} には 
  /home/user/public_html/upload/src/ などのサーバ内絶対PATHを使用することもできます
  相対PATH(デフォルト)で問題ない場合は特に設定しなくて構いません

$set{'link_target'}
  ファイル名に張られているリンクのtarget属性です
  新規のウィンドウで開きたい場合は _blank と入力します

Sn Uploader (c) 2003-2005 SUGA All rights reserved.
