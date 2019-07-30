#!/usr/bin/perl

# You will find a complete HTML tutorial/manual at:
# http://cgi.elitehost.com/acctlite/acctman1.htm
#
# Version 1.05
##############################################################
# EDIT USER CONFIGURATIONS BELOW
# 
# Note: These are the only configurations you will need to
# set in Account Manager LITE.
#
# Be sure to set the "require" paths in both the acctman.pl
# and the amadmin.pl files.
##############################################################

# body 태그 속성들 정의
$bodyspec = "background=\"\" bgcolor=\"#FFFFFF\" link=\"#0000FF\" vlink=\"#0000FF\"";

# header.txt 파일의 위치
$header = ".";

# footer.txt 파일의 위치
$footer = ".";

# 폰트칼라
$fontcolor = "#000000";

# 사이트 이름
$orgname = "WebWeaver";

# 관리자 메일주소
# @ 앞에 반드시 \ 가 있어야 합니다.
$orgmail = "i\@webweaver.pe.kr";

# 임시 디렉토리
$tempdir = "./temp";

# 센드메일 경로
$mailprog = "/usr/sbin/sendmail";

# email.txt 파일의 경로
$closing = ".";

# 회원등록 신청시 보낼 메일 제목
$response_subject = "회원등록 신청하셨습니다!";

# .htaccess 나 .nsconfig 를 사용할 수 있는 서버는 "1", otherwise ""(공백)
$htaccess = "1";

# .htpasswd 파일의 위치
$memaccess = "./memberonly/.htpasswd";

# 회원정보가 저장될 디렉토리
$memberinfo = "./memberinfo";

# 파일록(flock)함수 지원여부, 가능하면 "2", or ""(공백)
$LOCK_EX = "2";

# 관리자 패스워드 저장 디렉토리
$passfile = "./pass";

# 회원에게 메일보낼때 제목
$subject = "WebWeaver 로그인";

# Create two text files.  One called "approved.txt" and the other
# called "denied.txt".  In each, write the response that you would
# like your prospective members to receive when you have either
# approved or denied their application for membership, respectively.
# Then, upload both text files to your $memberinfo directory.
# The script will do the rest.
# Example, in the "approved.txt" file, you can type:
# "Your account is now active."

# 회원등록 거부되었을 경우 메일 제목
$denied_email_subject = "WebWeaver 회원등록 신청 불승인";

# 회원등록 승인되었을 경우 메일 제목
$approved_email_subject ="WebWeaver에 회원등록 되셨습니다.";