#!/usr/bin/perl

## ���α׷��� : AMLite 1.05
## Source : www.cgiscriptcenter.com
## ���� : ���ֿ� (webweaver@webweaver.pe.kr)
## ����ó : http://www.webweaver.pe.kr
## ������ : 2000�� 9�� 19��

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

		#-- HTML �Ľ�
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

		#--- �����޽��� ��� �� add ��ƾ ����
sub sorder {
unless ($INPUT{'agree'}) {&resultMsg('ȸ������ ����� ���� �ϼž� �մϴ�.','�̿��� üũ�ڽ��� ����ǥ�ø� �Ͻ� �� �ٽ� ������ �ּ���.');}
unless ($INPUT{'fname'}) {&resultMsg('�̸��� ���� �����̽��ϴ�.','������ �̸��� �Է��Ͻ� �� �ٽ� ������ �ֽñ� �ٶ��ϴ�.');}

$INPUT{'email'} =~ s/\s//g;
unless ($INPUT{'email'} =~ /(@.*@)|(\.\.)|(@\.)|(\.@)|(^\.)|(,)/ || $INPUT{'email'} !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/){
	$legalemail = 1;
} else {
	$legalemail = 0;
}

if ($legalemail !~ 1) {&resultMsg('E-Mail ����','�̸����� �����Ǿ��ų� �߸� ���̽��ϴ�.');}
unless ($INPUT{'username'}) {&resultMsg('User ID�� ���� �����̽��ϴ�.','���Ͻô� �α��� ID�� �Է��Ͻ� �� �ٽ� ������ �ֽñ� �ٶ��ϴ�.');}
unless ($INPUT{'pwd'}) {&resultMsg('Password�� ���� �����̽��ϴ�.','Password�� �Է��Ͻ� �� �ٽ� ������ �ֽñ� �ٶ��ϴ�.');}
unless ($INPUT{'pwd'} eq $INPUT{'pwd2'} && $INPUT{'pwd'} && $INPUT{'pwd2'}) {&resultMsg('Password ����ġ!','Password�� Ȯ���Ͻ� �� �ٽ� ������ �ֽñ� �ٶ��ϴ�.');}
unless ($INPUT{'phone'}) {&resultMsg('��ȭ��ȣ�� ���� �����̽��ϴ�.','������ ��ȭ��ȣ�� �Է��Ͻ� �� �ٽ� ������ �ֽñ� �ٶ��ϴ�.');}
unless ($INPUT{'address'}) {&resultMsg('�ּҸ� �Է����� �����̽��ϴ�.','������ �ּҸ� �Է��Ͻ� �� �ٽ� ������ �ֽñ� �ٶ��ϴ�.');}

&add;
}

		#--- ���� ������ ������.
sub close {

open (FILE,"$closing/email.txt"); #### Full path name from root.
@closing  = <FILE>;
close(FILE);

open (MAIL, "|$mailprog -t") || print "Can't start mail program";
    print MAIL "To: $INPUT{'email'}\n";
    print MAIL "From: $orgmail ($orgname)\n";
    print MAIL "Subject: $response_subject\n";
    print MAIL "$orgname �� ȸ������ ��û�� �ϼ̽��ϴ�.\n��û�Ͻ� ����� �����ڿ��� ��� ���޵Ǹ�,\n24�ð��̳��� ���Ͽ��� ó������� �߼��� �帳�ϴ�.\n�����մϴ�.\n\n";
    print MAIL "-" x 75 . "\n\n";

    foreach $line(@closing) {print MAIL "$line";}

    print MAIL"\n\n";
    close (MAIL);
              
		#--- �����ڿ��Ե� �ű԰����ڰ� ������ ���Ϸ� �˸���.
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

	&resultMsg('����!','�����Ͻ� �ڷᰡ ����Ʈ �����ڿ��� ���۵Ǿ����ϴ�. �����մϴ�.');
}

		#--- find ��ƾ�� ����ϱ� ���� email �ּ� ��Ģ �˻�
sub checkaddress {

$INPUT{'email'} =~ s/\s//g;

unless ($INPUT{'email'} =~ /(@.*@)|(\.\.)|(@\.)|(\.@)|(^\.)|(,)/ || $INPUT{'email'} !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/) {
	$legalemail = 1;
} else {
	$legalemail = 0;
}

if ($legalemail !~ 1) {&resultMsg('�̸��� �Է� ����.','�̸����� ��Ȯ�ϰ� �Էµ��� �ʾҽ��ϴ�. �ٽ��ѹ� �õ��� �ּ���.');}

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

unless ($edit_array[2] eq $email) {&resultMsg('�ڷ����.','������ ����Ÿ�� ã�� �� �����ϴ�.');}

print "Content-type: text/html\n\n";
&header;
print <<MSG;
<center>
  <br>
  <table border="0" width="400">
    <tr>
      <td> 
        <p> 
        <b><font face="verdana, arial, helvetica"><font color="#FF0000">ȸ������</font> <br>
        <p><font size="2">�� �� : ���� !</font></p></b>
        <p><font size="-1" color="$fontcolor">��û ����� ������ �̸��� : $INPUT{'email'} ��(����) ���۵˴ϴ�.</font></p>
        <p><font size="-1" color="$fontcolor">ȸ�����Կ� ���� �ñ��Ͻ� ������ �����ø� <a href="mailto:$orgmail">$orgname</a>��(����) �̸����� �ֽñ� �ٶ��ϴ�.</font></p>
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
    print MAIL "Subject: $orgname ȸ������ ����\n\n";
    #Date
    print MAIL "$date\n";
    
    # Check for Message Subject
    
    print MAIL "-" x 75 . "\n\n";
    print MAIL "���ϴ� $orgname ȸ������ ������ ��û�ϼ̽��ϴ�:\n\n";
    print MAIL "���ϰ� $orgname ���� ����Ͻ� User ID : $edit_array[0]\n";
    print MAIL "���ϰ� $orgname ���� ����Ͻ� �н����� : $edit_array[1]\n\n";
    print MAIL "�ñ��Ͻ� ������ �����ø� ����Ʈ �����ڿ��� ������ �ּ���: $orgmail\n";
    print MAIL "$orgname �� ������\n";

    close (MAIL);
        
exit;

}

sub add {

unless ($INPUT{'username'}) {&resultMsg('User ID ����!(����)','�ٽ��ѹ� �õ��� �ּ���.');}
if ($INPUT{'username'} =~ /\s/) {&resultMsg('User ID ����! ����(�����̽�)�� ������ �� �����ϴ�.','�� �ܾ�� �Է��Ͻ÷��� ( _ )�� �ְ� �ٽ� �õ��� �ּ���.');}
if ($INPUT{'username'} eq $INPUT{'pwd'}) {&resultMsg('�н����� ����!  User ID�� ���� �н������ ����Ͻ� �� �����ϴ�.','User ID�� �ٸ� �н����带 �Է��Ͻð� �ٽ� ������ �ּ���.');}

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

	if (($edit_array[0]) && ($edit_array[0] eq $desiredname)) {&resultMsg('������� User ID','�ٸ� ID�� �Է��Ͻ� �� �ٽ� ������ �ּ���.');}
}

&dupeaddress;
&dupeaddress2;
&usertemp;
&temp;
exit;
}

		#--- ID�ߺ� �˻�
sub usertemp {
opendir (DIR, "$memberinfo"); 
@file = grep { /.infotmp/} readdir(DIR);
foreach $lines(@file) {
	$lines =~ s/\W.*//;
	&parseusername;
	if ($lines eq $desiredname) {&resultMsg('�̹� ��û�� ID!',"User ID : $INPUT{'username'} ��(��) �̹� �ٸ� ȸ���� ��� ��û���Դϴ�. �ٸ� ID�� �ٽ��ѹ� �õ��� ������.");}
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

	if ($edit_array[2] eq $email) {&resultMsg('�̹� ������� E-Mail!',"�Է��Ͻ� E-mail : $INPUT{'email'} �� �̹� �ٸ� ȸ���� ����ϰ� �ֽ��ϴ�.");}
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

	if ($edit_approval[2] eq $email) {&resultMsg('�̹� ������� E-Mail!',"�Է��Ͻ� E-mail : $INPUT{'email'} �� �̹� �ٸ� ȸ���� ����ϰ� �ֽ��ϴ�.");}
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

	if ($edit_approval[1] =~ /$INPUT{'pwd'}\b/i) {&resultMsg('�̹� �����!','�Է��Ͻ� �н������ �̹� �ٸ� ȸ���� ��� ��û�߿� �ֽ��ϴ�.');}
}
}

		#--- �������� ȸ�������� ���� �ӽ����� ����
sub temp {

$INPUT{'fname'} =~ s/\s+$//;
$INPUT{'lname'} =~ s/\s+$//;

$newline2 = join ("\:",$INPUT{'username'},$INPUT{'pwd'},$INPUT{'email'},$INPUT{'fname'},$INPUT{'phone'},$INPUT{'address'});
$newline2 .= "\n";

open(TEMP2, ">$memberinfo/$INPUT{'username'}.infotmp") or print "�ӽ������� ������ �� �����ϴ�. ȸ������ ���丮 ������ Ȯ���� �ּ���";
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
        <b><font face="verdana, arial, helvetica"><font color="#FF0000">ȸ������</font> <br>
        <p><font size="2">�� �� : $_[0]</font></p></b>
        <p><font size="-1" color="$fontcolor">$_[1]</font></p>
        <p><font size="-1" color="$fontcolor">ȸ�����Կ� ���� �ñ��Ͻ� ������ �����ø� <a href="mailto:$orgmail">$orgname</a>��(����) �̸����� �ֽñ� �ٶ��ϴ�.</font></p>
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