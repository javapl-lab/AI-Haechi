contract MyContract {
    uint256 public number;
    fixed public sosu;

    function setNumber(uint256 __number) public {
        number = 9;
        number = 2;
        sosu = 1.2;

        if(number > 4)
            number = 2;
    }
}