#!/usr/bin/perl
use strict;
use warnings;
use utf8;

use PDFJ 'UTF8';
use Readonly;

# --定数--
Readonly my $MM2POINT => 72 / 25.4 ; # 1ポ = 1/72インチ 1インチ=25.4mm
my $page_width = 100 * $MM2POINT;
my $page_height = 148 * $MM2POINT;

my %ss_text = (
    red     => SStyle(fillcolor => Color('#ff0000')),
    black   => SStyle(fillcolor => Color('#000000')),
    gray    => SStyle(fillcolor => Color('#7f7f7f')),
);

my %ss_line = (
    normal  => SStyle(linewidth =>   1, strokecolor => Color('#000000')),
    harf    => SStyle(linewidth => 0.5, strokecolor => Color('#000000')),
    thin    => SStyle(linewidth => 0.3, strokecolor => Color('#000000')),
    dash    => SStyle(linedash => [2,2]),
);

my %psTbl = (
    head    => PStyle( size => 40 * $MM2POINT, align => 'W', linefeed => 12,
                       preskip => 12.5, postskip => 12.5 ),
    mark_u  => PStyle( size => 28 * $MM2POINT, align => 'm', linefeed => 12,
                       preskip => 12.5, postskip => 12.5),
    mark_d  => PStyle( size => 28 * $MM2POINT, align => 'm', linefeed => 15,
                       preskip => 12.5, postskip => 12.5),
    zipcode => PStyle( size => 45 * $MM2POINT, align => 'l', linefeed => 12,
                       preskip => 12.5, postskip => 12.5),
    from    => PStyle( size => 80 * $MM2POINT, align => 'l', linefeed => 9,
                       preskip => 12.5, postskip => 12.5),
    dear    => PStyle( size => 70 * $MM2POINT, align => 'm', linefeed => 12,
                       preskip => 12.5, postskip => 12.5),
    info_l  => PStyle( size => 20 * $MM2POINT, align => 'l', linefeed => '115%',
                       preskip => 1, postskip => 1, blockalign => 'm' ),
    info_r  => PStyle( size => 60 * $MM2POINT, align => 'l', linefeed => '115%',
                       preskip => 1, postskip => 1, blockalign => 'm' ),
);

my %bsTbl = (
    table   => BStyle( adjust => 1 ),
    addrbox => BStyle( padding => 0, align => 'b', withbox => 'f', 
                       height => 15,
                       withboxstyle => SStyle(fillcolor => Color('#ffffff')) ),
    info_e  => BStyle( padding => 1, align => 'b', withbox => 'f',
                       withboxstyle => SStyle(fillcolor => Color(0.83)),
                       rowskip=> '2', colskip => '5', height => 10,
                       align => 'lm' ),
    info_o  => BStyle( padding => 1, align => 'b', withbox => 'f',
                       withboxstyle => SStyle(fillcolor => Color(0.93)),
                       rowskip=> '2', colskip => '5', height => 10,
                       align => 'lm' ),
);

my %tsTbl; # 後で作成

# main
#  PDF作成
my $doc = PDFJ::Doc->new(1.3, $page_width, $page_height);
$doc->add_info(Title => 'sfcon PageList ', Author => '<admin@sfcon.jp>');

# PDF属性定義(font設定はPDF作成後でないと定義できない)
my $f_mt = $doc->new_font('Ryumin-Light', 'UniJIS-UCS2-HW-H',
                          'Times-Roman', 'WinAnsiEncoding', 1.05);
my $f_gh = $doc->new_font('GothicBBB-Medium', 'UniJIS-UCS2-HW-H',
                          'Helvetica', 'WinAnsiEncoding', 1.05);

%tsTbl = (
    head            => TStyle( font => $f_gh, fontsize => 7,
                               shapestyle => $ss_text{black}),
    mark_u          => TStyle( font => $f_gh, fontsize => 9.5,
                               shapestyle => $ss_text{black}),
    mark_d          => TStyle( font => $f_gh, fontsize => 14,
                               shapestyle => $ss_text{black}),
    zipcode         => TStyle( font => $f_gh, fontsize => 22,
                               shapestyle => $ss_text{red}),
    from            => TStyle( font => $f_gh, fontsize => 8,
                               shapestyle => $ss_text{red}, ),
    address         => TStyle( font => $f_mt, fontsize => 10,
                               shapestyle => $ss_text{red},
                               align => 'b', ),
    address_name    => TStyle( font => $f_mt, fontsize => 16,
                               shapestyle => $ss_text{red},
                               align => 'b', ),
    dear            => TStyle( font => $f_mt, fontsize => 10,
                               shapestyle => $ss_text{black},
                               align => 'b', ),
    info_l          => TStyle( font => $f_gh, fontsize => 6,
                               shapestyle => $ss_text{black} ),
    info_r          => TStyle( font => $f_gh, fontsize => 8,
                               shapestyle => $ss_text{red} ),
    info_rs         => TStyle( font => $f_gh, fontsize => 6,
                               shapestyle => $ss_text{red}),
);

my %person_info = (
    from_addr           => 'xxx-xxxx XX郵便局留置',
    from_name           => '第xx回日本SF大会hogehoge実行委員会',
    contact_zip_code    => '[郵便番号]',
    contact_pref        => '[住所県名]',
    contact_city        => '[住所市名]',
    contact_location    => '[住所地名]',
    contact_street      => '[住所番地]',
    contact_building    => '[住所ビル]',
    contact_name        => '[姓名]',
    reg_number          => '[登録番号]',
    status_name2        => '[登録区分]',
    person_status       => '[参加登録状態]',
    staff_status        => '[スタッフ登録状態]',
    badge_name          => '[バッジネーム]',
    real_name           => '[氏名]',
    birthday            => '[生年月日]',
    sex                 => '[性別]',
    contact_email       => '[電子メール]',
    contact_tel         => '[電話番号]',
    contact_mobile      => '[携帯電話番号]',
    contact_e_name      => '[緊急連絡先]',
    contact_e_relation  => '[緊急連絡先続柄]',
    contact_e_contact   => '[緊急連絡先電話]',
    ai1_info            => '[自主企画]',
    ai2_info            => '[ディーラーズルーム]',
    ai4_info            => '[公式合宿]',
);

foreach my $cnt (0..1) {
    Page_add_new( $doc->new_page, \%person_info);
}
$doc->print('-');
exit;

# sub
sub Page_add_new {
    my ($page_object, $person_info) = @_;

    my $tables;

#--固定部分--
#  ヘッダ
    $tables=Block('V',
        [ Paragraph( Text(['郵便はがき'], $tsTbl{head} ),
                     $psTbl{head} ),
        ], $bsTbl{table});
    $tables->show($page_object, 30 * $MM2POINT, 143 * $MM2POINT, 'tl');
#  消印
    my $stamp = Shape();
    $tables=Block('V',
        [ Paragraph( Text(['郵便局'], $tsTbl{mark_u} ),
                     $psTbl{mark_u} ),
        ], $bsTbl{table});
    $stamp->obj($tables, 0,18 * $MM2POINT,'bl');
    $tables=Block('V',
        [ Paragraph( Text(['料金後納',NewLine,'郵便'], $tsTbl{mark_d} ),
                     $psTbl{mark_d} ),
        ], $bsTbl{table});
    $stamp->obj($tables, 0,15 * $MM2POINT,'tl');
    $stamp->circle( 14 * $MM2POINT, 14 * $MM2POINT, 13 * $MM2POINT, 's','',
                    $ss_line{normal});
    $stamp->line( (1+13-12.65) * $MM2POINT, (14 +3) * $MM2POINT,
                  (12.65 * 2) * $MM2POINT, 0,
                  $ss_line{harf} );
    $stamp->show($page_object, 10, 400, 'tl');

# --大会ごと固定--
#  差出人
    $tables=Block('V',
        [ Paragraph( Text( [ '差出人 ',
                             $person_info->{from_addr},
                             NewLine,
                             '　　　 ',
                             $person_info->{from_name},
                           ], $tsTbl{from} ),
                     $psTbl{from} ),
        ], $bsTbl{table});
    $tables->show($page_object, 15 * $MM2POINT, 76 * $MM2POINT, 'bl');

# --各ページ異なる部分--
#  郵便番号
    $tables=Block('V',
        [ Paragraph( Text( [ $person_info->{contact_zip_code}
                           ], $tsTbl{zipcode} ),
                     $psTbl{zipcode} ),
        ], $bsTbl{table});
    $tables->show($page_object, 55 * $MM2POINT, 138 * $MM2POINT, 'tl');
#  宛先住所氏名
    $tables=Block('V',
        [ Paragraph( Text( [ Text( $person_info->{contact_pref},
                                   $tsTbl{address} ),
                             Null,
                             Text( $person_info->{contact_city},
                                   $tsTbl{address} ),
                             Null,
                             Text( $person_info->{contact_location},
                                   $tsTbl{address} ),
                             Null,
                             Text( $person_info->{contact_street},
                                   $tsTbl{address} ),
                             NewLine,
                             Text( $person_info->{contact_building},
                                   $tsTbl{address} ),
                             NewLine,
                             NewLine,
                             Text( '    ', $tsTbl{address_name} ),
                             Text( $person_info->{contact_name},
                                   $tsTbl{address_name} ),
                             ' 様',
                           ],
                           $tsTbl{dear} ),
                     $psTbl{dear} ),
        ], $bsTbl{addrbox} );
    $tables->show($page_object, 25 * $MM2POINT, 110 * $MM2POINT, 'tl');
#  参加者情報
    my $parea = Shape();
    $parea->line( (10) * $MM2POINT, (74) * $MM2POINT, (80) * $MM2POINT, 0,
                  $ss_line{normal});
    $parea->box( (5) * $MM2POINT, (5) * $MM2POINT, (90) * $MM2POINT, 65 * $MM2POINT, 's',
                  $ss_line{thin});

    my $box_offset_x = 10 * $MM2POINT;
    my $box_offset_y = 65 * $MM2POINT;
    $tables=Block('H',
        [ Paragraph( Text(['登録番号'], $tsTbl{info_l}), $psTbl{info_l} ),
          Paragraph( Text([$person_info->{reg_number}], $tsTbl{info_r}),
                     $psTbl{info_r} )
        ],
        , $bsTbl{info_e});
    $parea->obj($tables, $box_offset_x, $box_offset_y, 'tl');
    $box_offset_y -= $tables->height;

    $tables=Block('H',
        [ Paragraph( Text(['登録区分'], $tsTbl{info_l}), $psTbl{info_l} ),
          Paragraph( Text([$person_info->{status_name2}], $tsTbl{info_r}),
                     $psTbl{info_r})
        ],
        , $bsTbl{info_o});
    $parea->obj($tables, $box_offset_x, $box_offset_y, 'tl');
    $box_offset_y -= $tables->height;

    $tables=Block('H',
        [ Paragraph( Text(['参加登録状態'], $tsTbl{info_l}), $psTbl{info_l}),
          Paragraph( Text([$person_info->{person_status}], $tsTbl{info_r}),
                     $psTbl{info_r})
        ],
        , $bsTbl{info_e});
    $parea->obj($tables, $box_offset_x, $box_offset_y, 'tl');
    $box_offset_y -= $tables->height;

    $tables=Block('H',
        [ Paragraph( Text(['スタッフ登録状態'], $tsTbl{info_l}), $psTbl{info_l}),
          Paragraph( Text([$person_info->{staff_status}], $tsTbl{info_r}),
                     $psTbl{info_r})
        ],
        , $bsTbl{info_o});
    $parea->obj($tables, $box_offset_x, $box_offset_y, 'tl');
    $box_offset_y -= $tables->height;

    $tables=Block('H',
        [ Paragraph( Text(['バッジネーム'], $tsTbl{info_l}), $psTbl{info_l}),
          Paragraph( Text([$person_info->{badge_name}], $tsTbl{info_r}),
                     $psTbl{info_r})
        ],
        , $bsTbl{info_e});
    $parea->obj($tables, $box_offset_x, $box_offset_y, 'tl');
    $box_offset_y -= $tables->height;

    $tables=Block('H',
        [ Paragraph( Text(['氏名'], $tsTbl{info_l}), $psTbl{info_l}),
          Paragraph( Text([$person_info->{real_name}], $tsTbl{info_r}),
                     $psTbl{info_r})
        ],
        , $bsTbl{info_o});
    $parea->obj($tables , $box_offset_x, $box_offset_y, 'tl');
    $box_offset_y -= $tables->height;

    $tables=Block('H',
        [ Paragraph( Text(['生年月日・性別'], $tsTbl{info_l}), $psTbl{info_l}),
          Paragraph( Text( [ $person_info->{birthday},
                            ' / ',
                            $person_info->{sex}
                           ],
                           $tsTbl{info_r}),
                     $psTbl{info_r})
        ],
        , $bsTbl{info_e});
    $parea->obj($tables, $box_offset_x, $box_offset_y, 'tl');
    $box_offset_y -= $tables->height;

    $tables=Block('H',
        [ Paragraph( Text(['電子メール'], $tsTbl{info_l}), $psTbl{info_l}),
          Paragraph( Text([$person_info->{contact_email}], $tsTbl{info_r}),
                     $psTbl{info_r})
        ],
        , $bsTbl{info_o});
    $parea->obj($tables, $box_offset_x, $box_offset_y, 'tl');
    $box_offset_y -= $tables->height;

    $tables=Block('H',
        [ Paragraph( Text(['電話番号'], $tsTbl{info_l}), $psTbl{info_l}),
          Paragraph( Text([$person_info->{contact_tel}], $tsTbl{info_r}),
                     $psTbl{info_r})
        ],
        , $bsTbl{info_e});
    $parea->obj($tables, $box_offset_x, $box_offset_y, 'tl');
    $box_offset_y -= $tables->height;

    $tables=Block('H',
        [ Paragraph( Text(['携帯電話番号'], $tsTbl{info_l}), $psTbl{info_l}),
          Paragraph( Text([$person_info->{contact_mobile}], $tsTbl{info_r}),
                     $psTbl{info_r})
        ],
        , $bsTbl{info_o});
    $parea->obj($tables, $box_offset_x, $box_offset_y, 'tl');
    $box_offset_y -= $tables->height;

    $tables=Block('H',
        [ Paragraph( Text(['緊急連絡先'], $tsTbl{info_l}), $psTbl{info_l} ),
          Paragraph( Text([ '氏名',
                            $person_info->{contact_e_name},
                            NewLine,
                            '続柄',
                            $person_info->{contact_e_relation},
                            NewLine,
                            '電話',
                            $person_info->{contact_e_contact}
                          ], $tsTbl{info_rs}
                         ), $psTbl{info_r}
                   )
        ],
        , $bsTbl{info_e});
    $parea->obj($tables, $box_offset_x, $box_offset_y, 'tl');
    $box_offset_y -= $tables->height;

    $tables=Block('H',
        [ Paragraph( Text(['自主企画'], $tsTbl{info_l}), $psTbl{info_l}),
          Paragraph( Text([$person_info->{ai1_info}], $tsTbl{info_r}),
                     $psTbl{info_r})
        ],
        , $bsTbl{info_o});
    $parea->obj($tables, $box_offset_x, $box_offset_y, 'tl');
    $box_offset_y -= $tables->height;

    $tables=Block('H',
        [ Paragraph( Text(['ディーラーズルーム'], $tsTbl{info_l}),
                     $psTbl{info_l}),
          Paragraph( Text([$person_info->{ai2_info}], $tsTbl{info_r}),
                     $psTbl{info_r})
        ],
        , $bsTbl{info_e});
    $parea->obj($tables, $box_offset_x, $box_offset_y, 'tl');
    $box_offset_y -= $tables->height;

    $tables=Block('H',
        [ Paragraph( Text(['公式合宿'], $tsTbl{info_l}), $psTbl{info_l}),
          Paragraph( Text([$person_info->{ai4_info}], $tsTbl{info_r}),
                     $psTbl{info_r})
        ],
        , $bsTbl{info_o});
    $parea->obj($tables, $box_offset_x, $box_offset_y, 'tl');
    $box_offset_y -= $tables->height;

    $parea->show($page_object, 0, 0, 'bl');
}

1;
