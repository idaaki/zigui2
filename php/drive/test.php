<?php
require_once ("../pqs/dbg/dbg.php");
require_once './vendor/autoload.php';
require_once './Client.php';

// require_once './profiler.php';

use Goutte\Client;

$client = new Client();

$crawler = $client->request('GET', 'http://jptolx20305/drv/final3NG_files/result.htm');

$crawler->filter('title')->each(function($node)
{
    echo trim($node->text()) . "<br>";
    echo "<hr>";
});

$crawler->filter('span.saitenkekka')->each(function($node)
{
    echo trim($node->text()) . "<br>";
    echo "<hr>";
});
// <td valign="top" width="570">

$cnt = 0;
$subcnt = 0;
$illus = false;

$crawler->filterXPath('//td[contains(@valign, "top")]')->each(function($node) use(&$cnt, &$illus, &$subcnt) {
    $ctx  = "";
    $hrkn = "";
    $type = "";

    $node->filter('pre.font14pt')->each(function($txt) use (&$ctx)
    {
        // utf8: ？ (EFBC9F) to ?
        // $tmp = str_replace("\xef\xbc\x9f", "?", mb_convert_kana($txt->text(), "s", "UTF-8"));
        // utf8: whitespace from "&nbsp;" to C2A0
        $tmp = str_replace("\xc2\xa0", " ", mb_convert_kana($txt->text(), "s", "UTF-8"));
        $ctx .= trim($tmp);
    });

    $node->filter('pre.font8pt')->each(function($txt) use (&$hrkn)
    {
        $hrkn = trim($txt->text());
    });

    // echo "hirakana" . $hrkn . "<br>";
    if (!empty($ctx)) {
        if (strpos($ctx, "\xef\xbc\x9f") !== false) {
            $illus = true;
            $subcnt = 0;
        } else {
            $type = $cnt % 2? "Answer: ": "Question: ";
        }

        // illustration
        if ($illus) {
            if ($subcnt == 0) {
                $type = "Question: ";
            } else if ($subcnt % 2 == 0) {
                $type = "Sub-Question: ";
            } else if ($subcnt == 7) {
                    $type = "Answer: ";
                    $illus = false;
            }
            $subcnt++; // +1
        }
        $cnt++;
        // Not illustration
        if ($subcnt % 2 || $subcnt == 0 || $subcnt == 8)
            echo $type. $ctx . "<br>";
    }

  
    /*
    static $cnt = 0;
    $ctx =trim($node->text());

    if ($cnt == 0)
        echo "Question: <br>";
    else if ($cnt == 1)
        echo "Answer: <br>";

    if (strpos($ctx, '。') !== false) {
        $cnt++;
    }
    echo $ctx . "<br>";
    if ($cnt == 2) {
        echo "<hr>";
        $cnt = 0;
    }
    */
});
