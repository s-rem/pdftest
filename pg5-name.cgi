#!/usr/bin/perl
use strict;
use warnings;
use utf8;

use CGI;
use PDFJ 'UTF8';
use SFCON::Register_db;
require 'error.pl';

my $filename = 'test.txt';
my $cgi=CGI->new;
my $reg_number_req = $cgi->param('target');


my $pdfj_font_base = ((getpwuid($<))[7]) . "/local/lib/perl5/PDFJ-0.90/FONT/";

    my $ds   = "DBI:mysql:foo_db;host=db.sfcon.jp;port=3306";
    my $user = 'sfcon';
    my $pass = 'user_passwd';
    my $prefix= 'sfxx_';

my $db = DBI->connect($ds, $user, $pass) || die "Got error $DBI::errstr when connecting to $ds\n";
my $sth = $db->prepare("SET NAMES utf8");
$sth->execute;

our $room_width = 100;
our $hour_width = 72;
our $q_hour_width = $hour_width / 4;
our $room_height = 100;
our $time_height = 25;
our $time_count = 14;
our $room_count = 13;
our $line_width = $room_width + $hour_width * $time_count + $q_hour_width * 2;
our $line_height = $time_height + $room_height * $room_count;
our $line_height2 = $room_height * $room_count;
our $page_width = 100 * 2.8346;
our $page_height = 148 * 2.8346;
our $top_margin = 15;
our $left_margin = 15;
our $title_height = 50;
our $bottom_margin = $page_height - $line_height - $ title_height;
our @page;
our $page_max = 1;
my $n;
my $titles;

our $doc = PDFJ::Doc->new(1.3, $page_width, $page_height);

$doc->add_info(Title => 'sfcon PageList ', Author => '<admin@sfcon.jp>');

my $f_h = $doc->new_font('Helvetica');
my $f_t = $doc->new_font('Times-Roman');
my $f_m = $doc->new_font('Ryumin-Light', 'UniJIS-UCS2-HW-H');
my $f_mt = $doc->new_font('Ryumin-Light', 'UniJIS-UCS2-HW-H', 'Times-Roman',
    'WinAnsiEncoding', 1.05);
my $f_g = $doc->new_font($pdfj_font_base . 'HGRSGU.TTC:1', 'UniJIS-UCS2-HW-H','Helvetica',
    'WinAnsiEncoding', 1.05);
my $f_gh = $doc->new_font('GothicBBB-Medium', 'UniJIS-UCS2-HW-H', 'Helvetica',
    'WinAnsiEncoding', 1.05);
my $f_mv = $doc->new_font('Ryumin-Light', 'UniJIS-UCS2-HW-V');
my $f_mtv = $doc->new_font('Ryumin-Light', 'UniJIS-UCS2-HW-V', 'Times-Roman',
    'WinAnsiEncoding', 1.05);
my $f_gv = $doc->new_font($pdfj_font_base . 'HGRSGU.TTC:1', 'UniJIS-UCS2-HW-V');
my $f_ghv = $doc->new_font('GothicBBB-Medium', 'UniJIS-UCS2-HW-V', 'Helvetica',
    'WinAnsiEncoding', 1.05);
my $f_si = $doc->new_font($pdfj_font_base . 'HGRSGU.TTC:1', 'UniJIS-UCS2-HW-H',$pdfj_font_base . 'OCR-a___.ttf',
    'WinAnsiEncoding', 1.05);

my $c_black = Color('#000000');
my $c_darkblue = Color('#191970');
my $c_cadetblue = Color('#5f9ea0');
my $c_lightcyan = Color('#e0ffff');
my $c_white = Color(1);
my $c_darktgray = Color(0.2);
my $c_gray = Color(0.5);
my $c_lightgray = Color(0.97);
my $c_red = Color(1,0,0);

my $ss_red = SStyle(fillcolor => $c_red);
my $ss_darkblue = SStyle(fillcolor => $c_darkblue);
my $ss_white = SStyle(fillcolor => $c_white);
my $ss_black = SStyle(fillcolor => $c_black);
my $ss_gray = SStyle(fillcolor => $c_gray);
my $ss_dash = SStyle(linedash => [2,2]);

our $s_timetable_box = TStyle(font => $f_gh, fontsize => 16, 
    shapestyle => $ss_black);
our $s_address = TStyle(font => $f_mt, fontsize => 10, 
    shapestyle => $ss_black, align => 'b');
our $s_addr_name = TStyle(font => $f_mt, fontsize => 16, 
    shapestyle => $ss_black, align => 'b');
our $s_reg_num = TStyle(font => $f_gh, fontsize => 16, 
    shapestyle => $ss_black);
our $s_reg_name1 = TStyle(font => $f_gh, fontsize => 20, 
    shapestyle => $ss_black);
our $s_reg_name2 = TStyle(font => $f_g, fontsize => 24, 
    shapestyle => $ss_black);
our $s_reg_hon = TStyle(font => $f_gv, fontsize => 48, 
    shapestyle => $ss_black);
our $s_info_num = TStyle(font => $f_si, fontsize => 8, 
    shapestyle => $ss_black);

our $tables;
our $shapeobj;

my $width = 1110;
my $padding = 20;

my $bs_frame = 
    BStyle(padding => $padding, align => "tl", withbox => "f", 
    height => 15,
        withboxstyle => 
        SStyle(linewidth => 2, strokecolor => $c_black, 
            fillcolor => $c_lightcyan));

my $bs_confidential = 
    BStyle(padding => 0, align => "b", withbox => "f", 
    height => 15,
        withboxstyle => 
        SStyle(fillcolor => $c_white));

my $bs_table = BStyle(adjust => 1);
my $bs_tr = BStyle(adjust => 1);
my $bs_td = BStyle(padding => 10, align => "tl", withbox => "f", 
    withboxstyle => $ss_white);

my $LabelNum = 1;

sub resetlabelnum {
    $LabelNum = 1;
}

sub numlabel {
    my($fmt, $style) = @_;
    Text(sprintf($fmt, $LabelNum++), $style);
}

sub Page_add {
    my($reg_num, $post_num, $pref,  $city, $location, $street, $adrs2, $name1, $name2, $reg_class, $x_info) = @_;

    my ($name2_1, $name2_2, $name2_3);
    my $n = $reg_num;
    $page[$n] = $doc->new_page;

    $tables=Block('V', [
        Paragraph(
        Text(["郵便はがき"],TStyle(font => $f_gh, fontsize => 7, shapestyle => $ss_black)),
        PStyle(size => 40 * 2.8346 , align => 'W', linefeed => 12, preskip => 12.5, postskip => 12.5)),
        ], $bs_table);
    $tables->show($page[$n] , 30 * 2.8356 , 143 * 2.8356 , 'tl');

    my $stamp = Shape();
    $tables=Block('V', [
        Paragraph(
        Text(["広島中央支店"],TStyle(font => $f_gh, fontsize => 9.5, shapestyle => $ss_black)),
        PStyle(size => 28 * 2.8346 , align => 'm', linefeed => 12, preskip => 12.5, postskip => 12.5)),
        ], $bs_table);
    $stamp->obj($tables, 0,18 * 2.8346,'bl');
    $tables=Block('V', [
        Paragraph(
        Text(["料金後納",NewLine,"郵便"],TStyle(font => $f_gh, fontsize => 14, shapestyle => $ss_black)),
        PStyle(size => 28 * 2.8346 , align => 'm', linefeed => 15, preskip => 12.5, postskip => 12.5)),
        ], $bs_table);
    $stamp->obj($tables, 0,15 * 2.8346,'tl');
    $stamp->circle(14 * 2.8346 , 14 * 2.8346, 13 * 2.8346, 's','', SStyle(linewidth => 1, strokecolor => $c_black));
    $stamp->line((1+13-12.65) * 2.8346 ,(14 +3) * 2.8346 , (12.65 * 2) * 2.8346, 0, SStyle(linewidth => 0.5, strokecolor => $c_black));
    $stamp->show($page[$n] , 10, 400 , 'tl');

    
    $tables=Block('V', [
        Paragraph(
        Text([$post_num],TStyle(font => $f_gh, fontsize => 22, shapestyle => $ss_black)),
        PStyle(size => 45 * 2.8346 , align => 'l', linefeed => 12, preskip => 12.5, postskip => 12.5)),
        ], $bs_table);
    $tables->show($page[$n] , 55 * 2.8356 , 138 * 2.8356 , 'tl');

    $tables=Block('V', [
    Paragraph(
        Text([
            $pref,
            Null,
            $city,
            Null,
            $location,
            Null,
            $street,
            NewLine,
            $adrs2,
            NewLine,
            NewLine,
            Text("   ", $s_addr_name),
            Text($name1, $s_addr_name),
            Text(" 様", $s_addr_name),
        ], $s_address),
        PStyle(size => 65 * 2.8356 , align => 'm', linefeed => 12, preskip => 12.5, postskip => 12.5)),
    ], $bs_confidential);

    $tables->show($page[$n] , 30 * 2.8356 , 110 * 2.8356 , 'tl');

    my $parea = Shape();    
    $parea->line((10) * 2.8346 ,(74) * 2.8346 , (80) * 2.8346, 0, SStyle(linewidth => 1, strokecolor => $c_black));
    $parea->box((5) * 2.8346 ,(5) * 2.8346 , (90) * 2.8346, 65 * 2.8346, 's', SStyle(linewidth => 0.3, strokecolor => $c_black));
    $tables=Block('V', [
    Paragraph(
        Text([sprintf("登録内容: %s ", $reg_num),
            sprintf("%s",$name2),
            NewLine,
            sprintf("登録区分: %s",$reg_class) ,
            NewLine,
            ] ,$s_reg_num),
        PStyle(size => 80 * 2.8356 , align => 'l', linefeed => '120%', preskip => 12.5, postskip => 12.5)),
    ], $bs_confidential);
    $parea->obj($tables ,10 * 2.8356 , 60 * 2.8356 , 'tl');

    $parea->show($page[$n], 0, 0, 'bl');

}


for($n = 1; $n <= $page_max; $n ++){
}


    $sth = $db->prepare('SET @time=NOW()');
    $sth->execute();
    $sth = $db->prepare('SELECT
        bm.reg_number, bm.badge_name, pm.real_name, pm.real_name_f,
        CASE WHEN ps.status IS NULL THEN \'-\' ELSE ps.status END AS person_status,
        CASE WHEN ss.status IS NULL THEN \'-\' ELSE ss.status END AS person_status,
        CASE WHEN gs.status IS NULL THEN \'-\' ELSE gs.status END AS person_status,
        ps.class,cm.email,
        cm.zip_code, cm.addr_pref, cm.addr_city, cm.addr_location, cm.addr_street, cm.addr_building, cm.tel, cm.mobile,
        CASE WHEN pm.birthday > \'1991-09-03 00:00:00\' OR sm.class = \'C-C\'THEN 1 ELSE 0 END as child_flag
        FROM        ' . $prefix . 'person_master pm
        INNER JOIN    ' . $prefix . 'p_by_b b 
            ON pm.seq_number_p = b.seq_number_p
        INNER JOIN    ' . $prefix . 'p_by_a a
            ON pm.seq_number_p = a.seq_number_p
        INNER JOIN    ' . $prefix . 'badge_master bm
            ON bm.seq_number_b = b.seq_number_b
        INNER JOIN    ' . $prefix . 'contact_master cm
            ON cm.seq_number_a = a.seq_number_a
        LEFT JOIN    ' . $prefix . 'billing_table bt
            ON bt.seq_number_p = pm.seq_number_p
        LEFT JOIN(    ' . $prefix . 'person_status ps
        INNER JOIN    ' . $prefix . 'status_master sm
            ON  ps.class = sm.class
        )
            ON ps.seq_number_p = pm.seq_number_p
        LEFT JOIN    ' . $prefix . 'staff_status ss
            ON ss.seq_number_p = pm.seq_number_p
        LEFT JOIN    ' . $prefix . 'guest_status gs
            ON gs.seq_number_p = pm.seq_number_p
        LEFT JOIN    zip_pref_master zp
            ON cm.addr_pref = zp.pref
        WHERE 
            pm.ctime <= @time AND pm.dtime > @time
            AND
            b.ctime <= @time AND b.dtime > @time
            AND
            a.ctime <= @time AND a.dtime > @time
            AND
            cm.ctime <= @time AND cm.dtime > @time
            AND
            bm.ctime <= @time AND bm.dtime > @time
            AND
            (ps.seq_number IS NULL OR (ps.ctime <= @time AND ps.dtime > @time))
            AND
            (ss.seq_number IS NULL OR (ss.ctime <= @time AND ss.dtime > @time))
            AND
            (gs.seq_number IS NULL OR (gs.ctime <= @time AND gs.dtime > @time))
        GROUP BY  bm.reg_number
        ORDER BY  gs.status, child_flag, ss.status, ps.status, cm.zip_code, bm.reg_number
    ');
        
    $sth->execute();
    my (@row, $rec);
    while(@row = $sth->fetchrow_array){
        my ($reg_number, $badge_name, $real_name, $real_name_f,
        $person_status, $staff_status, $guest_status, $status_comment,$email,
        $zip_code, $pref, $city, $location, $street, $building, $tel, $mobile, $cflag ) = @row;

        Page_add($reg_number , $zip_code, $pref, $city, $location, $street ,$building,$real_name, $badge_name , $status_comment, sprintf("%s-%s-%1s%1s-%1s-%1s", $reg_number, $status_comment,$person_status, $staff_status, $guest_status, $cflag));

    }
    $sth->finish;
    $db->disconnect;

my    $sfile ="sfxx_pg1";
$sfile .= ".pdf";
    
print "Content-Type: application/pdf; name=\"$sfile\"\n";
print "Content-Disposition: attachment; filename=$sfile\n\n"; 
$doc->print('-');

    
print "Content-Type: application/pdf; name=\"$sfile\"\n";
print "Content-Disposition: attachment; filename=$sfile\n\n"; 
$doc->print('-');
exit;
1;
