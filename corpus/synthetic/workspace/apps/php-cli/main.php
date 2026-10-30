<?php

require __DIR__ . '/../../packages/php-lib/src/Price.php';

use DcFixture\Price;

$price = new Price(12.5, 'EUR');
echo $price->format(), PHP_EOL;

// Dynamic call: static analysis must not report this edge as resolved.
$method = getenv('DC_METHOD') ?: 'format';
echo call_user_func([$price, $method]), PHP_EOL;
