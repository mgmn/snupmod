#!/usr/bin/perl
use CGI;
use vars qw(%set %in);
use strict;
$set{'log_file'} = './log.cgi';		#ログファイル名
$set{'max_log'} = 30;		#保持件数
$set{'max_size'} = 1*1024;		#最大投稿容量(KB)
$set{'min_flag'} = 0;		#最小容量制限を使用する=1
$set{'min_size'} = 100;		#最小投稿容量(KB)
$set{'max_all_flag'} = 0;		#総容量制限を使用する=1
$set{'max_all_size'} = 20*1024;		#総制限容量(KB)
$set{'file_pre'} = 'up';		#ファイル接頭辞
$set{'pagelog'} = 10;		#1ページに表示するファイル数
$set{'base_html'} = 'upload.html';		#1ページ目のファイル名
$set{'interval'} = 0;		#同一IP投稿間隔秒数
$set{'deny_host'} = '';		#投稿禁止IP/HOST ,で区切る ex.(bbtec.net,219.119.66,ac.jp)
$set{'admin_name'} = 'admin';		#管理者ログインID
$set{'admin_pass'} = '1234';		#管理者パスワード

# 以下5項目を再設定する際にはPATH，ディレクトリは / で終わること
# $set{'html_dir'},$set{'base_cgi'}を ./ 以外に設定する場合,
# またはDLkeyを使用し なおかつHTMLキャッシュ($set{'dummy_html'} = 2 or 3)を使用する場合は
# $set{'base_cgi'} , $set{'http_html_path'} , $set{'http_src_path'} をフルパス(http://～～ or /～～)で記述する
$set{'html_dir'} = './';		# 内部HTML保存ディレクトリ
$set{'src_dir'} = './src/';		# 内部ファイル保存ディレクトリ
$set{'base_cgi'} = './upload.cgi'; # このスクリプト名 http://～の指定可能
$set{'http_html_path'} = './';		# html参照 httpPATH http://～の指定可能
$set{'http_src_path'} = './src/';		# file参照 httpPATH http://～の指定可能

$set{'dlkey'} = 0;		# DLKeyを使用する=1,DLkey必須=2
$set{'up_ext'} = 'txt,lzh,zip,rar,gca,mpg,mp3,avi,swf,bmp,jpg,gif,png'; #アップロードできる基本拡張子 半角英数小文字 ,で区切る
$set{'up_all'} = 0;		#登録以外のものもUPさせられるようにする=1
$set{'ext_org'} = 0;	#$set{'up_all'}が1の時オリジナルの拡張子にする=1
$set{'deny_ext'} = 'php,php3,phtml,rb,sh,bat,dll'; 	#投稿禁止の拡張子 半角英数小文字 ,で区切る
$set{'change_ext'} = 'cgi->txt,pl->txt,log->txt,jpeg->jpg,mpeg->mpg';		#拡張子変換 前->後 半角英数小文字 ,で区切る

$set{'home_url'} = '';		#[HOME]のリンク先 相対パス又は http://から始まる絶対パス
$set{'html_all'} = 1;		#[ALL]を出す=1
$set{'dummy_html'} = 0;		#ファイル個別HTMLを作成する 通常ファイルのみ=1,DLKey設定ファイルのみ=2,すべて=3
$set{'find_crypt'} = 1;		#暗号化ZIPを検出する=1
$set{'binary_compare'} = 0;		#既存ファイルとバイナリ比較する=1
$set{'post_flag'} = 0;		#PostKeyを使用する=1
$set{'post_key'} = 'postkey';		#PostKey ,で区切ると複数指定 ex.(postkey1,postkey2)
$set{'disp_error'} = 1;		#ユーザーにエラーを表示する=1
$set{'error_level'} = 1;		#エラーログを記録する=1
$set{'error_log'} = './error.cgi';		#エラーログファイル名
$set{'error_size'} = 1024;	# エラーログ最大容量(KB) 制限なし=0
$set{'zero_clear'} = 1;		#ファイルが見つからない場合ログから削除する=1

$set{'disp_comment'} = 1; 	#コメントを表示する=1
$set{'disp_date'} = 1;		#日付を表示する=1
$set{'disp_size'} = 1;		#サイズを表示する=1
$set{'disp_mime'} = 1;		#MIMETYPEを表示する=1
$set{'disp_orgname'} = 1;	#オリジナルファイル名を表示する=1

$set{'per_upfile'} = 0666;		#アップロードファイルのパーミッション suexec=0604,other=0666
$set{'per_dir'} = 0777;		#ソースアップディレクトリのパーミッション suexec=0701,other=0777
$set{'per_logfile'} = 0666;		#ログファイルのパーミッション　suexec=0600,other=0666
$set{'link_target'} = '';		#target属性

#------
$set{'ver'} = '2005/10/10e CGI.pm';
$set{'char_delname'} = 'D';

$in{'time'} = time(); $in{'date'} = conv_date($in{'time'});
$in{'addr'} = $ENV{'REMOTE_ADDR'};
$in{'host'} = gethostbyaddr(pack('C4',split(/\./, $in{'addr'})), 2) || $ENV{'REMOTE_HOST'} || '(none)';
if($in{'addr'} eq $in{'host'}){ $in{'host'} = '(none)'; }

$set{'html_head'} =<<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<HEAD>
<META name="robots" content="noindex,nofollow">
<META name="ROBOTS" content="NOINDEX,NOFOLLOW">
<META http-equiv="Content-type" content="text/html; charset=Shift_JIS">
<META http-equiv="Pragma" content="no-cache">
<META http-equiv="Cache-Control" content="no-cache">
<META http-equiv="Expires" content="0">
<TITLE>Uploader</TITLE>
EOM

$set{'html_css'} =<<"EOM";
<META http-equiv="Content-Style-Type" content="text/css">
<STYLE type="text/css"><!--
input,td{ font-size: 10pt;font-family:Chicago,Verdana,Arial,sans-serif,"ＭＳ Ｐゴシック"; }
a:hover { background-color:#EECCCC; }
input,textarea{	border-top : 1px solid ; border-bottom : 1px solid ; border-left : 1px solid ; border-right : 1px solid ;font-size:10pt;background-color:#FFFFFF; }
-->
</STYLE>
EOM

unless(-e $set{'log_file'}){ &init; }
unless(-e $set{'base_html'}){ &makehtml; }

{ #デコード
	if ($ENV{'REQUEST_METHOD'} eq "POST" && $ENV{'CONTENT_TYPE'} =~ /multipart\/form-data/i){
		if ($ENV{'CONTENT_LENGTH'} > ($set{'max_size'} * 1024 + 1024)){ if($ENV{'SERVER_SOFTWARE'} =~ /IIS/){ while(read(STDIN,my $buff,8192)){} } &error(106,$ENV{'CONTENT_LENGTH'});}
 	}else{
 		if ($ENV{'CONTENT_LENGTH'} > 1024*100){ error(98); }
 	}
	my %ck; foreach(split(/;/,$ENV{'HTTP_COOKIE'})){ my($key,$val) = split(/=/); $key =~ s/\s//g; $ck{$key} = $val;}
	my @ck = split(/<>/,$ck{'SN_USER'});
	if(length($ck[0]) < 5){ 
		my @salt = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/'); srand;
		my $salt = $salt[int(rand(@salt))] . $salt[int(rand(@salt))];
		$in{'user'} = crypt($in{'addr'}.$in{'time'}, $salt);
	}else{ $in{'user'} = $ck[0]; }
	
	my $q = new CGI;
	$in{'upfile'} = $q->param('upfile');
	$in{'tmpfile'} = $q->tmpFileName($in{'upfile'});
	$in{'type'} = $q->uploadInfo($in{'upfile'})->{'Content-Type'} if ($in{'upfile'});
	$in{'pass'} = $q->param('pass');	$in{'mode'} = $q->param('mode');	
	$in{'delno'} = $q->param('delno');	$in{'comment'} = $q->param('comment');
	$in{'jcode'} = $q->param('jcode');	$in{'delpass'} = $q->param('delpass');
	$in{'orgname'} = $in{'upfile'};	$in{'postkey'} = $q->param('postkey');
	$in{'org_pass'} = $in{'pass'};
	$in{'checkmode'} = $q->param('checkmode');
	$in{'file'} = $q->param('file');	$in{'dlkey'} = $q->param('dlkey');
	$in{'admin_delno'} = join(',',$q->param('admin_delno'));
	my @denyhost = split(/,/,$set{'deny_host'});
	foreach my $value (@denyhost){
		if ($in{'addr'} =~ /$value/ || $in{'host'} =~ /$value/){ &error(101);}
	}

	my @form = ($in{'comment'},$in{'orgname'},$in{'type'},$in{'dlkey'});
	foreach my $value (@form) {
		if (length($value) > 128) { $value = substr($value,0,128).'...'; }
#		$value =~ s/&/&amp;/g;
		$value =~ s/"/&quot;/g;
		$value =~ s/</&lt;/g;
		$value =~ s/>/&gt;/g;
		$value =~ s/\r//g;
		$value =~ s/\n//g;
		$value =~ s/\t//g;
		$value =~ s/\0//g;
	}
	($in{'comment'},$in{'orgname'},$in{'type'},$in{'dlkey'}) = @form;
	 $in{'tmpfile2'} = &filewrite() if ($in{'upfile'});
}

if($in{'delno'} eq $set{'admin_name'} && $in{'delpass'} eq $set{'admin_pass'}){ &admin_mode(); }
if(!$in{'delno'} && $in{'delpass'} eq $set{'admin_pass'}){ &makehtml(); &quit(); }
if($in{'mode'} eq 'dl'){ &dlfile;} #DL
if($in{'mode'} eq 'delete'){ &delete(); &quit(); }

{#メイン処理
	if(!$in{'upfile'}){ &error(99); }
	if($set{'post_flag'} && !check_postkey($in{'postkey'})){ error(109); }
	if($set{'dlkey'} == 2 && !$in{'dlkey'}){ unlink("$in{'tmpfile2'}"); &error(61); }
	open(IN,$set{'log_file'})||&error(303);
	my @log = <IN>;
	close(IN);
	my ($no,$lastip,$lasttime) = split(/<>/,$log[0]);

	if($set{'interval'} && $set{'interval'} && $in{'time'} <= ($lasttime + $set{'interval'}) && $in{'addr'} eq $lastip){ &error(203);}
	$in{'ext'} = extfind($in{'orgname'}); if(!$in{'ext'} && $in{'upfile'}){ &error(202); }

	my $orgname;
	if(split(/\//,$in{'orgname'}) > split(/\\/,$in{'orgname'})){	my @name = split(/\//,$in{'orgname'}); $orgname = $name[$#name]; }
	else{ my @name = split(/\\/,$in{'orgname'}); $orgname = $name[$#name];}
	
	my @salt = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');
	srand;
	my $salt = $salt[int(rand(@salt))] . $salt[int(rand(@salt))];
	$in{'pass'} = crypt($in{'pass'}, $salt);

	if($set{'binary_compare'}){
		my @files = globfile("$set{'src_dir'}",".*");
		my @dir = globdir("$set{'src_dir'}",".*");
		foreach my $dir (@dir){	push(@files,globfile($dir."/",".*")); }
		foreach my $value (@files){
			next if($value =~ /\.temporary$/);
			if(binarycmp($in{'tmpfile2'},$value)){ unlink($in{'tmpfile2'}); &error(205,$value);}
		}
	}

	if($set{'find_crypt'}){
		open(FILE,$in{'tmpfile'}); binmode(FILE); seek(FILE,0,0); read(FILE,my $buff,4); my $crypt_flag = 0;
		if($buff =~ /^\x50\x4b\x03\x04$/){ seek(FILE,6,0); read(FILE,my $buff,1); $crypt_flag = 1 if(($buff & "\x01") eq "\x01"); }
		close(FILE);
		$in{'comment'} = '<font color="#FF0000">*</font>'.$in{'comment'} if($crypt_flag);
	}

	open(IN,$set{'log_file'})||&error(303);
	@log = <IN>;
	close(IN);
	($no,$lastip,$lasttime) = split(/<>/,$log[0]);
	shift(@log);
	$no++;
	my $tmpno = sprintf("%04d",$no);

	my $dlsalt;
	my $filedir;
	my $allsize = (-s $in{'tmpfile2'});

	if($set{'dlkey'} && $in{'dlkey'}){
		my @salt = ('a'..'z', 'A'..'Z', '0'..'9'); srand;
		for (my $c = 1; $c <= 20; ++$c) { $dlsalt .= $salt[int(rand(@salt))]; }
	 	$filedir = "$set{'src_dir'}$set{'file_pre'}${tmpno}.$in{'ext'}_$dlsalt/";
		mkdir($filedir,$set{'per_dir'});
		rename("$in{'tmpfile2'}","$filedir$set{'file_pre'}$tmpno.$in{'ext'}");
		open(OUT,">${filedir}index.html");
		close(OUT);
		chmod($set{'per_upfile'},"${filedir}index.html");
		$in{'comment'} = '<font color="#FF0000">[DLKey] </font>'.$in{'comment'};
	}else{
		undef $in{'dlkey'};
		rename("$in{'tmpfile2'}","$set{'src_dir'}$set{'file_pre'}$tmpno.$in{'ext'}");
	}

	if (length($orgname) > 128) { $orgname = substr($orgname,0,128).'...'; }

	my @note;
	if($set{'post_flag'} && $set{'post_key'}){
		push(@note,'PostKey:'.$in{'postkey'});
	}
	if($ENV{'SERVER_SOFTWARE'} =~ /Apache|IIS/){
		my $disptime;
		my $time = time() - $in{'time'};
		my @str = ('Upload:','秒');
		my $disptime = $time.$str[1];
		push(@note,$str[0].$disptime);
	}
	if($in{'dlkey'}){
		my @salt = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/'); srand;
		my $salt = $salt[int(rand(@salt))] . $salt[int(rand(@salt))];
		my $crypt_dlkey  = crypt($in{'dlkey'}, $salt);
		push(@note,"DLKey<!-- DLKey:".$crypt_dlkey." --><!-- DLpath:".$dlsalt." -->");
	}
	my $note = join(',',@note);
	my $usersalt = substr($in{'user'},0,2);
	my $userid = crypt($in{'user'},$usersalt);
	$in{'time'} = time();
#	$in{'date'} = conv_date(time());
	my @new;
	$new[0] = "$no<>$in{'addr'}<>$in{'time'}<>1\n";
	my $addlog = "$no<>$in{'ext'}<>$in{'date'}<>$in{'comment'}<>$in{'type'}<>$orgname<>$in{'addr'}<>$in{'host'}<>$in{'pass'},$userid<>$set{'file_pre'}<>$note<>1\n";
	$new[1] = $addlog;

#	open(OUT,">>./alllog.cgi"); print OUT $addlog; close(OUT);

	my $i = 2;

	foreach my $value (@log){
		my ($no,$ext,$date,$comment,$mime,$orgname,$addr,$host,$pass,$filepre,$note,$dummy) = split(/<>/,$value);
		if(!$dummy){ $filepre = $set{'file_pre'};}
		$no = sprintf("%04d",$no);

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
		
		if($i <= $set{'max_log'} && !($set{'max_all_flag'} && $set{'max_all_size'}*1024 < $allsize)){ 
			if((-e $filename)||!$set{'zero_clear'}){ push(@new,$value); $i++; }
		}else{
			if(unlink($filename)){
				unlink("$set{'src_dir'}$filepre$no.$ext.html"); if($filedir){ foreach(globfile($filedir,".*")){ unlink; } } rmdir($filedir);
			}elsif(unlink($filename)){
				unlink("$set{'src_dir'}$filepre$no.$ext.html"); if($filedir){ foreach(globfile($filedir,".*")){ unlink; } } rmdir($filedir);
			}elsif(-e $filename){
				push(@new,$value);
			}else{
				unlink("$set{'src_dir'}$filepre$no.$ext.html"); if($filedir){ foreach(globfile($filedir,".*")){ unlink; } } rmdir($filedir);
			}
		}
	}
	logwrite(@new);
	if($in{'dlkey'} && ( $set{'dummy_html'} == 2 || $set{'dummy_html'} == 3)){
		&makedummyhtml("$set{'file_pre'}$tmpno.$in{'ext'}",$in{'comment'},"$set{'file_pre'}$tmpno.$in{'ext'}",$dlsalt,$in{'date'},$in{'type'},$orgname,$no);
	}elsif(!$in{'dlkey'} && ($set{'dummy_html'} == 1 || $set{'dummy_html'} == 3)){
		&makedummyhtml("$set{'file_pre'}$tmpno.$in{'ext'}");
	}
	&makehtml(); &quit();
}

sub makehtml{

	my ($buff,$init,$postval,$dlkey);
	my $page = 0; my $i = 1;
	
	open(IN,$set{'log_file'})||&error(303);
	my $log = my @log = <IN>;
	close(IN);
	
	if($log == 1){ $log++; $init++;}
	my $lastpage = int(($log - 2)/$set{'pagelog'}) + 1;
	$postval = ' obj.postkey.value =  unescape(p[1]);' if($set{'post_flag'});
	my $header =<<"EOM";
$set{'html_head'}<META http-equiv="Content-Script-Type" content="text/javascript">
<script type="text/javascript">
<!--
function getCookie(obj,cookiename){
	var i,str; c = new Array(); p = new Array("",""); str = document.cookie;c = str.split(";");
	for (i = 0; i < c.length; i++) { if (c[i].indexOf(cookiename+"=") >= 0) { p = (c[i].substr(c[i].indexOf("=")+1)).split("<>"); break; }}
	if(cookiename == "SN_UPLOAD"){ obj.pass.value =  unescape(p[0]);$postval }
	else if(cookiename == "SN_DEL"){ obj.delpass.value =  unescape(p[0]);}
	return true;
}
function delnoin(no){
	document.Del.delno.value = no;
	document.Del.del.focus();
}
//-->
</script>
$set{'html_css'}</HEAD>
<body bgcolor="#ffffff" text="#000000" LINK="#6060FF" VLINK="#6060FF" ALINK="#6060FF" onload="getCookie(document.Form,'SN_UPLOAD');getCookie(document.Del,'SN_DEL');">
<table summary="title" width="100%"><tr><td bgcolor="#caccff"><strong><font size="4" color="#3366cc">Uploader</font></strong></td></tr></table>
<p>
Now.. Testing..
</p>
EOM
	my $maxsize = 'Max '.dispsize($set{'max_size'}*1024);
	my ($minsize,$total);
	if($set{'min_flag'}){ $minsize = 'Min '.dispsize($set{'min_size'}*1024).' - '; }
	if($set{'max_all_flag'}){ $total .= ' Total '.dispsize($set{'max_all_size'}*1024);}
	$header .= qq|<FORM METHOD="POST" ENCTYPE="multipart/form-data" ACTION="$set{'base_cgi'}" name="Form">FILE $minsize$maxsize (*$set{'max_log'}Files$total)<br>|;
	$header .='<INPUT TYPE=file  SIZE="40" NAME="upfile">';
	$header .= ' DLKey: <INPUT TYPE=text SIZE="8" NAME="dlkey" maxlength="8">' if($set{'dlkey'});
	$header .= '
DELKey: <INPUT TYPE=password SIZE="10" NAME="pass" maxlength="8"><br>
COMMENT<br>
<INPUT TYPE=text SIZE="45" NAME="comment">
<INPUT TYPE=hidden NAME="jcode" VALUE="漢字">
<INPUT TYPE=submit VALUE="Upload"><INPUT TYPE=reset VALUE="Cancel"><br>
';
	if($set{'post_flag'}){ $header .= 'PostKey<br><INPUT TYPE=password SIZE="10" NAME="postkey" maxlength="10">'; }
	$header .= '</FORM>';

	my $allsize = 0;
	my @files = globfile("$set{'src_dir'}",".*");
	my @dir = globdir("$set{'src_dir'}",".*");
	foreach my $dir (@dir){	push(@files,globfile($dir."/",".*")); }
	foreach my $value (@files){ $allsize += (-s "$value"); }

	$allsize = dispsize($allsize);

	my $footer = "</table><HR size=1>Used ${allsize}\n<br>";
	if($set{'up_all'} && !$set{'ext_org'}){ $footer .= $set{'up_ext'}.' +'; }
	elsif(!$set{'up_all'}){ $footer .= $set{'up_ext'}; }
	$footer .= "\n<table summary=\"footer\" width=\"100%\"><tr><td><div align=left><FORM METHOD=POST ACTION=\"$set{'base_cgi'}\" name=\"Del\"><span style='font-size:9pt'><input type=hidden name=mode value=delete>No.<input type=text size=4 name=delno> key<input type=password size=4 name=delpass> <input type=submit value=\"del\" name=del></span></form></div>\n";
	$footer .= "</td><td><div align=right><!-- $set{'ver'} --><a href=\"http://sugachan.dip.jp/download/\" target=\"_blank\"><small>Sn Uploader</small></a></div></td></tr></table>\n</body>\n</html>";

	my $info_title = "<table summary=\"upinfo\" width=\"100%\">\n<tr><td></td><td>NAME</td>";
	if($set{'disp_comment'}){ $info_title .= "<td>COMMENT</td>"; } if($set{'disp_size'}){ $info_title .= "<td>SIZE</td>"; } if($set{'disp_date'}){ $info_title .= "<td>DATE</td>"; }
	if($set{'disp_mime'}){ $info_title .= "<td>MIME</td>"; } if($set{'disp_orgname'}){ $info_title .= "<td>ORIG</td>"; }
	$info_title .= "</tr>\n";

	my $home_url_link;
	if($set{'home_url'}){ $home_url_link = qq|<a href="$set{'home_url'}">[HOME]</a> |;}
	if($set{'html_all'}){
		my $buff; my $no = 1; my $time = time; my $subheader;
		foreach my $value (@log){
			my ($no,$ext,$date,$comment,$mime,$orgname,$addr,$host,$pass,$dummy) = split(/<>/,$value);
			if(!$dummy){ next; }
			$buff .= makeitem($value);
		}
		$subheader .= "[ALL] ";
		while($no <= $lastpage){
			if($no == $page) { $subheader .= "\[$no\] ";}
			else{	if($no == 1){ $subheader .= "<a href=\"$set{'http_html_path'}$set{'base_html'}?$time\">\[$no\]</a> "}
					else{$subheader .= "<a href=\"$set{'http_html_path'}$no.html?$time\">\[$no\]</a> ";}	}
			$no++;
		}
		$subheader .= $info_title;
		open(OUT,">$set{'html_dir'}all.html")||&error(306,"$set{'html_dir'}all.html");
		print OUT $header."<hr size=1>".$home_url_link.$subheader."<hr size=1>".$buff.$footer;
		close(OUT);
		chmod($set{'per_upfile'},"$set{'html_dir'}all.html");
	}else{ unlink("$set{'html_dir'}all.html"); }
	
	while($log > $i){
		$buff .= makeitem($log[$i]) unless($init);
		if(($i % $set{'pagelog'}) == 0||$i == $log -1){
			$page++; my $subheader; my $no = 1;	my $time = time;
			if($set{'html_all'}){ $subheader .= "<a href=\"./all.html?$time\">[ALL]</a> "; }
			while($no <= $lastpage){
				if($no == $page) { $subheader .= "\[$no\] ";}
				else{	if($no == 1){ $subheader .= "<a href=\"$set{'http_html_path'}$set{'base_html'}?$time\">\[$no\]</a> "}
						else{$subheader .= "<a href=\"$set{'http_html_path'}$no.html?$time\">\[$no\]</a> ";}
				}
				$no++;
			}
			$subheader .= $info_title;
			my $loghtml;
			if($page == 1){	$loghtml = "$set{'html_dir'}$set{'base_html'}"; }
			else{ $loghtml = "$set{'html_dir'}$page.html"; }

			open(OUT,">$loghtml") || &error(306,"$loghtml");
			print OUT $header."<hr size=1>".$home_url_link.$subheader."<hr size=1>".$buff.$footer;
			close(OUT);
			chmod($set{'per_upfile'},$loghtml);
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
	if(-e "$set{'src_dir'}$random.temporary"){ &error(204); }
	open (FILE,">$set{'src_dir'}$random.temporary") || &error(204);
	binmode(FILE);
	eval{ while(my $read = read($in{'upfile'}, my $buff, 8192)){ print FILE $buff; }};
	close(FILE);
	chmod($set{'per_upfile'},"$set{'src_dir'}$random.temporary");
	if((-s "$set{'src_dir'}$random.temporary") == 0){ unlink("$set{'src_dir'}$random.temporary"); &error(99); }
	my $size = (-s "$set{'src_dir'}$random.temporary");
	if($set{'min_flag'} && ($size < $set{'min_size'} * 1024)){ unlink("$set{'src_dir'}$random.temporary"); &error(107,$size);}
	if($size > $set{'max_size'} * 1024){ unlink("$set{'src_dir'}$random.temporary"); &error(106,$size);}
	eval { close($in{'upfile'});};
	unlink($in{'tmpfile'});
	return("$set{'src_dir'}$random.temporary");
}

sub delete{
	my $mode = $_[0];
	my @delno = split(/,/,$_[1]);
	my $delno; my $flag = 0; my $tmpaddr;
	my $delnote;

	if($in{'delno'} =~ /(\d+)/){ $delno = $1; }
	if($mode ne 'admin' && !$in{'delno'}){ return; }
	elsif($mode ne 'admin' && !$delno){ &error(401,$in{'delno'}); }

	open(IN,$set{'log_file'})|| &error(303);
	my @log = <IN>;
	close(IN);

	if($in{'addr'} =~ /(\d+).(\d+).(\d+).(\d+)/){ $tmpaddr = "$1.$2.$3."; }
	my $findflag = 0;
	foreach my $value (@log){
		my ($no,$ext,$date,$comment,$mime,$orgname,$addr,$host,$pass,$filepre,$note,$dummy) = split(/<>/,$value);
		$delnote = $note;
		my $delflag = 0;
		if(!$addr){ next; }
		if($mode eq 'admin'){
			foreach my $delno (@delno){ if($no == $delno){ $delflag = 1; last; } }
		}elsif($no == $delno){
			$findflag = 1;
			unless ($addr =~ /^$tmpaddr/){
				my ($pass,$id) = split(/,/,$pass);
				my $delpass = $in{'delpass'} || $in{'addr'}.time();
				my $salt = substr($pass, 0, 2);	$delpass = crypt($delpass,$salt);
				my $usersalt = substr($in{'user'},0,2); my $userid = crypt($in{'user'},$usersalt);
				if ($in{'delpass'} ne $set{'admin_pass'} && $delpass ne $pass && $userid ne $id){ 
					if($mode ne 'admin'){ if(!$dummy){ $filepre = $set{'file_pre'};} $no = sprintf("%04d",$no); &error(404,"$filepre$no.$ext");}
				}
			}
			$delflag = 1;
		}
		if($delflag){
#			open(OUT,">>./del.cgi"); print OUT $value; close(OUT);
			$flag = 1;
			if(!$dummy){ $filepre = $set{'file_pre'};}
			$no = sprintf("%04d",$no);
			my $filename;
			my ($dlpath,$filedir);
			if($delnote =~ /DLpath:(.+)\s/){
				$dlpath = $1;
				$filename = "$set{'src_dir'}$filepre$no.${ext}_$dlpath/$filepre$no.$ext";
				$filedir = "$set{'src_dir'}$filepre$no.${ext}_$dlpath/";
			}else{
				$filename = "$set{'src_dir'}$filepre$no.$ext";
			}
			
			if(unlink($filename)){
				unlink("$set{'src_dir'}$filepre$no.$ext.html"); if($filedir){ foreach(globfile($filedir,".*")){ unlink; } rmdir($filedir);} undef $value;
			}elsif(unlink($filename)){
				unlink("$set{'src_dir'}$filepre$no.$ext.html"); if($filedir){ foreach(globfile($filedir,".*")){ unlink; } rmdir($filedir);} undef $value;
			}elsif(!(-e $filename)){
				unlink("$set{'src_dir'}$filepre$no.$ext.html"); if($filedir){ foreach(globfile($filedir,".*")){ unlink; } rmdir($filedir);} undef $value;
			}else{
				if($mode ne 'admin'){ &error(403,"$filepre$no.$ext");}
			}
		}
	}
	if($mode ne 'admin' && !$findflag){ &error(402,$delno); }
	if($flag){
		logwrite(@log);
		&makehtml();
	}
}

sub quit{
	my ($cookiename,$buff);
	my $flag = 0;
	my @tmpfiles = globfile("$set{'src_dir'}","\.temporary");
	foreach my $value (@tmpfiles){ if((stat($value))[10] < time - 60*60){ unlink("$value"); $flag++; } }
	&makehtml() if($flag);
	$buff =<<"EOM";
$set{'html_head'}<META HTTP-EQUIV="Refresh" CONTENT="1;URL=$set{'http_html_path'}$set{'base_html'}">
EOM
	if($in{'jcode'} || $in{'mode'} eq 'delete'){
		$buff .=<<"EOM";
<META HTTP-EQUIV="Set-Cookie" content="SN_USER=$in{'user'}&lt;&gt;1; path=/; expires=Tue, 31-Dec-2030 23:59:59 GMT">
<META HTTP-EQUIV="CONTENT-SCRIPT-TYPE" CONTENT="text/javascript">
<script type="text/javascript">
<!--
setCookie();
function setCookie() {
	var key1,key2;
	var tmp = "path=/; expires=Tue, 31-Dec-2030 23:59:59; ";
EOM
		if($in{'jcode'}){
			my %ck; foreach(split(/;/,$ENV{'HTTP_COOKIE'})){ my($key,$val) = split(/=/); $key =~ s/\s//g; $ck{$key} = $val;}
			my @ck = split(/<>/,$ck{'SN_DEL'});
			if(!$ck[0] && $in{'org_pass'}){	$buff .= qq|\tdocument.cookie = "SN_DEL="+escape('$in{'org_pass'}')+"<>;"+ tmp;\n|;}
			$cookiename = 'SN_UPLOAD'; $buff .= "\tkey1 = escape('$in{'org_pass'}'); key2 = escape('$in{'postkey'}');\n";}
		else{ $cookiename = 'SN_DEL'; $buff .= "\tkey1 = escape('$in{'delpass'}'); key2 = '';\n"; }
		$buff .= qq|\tdocument.cookie = "$cookiename="+key1+"<>"+key2+"; "+ tmp;\n}\n//-->\n</script>\n|;
	}
	$buff .=<<"EOM";
<body>
<br><br><div align=center><font size="+1"><br><br>
<a href="$set{'http_html_path'}$set{'base_html'}?$in{'time'}">click here!</a></font><br>
</div>
</body></html>
EOM
	print "Content-type: text/html\n\n";
	print $buff;
	exit;
}

sub admin_mode{
	&errorclear() if($in{'mode'} eq 'errorclear');
	&delete('admin',$in{'admin_delno'}) if($in{'mode'} eq 'delete');

	open(IN,$set{'log_file'})||error(303);
	my @log = <IN>;
	close(IN);

	my ($header,$buff,$footer,$value);
	$buff =<<"EOM";
$set{'html_head'}$set{'html_css'}</HEAD>
<body bgcolor="#ffffff" text="#000000" LINK="#6060FF" VLINK="#6060FF" ALINK="#6060FF">
EOM

	$buff .= leaddisp(0,1,1).'<a name="up"></a><table summary="title" width="100%"><tr><td bgcolor="#caccff"><strong><font size="4" color="#3366cc">Upload Info</font></strong></td></tr></table>';
	$buff .= qq|<table summary="check"><tr><td><form action="$set{'base_cgi'}" method="POST"><input type=hidden name="checkmode" value="allcheck"><input type=hidden name=delno value="$in{'delno'}"><input type=hidden name=delpass value="$in{'delpass'}"><input type=submit value="すべてチェック"></form></td><td><form action="$set{'base_cgi'}" method="POST"><input type=hidden name="checkmode" value="nocheck"><input type=hidden name=delno value="$in{'delno'}"><input type=hidden name=delpass value="$in{'delpass'}"><input type=submit value="すべて外す"></form></td><td><form action="$set{'base_cgi'}" method="POST"><input type=hidden name=delpass value="$set{'admin_pass'}"><input type=submit value="HTMLを更新する/ログアウト"></form></td></tr></table>\n<form action="$set{'base_cgi'}" method="POST"><input type=hidden name="mode" value="delete"><input type=hidden name=delno value="$in{'delno'}"><input type=hidden name=delpass value="$in{'delpass'}"><input type=submit value="チェックしたものを削除"><br>\n|."<table summary=\"upinfo\" width=\"100%\">\n<tr><td>DEL</td><td>NAME</td><td>COMMENT</td><td>SIZE</td><td>ADDR</td><td>HOST</td><td>DATE</td><td>NOTE</td><td>MIME</td><td>ORIG</td></tr>\n";
	shift(@log);
	foreach (@log){	$buff .= makeitem($_,'admin'); }
	$buff .= '</table></form><br><br>';

	if($set{'error_level'}){
		$buff .= leaddisp(-1,0,1).'<a name="error"></a><table summary="errortitle" width="100%"><tr><td bgcolor="#caccff"><strong><font size="4" color="#3366cc">Error Info</font></strong></td></tr></table>';
		$buff .= qq|<form action="$set{'base_cgi'}" method="POST"><input type=hidden name=mode value="errorclear"><input type=hidden name=delno value="$in{'delno'}"><input type=hidden name=delpass value="$in{'delpass'}"><input type=submit value="エラーログクリア"></form>|;
		$buff .= "<table summary=\"errorinfo\" width=\"100%\">\n<tr><td>DATE</td><td>ADDR</td><td>HOST</td><td>NOTE</td></tr>\n";
		if(open(IN,$set{'error_log'})){	@log = reverse(<IN>); close(IN); foreach (@log){ my ($date,$no,$note,$addr,$host) = split(/<>/); $buff .= "<tr><td>$date</td><td>$addr</td><td>$host</td><td>$note</td></tr>\n"; }}
		$buff .= "</table><br><br>\n";
	}

	$buff .= leaddisp(-1,-1,0);
	$buff .= '<a name="set"></a><table summary="settitle" width="100%"><tr><td bgcolor="#caccff"><strong><font size="4" color="#3366cc">Setting Info</font></strong></td></tr></table>'."\n<table summary=\"setting\">\n";
	$buff .= tablestr('スクリプトVer',$set{'ver'});
	$buff .= tablestr('メインログファイル',$set{'log_file'});
	if($set{'error_level'}){
		$buff .= tablestr('エラーログファイル',$set{'error_log'});
		if($set{'error_size'}){ $buff .= tablestr('エラーログ最大容量',dispsize($set{'error_size'}*1024).' '.($set{'error_size'}*1024).'Bytes'); }
		else{ $buff .= tablestr('エラーログ最大容量制限','無'); }
	}else{ $buff .= tablestr('エラーログ記録','無'); }
	$buff .= tablestr('保持件数',$set{'max_log'});
	$buff .= tablestr('最大投稿容量',dispsize($set{'max_size'}*1024).' '.($set{'max_size'}*1024).'Bytes');

	if($set{'min_flag'}){ $buff .= tablestr('最小制限容量',dispsize($set{'min_size'}*1024).' '.($set{'min_size'}*1024).'Bytes'); }
	else{ $buff .= tablestr('最小制限容量',"無"); }
	if($set{'max_all_flag'}){ $buff .= tablestr('総容量制限',dispsize($set{'max_all_size'}*1024).' '.($set{'max_all_size'}*1024).'Bytes'); }
	else{ $buff .= tablestr('総容量制限',"無"); }

	$buff .= tablestr("ファイル接頭辞",$set{'file_pre'});
	$buff .= tablestr("HTML保存ディレクトリ",$set{'html_dir'});
	$buff .= tablestr("ファイル保存ディレクトリ",$set{'src_dir'});
	if($set{'http_html_path'} && $set{'html_dir'} ne $set{'http_html_path'}){ $buff .= "<tr><td>HTTP_HTML_PATH</td><td>$set{'http_html_path'}</td></tr>\n";}
	if($set{'http_src_path'} && $set{'src_dir'} ne $set{'http_src_path'}){ $buff .= "<tr><td>HTTP_SRC_PATH</td><td>$set{'http_src_path'}</td></tr>\n";}
	$buff .= tablestr('1ページに表示するファイル数',$set{'pagelog'});
	if($set{'interval'} > 0){ $value = $set{'interval'}.'秒'; }else{ $value = '無'; }
	$buff .= tablestr('同一IP投稿間隔秒数制限',$value);
	if($set{'up_ext'}){	$set{'up_ext'} =~ s/,/ /g; $buff .= tablestr('投稿可能基本拡張子',$set{'up_ext'}); }
	if($set{'deny_ext'}){ $set{'deny_ext'} =~ s/,/ /g; $buff .= tablestr('投稿禁止拡張子',$set{'deny_ext'}); }
	if($set{'change_ext'}){	$set{'change_ext'} =~ s/,/ /g; $set{'change_ext'} =~ s/>/&gt;/g; $buff .= tablestr('拡張子変換',$set{'change_ext'});	}

	if($set{'up_all'}){	$buff .= tablestr('指定外拡張子アップロード許可','有'); if($set{'ext_org'}){ $buff .= tablestr('指定外ファイル拡張子','オリジナル'); }else{ $buff .= tablestr('指定外ファイル拡張子','bin'); }}
	else{$buff .= tablestr('指定外拡張子アップロード許可','無');}

	if($set{'find_crypt'}){ $value = '有'; }else{ $value = '無';}
	$buff .= tablestr('暗号化アーカイブ検出(ZIP)',$value);
	if($set{'binary_compare'}){ $value = '有'; }else{ $value = '無';}
	$buff .= tablestr('バイナリ比較',$value);
	if($set{'post_flag'}){ $value = '有'; }else{ $value = '無';}
	$buff .= tablestr('PostKey投稿制限',$value);
	if($set{'dlkey'}){ if($set{'dlkey'} == 2){$value = '必須'}else{$value = '任意';}}else{ $value = '無';}
	$buff .= tablestr('DLkey',$value);
	if($set{'dummy_html'}){ if($set{'dummy_html'} == 3){$value = 'ALL'}elsif($set{'dummy_html'} == 2){$value = 'DLKeyのみ';}else{$value = '通常ファイルのみ';}}else{ $value = '無';}
	$buff .= tablestr('個別HTMLキャッシュ',$value);
	if($set{'disp_error'}){ $value = '有'; }else{ $value = '無';}
	$buff .= tablestr('ユーザエラー表示',$value);
	if($set{'zero_clear'}){ $value = '有'; }else{ $value = '無';}
	$buff .= tablestr('削除済ファイルリスト自動消去',$value);
	if($set{'home_url'}){ $buff .= "<tr><td>HOMEURL</td><td>$set{'home_url'}</td></tr>\n";}

	$buff .= '</table></body></html>';

	print "Content-type: text/html\n\n";
	print $buff;
	exit;
}

sub extfind{
	my $orgname = @_[0];
	my @filename = split(/\./,$orgname);
	my $ext = $filename[$#filename];
	$ext =~ tr/[A-Z]/[a-z]/;
	foreach my $value (split(/,/,$set{'change_ext'})){ my ($src,$dst) = split(/->/,$value); if($ext eq $src){ $ext = $dst; last; }}
	foreach my $value (split(/,/,$set{'deny_ext'})){ if($ext eq $value){ &error(206,$ext); }}
	foreach my $value (split(/,/,$set{'up_ext'})){ if ($ext eq $value) { return $value; } }
	if(length($ext) >= 5 || length($ext) == 0){ $ext = 'bin'; }
	unless ($ext =~ /^[A-Za-z0-9]+$/){ $ext = 'bin'; }
	if($set{'up_all'} && $set{'ext_org'}){ return $ext;}
	elsif($set{'up_all'}){ return 'bin'; }
	return 0;
}

sub conv_date{
	my @date = gmtime($_[0] + 9*60*60);
	$date[5] -= 100; $date[4]++;
	if ($date[5] < 10) { $date[5] = "0$date[5]" ; }	if ($date[4] < 10) { $date[4] = "0$date[4]" ; }
	if ($date[3] < 10) { $date[3] = "0$date[3]" ; }	if ($date[2] < 10) { $date[2] = "0$date[2]" ; }
	if ($date[1] < 10) { $date[1] = "0$date[1]" ; }	if ($date[0] < 10) { $date[0] = "0$date[0]" ; }
	my @w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	return ("$date[5]/$date[4]/$date[3]($w[$date[6]]),$date[2]:$date[1]:$date[0]");
}

sub dispsize{
	my $size = $_[0];
	if($size >= 1024*1024*1024*100){ $size = int($size/1024/1024/1024).'GB';}
	elsif($size >= 1024*1024*1024*10){ $size = sprintf("%.1fGB",$size/1024/1024/1024);}
	elsif($size > 1024*1024*1024){ $size = sprintf("%.2fGB",$size/1024/1024/1024);}
	elsif($size >= 1024*1024*100){ $size = int($size/1024/1024).'MB'; }
	elsif($size > 1024*1024){ $size =  sprintf("%.1fMB",$size/1024/1024); }
	elsif($size > 1024){ $size = int($size/1024).'KB'; }
	else{ $size = int($size).'B';}
	return $size;
}

sub makeitem{
	my ($src,$mode) = @_; my ($buff,$check,$target);
	my ($no,$ext,$date,$comment,$mime,$orgname,$addr,$host,$pass,$filepre,$note,$dummy) = split(/<>/,$src);
	if(!$dummy){ $filepre = $set{'file_pre'}; }
	my $orgno = $no;
	$no = sprintf("%04d",$no);
	my $size = 0;
	my $dlpath = 0;

	if($note =~ /DLpath:(.+)\s/){
		$dlpath = $1;
		$size = dispsize(-s "$set{'src_dir'}$filepre$no.${ext}_$dlpath/$filepre$no.$ext");
	}else{
		$size = dispsize(-s "$set{'src_dir'}$filepre$no.$ext");
	}

	my $path = $set{'http_src_path'} || $set{'src_dir'};
	if($set{'link_target'}){ $target = qq| target="$set{'link_target'}"|; }
	if($mode eq 'admin'){
		if($dlpath){ $path .= "$filepre$no.${ext}_$dlpath/"; }
		if($addr eq $host){ undef $host; }
		if($in{'checkmode'} eq 'allcheck'){$check = ' checked';}
		$buff = "<tr><td><INPUT TYPE=checkbox NAME=\"admin_delno\" VALUE=\"$no\"$check></td><td><a href=\"$path$filepre$no.$ext\"$target>$filepre$no.$ext</a></td><td>$comment</td><td>$size</td><td>$addr</td><td>$host</td><td>$date</td><td>$note</td><td>$mime</td><td>$orgname</td></tr>\n";
	}else{
		my($d_com,$d_date,$d_size,$d_mime,$d_org);
		if($set{'disp_comment'}){ $d_com = "<td>$comment</td>"; } if($set{'disp_size'}){ $d_size = "<td>$size</td>"; } if($set{'disp_date'}){ $d_date= "<td>$date</td>"; }
		if($set{'disp_mime'}){ $d_mime = "<td>$mime</td>"; } if($set{'disp_orgname'}){ $d_org = "<td>$orgname</td>"; }
		if(-e "$set{'src_dir'}$filepre$no.$ext.html"){$buff = "<tr><td><SCRIPT type=\"text/javascript\" Language=\"JavaScript\"><!--\ndocument.write(\"<a href=\\\"javascript:delnoin($orgno)\\\">$set{'char_delname'}<\\/a>\");\n// --></SCRIPT></td><td><a href=\"$path$filepre$no.$ext.html\"$target>$filepre$no.$ext</a></td>$d_com$d_size$d_date$d_mime$d_org</tr>\n";}
		elsif($dlpath){$buff = "<tr><td><SCRIPT type=\"text/javascript\" Language=\"JavaScript\"><!--\ndocument.write(\"<a href=\\\"javascript:delnoin($orgno)\\\">$set{'char_delname'}<\\/a>\");\n// --></SCRIPT></td><td><a href=\"$set{'base_cgi'}?mode=dl&file=$orgno\">$filepre$no.$ext</a></td>$d_com$d_size$d_date$d_mime$d_org</tr>\n";}
		else{ $buff = "<tr><td><SCRIPT type=\"text/javascript\" Language=\"JavaScript\"><!--\ndocument.write(\"<a href=\\\"javascript:delnoin($orgno)\\\">$set{'char_delname'}<\\/a>\");\n// --></SCRIPT></td><td><a href=\"$path$filepre$no.$ext\"$target>$filepre$no.$ext</a></td>$d_com$d_size$d_date$d_mime$d_org</tr>\n";}
	}
	return $buff;
}

sub makedummyhtml{
	my ($filename,$com,$file,$orgdlpath,$date,$mime,$orgname,$no) = @_;
	my $buff;

	if(!$no){
		$buff = "<html><head><title>$filename</title></head><body>";
		$buff .= qq|Download <a href="./$filename">$filename</a>|;
		$buff .= '</body></html>';
	}else{
		$buff = cryptfiledl($com,$file,$orgdlpath,$date,$mime,$orgname,$no);
	}

	open(OUT,">$set{'src_dir'}$filename.html")||&error(307,"$set{'src_dir'}$filename.html");
	print OUT $buff;
	close(OUT);
	chmod($set{'per_upfile'},"$set{'src_dir'}$filename.html");
	return 1;
}

sub logwrite{
	my @log = @_;
	open(OUT,"+>$set{'log_file'}")||&error(304);
	eval{ flock(OUT, 2);};
	eval{ truncate(OUT, 0);};
	seek(OUT, 0, 0);
	print OUT @log;
	eval{ flock(OUT, 8);};
	close(OUT);
	chmod($set{'per_upfile'},$set{'log_file'});
	return 1;
}

sub binarycmp{
	my ($src,$dst) = @_;
	return 0 if (-s $src != -s $dst);
	open(SRC,$src)||return 0; open(DST,$dst)||return 0;
	my ($buff,$buff2);
	binmode(SRC); binmode(DST); seek(SRC,0,0); seek(DST,0,0); 
	while(read(SRC,$buff,8192)){ read(DST,$buff2,8192); if($buff ne $buff2){ close(SRC); close(DST); return 0; } }
	close(SRC); close(DST);
	return 1;
}

sub init{
	my $buff;
	if(open(OUT,">$set{'log_file'}")){
		print OUT "0<>0<>0<>1\n";
		close(OUT);
		chmod($set{'per_logfile'},$set{'log_file'});
	}else{
		$buff = "<tr><td>メインログの作成に失敗しました</td></tr>";
	}
	
	unless (-d "$set{'src_dir'}"){
		if(mkdir("$set{'src_dir'}",$set{'per_dir'})){
			chmod($set{'per_dir'},"$set{'src_dir'}");
			open(OUT,">$set{'src_dir'}index.html");
			close(OUT);
			chmod($set{'per_upfile'},"$set{'src_dir'}index.html");
		}else{
			$buff .= "<tr><td>Source保存ディレクトリの作成に失敗しました</td></tr>";
		}
	}

	unless (-d "$set{'html_dir'}"){
		if(mkdir("$set{'html_dir'}",$set{'per_dir'})){
			chmod($set{'per_dir'},"$set{'html_dir'}");
		}else{
			$buff .= "<tr><td>HTML保存ディレクトリの作成に失敗しました</td></tr>";
		}
	}

	if($buff){
		$buff .= "<tr><td>ディレクトリに書き込み権限があるか確認してください</td></tr>";
		&error_disp($buff,'init');
	}
}

sub check_postkey{
	my $inputkey = @_[0];
	my @key = split(/,/,$set{'post_key'});
	foreach my $key (@key){ if($inputkey eq $key){ return 1; } }
	return 0;
}

sub leaddisp{
	my @src = @_;
	my ($str,$count);
	foreach my $value (@src){
		my ($mark,$name,$link); $count++;
		if($count == 1){ $name = 'Upload Info'; $link = 'up'; }
		elsif($count == 2){ $name = 'Error Info'; $link = 'error'; next if(!$set{'error_level'}); }
		elsif($count == 3){ $name = 'Setting Info'; $link = 'set'; }
		if($value){ if($value > 0){ $mark = '▼'; }else{ $mark = '▲'; } $str .= qq|<a href="#$link">${mark}${name}</a> |; }
		else{ $str .= qq|[$name] |; }
	}
	return $str;
}

sub errorclear{
	open(OUT,">$set{'error_log'}")||return 0;
	eval{ flock(OUT, 2);}; eval{ truncate(OUT, 0);}; seek(OUT, 0, 0); eval{ flock(OUT, 8);}; close(OUT);
	chmod($set{'per_upfile'},$set{'log_file'});
	return 1;
}

sub tablestr{
	my ($value1,$value2) = @_;
	return ("<tr><td>$value1</td><td>$value2</td></tr>\n");
}

sub globfile{
	my ($src_dir,$filename) = @_;
	opendir(DIR,$src_dir)||return 0; my @dir = readdir(DIR); closedir(DIR);
	my @new = (); foreach my $value (@dir){ push(@new,"$src_dir$value") if($value =~ /$filename/ && !(-d "$src_dir$value")); }
	return @new;
}

sub globdir{
	my ($src_dir,$dir) = @_;
	opendir(DIR,$src_dir)||return 0; my @dir = readdir(DIR); closedir(DIR);
	my @new = (); foreach my $value (@dir){ if($value eq '.' ||$value eq '..' ){ next; } push(@new,"$src_dir$value") if($value =~ /$dir/ && (-d "$src_dir$value")); }
	return @new;
}

sub error_disp{
	my ($message,$mode) = @_;
	my $url;
	if($mode eq 'init'){ $url = qq|<a href="$set{'base_cgi'}">[リロード]</a>|; }else{ $url = qq|<a href="$set{'http_html_path'}$set{'base_html'}">[戻る]</a>|; }
	my $buff =<<"EOM";
$set{'html_head'}$set{'html_css'}</HEAD>
<body bgcolor="#ffffff" text="#000000" LINK="#6060FF" VLINK="#6060FF" ALINK="#6060FF">
<div align="center">
<table summary="error">
$message
<tr><td></td></tr>
<tr><td><div align="center">$url</div></td></tr>
</table>
<br><br>
<table summary="info">
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
	my ($no,$note) = @_;
	if (length($note) > 64) { $note = substr($note,0,64).'...'; }
	$note =~ s/&/&amp;/g; $note =~ s/\"/&quot;/g; $note =~ s/</&lt;/g; $note =~ s/>/&gt;/g; $note =~ s/\r//g; $note =~ s/\n//g; $note =~ s/\t//g; $note =~ s/\0//g;
	my ($message,$dispmsg,$flag);
	if($no == 98){ $message = ""; }
	elsif($no == 99){ $message = "UpFileなし"; }
	elsif($no == 101){ $message = "投稿禁止HOST"; }
	elsif($no == 106){ $flag = 1; $message = "POSTサイズ超過"; $note = dispsize($note); $dispmsg= '<tr><td>ファイルをアップロードできませんでした</td></tr><tr><td>アップロードファイル('.$note.')は 最大容量設定('.dispsize($set{'max_size'}*1024).')を越えています</td></tr>';}
	elsif($no == 107){ $flag = 1; $message = "POSTサイズ過小"; $note = dispsize($note); $dispmsg= '<tr><td>ファイルをアップロードできませんでした</td></tr><tr><td>アップロードファイル('.$note.')は 最小容量設定('.dispsize($set{'min_size'}*1024).')未満です</td></tr>';}
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
	eval { close($in{'upfile'}); };
	unlink($in{'tmpfile'});
	if($set{'error_level'} && $no > 100){
		unless(-e $set{'error_log'}){
			open(OUT,">$set{'error_log'}");
			close(OUT);
			chmod($set{'per_logfile'},$set{'error_log'});
		}
		if($set{'error_size'} && ((-s $set{'error_log'}) > $set{'error_size'} * 1024)){
			my $err_bkup = "$set{'error_log'}.bak.cgi";
			unlink($err_bkup);
			rename($set{'error_log'},$err_bkup);
			open(OUT,">$set{'error_log'}");
			close(OUT);
			chmod($set{'per_logfile'},$set{'error_log'});
		}
		open(OUT,">>$set{'error_log'}");
		print OUT "$in{'date'}<>$no<>$message$note<>$in{'addr'}<>$in{'host'}<>1\n";
		close(OUT);
	}
	&error_disp($dispmsg) if($flag && $set{'disp_error'});
	&quit();
}

sub dlfile{
	my $msg;
	my ($orgdlkey,$orgdlpath);
	my ($dlext,$dlfilepre);
	my ($dl_date,$dl_comment,$dl_size,$dl_mime,,$dl_orgname);
	my $dlno = 0;
	my $findflag;

	open(IN,$set{'log_file'})||&error(303);
	my @log = <IN>;
	close(IN);
	shift(@log);

	if($in{'file'} =~ /(\d+)/){ $dlno = $1; }
	if($dlno == 0) { &error(51,$in{'file'}); }

	foreach my $value (@log){
		my ($no,$ext,$date,$comment,$mime,$orgname,$addr,$host,$pass,$filepre,$note,$dummy) = split(/<>/,$value);
			my @note = split(/,/,$note);
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
	if(!(-e "$set{'src_dir'}${dlfile}_$orgdlpath/$dlfile")){ &error(56,"$dlfile----$set{'src_dir'}${dlfile}_$orgdlpath/$dlfile"); }

	if($in{'dlkey'}){
		my $dlsalt = substr($orgdlkey,0,2);
		my $dlkey = crypt($in{'dlkey'},$dlsalt);

		if($findflag == 0){ &error(52,$dlfile); }
		elsif(!$orgdlkey){ &error(53,$dlfile); }
		elsif($orgdlkey ne $dlkey && $set{'admin_pass'} ne $in{'dlkey'}){ &error(54,$dlfile); }
		#print "Location: $set{'http_src_path'}${dlfile}_$orgdlpath/$dlfile\n\n";
		my $buff =<<"EOM";
$set{'html_head'}$set{'html_css'}
<META HTTP-EQUIV="Refresh" CONTENT="1;URL=$set{'http_src_path'}${dlfile}_$orgdlpath/$dlfile">
</HEAD>
<body bgcolor="#ffffff" text="#000000" LINK="#6060FF" VLINK="#6060FF" ALINK="#6060FF">
<div align="center">
<br>
<table summary="dlfrom">
<tr><td>飛ばない場合は <a href="$set{'http_src_path'}${dlfile}_$orgdlpath/$dlfile">こちら</a> から</td></tr>
</table>
</div>
</body></html>
EOM
		print "Content-type: text/html\n\n";
		print $buff;
	}else{
		my $buff = cryptfiledl($dl_comment,$dlfile,$orgdlpath,$dl_date,$dl_mime,$dl_orgname,$dlno);
		print "Content-type: text/html\n\n";
		print $buff;
	}
	exit;
}

sub cryptfiledl{
		my($com,$file,$orgdlpath,$date,$mime,$orgname,$no) = @_;
		my($d_com,$d_date,$d_size,$d_mime,$d_org);

		if($set{'disp_comment'}){ $d_com = "<tr><td>COMMENT</td><td>$com</td></td>"; } if($set{'disp_size'}){ $d_size = "<tr><td>SIZE</td><td>".dispsize(-s "$set{'src_dir'}${file}_$orgdlpath/$file")." (".(-s "$set{'src_dir'}${file}_$orgdlpath/$file")."bytes)"."</td></tr>"; } if($set{'disp_date'}){ $d_date= "<tr><td>DATE</td><td>$date</td></tr>"; }
		if($set{'disp_mime'}){ $d_mime = "<tr><td>ORGMIME</td><td>$mime</td></tr>"; } if($set{'disp_orgname'}){ $d_org = "<tr><td>ORGNAME</td><td>$orgname</td></tr>"; }

		my $buff =<<"EOM";
$set{'html_head'}$set{'html_css'}</HEAD>
<body bgcolor="#ffffff" text="#000000" LINK="#6060FF" VLINK="#6060FF" ALINK="#6060FF">
<div align="center">
<br>
$file にはDLKeyが設定されています
<table summary="dlform">
<tr><td></td></tr>
<FORM METHOD=POST ACTION="$set{'base_cgi'}" name="DL">
<tr><td>
<input type=hidden name=file value=$no>
<input type=hidden name=jcode value="漢字">
<input type=hidden name=mode value=dl></td></tr>
$d_com$d_date$d_size$d_mime$d_org
<tr><td>DLKey:<input type=text size=8 name="dlkey"></td></tr>
<tr><td><input type=submit value="DownLoad"></td></tr>
</FORM>
</table>
</div>
</body></html>
EOM

	return $buff;
}