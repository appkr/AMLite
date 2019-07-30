#!/usr/bin/perl

## 프로그램명 : AMLite 1.05
## Source : www.cgiscriptcenter.com
## 수정 : 김주원 (webweaver@webweaver.pe.kr)
## 배포처 : http://www.webweaver.pe.kr
## 배포일 : 2000년 9월 19일

############################################
##                                        ##
##     Account Manager LITE User Signup   ##
##          by CGI Script Center          ##
##       (e-mail cgi@elitehost.com)       ##
##                                        ##
##             version:  1.05             ##
##         last modified:  08/27/98       ##
##           copyright (c) 1998           ##
##                                        ##
##    latest version is available from    ##
##        http://cgi.elitehost.com        ##
##                                        ##
############################################
##############################################################
# EDIT THE VARIABLES BELOW ###################################
##############################################################

require "./config.pl";

##############################################################
##############################################################
#
# Copyright 1998 Elite Host.  All Rights Reserved.
#
# TERMS OF USE 
# 1. Account Manager LITE is offered as shareware.  In exchange
# for its use, the CGI Script Center requires the following:
#
# Customer/User may use/install Account Manager LITE as many
# times as customer wishes, as long as customer owns th web
# site that Account Manager LITE is installed on.  Account
# Manager LITE may not under any circumstances be sold
# or redistributed without the written consent of CGI Script Center and # its owner Diran Alemshah.
#
# 2. CGI Script Center, at its own discresion, will decide if any terms 
# of the this agreement have been violated by customer. Upon written e- # mailed notification to Customer of Terms of Use violations, CGI
# Script Center may revoke customer's license to use Account Manager
# LITE.
#
# In that event, Customer agrees to any and all of the following:
#
# a) Customers found in violation of this agreement, found reselling or
# redistributing Account Manager LITE, will no longer be licensed to 
# use Account Manager LITE and agrees to either immediately cease
# the use/distribution of Account Manager LITE or pay the CGI
# Script Center the full price of our Professional Series Account
# Manager for each copy used and/or distributed.
# 
# b). Customer will no longer be licensed to run any version of 
# Account Manager. 
#
# Indemnification
# 1. Customer agrees that it shall defend, indemnify, save and hold
# CGI Script Center, Elite Web Design and marketing, and any
# persons affiliated with either company, harmless from any and all
# demands, liabilities, losses, costs and claims, including reasonable
# attorney's fees asserted against CGI Script Center, its agents, its
# customers, officers and employees, that may arise or result from any
# service provided or performed or agreed to be performed or any product # sold by customer, its agents, employees or assigns. Customer agrees to # defend, indemnify and hold harmless CGI Script Center, its # agents,  # its cusomters, officers, and employes,against
# liabilities arising out of; a) any injury to person or property caused # by an products sold or  otherwise distributed in connection with CGI
# Script Center products; (b) any material supplied by customer
# infringing or allegedly infringing on the proprietary rights of a
# third party; c) copyright infringement and (d) any defective products # sold to customer from CGI Script Center products.
#
# This program may not be distributed in whole or part, freely, for pay, # or any other form of compensation.  This program may not be offered
# by Internet Service and/or other providers to their customers, whether
# for free or compensation.  Contanct the CGI Script Center for
# commercial licensing information.
#
#################################################################
# This version designed for UNIX web servers.  If you require
# an Win32(NT/WIN95) version, please contact cgi@elitehost.com
#################################################################
##############################################################
# DO NOT EDIT BELOW THIS LINE
##############################################################

		#-- HTML 파싱
read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
@pairs = split(/&/, $buffer);
foreach $pair (@pairs) {
	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	if ($INPUT{$name}) { $INPUT{$name} = $INPUT{$name}.",".$value; }
	else { $INPUT{$name} = $value; }
      $value =~ s/<!--(.|\n)*-->//g;
}

$version = "1.05";

$cgiurl = $ENV{'SCRIPT_NAME'};

if ($INPUT{'find'}) { &find; } ######### Will search for member info.
if ($INPUT{'process'}) { &sorder; } 
#elsif ($INPUT{'order'}) { &order; }
#elsif ($INPUT{'sorder'}) {&sorder; } 
else {&sorder;}############# IF no button was pressed, run just as 
exit;

		#--- 오류메시지 출력 및 add 루틴 실행
sub sorder {
unless ($INPUT{'agree'}) {&resultMsg('회원가입 약관에 동의 하셔야 합니다.','이용약관 체크박스에 동의표시를 하신 후 다시 제출해 주세요.');}
unless ($INPUT{'fname'}) {&resultMsg('이름을 넣지 않으셨습니다.','귀하의 이름을 입력하신 후 다시 제출해 주시기 바랍니다.');}

$INPUT{'email'} =~ s/\s//g;
unless ($INPUT{'email'} =~ /(@.*@)|(\.\.)|(@\.)|(\.@)|(^\.)|(,)/ || $INPUT{'email'} !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/){
	$legalemail = 1;
} else {
	$legalemail = 0;
}

if ($legalemail !~ 1) {&resultMsg('E-Mail 오류','이메일이 누락되었거나 잘못 쓰셨습니다.');}
unless ($INPUT{'username'}) {&resultMsg('User ID를 넣지 않으셨습니다.','원하시는 로그인 ID를 입력하신 후 다시 제출해 주시기 바랍니다.');}
unless ($INPUT{'pwd'}) {&resultMsg('Password를 넣지 않으셨습니다.','Password를 입력하신 후 다시 제출해 주시기 바랍니다.');}
unless ($INPUT{'pwd'} eq $INPUT{'pwd2'} && $INPUT{'pwd'} && $INPUT{'pwd2'}) {&resultMsg('Password 불일치!','Password를 확인하신 후 다시 제출해 주시기 바랍니다.');}
unless ($INPUT{'phone'}) {&resultMsg('전화번호를 넣지 않으셨습니다.','귀하의 전화번호를 입력하신 후 다시 제출해 주시기 바랍니다.');}
unless ($INPUT{'address'}) {&resultMsg('주소를 입력하지 않으셨습니다.','귀하의 주소를 입력하신 후 다시 제출해 주시기 바랍니다.');}

&add;
}

		#--- 가입 메일을 보낸다.
sub close {

open (FILE,"$closing/email.txt"); #### Full path name from root.
@closing  = <FILE>;
close(FILE);

open (MAIL, "|$mailprog -t") || print "Can't start mail program";
    print MAIL "To: $INPUT{'email'}\n";
    print MAIL "From: $orgmail ($orgname)\n";
    print MAIL "Subject: $response_subject\n";
    print MAIL "$orgname 에 회원가입 신청을 하셨습니다.\n신청하신 결과는 관리자에게 즉시 전달되며,\n24시간이내에 귀하에게 처리결과를 발송해 드립니다.\n감사합니다.\n\n";
    print MAIL "-" x 75 . "\n\n";

    foreach $line(@closing) {print MAIL "$line";}

    print MAIL"\n\n";
    close (MAIL);
              
		#--- 관리자에게도 신규가입자가 있음을 메일로 알린다.
$firstname = $INPUT{'fname'};

open (MAIL, "|$mailprog -t") || print "Can't start mail program";
 
    print MAIL "To: $orgmail\n";
    print MAIL "From: $INPUT{'email'} ($firstname)\n";
    print MAIL "Subject: $signupresponse\n";
    print MAIL "-" x 75 . "\n\n";

    print MAIL "Customer Information\n";
    print MAIL "-" x 75 . "\n\n";
    print MAIL "Name: $INPUT{'fname'}\n";
    print MAIL "Email: $INPUT{'email'}\n\n";
    
    close (MAIL);

	&resultMsg('성공!','제출하신 자료가 사이트 관리자에게 전송되었습니다. 감사합니다.');
}

		#--- find 루틴에 사용하기 위한 email 주소 규칙 검사
sub checkaddress {

$INPUT{'email'} =~ s/\s//g;

unless ($INPUT{'email'} =~ /(@.*@)|(\.\.)|(@\.)|(\.@)|(^\.)|(,)/ || $INPUT{'email'} !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/) {
	$legalemail = 1;
} else {
	$legalemail = 0;
}

if ($legalemail !~ 1) {&resultMsg('이메일 입력 오류.','이메일이 정확하게 입력되지 않았습니다. 다시한번 시도해 주세요.');}

}

sub find {

&checkaddress;

# Open member database, read info
open (DAT,"<$memberinfo/amdata.db");
if ($LOCK_EX){ 
      flock(DAT, $LOCK_EX); #Locks the file
	}
 @database_array = <DAT>;
 close (DAT);

foreach $lines(@database_array) {
          @edit_array = split(/\:/,$lines);
         
&parseemail;


if ($edit_array[2] eq $email) {last; }

}

unless ($edit_array[2] eq $email) {&resultMsg('자료없음.','귀하의 데이타를 찾을 수 없습니다.');}

print "Content-type: text/html\n\n";
&header;
print <<MSG;
<center>
  <br>
  <table border="0" width="400">
    <tr>
      <td> 
        <p> 
        <b><font face="verdana, arial, helvetica"><font color="#FF0000">회원관리</font> <br>
        <p><font size="2">결 과 : 성공 !</font></p></b>
        <p><font size="-1" color="$fontcolor">신청 결과는 귀하의 이메일 : $INPUT{'email'} 로(으로) 전송됩니다.</font></p>
        <p><font size="-1" color="$fontcolor">회원가입에 관해 궁금하신 사항이 있으시면 <a href="mailto:$orgmail">$orgname</a>로(으로) 이메일을 주시기 바랍니다.</font></p>
        <table border="0" width="100%">
          <tr> 
            <td> 
              <hr size="1">
              <div align="right"><font size="-2" face="verdana, arial, helvetica"><a href="http://www.webweaver.pe.kr" target="_blank">Improved by JuWon,Kim</a><br>
                <a href="http://cgi.elitehost.com/" target="elite">Account Manager $version</a></font> </div>
            </td>
          </tr>
        </table>
        </font>
      </td>
    </tr>
  </table>
</center>
MSG
&footer;

open (MAIL, "|$mailprog -t") || print "Can't start mail program";
    
    print MAIL "To: $edit_array[2]\n";
    print MAIL "From: $orgmail ($orgname Support)\n";
    print MAIL "Subject: $orgname 회원관리 정보\n\n";
    #Date
    print MAIL "$date\n";
    
    # Check for Message Subject
    
    print MAIL "-" x 75 . "\n\n";
    print MAIL "귀하는 $orgname 회원관리 정보를 요청하셨습니다:\n\n";
    print MAIL "귀하가 $orgname 에서 사용하실 User ID : $edit_array[0]\n";
    print MAIL "귀하가 $orgname 에서 사용하실 패스워드 : $edit_array[1]\n\n";
    print MAIL "궁금하신 내용이 있으시면 사이트 관리자에게 메일을 주세요: $orgmail\n";
    print MAIL "$orgname 고객 지원팀\n";

    close (MAIL);
        
exit;

}

sub add {

unless ($INPUT{'username'}) {&resultMsg('User ID 에러!(누락)','다시한번 시도해 주세요.');}
if ($INPUT{'username'} =~ /\s/) {&resultMsg('User ID 에러! 공백(스페이스)을 포함할 수 없습니다.','두 단어로 입력하시려면 ( _ )를 넣고 다시 시도해 주세요.');}
if ($INPUT{'username'} eq $INPUT{'pwd'}) {&resultMsg('패스워드 에러!  User ID와 같은 패스워드는 사용하실 수 없습니다.','User ID와 다른 패스워드를 입력하시고 다시 전송해 주세요.');}

if (-e "$memberinfo/amdata.db") {
	open (MEMBER, "<$memberinfo/amdata.db");
		if ($LOCK_EX){flock(MEMBER, $LOCK_EX);}
		@database_array = <MEMBER>;
	close (MEMBER);

	foreach $lines(@database_array) {
		@edit_array = split(/\:/,$lines);
		&parseusername2;
		if (($edit_array[0]) && ($edit_array[0] eq $desiredname)) {last; }
	}

	$INPUT{'username'} =~ s/\W.*//;

	if (($edit_array[0]) && ($edit_array[0] eq $desiredname)) {&resultMsg('사용중인 User ID','다른 ID를 입력하신 후 다시 전송해 주세요.');}
}

&dupeaddress;
&dupeaddress2;
&usertemp;
&temp;
exit;
}

		#--- ID중복 검사
sub usertemp {
opendir (DIR, "$memberinfo"); 
@file = grep { /.infotmp/} readdir(DIR);
foreach $lines(@file) {
	$lines =~ s/\W.*//;
	&parseusername;
	if ($lines eq $desiredname) {&resultMsg('이미 신청된 ID!',"User ID : $INPUT{'username'} 은(는) 이미 다른 회원이 등록 신청중입니다. 다른 ID로 다시한번 시도해 보세요.");}
}
}

sub dupeaddress {

open (EMAIL, "<$memberinfo/amdata.db");
if ($LOCK_EX){ 
      flock(EMAIL, $LOCK_EX); #Locks the file
	}
@database_array = <EMAIL>;
 close (EMAIL);

foreach $lines(@database_array) {
	@edit_array = split(/\:/,$lines);
	&parseemail;

	if ($edit_array[2] eq $email) {&resultMsg('이미 사용중인 E-Mail!',"입력하신 E-mail : $INPUT{'email'} 은 이미 다른 회원이 사용하고 있습니다.");}
}
}

sub dupeaddress2 {

opendir (DIR, "$memberinfo");
close (DIR); 
@file = grep { /.infotmp/} readdir(DIR);

foreach $lines(@file) {
	open (DAT, "<$memberinfo/$lines");
	if ($LOCK_EX){flock(DAT, $LOCK_EX);} 
	@approval = <DAT>;

	foreach $item(@approval) {
		@edit_approval = split(/\:/,$item);
		&parseemail;                 
		if ($edit_approval[2] eq $email) {last; }
	}

	if ($edit_approval[2] eq $email) {&resultMsg('이미 사용중인 E-Mail!',"입력하신 E-mail : $INPUT{'email'} 은 이미 다른 회원이 사용하고 있습니다.");}
}
}

sub dupepwd {

opendir (DIR, "$memberinfo");
close (DIR); 
@file = grep { /.infotmp/} readdir(DIR);

foreach $lines(@file) {
	open (DAT, "<$memberinfo/$lines");

	if ($LOCK_EX){flock(DAT, $LOCK_EX);} 
	@approval = <DAT>;

	foreach $item(@approval) {
		@edit_approval = split(/\:/,$item);
		if ($edit_approval[1] =~ /$INPUT{'pwd'}\b/i) {last; }
	}

	if ($edit_approval[1] =~ /$INPUT{'pwd'}\b/i) {&resultMsg('이미 사용중!','입력하신 패스워드는 이미 다른 회원이 등록 신청중에 있습니다.');}
}
}

		#--- 관리자의 회원승인을 위한 임시파일 생성
sub temp {

$INPUT{'fname'} =~ s/\s+$//;
$INPUT{'lname'} =~ s/\s+$//;

$newline2 = join ("\:",$INPUT{'username'},$INPUT{'pwd'},$INPUT{'email'},$INPUT{'fname'},$INPUT{'phone'},$INPUT{'address'});
$newline2 .= "\n";

open(TEMP2, ">$memberinfo/$INPUT{'username'}.infotmp") or print "임시파일을 생성할 수 없습니다. 회원정보 디렉토리 권한을 확인해 주세요";
if ($LOCK_EX){ 
      flock(TEMP2, $LOCK_EX); #Locks the file
	}
print TEMP2 $newline2;
close (TEMP2);


if ($INPUT{$lines}) {
unlink ("$memberinfo/$lines");
}

&close;

exit;

}


sub parseusername {
$desiredname = $INPUT{'username'};
$lines =~ tr/A-Z/a-z/;
$desiredname =~ tr/A-Z/a-z/;
}

sub parseusername2 {
$desiredname = $INPUT{'username'};
$edit_array[0] =~ tr/A-Z/a-z/;
$desiredname =~ tr/A-Z/a-z/;
}


sub parseemail {
$email = $INPUT{'email'};
$edit_array[2] =~ tr/A-Z/a-z/;
$email =~ tr/A-Z/a-z/;
}


sub header {
open (FILE,"<$header/header.txt"); #### Full path name from root. 
 @headerfile = <FILE>;
 close(FILE);
print "<HTML><HEAD><TITLE></TITLE></HEAD><BODY $bodyspec>\n";
foreach $line(@headerfile) {
print "$line";
  }
}


sub footer {
open (FILE,"<$footer/footer.txt"); #### Full path name from root. 
 @footerfile = <FILE>;
 close(FILE);
foreach $line(@footerfile) {
print "$line";
}
print "</BODY></HTML>";
}

sub resultMsg {
print "Content-type: text/html\n\n";
&header;
print <<MSG;
<center>
  <br>
  <table border="0" width="400">
    <tr>
      <td> 
        <p> 
        <b><font face="verdana, arial, helvetica"><font color="#FF0000">회원관리</font> <br>
        <p><font size="2">결 과 : $_[0]</font></p></b>
        <p><font size="-1" color="$fontcolor">$_[1]</font></p>
        <p><font size="-1" color="$fontcolor">회원가입에 관해 궁금하신 사항이 있으시면 <a href="mailto:$orgmail">$orgname</a>로(으로) 이메일을 주시기 바랍니다.</font></p>
        <table border="0" width="100%">
          <tr> 
            <td> 
              <hr size="1">
              <div align="right"><font size="-2" face="verdana, arial, helvetica"><a href="http://www.webweaver.pe.kr" target="_blank">Improved by JuWon,Kim</a><br>
                <a href="http://cgi.elitehost.com/" target="elite">Account Manager $version</a></font> </div>
            </td>
          </tr>
        </table>
        </font>
      </td>
    </tr>
  </table>
</center>
MSG
&footer;
exit;
}