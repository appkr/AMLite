#!/usr/bin/perl

## 프로그램명 : AMLite 1.05
## Source : www.cgiscriptcenter.com
## 수정 : 김주원 (webweaver@webweaver.pe.kr)
## 배포처 : http://www.webweaver.pe.kr
## 배포일 : 2000년 9월 19일

############################################
##                                        ##
##   Account Manager LITE Administration  ##
##          by CGI Script Center          ##
##       (e-mail cgi@elitehost.com)       ##
##                                        ##
##             version:  1.05             ##
##         last modified:  11/02/98       ##
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
# COPYRIGHT NOTICE:
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
# This version designed for UNIX servers.  If you require
# a Win32(NT/Win95) version, please visit: http://cgi.elitehost.com
#################################################################
#
#################################################################
# VERSION INFORMATION
#################################################################
#
# Version 1.01 - Bug Fix - 05/31/98
# Left an extra mailing routine in the accntman.pl file by mistake.
# It was sending those that signed up two sents of confirmation
# messages.  Removed the extra mailing routine.
#
# Responses on some flavors of UNIX servers were adding extra
# domain names to the name of the mail sender.  This was sending
# emails to the wrong persons.  Switch the Name and the Email 
# address on the mailing routines to stop this from happening.
#
# Version 1.02 - Bug Fix - 06/08/98
# "Denied" email text file not being read and thus not printing
# on the email of the denied accounts.  Bug squashed.
#
# Version 1.03 - Bug Fix - 06/11/98
# The Account Finder email was not placing the subject in the
# subject line.  Fixed.
#
# Version 1.04 - Bug Fix - 08/27/98
# When trying to approve or deny individuals, using the DETAILS
# portion of the amadmin.pl program, every waiting account was
# approved or denied, respectively.  Bug found... squashed.
#
# Version 1.05 - Bug Fix - 11/02/98
# It appears the checking routines we were using were confusing
# some email addresses and passwords, thus causing members with
# similar passwords and email addresses to have problems.
#
# We have rewritten the entire checking system, and make it very
# specific.  Bug squashed.
#
# We also had a problem with users using multi-word usernames.
# We've added a checking routine that will notify the user that
# if they would like a multi-word username, they will need to use
# a dash or underscore between words.  Bug squashed.
#
# Created only one page of configurations, now called config.pl.
# You no longer need to edit anything in either the acctman.pl
# or the amadmin.pl files, except for the "require" line
# near the top of each script.  This tells the programs where
# to find their configurations.
#
#########################################################
# DO NOT EDIT BELOW THIS LINE
#########################################################
#########################################################

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


$cgiurl = $ENV{'SCRIPT_NAME'};

# Define arrays for the day of the week and month of the year.           #
    @days   = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday');
    @months = ('January','February','March','April','May','June','July','August','September','October','November','December');

    # Get the current time and format the hour, minutes and seconds.  Add    #
    # 1900 to the year to get the full 4 digit year.                         #
    ($sec,$min,$hour,$mday,$mon,$year,$wday) = (localtime(time))[0,1,2,3,4,5,6];
    $time = sprintf("%02d:%02d:%02d",$hour,$min,$sec);
    $year += 1900;

    # Format the date.                                                       #
    $date = "$days[$wday], $months[$mon] $mday, $year at $time";
    $date2 = "$days[$wday], $months[$mon] $mday, $year";
    $month = "$months[$mon]";

    $version = "1.05";

if ($INPUT{'awaiting'}) {&awaiting; }
elsif ($INPUT{'process'}) {&process; }
elsif ($INPUT{'indapprove'}) {&indapprove; }
elsif ($INPUT{'inddeny'}) {&inddeny; }
elsif ($INPUT{'deny'}) {&process; }
elsif ($INPUT{'approve'}) {&process; }
elsif ($INPUT{'active'}) {&active; }
elsif ($INPUT{'adelete'}) {&adelete; }
elsif ($INPUT{'processac'}) {&processac; }
elsif ($INPUT{'processch'}) {&processch; }
elsif ($INPUT{'update'}) {&update; }
elsif ($INPUT{'search'}) {&search; }
elsif ($INPUT{'ambill'}) {&ambill; }
elsif ($INPUT{'admin'}) {&admin; }
elsif ($INPUT{'admin2'}) {&admin2; }
elsif ($INPUT{'processsearch'}) {&processsearch; }
elsif ($INPUT{'areyousure'}) {&areyousure; }
elsif ($INPUT{'mmailform'}) {&mmailform; }
elsif ($INPUT{'mmail'}) {&mmail; }
elsif ($INPUT{'setpwd'}) {&setpwd; }
elsif ($INPUT{'passcheck'}) {&passcheck; }
elsif ($INPUT{'payhist'}) {&payhist; }
else {&admin; }#### Run the Administration panel


sub read {

#################################
# Users Awaiting Approval
#################################

opendir (DIR, "$memberinfo");
@file = grep { /.infotmp/} readdir(DIR);
close (DIR); 

$new_files = push(@file);

#################################
# Active Members
#################################

open (DAT, "<$memberinfo/amdata.db");
if ($LOCK_EX){ 
      flock(DAT, $LOCK_EX); #Locks the file
	}
@active = <DAT>;
$count = 0;
foreach $lines(@active) {
          $count++;

} 
close (DAT);
}

sub admin {

print "Content-type: text/html\n\n";
unless (-e "$passfile/password.txt") {

&setpassword;
}

&adminpass;
}

		#--- 관리자 패스워드 입력폼 출력
sub adminpass {

&header;
print<<EOF;
<form action="$cgiurl" method="POST">
  <center>
    <br>
    <table border="0" width="400">
      <tr>
        <td>
          <p align="CENTER"><b><font face="verdana, arial, helvetica"><font color="#FF0000">회원관리</font> : 관리자 패스워드</font></b></p>
          <p align="center"><font size="-1" face="verdana, arial, helvetica">관리자 패스워드를 입력하여 주십시오.</font></p>
          <table border="0" align="center">
            <tr> 
              <td align="CENTER"><font size="-1" face="verdana, arial, helvetica"><b>패스워드</b></font><br>
                <input type="PASSWORD" name="pwd">
              </td>
            </tr>
            <tr> 
              <td align="CENTER" colstart="1"><br>
                <input type="SUBMIT" name="passcheck" value=" 패스워드 전송 "><input type="RESET" name="Input">
              </td>
            </tr>
          </table>
          <table border="0" width="400">
            <tr>
              <td colstart="1"><hr size="1"></td>
            </tr>
            <tr> 
              <td align="RIGHT" colstart="1"> <font size="-2" face="Verdana, Arial, Helvetica, sans-serif"><a href="http://www.webweaver.pe.kr" target="_blank"><b>Improved by JuWon,Kim</b></a><br>
                <a href="http://cgi.elitehost.com/" target="elite"><b>Account Manager LITE $version</b></a></font></td>
            </tr>
          </table>
          </td>
      </tr>
    </table>
  </center>
</form>

EOF
&footer;
exit;
}

		#--- 패스워드 대조
sub passcheck {

open (PASSWORD, "$passfile/password.txt");
           if ($LOCK_EX){ 
      flock(PASSWORD, $LOCK_EX); #Locks the file
	}
		$password = <PASSWORD>;
		close (PASSWORD);
		chop ($password) if ($password =~ /\n$/);


		if ($INPUT{'pwd'}) {
			$newpassword = crypt($INPUT{'pwd'}, aa);
		}
		else {&resultMsg ('Password Error!','패스워드를 입력해 주세요!');}
		unless ($newpassword eq $password) {&resultMsg ('Password Error!','패스워드 불일치!  다시한번 시도해 주세요.');}
&admin2;
}


sub admin2 {
&read;
print "Content-type: text/html\n\n";
&header;
print<<EOF; 

<center>
  <table border="1" width="450" cellpadding="5">
    <tr>
      <td align="CENTER" colspan="2" colstart="1"><b><font size="-2" face="verdana, arial, helvetica">CGI Script Center's</font><br><font size="-1" face="verdana, arial, helvetica" color="#FF0000">Account Manager LITE $version</font></b></td>
    </tr>
    <tr>
      <td valign="MIDDLE" align="CENTER" width="50%" bgcolor="#C0C0C0" rowspan="2" colstart="1"><font size="+1" face="verdana, arial, helvetica"><b>Main Menu</b></font></td>
      <td valign="MIDDLE" align="LEFT" width="50%" bgcolor="#C0C0C0" colstart="2"><font size="-2" face="verdana, arial, helvetica" color="#000000"><b>Active Users (회원): <font color="#0000FF">$count</font></b></font></td>
    </tr>
    <tr>
      <td valign="MIDDLE" align="LEFT" bgcolor="#C0C0C0" colstart="2"><font size="-2" face="verdana, arial, helvetica" color="#000000"><b>Awaiting Approval(대기자): <font color="#0000FF">$new_files</font></b></font></td>
    </tr>
  </table>
  <br>
</center>
<form action="$cgiurl" method="POST">
  <center>
    <table border="1" width="450" cellpadding="5">
      <tr>
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><input type="SUBMIT" value=" 실 행 " name="awaiting"></td>
        <td valign="MIDDLE" align="LEFT" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>Add/Delete Awaiting Approval Accounts<br>(등록 대기 회원 등록/삭제) </b></font></td>
      </tr>
      <tr>
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><input type="SUBMIT" value=" 실 행 " name="active"></td>
        <td valign="MIDDLE" align="LEFT" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>View/Delete/Edit Active Users<br>(회원리스트/삭제/수정) </b></font></td>
      </tr>
      <tr>
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><input type="SUBMIT" value=" N/A " name="search"></td>
        <td valign="MIDDLE" align="LEFT" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>Search for User by Username/Password<br>(배포버전에선 사용할 수 없음) </b></font></td>
      </tr>
      <tr>
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><input type="SUBMIT" value=" N/A " name="areyousure"></td>
        <td valign="MIDDLE" align="LEFT" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>E-mail all customer bills now<br>(배포버전에선 사용할 수 없음) </b></font></td>
      </tr>
      <tr>
        <td valign="MIDDLE" align="CENTER" colstart="1" bgcolor="#C0C0C0"><input type="SUBMIT" value=" N/A " name="mmailform"></td>
        <td colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>Mass Mail all users<br>(배포버전에선 사용할 수 없음) </b></font></td>
      </tr>
    </table>
  </center>
</form>
<center>
  <table border="0" width="450">
    <tr>
      <td colstart="1"><hr size="1" width="450"></td>
    </tr>
    <tr>
      <td valign="TOP" align="right" colstart="1"> <font size="-2" face="Verdana, Arial, Helvetica, sans-serif"><a href="http://www.webweaver.pe.kr" target="_blank">Improved by JuWon,Kim</a><br>
        <a href="http://cgi.elitehost.com/" target="elite"> Account Manager LITE $version</a></font></td>
    </tr>
  </table>
</center>

EOF
&footer;
exit;
}


sub awaiting {

&read;

opendir (DIR, "$memberinfo"); 
@file = grep { /.infotmp/} readdir(DIR);

print "Content-type: text/html\n\n";
&header;
print <<EOF;

<center>
  <table border="1" width="500" cellpadding="5">
    <tr>
      <td align="CENTER" colspan="2" colstart="1"><b><font size="-2" face="verdana, arial, helvetica">CGI Script Center's</font><br>
        <font size="-1" face="verdana, arial, helvetica" color="#FF0000">Account Manager LITE $version</font></b></td>
    </tr>
    <tr>
      <td valign="MIDDLE" align="CENTER" width="50%" bgcolor="#C0C0C0" rowspan="2" colstart="1"><font size="+1" face="verdana, arial, helvetica"><b>Awaiting Approval</b></font></td>
      <td valign="MIDDLE" align="LEFT" width="50%" bgcolor="#C0C0C0" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b><font color="#000000">Active Users(회원): <font color="#0000FF">$count</font></font></b></font></td>
    </tr>
    <tr>
      <td valign="MIDDLE" align="LEFT" bgcolor="#C0C0C0" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b><font color="#000000">Awaiting Approval(대기자): 
        <font color="#0000FF">$new_files</font></font></b></font></td>
    </tr>
  </table>
  <br>
</center>
<form action="$cgiurl" method="POST">
  <center>
    <table border="1" width="500" cellpadding="5">
      <tr>
        <td align="CENTER" nowrap width="40" bgcolor="#C0C0C0" colstart="1"><font size="-2" face="verdana, arial, helvetica"><b>Approve</b></font></td>
        <td align="CENTER" width="40" bgcolor="#C0C0C0" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>Deny</b></font></td>
        <td align="CENTER" width="40" bgcolor="#C0C0C0" colstart="3"><font size="-2" face="verdana, arial, helvetica"><b>Details</b></font></td>
        <td align="CENTER" bgcolor="#C0C0C0" colstart="4"><font size="-2" face="verdana, arial, helvetica"><b>Name</b></font></td>
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="5"><font size="-2" face="verdana, arial, helvetica"><b>Username</b></font></td>
      </tr>

EOF
foreach $lines(@file) {
open (DAT, "<$memberinfo/$lines");
if ($LOCK_EX){ 
      flock(DAT, $LOCK_EX); #Locks the file
	} 
      @approval = <DAT>;
      close (DAT);
      close (DIR); 

        foreach $item(@approval) {
	
             @edit_approval = split(/\:/,$item);      
             print <<EOF;
      <TR>
        <TD VALIGN="MIDDLE" ALIGN="CENTER" COLSTART="1"><INPUT TYPE="RADIO" NAME="$edit_approval[0].infotmp" VALUE="approve"></TD>
        <TD VALIGN="MIDDLE" ALIGN="CENTER" COLSTART="2"><INPUT TYPE="RADIO" NAME="$edit_approval[0].infotmp" VALUE="deny"></TD>
        <TD VALIGN="MIDDLE" ALIGN="CENTER" COLSTART="3"><INPUT TYPE="RADIO" NAME="$edit_approval[0].infotmp" VALUE="details"></TD>
        <TD VALIGN="MIDDLE" ALIGN="LEFT" COLSTART="4"><A HREF="mailto:$edit_approval[2]"><FONT SIZE="-2" FACE="verdana, arial, helvetica">$edit_approval[3] $edit_approval[4]</FONT></A></TD>
        <TD VALIGN="MIDDLE" ALIGN="LEFT" COLSTART="5"><FONT SIZE="-2" FACE="verdana, arial, helvetica">$edit_approval[0]</FONT></TD>
      </TR>
EOF

}

}
print<<EOF;
    </TABLE>
  </CENTER>
<hr size="1" width="500">
<center>
  <table border="1" width="500">
    <tr>
      <td valign="MIDDLE" align="CENTER" width="50%" bgcolor="#C0C0C0" colstart="1">
        <input type="SUBMIT" name="process" value="   Process   "><input type="RESET" name="Input">
      </td>
      <td align="CENTER" width="50%" bgcolor="#C0C0C0" colstart="2"><font size="-1" face="verdana, arial, helvetica"><b>Awaiting Approval</b></font><br>
        <font size="-2" face="verdana, arial, helvetica">Approve/Deny</font></td>
    </tr>
  </table>
</center>
<hr size="1" width="500">
<center>
  <table border="1" width="500">
    <tr>
      <td valign="MIDDLE" align="CENTER" width="50%" bgcolor="#C0C0C0" colstart="1"><input type="SUBMIT" value="Main Menu Return" name="admin2"></td>
      <td valign="MIDDLE" align="CENTER" width="50%" bgcolor="#C0C0C0" colstart="2"><font size="-1" face="verdana, arial, helvetica"><b>Main Menu Return</b></font></td>
    </tr>
  </table>
</center>
<center>
  <table border="0" width="500">
    <tr>
      <td colstart="1"><hr size="1" width="500"></td>
    </tr>
    <tr>
      <td valign="TOP" align="right" colstart="1"> <font size="-2" face="Verdana, Arial, Helvetica, sans-serif"><a href="http://www.webweaver.pe.kr" target="_blank">Improved by JuWon,Kim</a><br>
        <a href="http://cgi.elitehost.com/" target="elite"> Account Manager LITE $version</a></font></td>
    </tr>
  </table>
</center>
EOF
&footer;
exit;
}

sub process {

opendir (DIR, "$memberinfo"); 
@file = grep { /.infotmp/} readdir(DIR);

foreach $lines(@file) {
	if ($INPUT{$lines} eq details) {
		&read;
		open (DAT, "<$memberinfo/$lines");
		if ($LOCK_EX){ flock(DAT, $LOCK_EX);} 
		@array = <DAT>;
		close (DAT);
close (DIR); 

foreach $item(@array) {
	@edit_array = split(/\:/,$item);
}
print "Content-type: text/html\n\n";
&header;
print<<EOF;

<center>
  <table border="1" width="500" cellpadding="5">
    <tr>
      <td align="CENTER" colspan="2" colstart="1"><b><font size="-2" face="verdana, arial, helvetica">CGI Script Center's</font><br>
        <font size="-1" face="verdana, arial, helvetica" color="#FF0000">Account Manager LITE $version</font></b></td>
    </tr>
    <tr>
      <td valign="MIDDLE" align="CENTER" width="50%" bgcolor="#C0C0C0" rowspan="2" colstart="1"><font size="+1" face="verdana, arial, helvetica"><b>Awaiting Approval</b></font><br>
        <font size="-2" face="verdana, arial, helvetica">User Details</font></td>
      <td valign="MIDDLE" align="LEFT" width="50%" bgcolor="#C0C0C0" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b><font color="#000000">Active Users: 
        <font color="#0000FF">$count</font></font></b></font></td>
    </tr>
    <tr>
      <td valign="MIDDLE" align="LEFT" bgcolor="#C0C0C0" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b><font color="#000000">Awaiting Approval: 
        <font color="#0000FF">$new_files</font></font></b></font></td>
    </tr>
  </table>
  <br>
</center>
<form action="$cgiurl" method="POST">
  <input type="HIDDEN" name="marker" value="$edit_array[0]">
  <center>
    <table border="1" width="500">
      <tr>
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><font size="+1" face="verdana, arial, helvetica"><b>User Approval Details</b></font></td>
      </tr>
    </table>
    <br>
    <table border="1" width="500" cellpadding="5">
      <tr> 
        <td align="CENTER" colspan="3" height="0" bgcolor="#C0C0C0" colstart="1"><b><font size="-2" face="verdana, arial, helvetica">$edit_array[3]</font> </b></td>
      </tr>
      <tr> 
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><font size="-2" face="verdana, arial, helvetica"><b>이 름</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>$edit_array[3]</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="3"> 
          <input type="TEXT" size="9" name="fname">
        </td>
      </tr>
      <tr> 
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><font size="-2" face="verdana, arial, helvetica"><b>E-mail </b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>$edit_array[2]</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="3"> 
          <input type="TEXT" size="9" name="email">
        </td>
      </tr>
      <tr> 
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><font size="-2" face="verdana, arial, helvetica"><b>주 소</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>$edit_array[5]</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="3"> 
          <input type="TEXT" size="9" name="address">
        </td>
      </tr>
      <tr> 
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><font size="-2" face="verdana, arial, helvetica"><b>전 화</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>$edit_array[4]</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="3"> 
          <input type="TEXT" size="9" name="phone">
        </td>
      </tr>
      <tr> 
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><font size="-2" face="verdana, arial, helvetica"><b>Login ID</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>$edit_array[0]</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="3"> 
          <input type="TEXT" size="9" name="username">
        </td>
      </tr>
      <tr> 
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><font size="-2" face="verdana, arial, helvetica"><b>Password</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>$edit_array[1]</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="3"> 
          <input type="TEXT" size="9" name="password">
        </td>
      </tr>
    </table>
  </center>
</form>


EOF


print<<EOF;
</TR></TABLE></CENTER>
<hr size="1" width="500">
<center>
  <table border="1" width="500">
    <tr>
      <td valign="MIDDLE" align="CENTER" width="50%" bgcolor="#C0C0C0" colstart="1">
        <input type="SUBMIT" name="indapprove" value="Approve Account">
        <input type="SUBMIT" name="inddeny" value="Deny Account">
      </td>
      <td align="CENTER" width="50%" bgcolor="#C0C0C0" colstart="2"><font size="+1" face="verdana, arial, helvetica"><b><font size="-1">Awaiting Approval</font></b></font><br>
        <font size="-2" face="verdana, arial, helvetica">User Details</font></td>
    </tr>
  </table>
</center>
EOF

print<<EOF;

<hr size="1" width="500">
<center>
  <table border="1" width="500">
    <tr>
      <td valign="MIDDLE" align="CENTER" width="50%" bgcolor="#C0C0C0" colstart="1">
        <input type="SUBMIT" name="admin2" value="Main Menu Return">
      </td>
      <td valign="MIDDLE" align="CENTER" width="50%" bgcolor="#C0C0C0" colstart="2"><font size="-1" face="verdana, arial, helvetica"><b>Main Menu Return</b></font></td>
    </tr>
  </table>
</center>
<center>
  <table border="0" width="500">
    <tr>
      <td colstart="1">
        <hr size="1" width="500">
      </td>
    </tr>
    <tr>
      <td valign="TOP" align="right" colstart="1"> <font size="-2" face="Verdana, Arial, Helvetica, sans-serif"><a href="http://www.webweaver.pe.kr" target="_blank">Improved by JuWon,Kim</a></font><font size="-2" face="Verdana, Arial, Helvetica, sans-serif"><br>
        <a href="http://cgi.elitehost.com/" target="elite"> Account Manager LITE $version</a></font></td>
    </tr>
  </table>
</center>

EOF
exit;
}


      if (($INPUT{$lines} eq deny) || ($INPUT{'deny'})) {
      open (DAT, "<$memberinfo/$lines");
if ($LOCK_EX){ 
      flock(DAT, $LOCK_EX); #Locks the file
	} 
      @approval = <DAT>;
      close (DAT);
      close (DIR); 
        foreach $item(@approval) {
             @edit_approval = split(/\:/,$item);      

      open (FILE,"$memberinfo/denied.txt"); #### Full path name from root.
if ($LOCK_EX){ 
      flock(FILE, $LOCK_EX); #Locks the file
	} 
 @denied_email_file  = <FILE>;
 close(FILE);

open (MAIL, "|$mailprog -t")
	            || print "Can't start mail program";
    
    print MAIL "To: $edit_approval[2]\n";
    print MAIL "From: $orgmail\n";
    print MAIL "Subject: $denied_email_subject\n";
    #Date
    print MAIL "죄송합니다.\n귀하의 $orgname 회원가입이 거부되었습니다.\n더 자세한 정보를 원하시면 $orgmail 로 연락주십시오.\n감사합니다.\n";
    print MAIL "$date\n";
    
    print MAIL "-" x 75 . "\n\n";

    foreach $line(@denied_email_file) {
    print MAIL "$line";
    }
    print MAIL"\n\n";
    close (MAIL);
    unlink ("$memberinfo/$lines");

        }
}

      if (($INPUT{$lines} eq approve) || ($INPUT{'approve'})) {
      open (FILE, "<$memberinfo/$lines");
if ($LOCK_EX){ 
      flock(FILE, $LOCK_EX); #Locks the file
	}
      @approved = <FILE>;
      close (FILE);
      foreach $item(@approved) {
             
         open(DATABASE, ">>$memberinfo/amdata.db") or print"unable to create access temp file";
         if ($LOCK_EX){ 
      flock(DATABASE, $LOCK_EX); #Locks the file
	}
         chomp($item);
         print DATABASE "$item\n";

           if ($htaccess == "1") {
           open (DAT2, "<$memberinfo/$lines");
if ($LOCK_EX){ 
      flock(DAT2, $LOCK_EX); #Locks the file
	} 
           @second = <DAT2>;
           close (DAT2);
                foreach $item(@second) {
                @edit_second = split(/\:/,$item);
                chop ($edit_second[1]) if ($edit_second[1] =~ /\n$/);
		    $newpassword = crypt($edit_second[1], aa); 
                open(PASSWD, ">>$memaccess") or print"unable to create access temp file";
                print PASSWD "$edit_second[0]:$newpassword\n";
   }

close (PASSWD);


 }
close (DATABASE);
}

open (FILE, "<$memberinfo/$lines");
if ($LOCK_EX){ 
      flock(FILE, $LOCK_EX); #Locks the file
	}
       @approved = <FILE>;
       close (FILE);
       foreach $item(@approved) {

             @edit_approved = split(/\:/,$item);      



      #$tempfile = "$tempdir/$edit_approved[2]";      
      
      open (FILE,"$memberinfo/approved.txt"); #### Full path name from root.
if ($LOCK_EX){ 
      flock(FILE, $LOCK_EX); #Locks the file
	}
 @approved_email_file  = <FILE>;
 close(FILE);

open (MAIL, "|$mailprog -t")
	            || print "Can't start mail program";
    
    print MAIL "To: $edit_approved[2]\n";
    print MAIL "From: $orgmail\n";
    print MAIL "Subject: $approved_email_subject\n";
    #Date
    print MAIL "귀하께서는 $orgname 회원으로 승인 되셨습니다.\n회원가입에 대해 궁금한 내용은 $orgmail로 문의해 주십시오.\n\n";
    print MAIL "$date\n";
    

    print MAIL "-" x 75 . "\n\n";

    foreach $line(@approved_email_file) {
    print MAIL "$line";
    }
    print MAIL"\n\n";
    close (MAIL);
    unlink ("$memberinfo/$lines");
        }
unlink ("$memberinfo/$lines");


}

if ($INPUT{$lines}) {
unlink ("$memberinfo/$lines");

}

}
{&read; &admin2; }#### 

}

sub indapprove {

      
open (FILE, "<$memberinfo/$INPUT{'marker'}.infotmp");
if ($LOCK_EX){ 
      flock(FILE, $LOCK_EX); #Locks the file
	}
      @approved = <FILE>;
      close (FILE);

open(DATABASE, ">>$memberinfo/amdata.db") or print"unable to create access temp file";
         if ($LOCK_EX){ 
      flock(DATABASE, $LOCK_EX); #Locks the file
	}
         chomp @approved;
         print DATABASE "@approved\n";

if ($htaccess == "1") {
           
                foreach $item(@approved) {
                @edit_approved = split(/\:/,$item);
                chop ($edit_approved[1]) if ($edit_approved[1] =~ /\n$/);
		    $newpassword = crypt($edit_approved[1], aa); 
                open(PASSWD, ">>$memaccess") or print"unable to create access temp file";
                print PASSWD "$edit_approved[0]:$newpassword\n";
   }

close (PASSWD);


 }
close (DATABASE);

open (FILE, "<$memberinfo/$INPUT{'marker'}.infotmp");
if ($LOCK_EX){ 
      flock(FILE, $LOCK_EX); #Locks the file
	}
       @approved = <FILE>;
       close (FILE);
       foreach $item(@approved) {
             @edit_approved = split(/\:/,$item);      

      open (FILE,"$memberinfo/approved.txt"); #### Full path name from root.
if ($LOCK_EX){ 
      flock(FILE, $LOCK_EX); #Locks the file
	}
 @approved_email_file  = <FILE>;
 close(FILE);

    open (MAIL, "|$mailprog -t")
	            || print "Can't start mail program";
    
    print MAIL "To: $edit_approved[2]\n";
    print MAIL "From: $orgmail\n";
    print MAIL "Subject: $approved_email_subject\n";
    #Date
    print MAIL "귀하께서는 $orgname 회원으로 승인 되셨습니다.\n회원가입에 대해 궁금한 내용은 $orgmail로 문의해 주십시오.\n\n";
    print MAIL "$date\n";
    
    # Check for Message Subject
    
    print MAIL "-" x 75 . "\n\n";

    foreach $line(@approved_email_file) {
    print MAIL "$line";
    }
    print MAIL"\n\n";
    close (MAIL);

        unlink ("$memberinfo/$edit_approved[0].infotmp");
        }
unlink ("$memberinfo/$edit_approved[0].infotmp");

{&read; &admin2; }#### 
}

if ($INPUT{$lines}) {
unlink ("$memberinfo/$lines");
}


sub inddeny {

      open (DAT, "<$memberinfo/$INPUT{'marker'}.infotmp");
if ($LOCK_EX){ 
      flock(DAT, $LOCK_EX); #Locks the file
	} 
      @approval = <DAT>;
      close (DAT);
      close (DIR); 
        foreach $item(@approval) {
             @edit_approval = split(/\:/,$item);      

      open (FILE,"$memberinfo/denied.txt"); #### Full path name from root.
if ($LOCK_EX){ 
      flock(FILE, $LOCK_EX); #Locks the file
	} 
 @denied_email_file  = <FILE>;
 close(FILE);

# Output a temporary file

    open (MAIL, "|$mailprog -t")
	            || print "Can't start mail program";
    
    print MAIL "To: $edit_approval[2]\n";
    print MAIL "From: $orgmail\n";
    print MAIL "Subject: $denied_email_subject\n";
    #Date
    print MAIL "죄송합니다.\n귀하의 $orgname 회원가입이 거부되었습니다.\n더 자세한 정보를 원하시면 $orgmail 로 연락주십시오.\n감사합니다.\n\n";
    print MAIL "$date\n";
    
    
    
    print MAIL "-" x 75 . "\n\n";

    foreach $line(@denied_email_file) {
    print MAIL "$line";
    }
    print MAIL"\n\n";
    close (MAIL);

 
        unlink ("$memberinfo/$INPUT{'marker'}.infotmp");
        }

{&read; &admin2; }#### 
}

#########################################
# ACTIVE USERS ##########################
#########################################

sub active {
&read;
open (DAT,"<$memberinfo/amdata.db");
if ($LOCK_EX){ 
      flock(DAT, $LOCK_EX); #Locks the file
	}
 @database_array = <DAT>;
 close (DAT);

print "Content-type: text/html\n\n";
&header;
print <<EOF;
<CENTER><TABLE
BORDER="1" WIDTH="500" CELLPADDING="5"><TBODY><COLDEFS><COLDEF><COLDEF></COLDEFS>
<ROWS><TR><TD ALIGN="CENTER" COLSPAN="2" COLSTART="1"><B><FONT
SIZE="-2" FACE="verdana, arial, helvetica">CGI Script Center's</FONT><BR><FONT
SIZE="-1" FACE="verdana, arial, helvetica" COLOR="#FF0000">Account Manager LITE 
$version</FONT></B></TD></TR><TR><TD
VALIGN="MIDDLE" ALIGN="CENTER" WIDTH="50%" BGCOLOR="#C0C0C0" ROWSPAN="2" COLSTART="1"><FONT
SIZE="+1" FACE="verdana, arial, helvetica"><B>Active Users</B></FONT><BR><FONT
SIZE="-2" FACE="verdana, arial, helvetica">View/Edit/Delete</FONT></TD><TD
VALIGN="MIDDLE" ALIGN="LEFT" WIDTH="50%" BGCOLOR="#C0C0C0" COLSTART="2"><FONT
SIZE="-2" FACE="verdana, arial, helvetica"><B><FONT COLOR="#000000">Active
Users: <FONT COLOR="#0000FF">$count</FONT></FONT></B></FONT></TD></TR><TR><TD
VALIGN="MIDDLE" ALIGN="LEFT" BGCOLOR="#C0C0C0" COLSTART="2"><FONT
SIZE="-2" FACE="verdana, arial, helvetica"><B><FONT COLOR="#000000">Awaiting
Approval:  <FONT COLOR="#0000FF">$new_files</FONT></FONT></B></FONT></TD></TR></ROWS></TBODY></TABLE><BR></CENTER>
<FORM ACTION="$cgiurl" METHOD="POST"><CENTER><TABLE
BORDER="1" WIDTH="500" CELLPADDING="5"><TBODY><COLDEFS><COLDEF><COLDEF><COLDEF>
<COLDEF></COLDEFS><ROWS><TR><TD
ALIGN="CENTER" NOWRAP="NOWRAP" WIDTH="40" BGCOLOR="#C0C0C0" COLSTART="1"><FONT
SIZE="-2" FACE="verdana, arial, helvetica"><B>Update</B></FONT></TD><TD
ALIGN="CENTER" WIDTH="40" BGCOLOR="#C0C0C0" COLSTART="2"><FONT
SIZE="-2" FACE="verdana, arial, helvetica"><B>Delete</B></FONT></TD><TD
ALIGN="CENTER" BGCOLOR="#C0C0C0" COLSTART="3"><FONT
SIZE="-2" FACE="verdana, arial, helvetica"><B>Name</B></FONT></TD><TD
VALIGN="MIDDLE" ALIGN="CENTER" BGCOLOR="#C0C0C0" COLSTART="4"><FONT
SIZE="-2" FACE="verdana, arial, helvetica"><B>User ID</B></FONT></TD></TR>
EOF

foreach $lines(@database_array) {
          @edit_array = split(/\:/,$lines);
print<<EOF;
<TR><TD
 VALIGN="MIDDLE" ALIGN="CENTER" COLSTART="1"><INPUT
TYPE="RADIO" VALUE="$edit_array[0]" NAME="update"></TD><TD
VALIGN="MIDDLE" ALIGN="CENTER" COLSTART="2"><INPUT
TYPE="RADIO" VALUE="adelete" NAME="$edit_array[0]"></TD><TD
VALIGN="MIDDLE" ALIGN="LEFT" COLSTART="3"><A HREF="mailto:$edit_array[2]"><FONT
SIZE="-2" FACE="verdana, arial, helvetica">$edit_array[3]</FONT></A></TD>
<TD VALIGN="MIDDLE" ALIGN="CENTER" COLSTART="4"><FONT
SIZE="-2" FACE="verdana, arial, helvetica">$edit_array[0]</FONT></TD></TR>
EOF
   }


print<<EOF;
</ROWS></TBODY></TABLE></CENTER>

<hr size="1" width="500">
<center>
  <table border="1" width="500">
    <tr>
      <td valign="MIDDLE" align="CENTER" width="50%" bgcolor="#C0C0C0" colstart="1">
        <input type="SUBMIT" name="processac" value="   Process   "><input type="RESET" name="Input">
      </td>
      <td align="CENTER" width="50%" bgcolor="#C0C0C0" colstart="2"><font size="-1" face="verdana, arial, helvetica"><b>Active Users</b></font><br>
        <font size="-2" face="verdana, arial, helvetica">View/Edit/Delete</font></td>
    </tr>
  </table>
</center>
<hr size="1" width="500">
<center>
  <table border="1" width="500">
    <tr>
      <td valign="MIDDLE" align="CENTER" width="50%" bgcolor="#C0C0C0" colstart="1">
        <input type="SUBMIT" value="Main Menu Return" name="admin2">
      </td>
      <td valign="MIDDLE" align="CENTER" width="50%" bgcolor="#C0C0C0" colstart="2"><font size="-1" face="verdana, arial, helvetica"><b>Main Menu Return</b></font></td>
    </tr>
  </table>
</center>
<center>
  <table border="0" width="500">
    <tr>
      <td colstart="1">
        <hr size="1" width="500">
      </td>
    </tr>
    <tr>
      <td valign="TOP" align="right" colstart="1"> <font size="-2" face="Verdana, Arial, Helvetica, sans-serif"><a href="http://www.webweaver.pe.kr" target="_blank">Improved by JuWon,Kim</a></font><font face="Verdana, Arial, Helvetica, sans-serif" size="-2"><br>
        <a href="http://cgi.elitehost.com/" target="elite"> Account Manager LITE $version</a></font></td>
    </tr>
  </table>
</center>

EOF
&footer;
exit;
}

sub processac {

open (DAT,"<$memberinfo/amdata.db");
if ($LOCK_EX){ 
      flock(DAT, $LOCK_EX); #Locks the file
	}
 @database_array = <DAT>;
close (DAT);

open (DAT, ">$memberinfo/amdata.db");
if ($LOCK_EX){ 
      flock(DAT, $LOCK_EX); #Locks the file
	}
foreach $lines(@database_array) {
          @edit_array = split(/\:/,$lines);

if ($INPUT{$edit_array[0]} ne adelete) {
chomp($lines);
print DAT "$lines\n";
             
   }

}
close (DAT);
#&destatement;
&htaccess;


print "Content-type: text/html\n\n";
open (DAT,"<$memberinfo/amdata.db");
if ($LOCK_EX){ 
      flock(DAT, $LOCK_EX); #Locks the file
	}
 @database_array = <DAT>;
close (DAT);

foreach $lines(@database_array) {
          @edit_array = split(/\:/,$lines);
          
if ($edit_array[0] eq $INPUT{'update'}) {last; }

}
&update;

}

sub htaccess {
if ($htaccess == "1") {
       open (DAT2, "<$memaccess"); 
if ($LOCK_EX){ 
      flock(DAT2, $LOCK_EX); #Locks the file
	}
             @database_array = <DAT2>;
             close (DAT2);

open (DAT2, ">$memaccess");
if ($LOCK_EX){ 
      flock(DAT2, $LOCK_EX); #Locks the file
	} 
                foreach $lines(@database_array) {
          @edit_array = split(/\:/,$lines);
if ($INPUT{$edit_array[0]} ne adelete) {
chomp($lines);
print DAT2 "$lines\n";
}

}

}
close (DAT2);
unless ($INPUT{'update'}) {

&active;
exit;
}
}

sub update {
&read;

open (DAT,"<$memberinfo/amdata.db");
if ($LOCK_EX){ 
      flock(DAT, $LOCK_EX); #Locks the file
	}

 @database_array = <DAT>;
close (DAT);

foreach $lines(@database_array) {
          @edit_array = split(/\:/,$lines);
if ($edit_array[0] eq $INPUT{'update'}) {last; }
}
&header;
print<<EOF;

<center>
  <table border="1" width="500" cellpadding="5">
    <tr>
      <td align="CENTER" colspan="2" colstart="1"><b><font size="-2" face="verdana, arial, helvetica">CGI Script Center's</font><br>
        <font size="-1" face="verdana, arial, helvetica" color="#FF0000">Account Manager LITE $version</font></b></td>
    </tr>
    <tr>
      <td valign="MIDDLE" align="CENTER" width="50%" bgcolor="#C0C0C0" rowspan="2" colstart="1"><font size="+1" face="verdana, arial, helvetica"><b>Active Users</b></font><br>
        <font size="-2" face="verdana, arial, helvetica">View/Edit/Delete</font></td>
      <td valign="MIDDLE" align="LEFT" width="50%" bgcolor="#C0C0C0" colstart="2"><font size="-2" face="verdana, arial, helvetica" color="#000000"><b>Active Users: <font color="#0000FF">$count</font></b></font></td>
    </tr>
    <tr>
      <td valign="MIDDLE" align="LEFT" bgcolor="#C0C0C0" colstart="2"><font size="-2" face="verdana, arial, helvetica" color="#000000"><b>Awaiting Approval: 
        <font color="#0000FF">$new_files</font></b></font></td>
    </tr>
  </table>
  <br>
</center>
<form action="$cgiurl" method="POST">
  <input type="HIDDEN" name="marker" value="$edit_array[0]">
  <center>
    <table border="1" width="500">
      <tr>
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><font size="+1" face="verdana, arial, helvetica"><b>User Edit</b></font></td>
      </tr>
    </table>
    <br>
    <table border="1" width="500" cellpadding="5">
      <tr> 
        <td align="CENTER" colspan="3" height="0" bgcolor="#C0C0C0" colstart="1"><b><font size="-2" face="verdana, arial, helvetica">$edit_array[3]</font> </b></td>
      </tr>
      <tr> 
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><font size="-2" face="verdana, arial, helvetica"><b>이 름</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>$edit_array[3]</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="3"> 
          <input type="TEXT" size="9" name="fname">
        </td>
      </tr>
      <tr> 
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><font size="-2" face="verdana, arial, helvetica"><b>E-mail </b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>$edit_array[2]</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="3"> 
          <input type="TEXT" size="9" name="email">
        </td>
      </tr>
      <tr> 
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><font size="-2" face="verdana, arial, helvetica"><b>주 소</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>$edit_array[5]</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="3"> 
          <input type="TEXT" size="9" name="address">
        </td>
      </tr>
      <tr> 
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><font size="-2" face="verdana, arial, helvetica"><b>전 화</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>$edit_array[4]</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="3"> 
          <input type="TEXT" size="9" name="phone">
        </td>
      </tr>
      <tr> 
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><font size="-2" face="verdana, arial, helvetica"><b>Login ID</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>$edit_array[0]</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="3"> 
          <input type="TEXT" size="9" name="username">
        </td>
      </tr>
      <tr> 
        <td valign="MIDDLE" align="CENTER" bgcolor="#C0C0C0" colstart="1"><font size="-2" face="verdana, arial, helvetica"><b>Password</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="2"><font size="-2" face="verdana, arial, helvetica"><b>$edit_array[1]</b></font></td>
        <td valign="MIDDLE" align="CENTER" colstart="3"> 
          <input type="TEXT" size="9" name="password">
        </td>
      </tr>
EOF


print<<EOF;
    </TABLE>
  </CENTER>

<hr size="1" width="500">
<center>
  <table border="1" width="500">
    <tr>
      <td valign="MIDDLE" align="CENTER" width="50%" bgcolor="#C0C0C0" colstart="1">
        <input type="SUBMIT" name="processch" value="   Process   "><input type="RESET" name="Input">
      </td>
      <td align="CENTER" width="50%" bgcolor="#C0C0C0" colstart="2"><font size="-1" face="verdana, arial, helvetica"><b>Active Users</b></font><br>
        <font size="-2" face="verdana, arial, helvetica">View/Edit/Delete</font></td>
    </tr>
  </table>
</center>
EOF

print<<EOF;

<hr size="1" width="500">
<center>
  <table border="1" width="500">
    <tr>
      <td valign="MIDDLE" align="CENTER" width="50%" bgcolor="#C0C0C0" colstart="1">
        <input type="SUBMIT" name="admin2" value="Main Menu Return">
      </td>
      <td valign="MIDDLE" align="CENTER" width="50%" bgcolor="#C0C0C0" colstart="2"><font size="-1" face="verdana, arial, helvetica"><b>Main Menu Return</b></font></td>
    </tr>
  </table>
</center>
<center>
  <table border="0" width="500">
    <tr>
      <td colstart="1">
        <hr size="1" width="500">
      </td>
    </tr>
    <tr>
      <td valign="TOP" align="right" colstart="1"> <font size="-2" face="Verdana, Arial, Helvetica, sans-serif"><a href="http://www.webweaver.pe.kr" target="_blank">Improved by JuWon,Kim</a></font><font face="Verdana, Arial, Helvetica, sans-serif" size="-2"><br>
        <a href="http://cgi.elitehost.com/" target="elite"> Account Manager LITE $version</a></font></td>
    </tr>
  </table>
</center>

EOF
&footer;
exit;

}

sub processch {

open (DAT,"<$memberinfo/amdata.db");
if ($LOCK_EX){ 
      flock(DAT, $LOCK_EX); #Locks the file
	}
 @database_array = <DAT>;
close (DAT);
open (DAT2, ">$memberinfo/amdata.db");
if ($LOCK_EX){ 
      flock(DAT2, $LOCK_EX); #Locks the file
	}

foreach $lines(@database_array) {
          @edit_array = split(/\:/,$lines);
            if ($edit_array[0] eq $INPUT{'marker'}) {
            
$edit_array[0] = $INPUT{'username'} if $INPUT{'username'};
$edit_array[1] = $INPUT{'password'} if $INPUT{'password'};
$edit_array[2] = $INPUT{'email'} if $INPUT{'email'};
$edit_array[3] = $INPUT{'fname'} if $INPUT{'fname'};
$edit_array[4] = $INPUT{'phone'} if $INPUT{'phone'};
$edit_array[5] = $INPUT{'address'} if $INPUT{'address'};
$edit_array[6] = $INPUT{'citizen_no_1'} if $INPUT{'citizen_no_1'};
$edit_array[7] = $INPUT{'citizen_no_2'} if $INPUT{'citizen_no_2'};
$edit_array[8] = $INPUT{'zip_code'} if $INPUT{'zip_code'};
$edit_array[9] = $INPUT{'company'} if $INPUT{'company'};
$edit_array[10] = $INPUT{'company_phone'} if $INPUT{'company_phone'};
$edit_array[14] = $INPUT{'payment'} if $INPUT{'payment'};
$edit_array[24] = $INPUT{'lastinv'} if $INPUT{'lastinv'};
$edit_array[17] = $INPUT{'tlastinv'} if $INPUT{'tlastinv'};
$edit_array[18] = $INPUT{'papplied'} if $INPUT{'papplied'};
$edit_array[19] = $INPUT{'aapplied'} if $INPUT{'aapplied'};

}

$newline = join
("\:",@edit_array);

chomp($newline);
print DAT2 "$newline\n";
}


close (DAT2);


if ($htaccess == "1") {
if ($INPUT{'username'} || $INPUT{'password'}) {

       open (DAT3, "<$memaccess"); 
if ($LOCK_EX){ 
      flock(DAT3, $LOCK_EX); #Locks the file
	}
                @database_array = <DAT3>;          
                close (DAT3);

open (DAT3, ">$memaccess"); 
if ($LOCK_EX){ 
      flock(DAT3, $LOCK_EX); #Locks the file
	}
      
        foreach $lines(@database_array) {
          @edit_array = split(/\:/,$lines);
            if ($edit_array[0] eq $INPUT{'marker'}) {
$edit_array[0] = $INPUT{'username'} if $INPUT{'username'};

            if ($INPUT{'password'}) {
 
chop ($INPUT{'password'}) if ($INPUT{'password'} =~ /\n$/);
		$newpassword = crypt($INPUT{'password'}, aa);
    $edit_array[1] = $newpassword if $INPUT{'password'}
}
}

$newline3 = join
("\:",@edit_array);

chomp($newline3);
print DAT3 "$newline3\n";
}
close (DAT3);

}


}

&active;
exit;
}

sub search {
&read;
print "Content-type: text/html\n\n";
&header;
print<<EOF;
<CENTER><TABLE
BORDER="1" WIDTH="500" CELLPADDING="5"><TBODY><COLDEFS><COLDEF><COLDEF></COLDEFS>
<ROWS><TR><TD ALIGN="CENTER" COLSPAN="2" COLSTART="1"><B><FONT
SIZE="-2" FACE="verdana, arial, helvetica">CGI Script Center's</FONT><BR><FONT
SIZE="-1" FACE="verdana, arial, helvetica" COLOR="#FF0000">Account Manager LITE 
$version</FONT></B></TD></TR><TR><TD
VALIGN="MIDDLE" ALIGN="CENTER" WIDTH="50%" BGCOLOR="#C0C0C0" ROWSPAN="2" COLSTART="1"><FONT
SIZE="+1" FACE="verdana, arial, helvetica"><B>Search for User</B></FONT><BR><FONT
SIZE="-2" FACE="verdana, arial, helvetica">View/Edit/Delete</FONT></TD><TD
VALIGN="MIDDLE" ALIGN="LEFT" WIDTH="50%" BGCOLOR="#C0C0C0" COLSTART="2"><FONT
SIZE="-2" FACE="verdana, arial, helvetica"><B><FONT COLOR="#000000">Active
Users: <FONT COLOR="#0000FF">$count</FONT></FONT></B></FONT></TD></TR><TR><TD
VALIGN="MIDDLE" ALIGN="LEFT" BGCOLOR="#C0C0C0" COLSTART="2"><FONT
SIZE="-2" FACE="verdana, arial, helvetica"><B><FONT COLOR="#000000">Awaiting
Approval:  <FONT COLOR="#0000FF">$new_files</FONT></FONT></B></FONT></TD></TR></ROWS></TBODY></TABLE><BR></CENTER>
<FORM ACTION="$cgiurl" METHOD="POST"><HR SIZE="1" WIDTH="500"><CENTER><TABLE
BORDER="1" WIDTH="500" CELLPADDING="5"><TBODY><COLDEFS><COLDEF><COLDEF></COLDEFS>
<ROWS><TR><TD WIDTH="50%" BGCOLOR="#C0C0C0" COLSTART="1"><FONT
SIZE="-1" FACE="verdana, arial, helvetica"><B>Search by: </B></FONT> <SELECT
NAME="searchby"><OPTION VALUE="- Select One -">- Select One -</OPTION><OPTION
VALUE="Username">Username</OPTION><OPTION VALUE="fname">First Name</OPTION><OPTION
VALUE="lname">Last Name</OPTION></SELECT></TD><TD
VALIGN="MIDDLE" ALIGN="CENTER" BGCOLOR="#C0C0C0" COLSTART="2"><INPUT
TYPE="TEXT" SIZE="11" NAME="name"></TD></TR></ROWS></TBODY></TABLE></CENTER><HR
SIZE="1" WIDTH="500"><CENTER><BR><TABLE BORDER="1" WIDTH="500"><TBODY><COLDEFS>
<COLDEF><COLDEF></COLDEFS><ROWS><TR><TD
VALIGN="MIDDLE" ALIGN="CENTER" WIDTH="50%" BGCOLOR="#C0C0C0" COLSTART="1"><INPUT
TYPE="SUBMIT" NAME="processsearch" VALUE="   Process   "><INPUT
TYPE="RESET" NAME=""></TD><TD
ALIGN="CENTER" WIDTH="50%" BGCOLOR="#C0C0C0" COLSTART="2"><FONT
SIZE="+1" FACE="verdana, arial, helvetica"><B><FONT SIZE="-1">Search for User</FONT></B></FONT><BR><FONT
SIZE="-2" FACE="verdana, arial, helvetica">View/Edit/Delete</FONT></TD></TR></ROWS></TBODY></TABLE></CENTER>
<HR SIZE="1" WIDTH="500"><CENTER><TABLE BORDER="1" WIDTH="500"><TBODY><COLDEFS><COLDEF
><COLDEF></COLDEFS><ROWS><TR><TD
VALIGN="MIDDLE" ALIGN="CENTER" WIDTH="50%" BGCOLOR="#C0C0C0" COLSTART="1"><INPUT
TYPE="SUBMIT" VALUE="Main Menu Return" NAME="admin2"></TD><TD
VALIGN="MIDDLE" ALIGN="CENTER" WIDTH="50%" BGCOLOR="#C0C0C0" COLSTART="2"><FONT
SIZE="+1" FACE="verdana, arial, helvetica"><B><FONT SIZE="-1">Main Menu
Return</FONT></B></FONT></TD></TR></ROWS></TBODY></TABLE></CENTER></FORM><CENTER><TABLE
BORDER="0" WIDTH="500"><TBODY><COLDEFS><COLDEF></COLDEFS><ROWS><TR><TD
COLSTART="1"><HR SIZE="1" WIDTH="500"></TD></TR><TR><TD
VALIGN="TOP" ALIGN="right" COLSTART="1">
<FONT SIZE="-2" FACE="verdana, arial, helvetica"><A HREF="http://www.webweaver.pe.kr" target="_blank">Improved by JuWon,Kim</a><br>
<A HREF="http://cgi.elitehost.com/" target="elite">
Account Manager LITE $version</A></B></FONT></TD></TR></ROWS></TBODY></TABLE></CENTER></BODY></HTML>
EOF
&footer;
exit;
}

sub processsearch {

if ($INPUT{'searchby'} eq Username) {


print "Location: http://cgi.elitehost.com/acctlite/upgrade\n\n";

exit;

} 

if ($INPUT{'searchby'} eq fname) {


print "Location: http://cgi.elitehost.com/acctlite/upgrade\n\n";

exit;
} 

if ($INPUT{'searchby'} eq lname) {

print "Location: http://cgi.elitehost.com/acctlite/upgrade\n\n";
exit;
} 

}

sub areyousure {

print "Location: http://cgi.elitehost.com/acctlite/upgrade\n\n";
exit;
}

sub mmailform {

print "Location: http://cgi.elitehost.com/acctlite/upgrade\n\n";
exit;
}

sub mmail {

print "Location: http://cgi.elitehost.com/acctlite/upgrade\n\n";
exit;

}


sub searchedit {
&read;

print "Content-type: text/html\n\n";
&header;
print <<EOF;
<CENTER><TABLE
BORDER="1" WIDTH="500" CELLPADDING="5"><TBODY><COLDEFS><COLDEF><COLDEF></COLDEFS>
<ROWS><TR><TD ALIGN="CENTER" COLSPAN="2" COLSTART="1"><B><FONT
SIZE="-2" FACE="verdana, arial, helvetica">CGI Script Center's</FONT><BR><FONT
SIZE="-1" FACE="verdana, arial, helvetica" COLOR="#FF0000">Account Manager LITE 
$version</FONT></B></TD></TR><TR><TD
VALIGN="MIDDLE" ALIGN="CENTER" WIDTH="50%" BGCOLOR="#C0C0C0" ROWSPAN="2" COLSTART="1"><FONT
SIZE="+1" FACE="verdana, arial, helvetica"><B>Active Users</B></FONT><BR><FONT
SIZE="-2" FACE="verdana, arial, helvetica">View/Edit/Delete</FONT></TD><TD
VALIGN="MIDDLE" ALIGN="LEFT" WIDTH="50%" BGCOLOR="#C0C0C0" COLSTART="2"><FONT
SIZE="-2" FACE="verdana, arial, helvetica"><B><FONT COLOR="#000000">Active
Users: <FONT COLOR="#0000FF">$count</FONT></FONT></B></FONT></TD></TR><TR><TD
VALIGN="MIDDLE" ALIGN="LEFT" BGCOLOR="#C0C0C0" COLSTART="2"><FONT
SIZE="-2" FACE="verdana, arial, helvetica"><B><FONT COLOR="#000000">Awaiting
Approval:  <FONT COLOR="#0000FF">$new_files</FONT></FONT></B></FONT></TD></TR></ROWS></TBODY></TABLE><BR></CENTER>
<FORM ACTION="$cgiurl" METHOD="POST"><CENTER><TABLE
BORDER="1" WIDTH="500" CELLPADDING="5"><TBODY><COLDEFS><COLDEF><COLDEF><COLDEF>
<COLDEF></COLDEFS><ROWS><TR><TD
ALIGN="CENTER" NOWRAP="NOWRAP" WIDTH="40" BGCOLOR="#C0C0C0" COLSTART="1"><FONT
SIZE="-2" FACE="verdana, arial, helvetica"><B>Update</B></FONT></TD><TD
ALIGN="CENTER" WIDTH="40" BGCOLOR="#C0C0C0" COLSTART="2"><FONT
SIZE="-2" FACE="verdana, arial, helvetica"><B>Delete</B></FONT></TD><TD
ALIGN="CENTER" BGCOLOR="#C0C0C0" COLSTART="3"><FONT
SIZE="-2" FACE="verdana, arial, helvetica"><B>Name</B></FONT></TD><TD
VALIGN="MIDDLE" ALIGN="CENTER" BGCOLOR="#C0C0C0" COLSTART="4"><FONT
SIZE="-2" FACE="verdana, arial, helvetica"><B>Username</B></FONT></TD></TR>
EOF

print<<EOF;
<TR><TD
 VALIGN="MIDDLE" ALIGN="CENTER" COLSTART="1"><INPUT
TYPE="RADIO" VALUE="$edit_array[0]" NAME="update"></TD><TD
VALIGN="MIDDLE" ALIGN="CENTER" COLSTART="2"><INPUT
TYPE="RADIO" VALUE="adelete" NAME="$edit_array[0]"></TD><TD
VALIGN="MIDDLE" ALIGN="LEFT" COLSTART="3"><A HREF="mailto:$edit_array[2]"><FONT
SIZE="-2" FACE="verdana, arial, helvetica">$edit_array[3] $edit_array[5]</FONT></A></TD>
<TD VALIGN="MIDDLE" ALIGN="CENTER" COLSTART="4"><FONT
SIZE="-2" FACE="verdana, arial, helvetica">$edit_array[0]</FONT></TD></TR>
EOF

print<<EOF;
</ROWS></TBODY></TABLE></CENTER>
<HR SIZE="1" WIDTH="500"><CENTER><TABLE BORDER="1" WIDTH="500"><TBODY><COLDEFS><COLDEF
><COLDEF></COLDEFS><ROWS><TR><TD
VALIGN="MIDDLE" ALIGN="CENTER" WIDTH="50%" BGCOLOR="#C0C0C0" COLSTART="1"><INPUT
TYPE="SUBMIT" NAME="processac" VALUE="   Process   "><INPUT
TYPE="RESET" NAME=""></TD><TD
ALIGN="CENTER" WIDTH="50%" BGCOLOR="#C0C0C0" COLSTART="2"><FONT
SIZE="+1" FACE="verdana, arial, helvetica"><B><FONT SIZE="-1">Active Users</FONT></B></FONT><BR><FONT
SIZE="-2" FACE="verdana, arial, helvetica">View/Edit/Delete</FONT></TD></TR></ROWS></TBODY></TABLE></CENTER>
<HR SIZE="1" WIDTH="500"><CENTER><TABLE BORDER="1" WIDTH="500"><TBODY><COLDEFS><COLDEF
><COLDEF></COLDEFS><ROWS><TR><TD
VALIGN="MIDDLE" ALIGN="CENTER" WIDTH="50%" BGCOLOR="#C0C0C0" COLSTART="1"><INPUT
TYPE="SUBMIT" VALUE="Main Menu Return" NAME="admin2"></TD><TD
VALIGN="MIDDLE" ALIGN="CENTER" WIDTH="50%" BGCOLOR="#C0C0C0" COLSTART="2"><FONT
SIZE="+1" FACE="verdana, arial, helvetica"><B><FONT SIZE="-1">Main Menu Return</FONT></B></FONT></TD></TR></ROWS></TBODY></TABLE></CENTER></FORM>
<CENTER><TABLE BORDER="0" WIDTH="500"><TBODY><COLDEFS><COLDEF></COLDEFS><ROWS><TR
><TD COLSTART="1"><HR SIZE="1" WIDTH="500"></TD></TR><TR><TD
VALIGN="TOP" ALIGN="right" COLSTART="1">
<FONT SIZE="-2" FACE="verdana, arial, helvetica"><A HREF="http://www.webweaver.pe.kr" target="_blank">Improved by JuWon,Kim</a><br>
<A HREF="http://cgi.elitehost.com/" target="elite">
Account Manager LITE $version</A></B></FONT></TD></TR></ROWS></TBODY></TABLE></CENTER>
EOF
&footer;
exit;
}


sub header {
open (FILE,"<$header/header.txt"); #### Full path name from root.
if ($LOCK_EX){ 
      flock(FILE, $LOCK_EX); #Locks the file
	} 
 @headerfile = <FILE>;
 close(FILE);
print "<HTML><HEAD><TITLE></TITLE></HEAD><BODY $bodyspec>\n";
foreach $line(@headerfile) {
print "$line";
  }
}


sub footer {
open (FILE,"<$footer/footer.txt"); #### Full path name from root.
if ($LOCK_EX){ 
      flock(FILE, $LOCK_EX); #Locks the file
	} 
 @footerfile = <FILE>;
 close(FILE);
foreach $line(@footerfile) {
print "$line";

}
print "</BODY></HTML>";
}

sub ambill {

print "Location: http://cgi.elitehost.com/acctlite/upgrade\n\n";
exit;

}


sub mailbills {
print "Location: http://cgi.elitehost.com/acctlite/upgrade\n\n";
exit;

}


sub setpassword {

&header;
print<<EOF;
<FORM ACTION=\"$cgiurl\" METHOD=\"POST\"><CENTER><BR>
<TABLE BORDER=\"0\" WIDTH=\"400\"><TBODY><COLDEFS><COLDEF></COLDEFS><ROWS><TR><TD
COLSTART=\"1\"><P><B><FONT FACE=\"verdana, arial, helvetica\"><FONT
COLOR=\"#FF0000\">Account Manager LITE</FONT> 종 류:  패스워드 등록!</FONT></B></P>
<P><FONT SIZE=\"-1\" FACE=\"verdana, arial, helvetica\">처음 접속하시는 관리자께서는 관리용 패스워드를 
입력하셔야 합니다.</FONT></P>
<CENTER><TABLE BORDER=\"0\"><TBODY><COLDEFS><COLDEF><COLDEF></COLDEFS><ROWS><TR
><TD ALIGN=\"RIGHT\" COLSTART=\"1\"><INPUT TYPE=\"PASSWORD\" NAME=\"pwd\"></TD><TD
COLSTART=\"2\"><FONT SIZE=\"-2\" FACE=\"verdana, arial, helvetica\">password</FONT></TD></TR>
<TR><TD ALIGN=\"RIGHT\" COLSTART=\"1\"><INPUT TYPE=\"PASSWORD\" NAME=\"pwd2\"></TD><TD
COLSTART=\"2\"><FONT SIZE=\"-2\" FACE=\"verdana, arial, helvetica\">재 확인</FONT></TD></TR>
<TR><TD ALIGN=\"CENTER\" COLSTART=\"1\"><BR><INPUT
TYPE=\"SUBMIT\" NAME=\"setpwd\" VALUE=\"  Set Password  \"></TD><TD COLSTART=\"2\"><BR><INPUT
TYPE=\"RESET\" NAME=\"\"></TD></TR></ROWS></TBODY></TABLE></CENTER><CENTER><TABLE
BORDER=\"0\" WIDTH=\"400\"><TBODY><COLDEFS><COLDEF></COLDEFS><ROWS><TR><TD
COLSTART=\"1\"><HR SIZE=\"1\"></TD></TR><TR><TD ALIGN=\"right\" COLSTART=\"1\">
<FONT SIZE=\"-2\" FACE=\"verdana, arial, helvetica\"><A HREF=\"http://www.webweaver.pe.kr\" target=\"_blank\">Improved by JuWon,Kim</a><br>
<A HREF=\"http://cgi.elitehost.com/\" target=\"elite\">
<B>Account Manager LITE $version</B></A></FONT>
</TD></TR></ROWS></TBODY></TABLE></CENTER></TD></TR></ROWS></TBODY></TABLE></CENTER></FORM>
EOF
&footer;
exit;
}

sub setpwd {
print "Content-type: text/html\n\n";
unless ($INPUT{'pwd'} && $INPUT{'pwd2'}) {&resultMsg ('PassWord Error !','PassWord 를 두번 입력해야 합니다.');}
if ($INPUT{'pwd'} && $INPUT{'pwd2'}) {
    if ($INPUT{'pwd'} ne $INPUT{'pwd2'}) {&resultMsg ('패스워드 불일치 !','확인용 패스워드가 처음과 일치하지 않습니다. 다시한번 시도해 주세요.');}
}

chop ($pwd) if ($pwd =~ /\n$/);
		$newpassword = crypt($INPUT{'pwd'}, aa);

open (PASSWORD, ">$passfile/password.txt") || print "Could not write password text file.  Check your permission settings";
     
    if ($LOCK_EX){ 
      flock(PASSWORD, $LOCK_EX); #Locks the file
	}
      print PASSWORD "$newpassword";
	close (PASSWORD);
&adminpass;
exit;
}

sub payhist {


print "Location: http://cgi.elitehost.com/acctlite/upgrade\n\n";
exit;

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
