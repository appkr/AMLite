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

# body �±� �Ӽ��� ����
$bodyspec = "background=\"\" bgcolor=\"#FFFFFF\" link=\"#0000FF\" vlink=\"#0000FF\"";

# header.txt ������ ��ġ
$header = ".";

# footer.txt ������ ��ġ
$footer = ".";

# ��ƮĮ��
$fontcolor = "#000000";

# ����Ʈ �̸�
$orgname = "WebWeaver";

# ������ �����ּ�
# @ �տ� �ݵ�� \ �� �־�� �մϴ�.
$orgmail = "i\@webweaver.pe.kr";

# �ӽ� ���丮
$tempdir = "./temp";

# ������� ���
$mailprog = "/usr/sbin/sendmail";

# email.txt ������ ���
$closing = ".";

# ȸ����� ��û�� ���� ���� ����
$response_subject = "ȸ����� ��û�ϼ̽��ϴ�!";

# .htaccess �� .nsconfig �� ����� �� �ִ� ������ "1", otherwise ""(����)
$htaccess = "1";

# .htpasswd ������ ��ġ
$memaccess = "./memberonly/.htpasswd";

# ȸ�������� ����� ���丮
$memberinfo = "./memberinfo";

# ���Ϸ�(flock)�Լ� ��������, �����ϸ� "2", or ""(����)
$LOCK_EX = "2";

# ������ �н����� ���� ���丮
$passfile = "./pass";

# ȸ������ ���Ϻ����� ����
$subject = "WebWeaver �α���";

# Create two text files.  One called "approved.txt" and the other
# called "denied.txt".  In each, write the response that you would
# like your prospective members to receive when you have either
# approved or denied their application for membership, respectively.
# Then, upload both text files to your $memberinfo directory.
# The script will do the rest.
# Example, in the "approved.txt" file, you can type:
# "Your account is now active."

# ȸ����� �źεǾ��� ��� ���� ����
$denied_email_subject = "WebWeaver ȸ����� ��û �ҽ���";

# ȸ����� ���εǾ��� ��� ���� ����
$approved_email_subject ="WebWeaver�� ȸ����� �Ǽ̽��ϴ�.";