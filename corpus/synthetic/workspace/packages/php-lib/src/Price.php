<?php

namespace DcFixture;

class Price
{
    private $amount;
    private $currency;

    public function __construct($amount, $currency)
    {
        $this->amount = $amount;
        $this->currency = $currency;
    }

    public function format()
    {
        return sprintf('%.2f %s', $this->amount, $this->currency);
    }
}
