# Sn Uploader ��

Sn Uploader (CGI.pm��) �ɃT���l�C�������@�\�ƃ��[���ʒm�@�\�𖳗���t���������A�b�v���[�_�X�N���v�g�ł��B

## �ǉ��@�\

* ImageMagick�ɂ��T���l�C���摜�쐬
* �t�@�C���̃A�b�v���[�h���ƍ폜���Ɏw��A�h���X�փ��[���ʒm���M

## �ݒu�̑O��

�A�b�v���[�_�̐ݒu�ɂ̓��X�N���Ƃ��Ȃ��܂��B

* 2007-02-24 �Ђǂ��ڂɂ�����(�ʕ��Ҕ���)
* 2007-02-27 �����ĂȂ�Ĕn���n���n���n��(�ʕ��Ҕ���)
* ���u�T�[�o�[�Ƀ��o�������u����ĉƑ�{��(�X���h)

���̃X�N���v�g�̓��[���ʒm������Ă��܂����A��ɐ��������삷�邩�̕ۏ؂͂ł��܂���B �ݒu����ꍇ�͐ݒu�ꏊ�̖@�ɑ������Ǘ������Ă��������B

## �����

Sn Uploader ���̓���ɂ͈ȉ��̃��W���[�����K�v�ɂȂ�܂��B

* Encode
* Net::SMTP
* Net::POP3
* ImageMagick (PerlMagick)

Windows + Perl 5.8 (32bit/64bit) �� CentOS + Perl 5.10 (64bit) �œ���m�F���Ă��܂��B mod_perl �ł�������������܂���B

## �ݒu���@

zip���𓀂��Aupload.pl ���̐ݒ�ϐ����e�L�X�g�G�f�B�^�ŕҏW���܂��B �e�ݒ�ϐ��̐����͓�����readme��X�N���v�g���Q�Ƃ��Ă��������B
�ݒu����f�B���N�g�����쐬���A���̉���zip���̃t�@�C�����A�b�v���[�h���Ă��������B doc �f�B���N�g���͍폜���č\���܂���B

### �\����
    -- uploader / upload.pl  --- �X�N���v�g�{��
        |   index.html --- (��������)
        |
        +-- src   --- �A�b�v���[�h�t�@�C���ۑ��f�B���N�g��
        +-- thumb --- �T���l�C���ۑ��f�B���N�g��
        +-- log   --- ���O�f�B���N�g��
        +-- img   --- CSS�f�B���N�g��

### chmod ��
    chmod 777 uploader uploader/src uploader/thumb uploader/log uploader/img
    chmod 755 uploader/upload.pl
    chmod 666 uploader/index.html

�ݒu��Auploader/upload.pl �Ƀu���E�U����A�N�Z�X����� index.html ��������������܂��B

## �T�|�[�g

���̃X�N���v�g�Ɋւ���o�O�񍐓��� �{��Sn Uploader�̃T�C�g�ł͂Ȃ��A���T�C�g�܂� ���肢���܂� (�A����̓g�b�v�y�[�W�Ɍf�ڂ��Ă��܂�)�B

�ۏ؂͂���܂��񂪁A�o�������͈̔͂őΉ�����Ǝv���܂��B

## ���C�Z���X

�{�� Sn Uploader �̍Ĕz�z�K��ɏ����܂��B ���T�C�g�̃����N�\���͍폜�ł��B
Changelog

### mod.1603072206
* ���[���ʒm�@�\���������܂����B
* DLKey��L���ɂ��Ă����DLKey���ݒ肳��Ă��Ȃ��t�@�C���ł��T���l�C�����쐬����Ȃ��s����C�����܂����B
* [ALL]��L���ɂ��Ă���Ƒ��̃t�@�C�����X�g���d�����ďo�͂����s����C�����܂����B
* DLKey�܂���dummyHTML�̂���t�@�C���ŃT���l�C���̃����N�悪404�ɂȂ�s����C�����܂����B
* DLKey�t���̃t�@�C���A�b�v���[�h���� Use of uninitialized value �x�����o��s����C�����܂����B

### mod.1403110536
* �Ƃ肠�����������B
