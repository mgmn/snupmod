#!/usr/bin/perl

package snup;

use strict;
use warnings;
no warnings 'redefine';
use CGI;
use Encode;
use Net::SMTP;
use Net::POP3;

# カレントディレクトリの取得・変更
if(exists $ENV{MOD_PERL}){ my $chpath = $ENV{SCRIPT_FILENAME}; $chpath =~ s/[^\/]+$//; chdir($chpath); undef $chpath; }

our %set;
our %in;

$set{'log_file'} = './log/upload.log';	#ログファイル名
$set{'max_log_flag'} = 0;				#保持件数制限を使用する=1
$set{'max_log'} = 30;					#保持件数
$set{'max_size'} = 10*1024;				#最大投稿容量(KB)
$set{'min_flag'} = 0;					#最小容量制限を使用する=1
$set{'min_size'} = 100;					#最小投稿容量(KB)
$set{'max_all_flag'} = 0;				#総容量制限を使用する=1
$set{'max_all_size'} = 20*1024;			#総制限容量(KB)
$set{'file_pre'} = 'up';				#ファイル接頭辞
$set{'pagelog'} = 10;					#1ページに表示するファイル数
$set{'base_html'} = 'index.html';		#1ページ目のファイル名
$set{'interval'} = 0;					#同一IP投稿間隔秒数
$set{'deny_host'} = '';					#投稿禁止IP/HOST ,で区切る ex.(bbtec.net,219.119.66,ac.jp)
$set{'admin_name'} = 'admin';			#管理者ログインID
$set{'admin_pass'} = '1234';			#管理者パスワード

$set{'mail_notify'} = 0;					#メール通知を使う
$set{'mail_server'} = 'localhost';			#SMTPサーバ
$set{'mail_port'} = 25;						#SMTPポート
$set{'notify_to'} = 'admin@example.com';	#メール通知の宛先アドレス
$set{'notify_from'} = 'notify@example.com';	#メール通知の送信元アドレス
$set{'smtp_auth'} = 0;						#POP before SMTP認証を行う
$set{'pop_server'} = 'localhost';			#POP3サーバ
$set{'pop_port'} = 110;						#POP3ポート
$set{'pop_userid'} = '';					#POP3ログインID
$set{'pop_passwd'} = '';					#POP3パスワード

# 以下7項目を再設定する際にはPATH，ディレクトリは / で終わること
# $set{'html_dir'}, $set{'base_cgi'}を ./ 以外に設定する場合,
# またはDLkeyを使用し なおかつHTMLキャッシュ($set{'dummy_html'} = 2 or 3)を使用する場合は
# $set{'base_cgi'} , $set{'http_html_path'} , $set{'http_src_path'} , $set{'img_dir'}を
# フルパス(http://～～ or /～～)で記述する
$set{'html_dir'} = './';			#内部HTML保存ディレクトリ
$set{'src_dir'} = './src/';			#内部ファイル保存ディレクトリ
$set{'thumb_dir'} = './thumb/';		#サムネイル保存ディレクトリ
$set{'base_cgi'} = './upload.pl';	#このスクリプト名 http://～の指定可能
$set{'http_html_path'} = './';		#html参照 httpPATH http://～の指定可能
$set{'http_src_path'} = './src/';	#file参照 httpPATH http://～の指定可能
$set{'img_dir'} = './img/';			#css, jsの参照先 http://～の指定可能

$set{'dlkey'} = 0;		# DLKeyを使用する=1,DLkey必須=2
# アップロードできる基本拡張子 半角英数小文字 ,で区切る
$set{'up_ext'} = 'bmp,class,css,dat,gca,gif,hta,jar,java,jpg,js,lzh,png,rar,swf,txt,vbs,wsf,xml,zip';
$set{'up_all'} = 0;		#登録以外のものもUPさせられるようにする=1
$set{'ext_org'} = 0;	#$set{'up_all'}が1の時オリジナルの拡張子にする=1
# 投稿禁止の拡張子 半角英数小文字 ,で区切る
$set{'deny_ext'} = 'php,php3,phtml,rb,sh,bat,dll';
# 拡張子変換 前->後 半角英数小文字 ,で区切る
$set{'change_ext'} = 'cgi->txt,pl->txt,log->txt,jpeg->jpg,mpeg->mpg';

$set{'home_url'} = '';					#[HOME]のリンク先 相対パス又は http://から始まる絶対パス
$set{'html_all'} = 0;					#[ALL]を出す=1
$set{'dummy_html'} = 0;					#ファイル個別HTMLを作成する 通常ファイルのみ=1,DLKey設定ファイルのみ=2,すべて=3
$set{'find_crypt'} = 1;					#暗号化ZIPを検出する=1
$set{'binary_compare'} = 0;				#既存ファイルとバイナリ比較する=1
$set{'post_flag'} = 0;					#PostKeyを使用する=1
$set{'post_key'} = 'postkey';			#PostKey ,で区切ると複数指定 ex.(postkey1,postkey2)
$set{'disp_error'} = 1;					#ユーザーにエラーを表示する=1
$set{'error_level'} = 1;				#エラーログを記録する=1
$set{'error_log'} = './log/error.log';	#エラーログファイル名
$set{'error_size'} = 1024;				#エラーログ最大容量(KB) 制限なし=0
$set{'zero_clear'} = 1;					#ファイルが見つからない場合ログから削除する=1

$set{'disp_comment'} = 1; 	#コメントを表示する=1
$set{'disp_date'} = 1;		#日付を表示する=1
$set{'disp_size'} = 1;		#サイズを表示する=1
$set{'disp_mime'} = 0;		#MIMETYPEを表示する=1
$set{'disp_orgname'} = 0;	#オリジナルファイル名を表示する=1
$set{'disp_thumb'} = 1;		#サムネイルを表示する=1

$set{'per_upfile'} = 0666;	#アップロードファイルのパーミッション suexec=0604,other=0666
$set{'per_dir'} = 0777;		#ソースアップディレクトリのパーミッション suexec=0701,other=0777
$set{'per_logfile'} = 0666;	#ログファイルのパーミッション　suexec=0600,other=0666
$set{'link_target'} = '';	#target属性

#------
$set{'ver'} = '2005/10/10e CGI.pm + mod.1603072206';
if(defined($ENV{'MOD_PERL'})){ $set{'ver'} .= ' + ' .$ENV{'MOD_PERL'}; }
$set{'char_delname'} = '消';

$in{'time'} = time(); $in{'date'} = &snup::conv_date($in{'time'});
$in{'addr'} = $ENV{'REMOTE_ADDR'};
$in{'host'} = gethostbyaddr(pack('C4',split(/\./, $in{'addr'})), 2) || $ENV{'REMOTE_HOST'} || '(none)';

if($in{'addr'} eq $in{'host'}){ $in{'host'} = '(none)'; }

#タイトル
$set{'html_title'} = 'Uploader';

#説明
$set{'html_desc'} = <<"EOM";
	<ul>
		<li>アップローダーです。</li>
		<li>画像を上げるとサムネイルが生成されます。</li>
		<li>画像じゃなくても色々上げられます。</li>
		<li style="color:#f00">注: DELKeyを空白にするとup時と異なるIPからファイル削除ができなくなります。</li>
	</ul>
	<hr />
EOM

#HTMLヘッダ
$set{'html_head'} = <<"EOM";
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE html>
<html lang="ja-jp" xml:lang="ja-jp" xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta charset="UTF-8" />
	<title>$set{'html_title'}</title>
	<!--[if lte IE 8]>
		<script type="text/javascript" src="$set{'img_dir'}html5.js"></script>
		<link rel="stylesheet" href="$set{'img_dir'}html5.css" type="text/css" />
	<![endif]-->
	<link rel="stylesheet" href="$set{'img_dir'}style.css" type="text/css" />
EOM

&snup::main();

#変数破棄
undef %set;
undef %in;


BEGIN{
sub main{

unless(-e $set{'log_file'}){ &snup::init; }
unless(-e $set{'base_html'}){ &snup::makehtml; }

{ #デコード
	my $q = new CGI;

	my $postsize = defined($q->param('POSTDATA')) ? length($q->param('POSTDATA')) : 0;
	if ($ENV{'REQUEST_METHOD'} eq 'POST' && $ENV{'CONTENT_TYPE'} =~ /multipart\/form-data/i){
		if($postsize > ($set{'max_size'} * 1024 + 1024)){ &snup::error(106, $postsize); }
	}else{
		if($postsize > 1024*100){ &snup::error(98); }
	}

	my(%ck, @ck);
	if(defined($ENV{'HTTP_COOKIE'})){
		foreach(split(/;/, $ENV{'HTTP_COOKIE'})){ my($key, $val) = split(/=/); $key =~ s/\s//g; $ck{$key} = $val;}
		@ck = split(/<>/, $ck{'SN_USER'});
	}else{ @ck = (''); }
	if(length($ck[0]) < 5){
		my @salt = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/'); srand;
		my $salt = $salt[int(rand(@salt))] . $salt[int(rand(@salt))];
		$in{'user'} = crypt($in{'addr'}.$in{'time'}, $salt);
	}else{ $in{'user'} = $ck[0]; }

	$in{'upfile'} = $q->param('upfile') || 0;
	$in{'tmpfile'} = $q->tmpFileName($in{'upfile'}) || 0;
	$in{'type'} = $in{'upfile'} ? $q->uploadInfo($in{'upfile'})->{'Content-Type'} : '';
	$in{'pass'} = $q->param('pass') || '';
	$in{'mode'} = $q->param('mode') || '';
	$in{'delno'} = $q->param('delno') || '';
	$in{'comment'} = $q->param('comment') || '';
	$in{'jcode'} = $q->param('jcode') || '';
	$in{'delpass'} = $q->param('delpass') || '';
	$in{'orgname'} = $in{'upfile'};
	$in{'postkey'} = $q->param('postkey') || '';
	$in{'org_pass'} = $in{'pass'} || '';
	$in{'checkmode'} = $q->param('checkmode') || '';
	$in{'file'} = $q->param('file');
	$in{'dlkey'} = $q->param('dlkey') || '';
	$in{'admin_delno'} = join(',', $q->param('admin_delno'));
	my @denyhost = split(/,/, $set{'deny_host'});
	foreach my $value (@denyhost){
		if ($in{'addr'} =~ /$value/ || $in{'host'} =~ /$value/){ &snup::error(101);}
	}

	my @form = ($in{'comment'}, $in{'orgname'}, $in{'type'}, $in{'dlkey'});
	my $aaa;
	foreach my $value (@form){
		if(defined($value)){
			if (length($value) > 128){ $value = substr($value, 0, 128).'...'; }
			$value =~ s/&/&amp;/g;
			$value =~ s/"/&quot;/g;
			$value =~ s/</&lt;/g;
			$value =~ s/>/&gt;/g;
			$value =~ s/\r//g;
			$value =~ s/\n//g;
			$value =~ s/\t//g;
			$value =~ s/\0//g;
		}
	}
	($in{'comment'}, $in{'orgname'}, $in{'type'}, $in{'dlkey'}) = @form;
	 $in{'tmpfile2'} = &snup::filewrite() if ($in{'upfile'});
}

if($in{'delno'} eq $set{'admin_name'} && $in{'delpass'} eq $set{'admin_pass'}){ &snup::admin_mode(); }
if(!$in{'delno'} && $in{'delpass'} eq $set{'admin_pass'}){ &snup::makehtml(); &snup::quit(); }
if($in{'mode'} eq 'dl'){ &snup::dlfile;} #DL
if($in{'mode'} eq 'delete'){ &snup::delete(); &snup::quit(); }

{#メイン処理
	if(!$in{'upfile'}){ &snup::error(99); }
	if($set{'post_flag'} && !&snup::check_postkey($in{'postkey'})){ &snup::error(109); }
	if($set{'dlkey'} == 2 && !$in{'dlkey'}){ unlink("$in{'tmpfile2'}"); &snup::error(61); }
	open(IN, $set{'log_file'}) || &snup::error(303);
	my @log = <IN>;
	close(IN);
	my ($no, $lastip, $lasttime) = split(/<>/, $log[0]);

	if($set{'interval'} && $set{'interval'} && $in{'time'} <= ($lasttime + $set{'interval'}) && $in{'addr'} eq $lastip){ &snup::error(203);}
	$in{'ext'} = &snup::extfind($in{'orgname'}); if(!$in{'ext'} && $in{'upfile'}){ &snup::error(202); }

	my $orgname;
	if((() = $in{'orgname'} =~ /\//g) > (() = $in{'orgname'} =~ /\\/g)){	my @name = split(/\//, $in{'orgname'}); $orgname = $name[$#name]; }
	else{ my @name = split(/\\/, $in{'orgname'}); $orgname = $name[$#name];}

	my @salt = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');
	srand;
	my $salt = $salt[int(rand(@salt))] . $salt[int(rand(@salt))];
	$in{'pass'} = crypt($in{'pass'}, $salt);

	if($set{'binary_compare'}){
		my @files = &snup::globfile("$set{'src_dir'}", ".*");
		my @dir = &snup::globdir("$set{'src_dir'}", ".*");
		foreach my $dir (@dir){ push(@files, &snup::globfile($dir."/", ".*")); }
		foreach my $value (@files){
			next if($value =~ /\.temporary$/);
			if(&snup::binarycmp($in{'tmpfile2'}, $value)){ unlink($in{'tmpfile2'}); &snup::error(205, $value);}
		}
	}

	if($set{'find_crypt'}){
		open(FILE, $in{'tmpfile2'}); binmode(FILE); seek(FILE, 0, 0); read(FILE,my $buff, 4); my $crypt_flag = 0;
		if($buff =~ /^\x50\x4b\x03\x04$/){ seek(FILE, 6, 0); read(FILE,my $buff, 1); $crypt_flag = 1 if(($buff & "\x01") eq "\x01"); }
		close(FILE);
		$in{'comment'} = '<span class="red">*</span>'.$in{'comment'} if($crypt_flag);
	}

	open(IN, $set{'log_file'}) || &snup::error(303);
	@log = <IN>;
	close(IN);
	($no, $lastip, $lasttime) = split(/<>/, $log[0]);
	shift(@log);
	$no++;
	my $tmpno = sprintf("%04d", $no);

	my $dlsalt;
	my $filedir;
	my $allsize = (-s $in{'tmpfile2'});

	if($set{'dlkey'} && $in{'dlkey'}){
		my @salt = ('a'..'z', 'A'..'Z', '0'..'9'); srand;
		for (my $c = 1; $c <= 20; ++$c){ $dlsalt .= $salt[int(rand(@salt))]; }
	 	$filedir = "$set{'src_dir'}$set{'file_pre'}${tmpno}.$in{'ext'}_$dlsalt/";
		mkdir($filedir, $set{'per_dir'});
		rename("$in{'tmpfile2'}", "$filedir$set{'file_pre'}$tmpno.$in{'ext'}");
		open(OUT, ">${filedir}index.html");
		close(OUT);
		chmod($set{'per_upfile'}, "${filedir}index.html");
		$in{'comment'} = '<span class="red">[DLKey] </span>'.$in{'comment'};
	}else{
		$in{'dlkey'} = 0;
		rename("$in{'tmpfile2'}", "$set{'src_dir'}$set{'file_pre'}$tmpno.$in{'ext'}");
	}

	# サムネイル作成
	require Image::Magick;
	my $thumb = Image::Magick->new;
	# ImageMagickではカレントディレクトリが変わらない対策
	my $chpath = $ENV{SCRIPT_FILENAME};
	$chpath =~ s/[^\/]+$//;
	unless($set{'dlkey'} && $in{'dlkey'}){
		if($in{'type'} =~ /bmp|gif|jpe?g|png/){ # 画像ファイル
			$thumb->Read("${chpath}$set{'src_dir'}$set{'file_pre'}${tmpno}.$in{'ext'}");
			my $w = $thumb->Get('width');
			my $h = $thumb->Get('height');
			my $ts = $w < $h ? $w : $h;
			my $tx = ($w - $ts) /2;
			my $ty = ($h - $ts) /2;
			$thumb->Crop(width=>$ts, height=>$ts, x=>$tx, y=>$ty);
			$thumb->Resize(width=>100, height=>100);
			$thumb->Set(quality=>90);
			$thumb->Write("${chpath}$set{'thumb_dir'}$set{'file_pre'}${tmpno}.jpg");
		}elsif($in{'type'} =~ /zip|lzh|rar/){ # zipファイル
			$thumb->Read("${chpath}$set{'thumb_dir'}_zip.jpg");
			$thumb->Write("${chpath}$set{'thumb_dir'}$set{'file_pre'}${tmpno}.jpg");
		}else{ # その他
			$thumb->Read("${chpath}$set{'thumb_dir'}_noimage.jpg");
			$thumb->Write("${chpath}$set{'thumb_dir'}$set{'file_pre'}${tmpno}.jpg");
		}
	}else{ # パス付き
		$thumb->Read("${chpath}$set{'thumb_dir'}_noimage.jpg");
		$thumb->Write("${chpath}$set{'thumb_dir'}$set{'file_pre'}${tmpno}.jpg");
	}
	undef $thumb;
	undef $chpath;

	if (length($orgname) > 128){ $orgname = substr($orgname, 0, 128).'...'; }

	my @note;
	if($set{'post_flag'} && $set{'post_key'}){
		push(@note, 'PostKey:'.$in{'postkey'});
	}
	if($ENV{'SERVER_SOFTWARE'} =~ /Apache|IIS/){
		my $disptime;
		my $time = time() - $in{'time'};
		my @str = ('Upload:', '秒');
		$disptime = $time.$str[1];
		push(@note, $str[0].$disptime);
	}
	if($in{'dlkey'}){
		my @salt = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/'); srand;
		my $salt = $salt[int(rand(@salt))] . $salt[int(rand(@salt))];
		my $crypt_dlkey  = crypt($in{'dlkey'}, $salt);
		push(@note, "DLKey<!-- DLKey:".$crypt_dlkey." --><!-- DLpath:".$dlsalt." -->");
	}
	my $note = join(',', @note);
	my $usersalt = substr($in{'user'}, 0, 2);
	my $userid = crypt($in{'user'}, $usersalt);
	$in{'time'} = time();
#	$in{'date'} = &snup::conv_date(time());
	my @new;
	$new[0] = "$no<>$in{'addr'}<>$in{'time'}<>1\n";
	my $addlog = "$no<>$in{'ext'}<>$in{'date'}<>$in{'comment'}<>$in{'type'}<>$orgname<>$in{'addr'}<>$in{'host'}<>$in{'pass'}, $userid<>$set{'file_pre'}<>$note<>1\n";
	$new[1] = $addlog;

#	open(OUT, ">>./alllog.cgi"); print OUT $addlog; close(OUT);
	my $notification_body = <<"EOM";
UPLOADED: $set{'file_pre'}$tmpno.$in{'ext'}
UPLOADED_DATE: $in{'date'}
COMMENT: $in{'comment'}
MIME_TYPE: $in{'type'}
ORIGINAL: $orgname
REMOTE_ADDR: $in{'addr'}
REMOTE_HOST: $in{'host'}
NOTE: $note
EOM
	&snup::send_notification('File uploaded', $notification_body);

	my $i = 2;

	foreach my $value (@log){
		my ($no, $ext, $date, $comment, $mime, $orgname, $addr, $host, $pass, $filepre, $note, $dummy) = split(/<>/, $value);
		if(!$dummy){ $filepre = $set{'file_pre'};}
		$no = sprintf("%04d", $no);

		my $filename;
		my $filedir;
		if($note =~ /DLpath:(.+)\s/){
			my $dlpath = $1;
			$filename = "$set{'src_dir'}$filepre$no.${ext}_$dlpath/$filepre$no.$ext";
			$filedir = "$set{'src_dir'}$filepre$no.${ext}_$dlpath/";
		}else{
			$filename = "$set{'src_dir'}$filepre$no.$ext";
		}
		$allsize += (-s $filename);

		if((!$set{'max_log_flag'} || $i <= $set{'max_log'}) && !($set{'max_all_flag'} && $set{'max_all_size'}*1024 < $allsize)){
			if((-e $filename) || !$set{'zero_clear'}){ push(@new, $value); $i++; }
		}else{
			if(unlink($filename)){
				unlink("$set{'src_dir'}$filepre$no.$ext.html"); if($filedir){ foreach(&snup::globfile($filedir, ".*")){ unlink; } } rmdir($filedir);
			}elsif(unlink($filename)){
				unlink("$set{'src_dir'}$filepre$no.$ext.html"); if($filedir){ foreach(&snup::globfile($filedir, ".*")){ unlink; } } rmdir($filedir);
			}elsif(-e $filename){
				push(@new, $value);
			}else{
				unlink("$set{'src_dir'}$filepre$no.$ext.html"); if($filedir){ foreach(&snup::globfile($filedir, ".*")){ unlink; } } rmdir($filedir);
			}
		}
	}
	&snup::logwrite(@new);
	if($in{'dlkey'} && ( $set{'dummy_html'} == 2 || $set{'dummy_html'} == 3)){
		&snup::makedummyhtml("$set{'file_pre'}$tmpno.$in{'ext'}", $in{'comment'}, "$set{'file_pre'}$tmpno.$in{'ext'}", $dlsalt, $in{'date'}, $in{'type'}, $orgname, $no);
	}elsif(!$in{'dlkey'} && ($set{'dummy_html'} == 1 || $set{'dummy_html'} == 3)){
		&snup::makedummyhtml("$set{'file_pre'}$tmpno.$in{'ext'}");
	}
	&snup::makehtml(); &snup::quit();
}

} # /sub main

sub makehtml{

	my $buff = '';
	my $init = 0;
	my $page = 0; my $i = 1;

	open(IN, $set{'log_file'}) || &snup::error(303);
	my $log = my @log = <IN>;
	close(IN);

	if($log == 1){ $log++; $init++;}
	my $lastpage = int(($log - 2) / $set{'pagelog'}) + 1;
	my $header = <<"EOM";
$set{'html_head'}	<script src="$set{'img_dir'}upload.js" type="text/javascript"></script>
</head>
<body>

<header id="header">
	<h1>$set{'html_title'}</h1>
$set{'html_desc'}
</header><!-- /#header -->

<section id="upform">
EOM
	my $maxsize = 'Max '.&snup::dispsize($set{'max_size'}*1024);
	my ($minsize, $total);
	$minsize = $set{'min_flag'} ? 'Min '.&snup::dispsize($set{'min_size'}*1024).' - ' : '';
	if($set{'max_all_flag'}){ $total .= ' Total '.&snup::dispsize($set{'max_all_size'}*1024);}
	$header .= qq|\t<form method="post" enctype="multipart/form-data" action="$set{'base_cgi'}" name="Form" id="Form">|;
	$header .= "\n\t\t<ul>\n";
	$header .= "\t\t\t<li>アプするファイル（$minsize$maxsize）";
	if($set{'max_log_flag'}){ $header .= qq|(*$set{'max_log'}Files$total)|; }
	$header .= "</li>\n\t\t\t<li>";
	$header .= qq|\n\t\t\t\t<input type="file" name="upfile" id="upfile" />|;
	$header .= qq|\n\t\t\t\tDLKey: <input type="text" size="8" maxlength="8" name="dlkey" id="dlkey" />| if($set{'dlkey'});
	$header .= qq|\n\t\t\t\tDELKey: <input type="password" size="10" maxlength="8" name="pass" id="pass" />
			</li>
			<li>コメント</li>
			<li>
				<input type="text" size="45" name="comment" id="comment" />
				<input type="hidden" value="漢字" name="jcode" id="jcode" />
				<input type="submit" value="Upload" /><input type="reset" value="Cancel" />
			</li>|;
	if($set{'post_flag'}){
		$header .= "\t\t<li>PostKey</li>";
		$header .= qq|\n\t\t<li><input type="password" size="10" maxlength="10" name="postkey" id="postkey" /></li>\n|;
	}
	$header .= qq|
		</ul>
	</form>
</section><!-- /#upform -->
|;

	my $allsize = 0;
	my @files = &snup::globfile("$set{'src_dir'}", ".*");
	my @dir = &snup::globdir("$set{'src_dir'}", ".*");
	foreach my $dir (@dir){	push(@files,&snup::globfile($dir."/", ".*")); }
	foreach my $value (@files){ $allsize += (-s "$value"); }

	$allsize = &snup::dispsize($allsize);

	my $footer = qq|
<footer id="footer">
	<p>Used ${allsize}</p>
	<p>up可能拡張子: |;

	if($set{'up_all'} && !$set{'ext_org'}){ $footer .= $set{'up_ext'}.' +'; }
	elsif(!$set{'up_all'}){ $footer .= $set{'up_ext'}; }
	$footer .= <<"EOM";
</p>
	<div style="float: left;">
		<form method="post" action="$set{'base_cgi'}" name="Del" id="Del">
			<span style="font-size: 9pt">
				<input type="hidden" name="mode" value="delete" />
				No.<input type="text" size="4" name="delno" />
				key<input type="password" size="4" name="delpass" />
				<input type="submit" value="del" name="del" />
			</span>
		</form>
	</div>
	<div style="float: right;">
		<!-- $set{'ver'} -->
		<address>
			<a href="http://sugachan.dip.jp/download/">Sn Uploader</a>
			<a href="http://kaz-ic.net/tools/sn-uploader-kai">kai</a>
		</address>
	</div>
</footer><!-- /#footer -->

</body>
</html>
EOM

	my $upinfo_section_start = qq|\n<section id="upinfo">\n|;
	my $upinfo_section_end   = qq|\n</section><!-- /#upinfo -->\n|;

	my $table_header = qq|
	<table style="width: 100%;">
		<tr>
			<th></th>
			<th>NAME</th>\n|;
	if($set{'disp_comment'}){ $table_header .= "\t\t\t<th>COMMENT</th>\n"; }
	if($set{'disp_size'}){ $table_header .= "\t\t\t<th>SIZE</th>\n"; }
	if($set{'disp_date'}){ $table_header .= "\t\t\t<th>DATE</th>\n"; }
	if($set{'disp_mime'}){ $table_header .= "\t\t\t<th>MIME</th>\n"; }
	if($set{'disp_orgname'}){ $table_header .= "\t\t\t<th>ORIG</th>\n"; }
	if($set{'disp_thumb'}){ $table_header .= "\t\t\t<th>THUMBNAIL</th>\n"; }
	$table_header .= "\t\t</tr>\n";

	my $table_footer = "\t</table>\n";

	my $home_url_link = $set{'home_url'} ? "\t\t<li><a href=\"$set{'home_url'}\">[HOME]</a></li>\n" : '';
	if($set{'html_all'}){
		my $no = 1; my $subheader;
		foreach my $value (@log){
			my ($no, $ext, $date, $comment, $mime, $orgname, $addr, $host, $pass, $dummy) = split(/<>/, $value);
			if(!$dummy){ next; }
			$buff .= &snup::makeitem($value);
		}
		$subheader .= "\t<hr />\n\t<ul>\n";
		$subheader .= "\t\t<li>[ALL]</li>\n";
		while($no <= $lastpage){
			if($no == $page){ $subheader .= "<li>\[$no\]</li>\n";}
			else{
				if($no == 1){ $subheader .= "\t\t<li><a href=\"$set{'http_html_path'}$set{'base_html'}\">\[$no\]</a></li>\n"; }
				else{ $subheader .= "\t\t<li><a href=\"$set{'http_html_path'}$no.html\">\[$no\]</a></li>\n"; }
			}
			$no++;
		}
		$subheader .= "\t</ul>\n\t<hr />\n";

		open(OUT, ">$set{'html_dir'}all.html") || &snup::error(306, "$set{'html_dir'}all.html");
		print OUT $header
			.$home_url_link
			.$upinfo_section_start
			.$subheader
			.$table_header
			.$buff
			.$table_footer
			.$subheader
			.$upinfo_section_end
			.$footer;
		close(OUT);
		chmod($set{'per_upfile'}, "$set{'html_dir'}all.html");
		$buff = '';
	}else{ unlink("$set{'html_dir'}all.html"); }

	while($log > $i){
		$buff .= &snup::makeitem($log[$i]) unless($init);
		if(($i % $set{'pagelog'}) == 0 || $i == $log -1){
			$page++; my $subheader; my $no = 1;
			$subheader .= "\t<hr />\n\t<ul>\n";
			if($set{'html_all'}){ $subheader .= "\t\t<li><a href=\"./all.html\">[ALL]</a></li>\n"; }
			while($no <= $lastpage){
				if($no == $page){ $subheader .= "\t\t<li>\[$no\]</li>\n";}
				else{	if($no == 1){ $subheader .= "\t\t<li><a href=\"$set{'http_html_path'}$set{'base_html'}\">\[$no\]</a></li>\n"}
						else{$subheader .= "\t\t<li><a href=\"$set{'http_html_path'}$no.html\">\[$no\]</a></li>\n";}
				}
				$no++;
			}
			$subheader .= "\t</ul>\n\t<hr />\n";

			my $loghtml;
			if($page == 1){	$loghtml = "$set{'html_dir'}$set{'base_html'}"; }
			else{ $loghtml = "$set{'html_dir'}$page.html"; }

			open(OUT, ">$loghtml") || &snup::error(306, "$loghtml");
			print OUT $header
				.$home_url_link
				.$upinfo_section_start
				.$subheader
				.$table_header
				.$buff
				.$table_footer
				.$subheader
				.$upinfo_section_end
				.$footer;
			close(OUT);
			chmod($set{'per_upfile'}, $loghtml);
			undef $buff;
		}
		$i++;
	}

	while($page < 1000){
		$page ++;
		if(-e "$set{'html_dir'}$page.html"){ unlink("$set{'html_dir'}$page.html"); }else{ last; }
	}
}

sub filewrite{
	my $random = int(rand(900000)) + 100000;
	if(-e "$set{'src_dir'}$random.temporary"){ $random++; }
	if(-e "$set{'src_dir'}$random.temporary"){ &snup::error(204); }
	open (FILE, ">$set{'src_dir'}$random.temporary") || &snup::error(204);
	binmode(FILE);
	eval{ while(my $read = read($in{'upfile'}, my $buff, 8192)){ print FILE $buff; }};
	close(FILE);
	chmod($set{'per_upfile'}, "$set{'src_dir'}$random.temporary");
	if((-s "$set{'src_dir'}$random.temporary") == 0){ unlink("$set{'src_dir'}$random.temporary"); &snup::error(99); }
	my $size = (-s "$set{'src_dir'}$random.temporary");
	if($set{'min_flag'} && ($size < $set{'min_size'} * 1024)){ unlink("$set{'src_dir'}$random.temporary"); &snup::error(107, $size);}
	if($size > $set{'max_size'} * 1024){ unlink("$set{'src_dir'}$random.temporary"); &snup::error(106, $size);}
	eval{ if(defined($in{'upfile'}) && -t $in{'upfile'}){ close($in{'upfile'}); }};
	unlink($in{'tmpfile'});
	return("$set{'src_dir'}$random.temporary");
}

sub delete{
	my $mode = $_[0];
	if(!defined($mode)){ $mode = ''; }
	my @delno = defined($_[1]) ? split(/,/, $_[1]) : ();
	my $delno; my $flag = 0; my $tmpaddr;
	my $delnote;
	my $deleted_list = '';

	if($in{'delno'} =~ /(\d+)/){ $delno = $1; }
	if($mode ne 'admin' && !$in{'delno'}){ return; }
	elsif($mode ne 'admin' && !$delno){ &snup::error(401, $in{'delno'}); }

	open(IN, $set{'log_file'}) || &snup::error(303);
	my @log = <IN>;
	close(IN);

	if($in{'addr'} =~ /(\d+).(\d+).(\d+).(\d+)/){ $tmpaddr = "$1.$2.$3."; }
	my $findflag = 0;
	foreach my $value (@log){
		my ($no, $ext, $date, $comment, $mime, $orgname, $addr, $host, $pass, $filepre, $note, $dummy) = split(/<>/, $value);
		$delnote = $note;
		my $delflag = 0;
		if(!$addr){ next; }
		if($mode eq 'admin'){
			foreach my $delno (@delno){ if($no == $delno){ $delflag = 1; last; } }
		}elsif($no == $delno){
			$findflag = 1;
			unless ($addr =~ /^$tmpaddr/){
				my ($pass, $id) = split(/,/, $pass);
				my $delpass = $in{'delpass'} || $in{'addr'}.time();
				my $salt = substr($pass, 0, 2);	$delpass = crypt($delpass, $salt);
				my $usersalt = substr($in{'user'}, 0, 2); my $userid = crypt($in{'user'}, $usersalt);
				if ($in{'delpass'} ne $set{'admin_pass'} && $delpass ne $pass && $userid ne $id){
					if($mode ne 'admin'){ if(!$dummy){ $filepre = $set{'file_pre'};} $no = sprintf("%04d", $no); &snup::error(404, "$filepre$no.$ext");}
				}
			}
			$delflag = 1;
		}
		if($delflag){
#			open(OUT, ">>./del.cgi"); print OUT $value; close(OUT);
			$flag = 1;
			if(!$dummy){ $filepre = $set{'file_pre'};}
			$no = sprintf("%04d", $no);
			my $filename;
			my ($dlpath, $filedir);
			if($delnote =~ /DLpath:(.+)\s/){
				$dlpath = $1;
				$filename = "$set{'src_dir'}$filepre$no.${ext}_$dlpath/$filepre$no.$ext";
				$filedir = "$set{'src_dir'}$filepre$no.${ext}_$dlpath/";
			}else{
				$filename = "$set{'src_dir'}$filepre$no.$ext";
			}

			if(unlink($filename)){
				unlink("$set{'src_dir'}$filepre$no.$ext.html"); if($filedir){ foreach(&snup::globfile($filedir, ".*")){ unlink; } rmdir($filedir);} $value = '';
			}elsif(unlink($filename)){
				unlink("$set{'src_dir'}$filepre$no.$ext.html"); if($filedir){ foreach(&snup::globfile($filedir, ".*")){ unlink; } rmdir($filedir);} $value = '';
			}elsif(!(-e $filename)){
				unlink("$set{'src_dir'}$filepre$no.$ext.html"); if($filedir){ foreach(&snup::globfile($filedir, ".*")){ unlink; } rmdir($filedir);} $value = '';
			}else{
				if($mode ne 'admin'){ &snup::error(403, "$filepre$no.$ext");}
			}
			$deleted_list .= " $filepre$no.$ext";
		}
	}
	if($mode ne 'admin' && !$findflag){ &snup::error(402, $delno); }
	if($flag){
		my $notification_body = <<"EOM";
DELETED:$deleted_list
DELETED_DATE: $in{'date'}
REMOTE_ADDR: $in{'addr'}
REMOTE_HOST: $in{'host'}
EOM
		&snup::send_notification('File deleted', $notification_body);
		&snup::logwrite(@log);
		&snup::makehtml();
	}
}

sub quit{
	my ($cookiename, $buff);
	my $flag = 0;
	my @tmpfiles = &snup::globfile("$set{'src_dir'}", "\.temporary");
	foreach my $value (@tmpfiles){ if((stat($value))[10] < time - 60*60){ unlink("$value"); $flag++; } }
	&snup::makehtml() if($flag);
	$buff = <<"EOM";
$set{'html_head'}	<script type="text/javascript"><!--
		setTimeout(function(){ location.href = "$set{'http_html_path'}$set{'base_html'}?$in{'time'}" }, 1000);
	--></script>
EOM
	if($in{'jcode'} || $in{'mode'} eq 'delete'){
		$buff .= <<"EOM";
	<meta http-equiv="Set-Cookie" content="SN_USER=$in{'user'}&lt;&gt;1; path=/; expires=Tue, 31-Dec-2030 23:59:59 GMT">
	<script type="text/javascript"><!--
		setCookie();
		function setCookie(){
			var key1,key2;
			var tmp = "path=/; expires=Tue, 31-Dec-2030 23:59:59; ";
EOM
		if($in{'jcode'}){
			my(%ck, @ck);
			if(defined($ENV{'HTTP_COOKIE'})){
				foreach(split(/;/, $ENV{'HTTP_COOKIE'})){ my($key, $val) = split(/=/); $key =~ s/\s//g; $ck{$key} = $val;}
				@ck = split(/<>/, $ck{'SN_DEL'});
			}else{ @ck = (); }
			if(!$ck[0] && $in{'org_pass'}){ $buff .= qq|\t\t\tdocument.cookie = "SN_DEL="+escape('$in{'org_pass'}')+"<>;"+ tmp;\n|; }
			$cookiename = 'SN_UPLOAD'; $buff .= "\t\t\tkey1 = escape('$in{'org_pass'}'); key2 = escape('$in{'postkey'}');\n";}
		else{ $cookiename = 'SN_DEL'; $buff .= "\t\t\tkey1 = escape('$in{'delpass'}'); key2 = '';\n"; }
		$buff .= qq|\t\t\tdocument.cookie = "$cookiename=" +key1 +"<>" +key2 +"; " +tmp;\n\t\t}\n\t--></script>\n|;
	}
	$buff .= <<"EOM";
</head>
<body>

<div id="wrapper">
	<section id="content">
		<a href="$set{'http_html_path'}$set{'base_html'}?$in{'time'}" style="font-size: 20px;">click here!</a>
	</section><!-- /#content -->
</div>

</body>
</html>
EOM
	print "Content-type: text/html\n\n";
	print $buff;
	exit;
}

sub admin_mode{
	&snup::errorclear() if($in{'mode'} eq 'errorclear');
	&snup::delete('admin', $in{'admin_delno'}) if($in{'mode'} eq 'delete');

	open(IN, $set{'log_file'}) || &snup::error(303);
	my @log = <IN>;
	close(IN);

	my ($header, $buff, $footer, $value);
	$buff = <<"EOM";
$set{'html_head'}</head>
<body>

<header id="header">
	<h1>Admin</h1>
	<form action="$set{'base_cgi'}" method="post">
		<input type="hidden" name="delpass" value="$set{'admin_pass'}" />
		<input type="submit" value="HTMLを更新する/ログアウト" />
	</form>
</header><!-- /#header -->

<section id="content">
EOM

	$buff .= qq|\t<section id="up">\n|;
	$buff .= &snup::leaddisp(0, 1, 1);
	$buff .= qq|\t\t<h2>Upload Info</h2>\n|;
	$buff .= <<"EOM";
		<table>
			<tr>
				<td>
					<form action="$set{'base_cgi'}" method="post">
						<input type="hidden" name="checkmode" value="allcheck" />
						<input type="hidden" name="delno" value="$in{'delno'}" />
						<input type="hidden" name="delpass" value="$in{'delpass'}" />
						<input type="submit" value="すべてチェック" />
					</form>
				</td>
				<td>
					<form action="$set{'base_cgi'}" method="post">
						<input type="hidden" name="checkmode" value="nocheck" />
						<input type="hidden" name="delno" value="$in{'delno'}" />
						<input type="hidden" name="delpass" value="$in{'delpass'}" />
						<input type="submit" value="すべて外す" />
					</form>
				</td>
			</tr>
		</table>
		<form action="$set{'base_cgi'}" method="post">
			<table style="width: 100%;">
				<tr>
					<th>DEL</th>
					<th>NAME</th>
					<th>COMMENT</th>
					<th>SIZE</th>
					<th>ADDR</th>
					<th>HOST</th>
					<th>DATE</th>
					<th>NOTE</th>
					<th>MIME</th>
					<th>ORIG</th>
					<th>THUMBNAIL</th>
				</tr>
EOM
	shift(@log);
	foreach (@log){	$buff .= &snup::makeitem($_, 'admin'); }
	$buff .= <<"EOM";
			</table>
			<input type="hidden" name="mode" value="delete" />
			<input type="hidden" name="delno" value="$in{'delno'}" />
			<input type="hidden" name="delpass" value="$in{'delpass'}" />
			<input type="submit" value="チェックしたものを削除" />
		</form>
	</section>
EOM

	if($set{'error_level'}){
		$buff .= qq|\t<section id="error">\n|;
		$buff .= &snup::leaddisp(-1, 0, 1);
		$buff .= qq|\t\t<h2>Error Info</h2>\n|;
		$buff .= <<"EOM";
		<form action="$set{'base_cgi'}" method="post">
			<input type="hidden" name="mode" value="errorclear" />
			<input type="hidden" name="delno" value="$in{'delno'}" />
			<input type="hidden" name="delpass" value="$in{'delpass'}" />
			<input type="submit" value="エラーログクリア" />
		</form>
EOM
		$buff .= <<"EOM";
		<table style="width: 100%;">
			<tr>
				<th>DATE</th>
				<th>ADDR</th>
				<th>HOST</th>
				<th>NOTE</th>
			</tr>
EOM
		if(open(IN, $set{'error_log'})){
			@log = reverse(<IN>);
			close(IN);
			foreach (@log){
				my ($date, $no, $note, $addr, $host) = split(/<>/);
				$buff .= <<"EOM";
			<tr>
				<td>$date</td>
				<td>$addr</td>
				<td>$host</td>
				<td>$note</td>
			</tr>
EOM
			}
		}
		$buff .= "\t\t</table>\n";
		$buff .= "\t</section>\n";
	}

	$buff .= qq|\t<section id="set">\n|;
	$buff .= &snup::leaddisp(-1,-1, 0);
	$buff .= qq|\t\t<h2>Setting Info</h2>\n|;
	$buff .= "\t\t<table>\n";

	$buff .= &snup::tablestr('スクリプトVer', $set{'ver'});
	$buff .= &snup::tablestr('メインログファイル', $set{'log_file'});
	if($set{'error_level'}){
		$buff .= &snup::tablestr('エラーログファイル', $set{'error_log'});
		if($set{'error_size'}){ $buff .= &snup::tablestr('エラーログ最大容量',&snup::dispsize($set{'error_size'}*1024).' '.($set{'error_size'}*1024).'Bytes'); }
		else{ $buff .= &snup::tablestr('エラーログ最大容量制限', '無'); }
	}else{ $buff .= &snup::tablestr('エラーログ記録', '無'); }
	if($set{'max_log_flag'}){ $buff .= &snup::tablestr('保持件数制限', $set{'max_log'}); }
	else{ $buff .= &snup::tablestr('保持件数制限', '無'); }
	$buff .= &snup::tablestr('最大投稿容量',&snup::dispsize($set{'max_size'}*1024).' '.($set{'max_size'}*1024).'Bytes');

	if($set{'min_flag'}){ $buff .= &snup::tablestr('最小制限容量',&snup::dispsize($set{'min_size'}*1024).' '.($set{'min_size'}*1024).'Bytes'); }
	else{ $buff .= &snup::tablestr('最小制限容量', '無'); }
	if($set{'max_all_flag'}){ $buff .= &snup::tablestr('総容量制限',&snup::dispsize($set{'max_all_size'}*1024).' '.($set{'max_all_size'}*1024).'Bytes'); }
	else{ $buff .= &snup::tablestr('総容量制限', '無'); }

	$buff .= &snup::tablestr('ファイル接頭辞', $set{'file_pre'});
	$buff .= &snup::tablestr('HTML保存ディレクトリ', $set{'html_dir'});
	$buff .= &snup::tablestr('ファイル保存ディレクトリ', $set{'src_dir'});
	if($set{'http_html_path'} && $set{'html_dir'} ne $set{'http_html_path'}){ $buff .= "<tr><td>HTTP_HTML_PATH</td><td>$set{'http_html_path'}</td></tr>\n";}
	if($set{'http_src_path'} && $set{'src_dir'} ne $set{'http_src_path'}){ $buff .= "<tr><td>HTTP_SRC_PATH</td><td>$set{'http_src_path'}</td></tr>\n";}
	$buff .= &snup::tablestr('1ページに表示するファイル数', $set{'pagelog'});
	if($set{'interval'} > 0){ $value = $set{'interval'}.'秒'; }else{ $value = '無'; }
	$buff .= &snup::tablestr('同一IP投稿間隔秒数制限', $value);
	if($set{'up_ext'}){	$set{'up_ext'} =~ s/,/ /g; $buff .= &snup::tablestr('投稿可能基本拡張子', $set{'up_ext'}); }
	if($set{'deny_ext'}){ $set{'deny_ext'} =~ s/,/ /g; $buff .= &snup::tablestr('投稿禁止拡張子', $set{'deny_ext'}); }
	if($set{'change_ext'}){	$set{'change_ext'} =~ s/,/ /g; $set{'change_ext'} =~ s/>/&gt;/g; $buff .= &snup::tablestr('拡張子変換', $set{'change_ext'});	}

	if($set{'up_all'}){	$buff .= &snup::tablestr('指定外拡張子アップロード許可', '有'); if($set{'ext_org'}){ $buff .= &snup::tablestr('指定外ファイル拡張子', 'オリジナル'); }else{ $buff .= &snup::tablestr('指定外ファイル拡張子', 'bin'); }}
	else{$buff .= &snup::tablestr('指定外拡張子アップロード許可', '無');}

	if($set{'find_crypt'}){ $value = '有'; }else{ $value = '無';}
	$buff .= &snup::tablestr('暗号化アーカイブ検出(ZIP)', $value);
	if($set{'binary_compare'}){ $value = '有'; }else{ $value = '無';}
	$buff .= &snup::tablestr('バイナリ比較', $value);
	if($set{'post_flag'}){ $value = '有'; }else{ $value = '無';}
	$buff .= &snup::tablestr('PostKey投稿制限', $value);
	if($set{'dlkey'}){ if($set{'dlkey'} == 2){$value = '必須'}else{$value = '任意';}}else{ $value = '無';}
	$buff .= &snup::tablestr('DLkey', $value);
	if($set{'dummy_html'}){ if($set{'dummy_html'} == 3){$value = 'ALL'}elsif($set{'dummy_html'} == 2){$value = 'DLKeyのみ';}else{$value = '通常ファイルのみ';}}else{ $value = '無';}
	$buff .= &snup::tablestr('個別HTMLキャッシュ', $value);
	if($set{'disp_error'}){ $value = '有'; }else{ $value = '無';}
	$buff .= &snup::tablestr('ユーザエラー表示', $value);
	if($set{'zero_clear'}){ $value = '有'; }else{ $value = '無';}
	$buff .= &snup::tablestr('削除済ファイルリスト自動消去', $value);
	if($set{'home_url'}){ $buff .= <<"EOM";
			<tr>
				<td>HOMEURL</td>
				<td>$set{'home_url'}</td>
			</tr>
EOM
	}

	$buff .= "\t\t</table>\n";
	$buff .= "\t</section>\n";

	$buff .= "</section><!-- /#content -->\n\n</body>\n</html>";

	print "Content-type: text/html\n\n";
	print $buff;
	exit;
}

sub extfind{
	my $orgname = $_[0];
	my @filename = split(/\./, $orgname);
	my $ext = $filename[$#filename];
	$ext =~ tr/[A-Z]/[a-z]/;
	foreach my $value (split(/,/, $set{'change_ext'})){ my ($src, $dst) = split(/->/, $value); if($ext eq $src){ $ext = $dst; last; }}
	foreach my $value (split(/,/, $set{'deny_ext'})){ if($ext eq $value){ &snup::error(206, $ext); }}
	foreach my $value (split(/,/, $set{'up_ext'})){ if ($ext eq $value){ return $value; } }
	if(length($ext) >= 5 || length($ext) == 0){ $ext = 'bin'; }
	unless ($ext =~ /^[A-Za-z0-9]+$/){ $ext = 'bin'; }
	if($set{'up_all'} && $set{'ext_org'}){ return $ext;}
	elsif($set{'up_all'}){ return 'bin'; }
	return 0;
}

sub conv_date{
	my @date = gmtime($_[0] + 9*60*60);
	$date[5] -= 100; $date[4]++;
	if ($date[5] < 10){ $date[5] = "0$date[5]" ; }	if ($date[4] < 10){ $date[4] = "0$date[4]" ; }
	if ($date[3] < 10){ $date[3] = "0$date[3]" ; }	if ($date[2] < 10){ $date[2] = "0$date[2]" ; }
	if ($date[1] < 10){ $date[1] = "0$date[1]" ; }	if ($date[0] < 10){ $date[0] = "0$date[0]" ; }
	my @w = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat');
	return ("$date[5]/$date[4]/$date[3]($w[$date[6]]), $date[2]:$date[1]:$date[0]");
}

sub dispsize{
	my $size = $_[0];
	if($size >= 1024*1024*1024*100){ $size = int($size/1024/1024/1024).'GB';}
	elsif($size >= 1024*1024*1024*10){ $size = sprintf("%.1fGB", $size/1024/1024/1024);}
	elsif($size > 1024*1024*1024){ $size = sprintf("%.2fGB", $size/1024/1024/1024);}
	elsif($size >= 1024*1024*100){ $size = int($size/1024/1024).'MB'; }
	elsif($size > 1024*1024){ $size =  sprintf("%.1fMB", $size/1024/1024); }
	elsif($size > 1024){ $size = int($size/1024).'KB'; }
	else{ $size = int($size).'B';}
	return $size;
}

sub makeitem{
	my ($src, $mode) = @_;
	if(!defined($mode)){ $mode = ''; }
	my ($buff, $check, $target);
	my ($no, $ext, $date, $comment, $mime, $orgname, $addr, $host, $pass, $filepre, $note, $dummy) = split(/<>/, $src);
	if(!$dummy){ $filepre = $set{'file_pre'}; }
	my $orgno = $no;
	$no = sprintf("%04d", $no);
	my $size = 0;
	my $dlpath = 0;

	if($note =~ /DLpath:(.+)\s/){
		$dlpath = $1;
		$size = &snup::dispsize(-s "$set{'src_dir'}$filepre$no.${ext}_$dlpath/$filepre$no.$ext");
	}else{
		$size = &snup::dispsize(-s "$set{'src_dir'}$filepre$no.$ext");
	}

	my $path = $set{'http_src_path'} || $set{'src_dir'};
	if($set{'link_target'}){ $target = qq| target="$set{'link_target'}"|; }
	else{ $target = ''; }
	if($mode eq 'admin'){
		if($dlpath){ $path .= "$filepre$no.${ext}_$dlpath/"; }
		if($addr eq $host){ $host = ''; }
		if($in{'checkmode'} eq 'allcheck'){ $check = 'checked="checked"'; }
		else{ $check = ''; }
		$buff = <<"EOM";
	<tr>
		<td><input type="checkbox" name="admin_delno" value="$no"$check /></td>
		<td><a href="$path$filepre$no.$ext"$target>$filepre$no.$ext</a></td>
		<td>$comment</td>
		<td>$size</td>
		<td>$addr</td>
		<td>$host</td>
		<td>$date</td>
		<td>$note</td>
		<td>$mime</td>
		<td>$orgname</td>
		<td><img src="$set{'thumb_dir'}$filepre$no.jpg" width="100" height="100" alt="$filepre$no.${ext}のサムネイル" /></td>
	</tr>
EOM
	}else{
		my($a_tag, $d_com, $d_date, $d_size, $d_mime, $d_org, $d_thumb);
		$d_com  = $set{'disp_comment'} ? "<td>$comment</td>" : '';
		$d_size = $set{'disp_size'}    ? "<td>$size</td>" : '';
		$d_date = $set{'disp_date'}    ? "<td>$date</td>" : '';
		$d_mime = $set{'disp_mime'}    ? "<td>$mime</td>" : '';
		$d_org  = $set{'disp_orgname'} ? "<td>$orgname</td>" : '';
		if(-e "$set{'src_dir'}$filepre$no.$ext.html"){
			$a_tag = qq|href="$path$filepre$no.$ext.html"$target|;
		}elsif($dlpath){
			$a_tag = qq|href="$set{'base_cgi'}?mode=dl&amp;file=$orgno"|;
		}else{
			$a_tag = qq|href="$path$filepre$no.$ext"$target|;
		}
		$d_thumb = $set{'disp_thumb'} ? qq|<td><a $a_tag><img src="$set{'thumb_dir'}$filepre$no.jpg" width="100" height="100" alt="$filepre$no.${ext}のサムネイル" /></a></td>| : '';
		$buff = <<"EOM";
		<tr>
			<td><a href="javascript:delnoin($orgno)">$set{'char_delname'}</a></td>
			<td><a $a_tag>$filepre$no.$ext</a></td>
			$d_com
			$d_size
			$d_date
			$d_mime
			$d_org
			$d_thumb
		</tr>
EOM
	}
	return $buff;
}

sub makedummyhtml{
	my ($filename, $com, $file, $orgdlpath, $date, $mime, $orgname, $no) = @_;
	my $buff;

	if(!$no){
		$buff = "<html><head><title>$filename</title></head><body>";
		$buff .= qq|Download <a href="./$filename">$filename</a>|;
		$buff .= '</body></html>';
	}else{
		$buff = &snup::cryptfiledl($com, $file, $orgdlpath, $date, $mime, $orgname, $no);
	}

	open(OUT, ">$set{'src_dir'}$filename.html") || &snup::error(307, "$set{'src_dir'}$filename.html");
	print OUT $buff;
	close(OUT);
	chmod($set{'per_upfile'}, "$set{'src_dir'}$filename.html");
	return 1;
}

sub logwrite{
	my @log = @_;
	open(OUT, "+>$set{'log_file'}") || &snup::error(304);
	eval{ flock(OUT, 2);};
	eval{ truncate(OUT, 0);};
	seek(OUT, 0, 0);
	print OUT @log;
	eval{ flock(OUT, 8);};
	close(OUT);
	chmod($set{'per_upfile'}, $set{'log_file'});
	return 1;
}

sub binarycmp{
	my ($src, $dst) = @_;
	return 0 if (-s $src != -s $dst);
	open(SRC, $src) || return 0; open(DST, $dst) || return 0;
	my ($buff, $buff2);
	binmode(SRC); binmode(DST); seek(SRC, 0, 0); seek(DST, 0, 0);
	while(read(SRC, $buff, 8192)){ read(DST, $buff2, 8192); if($buff ne $buff2){ close(SRC); close(DST); return 0; } }
	close(SRC); close(DST);
	return 1;
}

sub init{
	my $buff;
	if(open(OUT, ">$set{'log_file'}")){
		print OUT "0<>0<>0<>1\n";
		close(OUT);
		chmod($set{'per_logfile'}, $set{'log_file'});
	}else{
		$buff = "<tr><td>メインログの作成に失敗しました</td></tr>";
	}

	unless (-d "$set{'src_dir'}"){
		if(mkdir("$set{'src_dir'}", $set{'per_dir'})){
			chmod($set{'per_dir'}, "$set{'src_dir'}");
			open(OUT, ">$set{'src_dir'}index.html");
			close(OUT);
			chmod($set{'per_upfile'}, "$set{'src_dir'}index.html");
		}else{
			$buff .= "<tr><td>Source保存ディレクトリの作成に失敗しました</td></tr>";
		}
	}

	unless (-d "$set{'html_dir'}"){
		if(mkdir("$set{'html_dir'}", $set{'per_dir'})){
			chmod($set{'per_dir'}, "$set{'html_dir'}");
		}else{
			$buff .= "<tr><td>HTML保存ディレクトリの作成に失敗しました</td></tr>";
		}
	}

	if($buff){
		$buff .= "<tr><td>ディレクトリに書き込み権限があるか確認してください</td></tr>";
		&snup::error_disp($buff, 'init');
	}
}

sub check_postkey{
	my $inputkey = $_[0];
	my @key = split(/,/, $set{'post_key'});
	foreach my $key (@key){ if($inputkey eq $key){ return 1; } }
	return 0;
}

sub leaddisp{
	my @src = @_;
	my ($str, $count);
	$str = qq|\t\t<nav class="leaddisp">\n|;
	$str .= "\t\t\t<ul>\n";
	foreach my $value (@src){
		my ($mark, $name, $link); $count++;
		if($count == 1){ $name = 'Upload Info'; $link = 'up'; }
		elsif($count == 2){ $name = 'Error Info'; $link = 'error'; next if(!$set{'error_level'}); }
		elsif($count == 3){ $name = 'Setting Info'; $link = 'set'; }
		if($value){ if($value > 0){ $mark = '▼'; }else{ $mark = '▲'; } $str .= qq|\t\t\t\t<li><a href="#$link">${mark}${name}</a></li>\n|; }
		else{ $str .= qq|\t\t\t\t<li>[$name]</li>\n|; }
	}
	$str .= "\t\t\t</ul>\n";
	$str .= "\t\t</nav>\n";
	return $str;
}

sub errorclear{
	open(OUT, ">$set{'error_log'}") || return 0;
	eval{ flock(OUT, 2);}; eval{ truncate(OUT, 0);}; seek(OUT, 0, 0); eval{ flock(OUT, 8);}; close(OUT);
	chmod($set{'per_upfile'}, $set{'log_file'});
	return 1;
}

sub tablestr{
	my ($value1, $value2) = @_;
	return <<"EOM";
			<tr>
				<td>$value1</td>
				<td>$value2</td>
			</tr>
EOM
}

sub globfile{
	my ($src_dir, $filename) = @_;
	opendir(DIR, $src_dir) || return 0; my @dir = readdir(DIR); closedir(DIR);
	my @new = (); foreach my $value (@dir){ push(@new, "$src_dir$value") if($value =~ /$filename/ && !(-d "$src_dir$value")); }
	return @new;
}

sub globdir{
	my ($src_dir, $dir) = @_;
	opendir(DIR, $src_dir) || return 0; my @dir = readdir(DIR); closedir(DIR);
	my @new = (); foreach my $value (@dir){ if($value eq '.' || $value eq '..' ){ next; } push(@new, "$src_dir$value") if($value =~ /$dir/ && (-d "$src_dir$value")); }
	return @new;
}

sub error_disp{
	my ($message, $mode) = @_;
	$mode = '' if(!defined($mode));
	my $url = ($mode eq 'init') ? qq|<a href="$set{'base_cgi'}">[リロード]</a>| : qq|<a href="$set{'http_html_path'}$set{'base_html'}">[戻る]</a>|;
	my $buff = <<"EOM";
$set{'html_head'}</head>
<body>
<div align="center">
<table>
$message
<tr><td></td></tr>
<tr><td><div align="center">$url</div></td></tr>
</table>
<br><br>
<table>
<tr>
<td>DATE</td><td>$in{'date'}</td></tr>
<tr><td>ADDR</td><td>$in{'addr'}</td></tr>
<tr><td>HOST</td><td>$in{'host'}</td></tr>
</table>
</div>
</body></html>
EOM
	print "Content-type: text/html\n\n";
	print $buff;
	exit;
}

sub error{
	my ($no, $note) = @_;
	if(!defined($note)){ $note = ''; }
	if (length($note) > 64){ $note = substr($note, 0, 64).'...'; }
	$note =~ s/&/&amp;/g;
	$note =~ s/\"/&quot;/g;
	$note =~ s/</&lt;/g;
	$note =~ s/>/&gt;/g;
	$note =~ s/\r//g;
	$note =~ s/\n//g;
	$note =~ s/\t//g;
	$note =~ s/\0//g;
	my ($message, $dispmsg, $flag);

	if($no == 98){ $message = ""; }
	elsif($no == 99){ $message = "UpFileなし"; }
	elsif($no == 101){ $message = "投稿禁止HOST"; }
	elsif($no == 106){ $flag = 1; $message = "POSTサイズ超過"; $note = &snup::dispsize($note); $dispmsg= '<tr><td>ファイルをアップロードできませんでした</td></tr><tr><td>アップロードファイル('.$note.')は 最大容量設定('.&snup::dispsize($set{'max_size'}*1024).')を越えています</td></tr>';}
	elsif($no == 107){ $flag = 1; $message = "POSTサイズ過小"; $note = &snup::dispsize($note); $dispmsg= '<tr><td>ファイルをアップロードできませんでした</td></tr><tr><td>アップロードファイル('.$note.')は 最小容量設定('.&snup::dispsize($set{'min_size'}*1024).')未満です</td></tr>';}
#	elsif($no == 108){ $flag = 1; $message = "POSTデータ不完全"; $dispmsg = '<tr><td>ファイルをアップロードできませんでした</td></tr><tr><td>POSTデータが不完全です</td></tr>';}
	elsif($no == 109){ $flag = 1; $message = "POSTKey不一致"; $dispmsg = '<tr><td>ファイルをアップロードできませんでした</td></tr><tr><td>POSTKeyが一致しません</td></tr>';}
	elsif($no == 202){ $flag = 1; $message = "拡張子合わず"; $dispmsg = '<tr><td>ファイルをアップロードできませんでした</td></tr><tr><td>投稿できる拡張子は'.$set{'up_ext'}.'です</td></tr>';}
	elsif($no == 203){ $flag = 1; $message = "投稿早すぎ"; $dispmsg = '<tr><td>ファイルをアップロードできませんでした</td></tr><tr><td>同一IPアドレスから'.$set{'interval'}.'秒以内に再投稿できません</td></tr>';}
	elsif($no == 204){ $flag = 1; $message = "一時ファイル書き込めず"; $dispmsg = '<tr><td>ファイルをアップロードできませんでした</td></tr><tr><td>一時ファイルの作成に失敗しました</td></tr>';}
	elsif($no == 205){ $flag = 1; $message = "同一ファイル存在"; $note =~ /([^\/]+)$/; my $filename = $1; $dispmsg = '<tr><td>ファイルをアップロードできませんでした</td></tr><tr><td>同一ファイルが '.$filename.' に存在します</td></tr>';}
	elsif($no == 206){ $flag = 1; $message = "禁止拡張子"; $dispmsg = '<tr><td>ファイルをアップロードできませんでした</td></tr><tr><td>拡張子 '.$note.' はアップロードできません</td></tr>';}
	elsif($no == 303){ $flag = 1; $message = "ログファイルに読み込めず"; $dispmsg = '<tr><td>メインログの読み込みに失敗しました</td></tr>';}
	elsif($no == 304){ $flag = 1; $message = "ログファイルに書き込めず"; $dispmsg = '<tr><td>メインログの書き込みに失敗しました</td></tr>';}
	elsif($no == 306){ $message = "ファイルリストHTML書き込めず";}
	elsif($no == 307){ $message = "ファイルHTMLファイル書き込めず";}
	elsif($no == 401){ $flag = 1; $message = "削除No.検出できず"; $dispmsg = '<tr><td>ファイルを削除できませんでした</td></tr><tr><td>'.$note.' から削除No.を検出できませんでした</td></tr><tr><td>'.$set{'file_pre'}.'0774.zipの場合 No.には 774 を入力します</td></tr>';}
	elsif($no == 402){ $flag = 1; $note = sprintf("%04d",int($note)); $message = "削除No.存在せず"; $dispmsg = '<tr><td>ファイルを削除できませんでした</td></tr><tr><td>'.$set{'file_pre'}.$note.'.*** はメインログに存在しません</td></tr>';}
	elsif($no == 403){ $flag = 1; $message = "削除アクセス拒否"; $dispmsg = '<tr><td>ファイルを削除できませんでした</td></tr><tr><td>ファイル削除条件は満たしていますが '.$note.' のファイルの削除が拒否されました</td></tr><tr><td>アクセスが過剰な場合等は時間を置いて再操作すると削除できることがあります</td></tr>';}
	elsif($no == 404){ $flag = 1; $message = "削除Key不一致"; $dispmsg = '<tr><td>ファイルを削除できませんでした</td></tr><tr><td>'.$note.' 削除Keyが一致しませんでした</td></tr>';}

	elsif($no == 51){ $flag = 1; $message = "[DLMode] No.見つからず";  $dispmsg = '<tr><td>[DLMode] ファイルが見つかりませんでした</td></tr><tr><td>'.$note.' からファイルNo.を検出できませんでした</td></tr>'; }
	elsif($no == 52){ $flag = 1; $message = "[DLMode] File見つからず";  $dispmsg = '<tr><td>[DLMode] ファイルが見つかりませんでした</td></tr><tr><td>'.$set{'file_pre'}.$note.'.*** はメインログに存在しません</td></tr>'; }
	elsif($no == 53){ $flag = 1; $message = "[DLMode] DLkey未設定";  $dispmsg = '<tr><td>[DLMode] orgDLkeyError</td></tr><tr><td>'.$note.' DLKeyが未設定です</td></tr>'; }
	elsif($no == 54){ $flag = 1; $message = "[DLMode] DLkey不一致";  $dispmsg = '<tr><td>[DLMode] orgDLkeyError</td></tr><tr><td>'.$note.' DLKeyが一致しませんでした</td></tr>'; }
	elsif($no == 55){ $flag = 1; $message = "[DLMode] File Oepn Error";  $dispmsg = '<tr><td>[DLMode] Open Error</td></tr><tr><td>'.$note.' ファイルの読み込みに失敗しました</td></tr>'; }
	elsif($no == 56){ $flag = 1; $message = "[DLMode] File Not Found";  $dispmsg = '<tr><td>[DLMode] Not Found</td></tr><tr><td>'.$note.' ファイルが存在しません</td></tr>'; }

	elsif($no == 61){ $flag = 1; $message = "DLkey未設定";  $dispmsg = '<tr><td>DLKeyが未設定です</td></tr>'; }

	if($note){$message .= ' ';}
	eval{ if(defined($in{'upfile'}) && -t $in{'upfile'}){ close($in{'upfile'}); }};
	unlink($in{'tmpfile2'}) if(defined($in{'tmpfile2'}));
	if($set{'error_level'} && $no > 100){
		unless(-e $set{'error_log'}){
			open(OUT, ">$set{'error_log'}");
			close(OUT);
			chmod($set{'per_logfile'}, $set{'error_log'});
		}
		if($set{'error_size'} && ((-s $set{'error_log'}) > $set{'error_size'} * 1024)){
			my $err_bkup = "$set{'error_log'}.bak.cgi";
			unlink($err_bkup);
			rename($set{'error_log'}, $err_bkup);
			open(OUT, ">$set{'error_log'}");
			close(OUT);
			chmod($set{'per_logfile'}, $set{'error_log'});
		}
		open(OUT, ">>$set{'error_log'}");
		print OUT "$in{'date'}<>$no<>$message$note<>$in{'addr'}<>$in{'host'}<>1\n";
		close(OUT);
	}
	&snup::error_disp($dispmsg) if($flag && $set{'disp_error'});
	&snup::quit();
}

sub dlfile{
	my $msg;
	my ($orgdlkey, $orgdlpath);
	my ($dlext, $dlfilepre);
	my ($dl_date, $dl_comment, $dl_size, $dl_mime,, $dl_orgname);
	my $dlno = 0;
	my $findflag;

	open(IN, $set{'log_file'}) || &snup::error(303);
	my @log = <IN>;
	close(IN);
	shift(@log);

	if($in{'file'} =~ /(\d+)/){ $dlno = $1; }
	if($dlno == 0){ &snup::error(51, $in{'file'}); }

	foreach my $value (@log){
		my ($no, $ext, $date, $comment, $mime, $orgname, $addr, $host, $pass, $filepre, $note, $dummy) = split(/<>/, $value);
			my @note = split(/,/, $note);
			if(int($dlno) == $no){
				$dl_comment = $comment;
				$dl_mime = $mime;
				$dl_date = $date;
				$dl_orgname = $orgname;
				$dlext = $ext;
				$dlfilepre = $filepre;
				foreach my $tmpnote (@note){
					if($tmpnote =~ /\!--\sDLKey:(.+)\s--.*\!--\sDLpath:(.+)\s--/){
						$orgdlkey = $1;
						$orgdlpath = $2;
						last;
					}
				}
				$findflag = 1;
				last;
			}
	}

	my $dlfile = $dlfilepre.sprintf("%04d",int($dlno)).'.'.$dlext;
	if(!(-e "$set{'src_dir'}${dlfile}_$orgdlpath/$dlfile")){ &snup::error(56, "$dlfile----$set{'src_dir'}${dlfile}_$orgdlpath/$dlfile"); }

	if($in{'dlkey'}){
		my $dlsalt = substr($orgdlkey, 0, 2);
		my $dlkey = crypt($in{'dlkey'}, $dlsalt);

		if($findflag == 0){ &snup::error(52, $dlfile); }
		elsif(!$orgdlkey){ &snup::error(53, $dlfile); }
		elsif($orgdlkey ne $dlkey && $set{'admin_pass'} ne $in{'dlkey'}){ &snup::error(54, $dlfile); }
		#print "Location: $set{'http_src_path'}${dlfile}_$orgdlpath/$dlfile\n\n";
		my $buff = <<"EOM";
$set{'html_head'}	<script type="text/javascript"><!--
		setTimeout(function(){ location.href = "$set{'http_src_path'}${dlfile}_$orgdlpath/$dlfile" }, 1000);
	--></script>
</head>
<body>

<div id="wrapper">

<section id="content">
	<p>飛ばない場合は <a href="$set{'http_src_path'}${dlfile}_$orgdlpath/$dlfile">こちら</a> から</p>
</section><!-- /#content -->

</div>

</body>
</html>
EOM
		print "Content-type: text/html\n\n";
		print $buff;
	}else{
		my $buff = &snup::cryptfiledl($dl_comment, $dlfile, $orgdlpath, $dl_date, $dl_mime, $dl_orgname, $dlno);
		print "Content-type: text/html\n\n";
		print $buff;
	}
	exit;
}

sub cryptfiledl{
		my($com, $file, $orgdlpath, $date, $mime, $orgname, $no) = @_;
		my($d_com, $d_date, $d_size, $d_mime, $d_org);

		$d_com  = $set{'disp_comment'} ? "<tr><td>COMMENT</td><td>$com</td></tr>" : '';
		$d_size = $set{'disp_size'}    ? "<tr><td>SIZE</td><td>".&snup::dispsize(-s "$set{'src_dir'}${file}_$orgdlpath/$file")." (".(-s "$set{'src_dir'}${file}_$orgdlpath/$file")."bytes)"."</td></tr>" : '';
		$d_date = $set{'disp_date'}    ? "<tr><td>DATE</td><td>$date</td></tr>" : '';
		$d_mime = $set{'disp_mime'}    ? "<tr><td>ORGMIME</td><td>$mime</td></tr>" : '';
		$d_org  = $set{'disp_orgname'} ? "<tr><td>ORGNAME</td><td>$orgname</td></tr>" : '';

		my $buff = <<"EOM";
$set{'html_head'}</head>
<body>

<div id="wrapper">

<section id="content">
	<p>$file にはDLKeyが設定されています</p>
	<table>
		$d_com
		$d_date
		$d_size
		$d_mime
		$d_org
	</table>
	<form method="post" action="$set{'base_cgi'}" name="DL">
		<p>
			DLKey:<input type="text" size="8" name="dlkey" />
			<input type="hidden" name="file" value="$no" />
			<input type="hidden" name="jcode" value="漢字" />
			<input type="hidden" name="mode" value="dl" />
			<input type="submit" value="DownLoad" />
		</p>
	</form>
</section><!-- /#content -->

</div>

</body>
</html>
EOM

	return $buff;
}

sub send_notification{
	unless($set{'mail_notify'}){ return; }
	my $subject = encode('MIME-Header-ISO_2022_JP', decode('utf8', $_[0]));
	my $body = encode('iso-2022-jp', decode('utf8', $_[1]));
	my $header = <<"EOM";
From: Sn Uploader <$set{'notify_from'}>
To: $set{'notify_to'}
Subject: [$set{'html_title'}] $subject
Mime-Version: 1.0
X-Mailer: Sn Uploader $set{'ver'}
Content-Type: text/plain; charset="iso-2022-jp"
Content-Transfer-Encoding: 7bit

EOM

if($set{'smtp_auth'}){
	my $pop = Net::POP3->new($set{'pop_server'}, Port => $set{'pop_port'}) || return;
	$pop->login($set{'pop_userid'}, $set{'pop_passwd'});
}
my $smtp = Net::SMTP->new($set{'mail_server'}, Port => $set{'mail_port'}) || return;
$smtp->mail($set{'notify_from'});
$smtp->to($set{'notify_to'});
$smtp->data();
$smtp->datasend($header);
$smtp->datasend($body);
$smtp->dataend();
$smtp->quit;
}

}

1;
