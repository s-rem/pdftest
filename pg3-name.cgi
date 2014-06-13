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
our $page_width = 210 * 2.8346;
our $page_height = 297 * 2.8346;
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

my %pdf_font = {};
$pdf_font{'h'} = $f_h;
$pdf_font{'t'} = $f_m;
$pdf_font{'m'} = $f_m;
$pdf_font{'mt'} = $f_mt;
$pdf_font{'mv'} = $f_mv;
$pdf_font{'mtv'} = $f_mtv;
$pdf_font{'g'} = $f_g;
$pdf_font{'gh'} = $f_gh;
$pdf_font{'gv'} = $f_gv;
$pdf_font{'ghv'} = $f_ghv;
$pdf_font{'si'} = $f_si;

my %pdf_color = {};
$pdf_color{'black'} = Color('#000000');
$pdf_color{'darkblue'} = Color('#191970');
$pdf_color{'cadetblue'} = Color('#5f9ea0');
$pdf_color{'lightcyan'} = Color('#e0ffff');
$pdf_color{'white'} = Color(1);
$pdf_color{'darktgray'} = Color(0.2);
$pdf_color{'gray'} = Color(0.5);
$pdf_color{'lightgray'} = Color(0.97);
$pdf_color{'red'} = Color(1,0,0);

my $ss_red = SStyle(fillcolor => $c_red);
my $ss_darkblue = SStyle(fillcolor => $c_darkblue);
my $ss_white = SStyle(fillcolor => $c_white);
my $ss_black = SStyle(fillcolor => $pdf_color{'black'});
my $ss_gray = SStyle(fillcolor => $c_gray);
my $ss_dash = SStyle(linedash => [2,2]);

my %pdf_shapestyle = {};
$pdf_shapestyle{'black'} =  SStyle(fillcolor => $pdf_color{'black'});
$pdf_shapestyle{'gray'} =  SStyle(fillcolor => $pdf_color{'gray'});
$pdf_shapestyle{'dash'} =  SStyle(linedash => [2,2]);


my %pdf_textstyle = {};
$pdf_textstyle{'address'}  = TStyle(font => $pdf_font{'mt'}, fontsize => 10, 
    shapestyle => $pdf_shapestyle{'black'}, align => 'b');
$pdf_textstyle{'address_name'}  = TStyle(font => $pdf_font{'mt'}, fontsize => 16, 
    shapestyle => $pdf_shapestyle{'black'}, align => 'b');


sub Page_add_new_nenga {
    my ($person_info, $page_num) = @_;
    $page_num = 0;
    ;
    my ($name2_1, $name2_2, $name2_3);
    my $page_object = $doc->new_page;
    my $tables;

    my $bs_table = BStyle(adjust => 1);
    my $bs_addressbox = 
        BStyle(padding => 0, align => "b", withbox => "f", 
            height => 15,
            withboxstyle => 
            SStyle(fillcolor => $c_white));

    $tables=Block('V', [
    Paragraph(
        Text([
            $person_info->{'contact_zip_code'},
            NewLine,
            $person_info->{'contact_pref'},
            Null,
            $person_info->{'contact_city'},
            Null,
            $person_info->{'contact_location'},
            Null,
            $person_info->{'contact_street'},
            NewLine,
            $person_info->{'contact_building'},
            NewLine,
            NewLine,
            Text("    ", $pdf_textstyle{'address_name'}),
            Text($person_info->{'contact_name'}, $pdf_textstyle{'address_name'}),
            " 様",
        ], $pdf_textstyle{'address'}),
        PStyle(size => 70 * 2.8356 , align => 'm', linefeed => 12, preskip => 12.5, postskip => 12.5)),
    ], $bs_addressbox);

    $tables->show($page_object , 70 * 2.8356 , 290 * 2.8356 , 'tl');

    my $ts_infobox_all = TStyle(font => $f_gh, fontsize => 6, shapestyle => $pdf_shapestyle{'black'});
    my $ps_infobox_all = PStyle(size => 80 * 2.8356 , align => 'l', linefeed => '115%', preskip => 1, postskip => 1, blockalign => "m");
    my $ts_infobox_l = TStyle(font => $f_gh, fontsize => 6, shapestyle => $pdf_shapestyle{'black'});
    my $ps_infobox_l = PStyle(size => 20 * 2.8356 , align => 'l', linefeed => '115%', preskip => 1, postskip => 1, blockalign => "m");
    my $ts_infobox_r = TStyle(font => $f_gh, fontsize => 8, shapestyle => $pdf_shapestyle{'black'});
    my $ps_infobox_r = PStyle(size => 60 * 2.8356 , align => 'l', linefeed => '115%', preskip => 1, postskip => 1, blockalign => "m");
    my $bs_infobox_e   = BStyle(padding => 1, align => "b", withbox => "f", 
        withboxstyle => SStyle(fillcolor => Color(0.83)),
        rowskip=> "2", colskip => "5", height => 10, align => "lm" );
    my $bs_infobox_o   = BStyle(padding => 1, align => "b", withbox => "f", 
        withboxstyle => SStyle(fillcolor => Color(0.93)),
        rowskip=> "2", colskip => "5", height => 10, align => "lm" );
    my $bs_infobox_n   = BStyle(padding => 1, align => "b", withbox => "f", 
        withboxstyle => SStyle(fillcolor => Color(1.00)),
        rowskip=> "2", colskip => "5", height => 10, align => "lm" );

    my $parea = Shape();
    #$parea->line((10) * 2.8346 ,(74) * 2.8346 , (80) * 2.8346, 0, SStyle(linewidth => 1, strokecolor => $c_black));
    $parea->box((5) * 2.8346 ,(5) * 2.8346 , (90) * 2.8346, 23 * 2.8346, 's', SStyle(linewidth => 0.3, strokecolor => $c_black));
    my $box_offset_x = 10 * 2.8356;
    my $box_offset_y = 25 * 2.8356;
    $tables=Block('H',
        [Paragraph(Text(["星雲賞投票権は下記の方がお持ちです"]     ,$ts_infobox_all) ,$ps_infobox_all)],
    , $bs_infobox_n);
    $parea->obj($tables ,$box_offset_x , $box_offset_y , 'tl');
    $box_offset_y -= $tables->height;

    $tables=Block('H',
        [Paragraph(Text(["登録番号"]     ,$ts_infobox_l) ,$ps_infobox_l),Paragraph(Text([$person_info->{'reg_number'}]   ,$ts_infobox_r) ,$ps_infobox_r)],
    , $bs_infobox_e);
    $parea->obj($tables ,$box_offset_x , $box_offset_y , 'tl');
    $box_offset_y -= $tables->height;

    $tables=Block('H',
        [Paragraph(Text(["登録区分"]     ,$ts_infobox_l) ,$ps_infobox_l),Paragraph(Text([$person_info->{'status_name2'}] ,$ts_infobox_r) ,$ps_infobox_r)],
    , $bs_infobox_o);
    $parea->obj($tables ,$box_offset_x , $box_offset_y , 'tl');
    $box_offset_y -= $tables->height;

    $tables=Block('H',
        [Paragraph(Text(["バッジネーム"] ,$ts_infobox_l) ,$ps_infobox_l),Paragraph(Text([$person_info->{'badge_name'}]     ,$ts_infobox_r) ,$ps_infobox_r)],
    , $bs_infobox_e);
    $parea->obj($tables ,$box_offset_x , $box_offset_y , 'tl');
    $box_offset_y -= $tables->height;

    $tables=Block('H',
        [Paragraph(Text(["氏名"]         ,$ts_infobox_l) ,$ps_infobox_l),Paragraph(Text([$person_info->{'real_name'}]     ,$ts_infobox_r) ,$ps_infobox_r)],
    , $bs_infobox_o);
    $parea->obj($tables ,$box_offset_x , $box_offset_y , 'tl');
    $box_offset_y -= $tables->height;

    $parea->show($page_object, 0, 0, 'bl');


}


# main

my $dbaccess = SFCON::Register_db->new();
my @status;

if($reg_number_req){
    @status = $dbaccess->get_member_list_ext("bm.reg_number = ? AND sm.status_send = 1", $reg_number_req);
} else {
    $reg_number_req = "all";
    @status = $dbaccess->get_member_list_ext("sm.status_send = 1" );
}
my $result = shift (@status);
if ($result) {
    if($result != 0){
        while (my $person_info = shift (@status)){
            Page_add_new_nenga($person_info, $n);
            $n ++ ;
        }
        my    $sfile ="sfcon_pg3";
        $sfile .= "_" . $reg_number_req . ".pdf";
        if($result > 0){
            print "Content-Type: application/octet-stream; name=\"$sfile\"\n";
            print "Content-Disposition: attachment; filename=$sfile\n";
        } else {
            print "Content-Type: application/pdf\n";
        }
        print "\n"; 
        $doc->print('-');
    } else {
        error("Error", "投票権がないか登録番号が間違っています");
    }
} else {
    error("Error", shift (@status));
}
exit;
1;
