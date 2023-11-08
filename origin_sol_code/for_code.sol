contract MyContract {

    function setNumber(uint256 __number) public {
        if(voided_bet || !race_end)
            return (false,bytes32(0));
    }
}