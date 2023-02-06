#!/usr/bin/perl
use CGI;
use vars qw(%set %in);
use strict;
$set{'log_file'} = './log.cgi';		#���O�t�@�C����
$set{'max_log'} = 30;		#�ێ�����
$set{'max_size'} = 1*1024;		#�ő哊�e�e��(KB)
$set{'min_flag'} = 0;		#�ŏ��e�ʐ������g�p����=1
$set{'min_size'} = 100;		#�ŏ����e�e��(KB)
$set{'max_all_flag'} = 0;		#���e�ʐ������g�p����=1
$set{'max_all_size'} = 20*1024;		#�������e��(KB)
$set{'file_pre'} = 'up';		#�t�@�C���ړ���
$set{'pagelog'} = 10;		#1�y�[�W�ɕ\������t�@�C����
$set{'base_html'} = 'upload.html';		#1�y�[�W�ڂ̃t�@�C����
$set{'interval'} = 0;		#����IP���e�Ԋu�b��
$set{'deny_host'} = '';		#���e�֎~IP/HOST ,�ŋ�؂� ex.(bbtec.net,219.119.66,ac.jp)
$set{'admin_name'} = 'admin';		#�Ǘ��҃��O�C��ID
$set{'admin_pass'} = '1234';		#�Ǘ��҃p�X���[�h

# �ȉ�5���ڂ��Đݒ肷��ۂɂ�PATH�C�f�B���N�g���� / �ŏI��邱��
# $set{'html_dir'},$set{'base_cgi'}�� ./ �ȊO�ɐݒ肷��ꍇ,
# �܂���DLkey���g�p�� �Ȃ�����HTML�L���b�V��($set{'dummy_html'} = 2 or 3)���g�p����ꍇ��
# $set{'base_cgi'} , $set{'http_html_path'} , $set{'http_src_path'} ���t���p�X(http://�`�` or /�`�`)�ŋL�q����
$set{'html_dir'} = './';		# ����HTML�ۑ��f�B���N�g��
$set{'src_dir'} = './src/';		# �����t�@�C���ۑ��f�B���N�g��
$set{'base_cgi'} = './upload.cgi'; # ���̃X�N���v�g�� http://�`�̎w��\
$set{'http_html_path'} = './';		# html�Q�� httpPATH http://�`�̎w��\
$set{'http_src_path'} = './src/';		# file�Q�� httpPATH http://�`�̎w��\

$set{'dlkey'} = 0;		# DLKey���g�p����=1,DLkey�K�{=2
$set{'up_ext'} = 'txt,lzh,zip,rar,gca,mpg,mp3,avi,swf,bmp,jpg,gif,png'; #�A�b�v���[�h�ł����{�g���q ���p�p�������� ,�ŋ�؂�
$set{'up_all'} = 0;		#�o�^�ȊO�̂��̂�UP��������悤�ɂ���=1
$set{'ext_org'} = 0;	#$set{'up_all'}��1�̎��I���W�i���̊g���q�ɂ���=1
$set{'deny_ext'} = 'php,php3,phtml,rb,sh,bat,dll'; 	#���e�֎~�̊g���q ���p�p�������� ,�ŋ�؂�
$set{'change_ext'} = 'cgi->txt,pl->txt,log->txt,jpeg->jpg,mpeg->mpg';		#�g���q�ϊ� �O->�� ���p�p�������� ,�ŋ�؂�

$set{'home_url'} = '';		#[HOME]�̃����N�� ���΃p�X���� http://����n�܂��΃p�X
$set{'html_all'} = 1;		#[ALL]���o��=1
$set{'dummy_html'} = 0;		#�t�@�C����HTML���쐬���� �ʏ�t�@�C���̂�=1,DLKey�ݒ�t�@�C���̂�=2,���ׂ�=3
$set{'find_crypt'} = 1;		#�Í���ZIP�����o����=1
$set{'binary_compare'} = 0;		#�����t�@�C���ƃo�C�i����r����=1
$set{'post_flag'} = 0;		#PostKey���g�p����=1
$set{'post_key'} = 'postkey';		#PostKey ,�ŋ�؂�ƕ����w�� ex.(postkey1,postkey2)
$set{'disp_error'} = 1;		#���[�U�[�ɃG���[��\������=1
$set{'error_level'} = 1;		#�G���[���O���L�^����=1
$set{'error_log'} = './error.cgi';		#�G���[���O�t�@�C����
$set{'error_size'} = 1024;	# �G���[���O�ő�e��(KB) �����Ȃ�=0
$set{'zero_clear'} = 1;		#�t�@�C����������Ȃ��ꍇ���O����폜����=1

$set{'disp_comment'} = 1; 	#�R�����g��\������=1
$set{'disp_date'} = 1;		#���t��\������=1
$set{'disp_size'} = 1;		#�T�C�Y��\������=1
$set{'disp_mime'} = 1;		#MIMETYPE��\������=1
$set{'disp_orgname'} = 1;	#�I���W�i���t�@�C������\������=1

$set{'per_upfile'} = 0666;		#�A�b�v���[�h�t�@�C���̃p�[�~�b�V���� suexec=0604,other=0666
$set{'per_dir'} = 0777;		#�\�[�X�A�b�v�f�B���N�g���̃p�[�~�b�V���� suexec=0701,other=0777
$set{'per_logfile'} = 0666;		#���O�t�@�C���̃p�[�~�b�V�����@suexec=0600,other=0666
$set{'link_target'} = '';		#target����

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
input,td{ font-size: 10pt;font-family:Chicago,Verdana,Arial,sans-serif,"�l�r �o�S�V�b�N"; }
a:hover { background-color:#EECCCC; }
input,textarea{	border-top : 1px solid ; border-bottom : 1px solid ; border-left : 1px solid ; border-right : 1px solid ;font-size:10pt;background-color:#FFFFFF; }
-->
</STYLE>
EOM

unless(-e $set{'log_file'}){ &init; }
unless(-e $set{'base_html'}){ &makehtml; }

{ #�f�R�[�h
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

{#���C������
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
		my @str = ('Upload:','�b');
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
<INPUT TYPE=hidden NAME="jcode" VALUE="����">
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
	$buff .= qq|<table summary="check"><tr><td><form action="$set{'base_cgi'}" method="POST"><input type=hidden name="checkmode" value="allcheck"><input type=hidden name=delno value="$in{'delno'}"><input type=hidden name=delpass value="$in{'delpass'}"><input type=submit value="���ׂă`�F�b�N"></form></td><td><form action="$set{'base_cgi'}" method="POST"><input type=hidden name="checkmode" value="nocheck"><input type=hidden name=delno value="$in{'delno'}"><input type=hidden name=delpass value="$in{'delpass'}"><input type=submit value="���ׂĊO��"></form></td><td><form action="$set{'base_cgi'}" method="POST"><input type=hidden name=delpass value="$set{'admin_pass'}"><input type=submit value="HTML���X�V����/���O�A�E�g"></form></td></tr></table>\n<form action="$set{'base_cgi'}" method="POST"><input type=hidden name="mode" value="delete"><input type=hidden name=delno value="$in{'delno'}"><input type=hidden name=delpass value="$in{'delpass'}"><input type=submit value="�`�F�b�N�������̂��폜"><br>\n|."<table summary=\"upinfo\" width=\"100%\">\n<tr><td>DEL</td><td>NAME</td><td>COMMENT</td><td>SIZE</td><td>ADDR</td><td>HOST</td><td>DATE</td><td>NOTE</td><td>MIME</td><td>ORIG</td></tr>\n";
	shift(@log);
	foreach (@log){	$buff .= makeitem($_,'admin'); }
	$buff .= '</table></form><br><br>';

	if($set{'error_level'}){
		$buff .= leaddisp(-1,0,1).'<a name="error"></a><table summary="errortitle" width="100%"><tr><td bgcolor="#caccff"><strong><font size="4" color="#3366cc">Error Info</font></strong></td></tr></table>';
		$buff .= qq|<form action="$set{'base_cgi'}" method="POST"><input type=hidden name=mode value="errorclear"><input type=hidden name=delno value="$in{'delno'}"><input type=hidden name=delpass value="$in{'delpass'}"><input type=submit value="�G���[���O�N���A"></form>|;
		$buff .= "<table summary=\"errorinfo\" width=\"100%\">\n<tr><td>DATE</td><td>ADDR</td><td>HOST</td><td>NOTE</td></tr>\n";
		if(open(IN,$set{'error_log'})){	@log = reverse(<IN>); close(IN); foreach (@log){ my ($date,$no,$note,$addr,$host) = split(/<>/); $buff .= "<tr><td>$date</td><td>$addr</td><td>$host</td><td>$note</td></tr>\n"; }}
		$buff .= "</table><br><br>\n";
	}

	$buff .= leaddisp(-1,-1,0);
	$buff .= '<a name="set"></a><table summary="settitle" width="100%"><tr><td bgcolor="#caccff"><strong><font size="4" color="#3366cc">Setting Info</font></strong></td></tr></table>'."\n<table summary=\"setting\">\n";
	$buff .= tablestr('�X�N���v�gVer',$set{'ver'});
	$buff .= tablestr('���C�����O�t�@�C��',$set{'log_file'});
	if($set{'error_level'}){
		$buff .= tablestr('�G���[���O�t�@�C��',$set{'error_log'});
		if($set{'error_size'}){ $buff .= tablestr('�G���[���O�ő�e��',dispsize($set{'error_size'}*1024).' '.($set{'error_size'}*1024).'Bytes'); }
		else{ $buff .= tablestr('�G���[���O�ő�e�ʐ���','��'); }
	}else{ $buff .= tablestr('�G���[���O�L�^','��'); }
	$buff .= tablestr('�ێ�����',$set{'max_log'});
	$buff .= tablestr('�ő哊�e�e��',dispsize($set{'max_size'}*1024).' '.($set{'max_size'}*1024).'Bytes');

	if($set{'min_flag'}){ $buff .= tablestr('�ŏ������e��',dispsize($set{'min_size'}*1024).' '.($set{'min_size'}*1024).'Bytes'); }
	else{ $buff .= tablestr('�ŏ������e��',"��"); }
	if($set{'max_all_flag'}){ $buff .= tablestr('���e�ʐ���',dispsize($set{'max_all_size'}*1024).' '.($set{'max_all_size'}*1024).'Bytes'); }
	else{ $buff .= tablestr('���e�ʐ���',"��"); }

	$buff .= tablestr("�t�@�C���ړ���",$set{'file_pre'});
	$buff .= tablestr("HTML�ۑ��f�B���N�g��",$set{'html_dir'});
	$buff .= tablestr("�t�@�C���ۑ��f�B���N�g��",$set{'src_dir'});
	if($set{'http_html_path'} && $set{'html_dir'} ne $set{'http_html_path'}){ $buff .= "<tr><td>HTTP_HTML_PATH</td><td>$set{'http_html_path'}</td></tr>\n";}
	if($set{'http_src_path'} && $set{'src_dir'} ne $set{'http_src_path'}){ $buff .= "<tr><td>HTTP_SRC_PATH</td><td>$set{'http_src_path'}</td></tr>\n";}
	$buff .= tablestr('1�y�[�W�ɕ\������t�@�C����',$set{'pagelog'});
	if($set{'interval'} > 0){ $value = $set{'interval'}.'�b'; }else{ $value = '��'; }
	$buff .= tablestr('����IP���e�Ԋu�b������',$value);
	if($set{'up_ext'}){	$set{'up_ext'} =~ s/,/ /g; $buff .= tablestr('���e�\��{�g���q',$set{'up_ext'}); }
	if($set{'deny_ext'}){ $set{'deny_ext'} =~ s/,/ /g; $buff .= tablestr('���e�֎~�g���q',$set{'deny_ext'}); }
	if($set{'change_ext'}){	$set{'change_ext'} =~ s/,/ /g; $set{'change_ext'} =~ s/>/&gt;/g; $buff .= tablestr('�g���q�ϊ�',$set{'change_ext'});	}

	if($set{'up_all'}){	$buff .= tablestr('�w��O�g���q�A�b�v���[�h����','�L'); if($set{'ext_org'}){ $buff .= tablestr('�w��O�t�@�C���g���q','�I���W�i��'); }else{ $buff .= tablestr('�w��O�t�@�C���g���q','bin'); }}
	else{$buff .= tablestr('�w��O�g���q�A�b�v���[�h����','��');}

	if($set{'find_crypt'}){ $value = '�L'; }else{ $value = '��';}
	$buff .= tablestr('�Í����A�[�J�C�u���o(ZIP)',$value);
	if($set{'binary_compare'}){ $value = '�L'; }else{ $value = '��';}
	$buff .= tablestr('�o�C�i����r',$value);
	if($set{'post_flag'}){ $value = '�L'; }else{ $value = '��';}
	$buff .= tablestr('PostKey���e����',$value);
	if($set{'dlkey'}){ if($set{'dlkey'} == 2){$value = '�K�{'}else{$value = '�C��';}}else{ $value = '��';}
	$buff .= tablestr('DLkey',$value);
	if($set{'dummy_html'}){ if($set{'dummy_html'} == 3){$value = 'ALL'}elsif($set{'dummy_html'} == 2){$value = 'DLKey�̂�';}else{$value = '�ʏ�t�@�C���̂�';}}else{ $value = '��';}
	$buff .= tablestr('��HTML�L���b�V��',$value);
	if($set{'disp_error'}){ $value = '�L'; }else{ $value = '��';}
	$buff .= tablestr('���[�U�G���[�\��',$value);
	if($set{'zero_clear'}){ $value = '�L'; }else{ $value = '��';}
	$buff .= tablestr('�폜�σt�@�C�����X�g��������',$value);
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
		$buff = "<tr><td>���C�����O�̍쐬�Ɏ��s���܂���</td></tr>";
	}
	
	unless (-d "$set{'src_dir'}"){
		if(mkdir("$set{'src_dir'}",$set{'per_dir'})){
			chmod($set{'per_dir'},"$set{'src_dir'}");
			open(OUT,">$set{'src_dir'}index.html");
			close(OUT);
			chmod($set{'per_upfile'},"$set{'src_dir'}index.html");
		}else{
			$buff .= "<tr><td>Source�ۑ��f�B���N�g���̍쐬�Ɏ��s���܂���</td></tr>";
		}
	}

	unless (-d "$set{'html_dir'}"){
		if(mkdir("$set{'html_dir'}",$set{'per_dir'})){
			chmod($set{'per_dir'},"$set{'html_dir'}");
		}else{
			$buff .= "<tr><td>HTML�ۑ��f�B���N�g���̍쐬�Ɏ��s���܂���</td></tr>";
		}
	}

	if($buff){
		$buff .= "<tr><td>�f�B���N�g���ɏ������݌��������邩�m�F���Ă�������</td></tr>";
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
		if($value){ if($value > 0){ $mark = '��'; }else{ $mark = '��'; } $str .= qq|<a href="#$link">${mark}${name}</a> |; }
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
	if($mode eq 'init'){ $url = qq|<a href="$set{'base_cgi'}">[�����[�h]</a>|; }else{ $url = qq|<a href="$set{'http_html_path'}$set{'base_html'}">[�߂�]</a>|; }
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
	elsif($no == 99){ $message = "UpFile�Ȃ�"; }
	elsif($no == 101){ $message = "���e�֎~HOST"; }
	elsif($no == 106){ $flag = 1; $message = "POST�T�C�Y����"; $note = dispsize($note); $dispmsg= '<tr><td>�t�@�C�����A�b�v���[�h�ł��܂���ł���</td></tr><tr><td>�A�b�v���[�h�t�@�C��('.$note.')�� �ő�e�ʐݒ�('.dispsize($set{'max_size'}*1024).')���z���Ă��܂�</td></tr>';}
	elsif($no == 107){ $flag = 1; $message = "POST�T�C�Y�ߏ�"; $note = dispsize($note); $dispmsg= '<tr><td>�t�@�C�����A�b�v���[�h�ł��܂���ł���</td></tr><tr><td>�A�b�v���[�h�t�@�C��('.$note.')�� �ŏ��e�ʐݒ�('.dispsize($set{'min_size'}*1024).')�����ł�</td></tr>';}
#	elsif($no == 108){ $flag = 1; $message = "POST�f�[�^�s���S"; $dispmsg = '<tr><td>�t�@�C�����A�b�v���[�h�ł��܂���ł���</td></tr><tr><td>POST�f�[�^���s���S�ł�</td></tr>';}
	elsif($no == 109){ $flag = 1; $message = "POSTKey�s��v"; $dispmsg = '<tr><td>�t�@�C�����A�b�v���[�h�ł��܂���ł���</td></tr><tr><td>POSTKey����v���܂���</td></tr>';}
	elsif($no == 202){ $flag = 1; $message = "�g���q���킸"; $dispmsg = '<tr><td>�t�@�C�����A�b�v���[�h�ł��܂���ł���</td></tr><tr><td>���e�ł���g���q��'.$set{'up_ext'}.'�ł�</td></tr>';}
	elsif($no == 203){ $flag = 1; $message = "���e������"; $dispmsg = '<tr><td>�t�@�C�����A�b�v���[�h�ł��܂���ł���</td></tr><tr><td>����IP�A�h���X����'.$set{'interval'}.'�b�ȓ��ɍē��e�ł��܂���</td></tr>';}
	elsif($no == 204){ $flag = 1; $message = "�ꎞ�t�@�C���������߂�"; $dispmsg = '<tr><td>�t�@�C�����A�b�v���[�h�ł��܂���ł���</td></tr><tr><td>�ꎞ�t�@�C���̍쐬�Ɏ��s���܂���</td></tr>';}
	elsif($no == 205){ $flag = 1; $message = "����t�@�C������"; $note =~ /([^\/]+)$/; my $filename = $1; $dispmsg = '<tr><td>�t�@�C�����A�b�v���[�h�ł��܂���ł���</td></tr><tr><td>����t�@�C���� '.$filename.' �ɑ��݂��܂�</td></tr>';}
	elsif($no == 206){ $flag = 1; $message = "�֎~�g���q"; $dispmsg = '<tr><td>�t�@�C�����A�b�v���[�h�ł��܂���ł���</td></tr><tr><td>�g���q '.$note.' �̓A�b�v���[�h�ł��܂���</td></tr>';}
	elsif($no == 303){ $flag = 1; $message = "���O�t�@�C���ɓǂݍ��߂�"; $dispmsg = '<tr><td>���C�����O�̓ǂݍ��݂Ɏ��s���܂���</td></tr>';}
	elsif($no == 304){ $flag = 1; $message = "���O�t�@�C���ɏ������߂�"; $dispmsg = '<tr><td>���C�����O�̏������݂Ɏ��s���܂���</td></tr>';}
	elsif($no == 306){ $message = "�t�@�C�����X�gHTML�������߂�";}
	elsif($no == 307){ $message = "�t�@�C��HTML�t�@�C���������߂�";}
	elsif($no == 401){ $flag = 1; $message = "�폜No.���o�ł���"; $dispmsg = '<tr><td>�t�@�C�����폜�ł��܂���ł���</td></tr><tr><td>'.$note.' ����폜No.�����o�ł��܂���ł���</td></tr><tr><td>'.$set{'file_pre'}.'0774.zip�̏ꍇ No.�ɂ� 774 ����͂��܂�</td></tr>';}
	elsif($no == 402){ $flag = 1; $note = sprintf("%04d",int($note)); $message = "�폜No.���݂���"; $dispmsg = '<tr><td>�t�@�C�����폜�ł��܂���ł���</td></tr><tr><td>'.$set{'file_pre'}.$note.'.*** �̓��C�����O�ɑ��݂��܂���</td></tr>';}
	elsif($no == 403){ $flag = 1; $message = "�폜�A�N�Z�X����"; $dispmsg = '<tr><td>�t�@�C�����폜�ł��܂���ł���</td></tr><tr><td>�t�@�C���폜�����͖������Ă��܂��� '.$note.' �̃t�@�C���̍폜�����ۂ���܂���</td></tr><tr><td>�A�N�Z�X���ߏ�ȏꍇ���͎��Ԃ�u���čđ��삷��ƍ폜�ł��邱�Ƃ�����܂�</td></tr>';}
	elsif($no == 404){ $flag = 1; $message = "�폜Key�s��v"; $dispmsg = '<tr><td>�t�@�C�����폜�ł��܂���ł���</td></tr><tr><td>'.$note.' �폜Key����v���܂���ł���</td></tr>';}

	elsif($no == 51){ $flag = 1; $message = "[DLMode] No.�����炸";  $dispmsg = '<tr><td>[DLMode] �t�@�C����������܂���ł���</td></tr><tr><td>'.$note.' ����t�@�C��No.�����o�ł��܂���ł���</td></tr>'; }
	elsif($no == 52){ $flag = 1; $message = "[DLMode] File�����炸";  $dispmsg = '<tr><td>[DLMode] �t�@�C����������܂���ł���</td></tr><tr><td>'.$set{'file_pre'}.$note.'.*** �̓��C�����O�ɑ��݂��܂���</td></tr>'; }
	elsif($no == 53){ $flag = 1; $message = "[DLMode] DLkey���ݒ�";  $dispmsg = '<tr><td>[DLMode] orgDLkeyError</td></tr><tr><td>'.$note.' DLKey�����ݒ�ł�</td></tr>'; }
	elsif($no == 54){ $flag = 1; $message = "[DLMode] DLkey�s��v";  $dispmsg = '<tr><td>[DLMode] orgDLkeyError</td></tr><tr><td>'.$note.' DLKey����v���܂���ł���</td></tr>'; }
	elsif($no == 55){ $flag = 1; $message = "[DLMode] File Oepn Error";  $dispmsg = '<tr><td>[DLMode] Open Error</td></tr><tr><td>'.$note.' �t�@�C���̓ǂݍ��݂Ɏ��s���܂���</td></tr>'; }
	elsif($no == 56){ $flag = 1; $message = "[DLMode] File Not Found";  $dispmsg = '<tr><td>[DLMode] Not Found</td></tr><tr><td>'.$note.' �t�@�C�������݂��܂���</td></tr>'; }

	elsif($no == 61){ $flag = 1; $message = "DLkey���ݒ�";  $dispmsg = '<tr><td>DLKey�����ݒ�ł�</td></tr>'; }

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
<tr><td>��΂Ȃ��ꍇ�� <a href="$set{'http_src_path'}${dlfile}_$orgdlpath/$dlfile">������</a> ����</td></tr>
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
$file �ɂ�DLKey���ݒ肳��Ă��܂�
<table summary="dlform">
<tr><td></td></tr>
<FORM METHOD=POST ACTION="$set{'base_cgi'}" name="DL">
<tr><td>
<input type=hidden name=file value=$no>
<input type=hidden name=jcode value="����">
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