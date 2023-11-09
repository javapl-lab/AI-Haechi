pragma solidity ^0.4.24;
contract BREBuy {
    
    struct ContractParam {
        uint32  totalSize ; 
        uint256 singlePrice;
        uint8  pumpRate;
        bool hasChange;
    }
    
    address owner = 0x0;
    uint32  gameIndex = 0;
    uint256 totalPrice= 0;
    bool isLock = false;
    ContractParam public setConfig;
    ContractParam public curConfig;
    
    address[] public addressArray = new address[](0);
                    
    event openLockEvent();
    event addPlayerEvent(uint32 gameIndex,address player);
    event gameOverEvent(uint32 gameIndex,uint32 totalSize,uint256 singlePrice,uint8 pumpRate,address winAddr,uint overTime);
    event stopGameEvent(uint totalBalace,uint totalSize,uint price);
          
     
    constructor ( uint32 _totalSize,
                  uint256 _singlePrice
    )  public  {
        owner = msg.sender;
        setConfig = ContractParam(_totalSize,_singlePrice * 1 finney ,5,false);
        curConfig = ContractParam(_totalSize,_singlePrice * 1 finney ,5,false);
        startNewGame();
    }

    modifier onlyOwner {
        require(msg.sender == owner,"only owner can call this function");
        _;
    }
    
     modifier notLock {
        require(isLock == false,"contract current is lock status");
        _;
    }
    
    function isNotContract(address addr) private view returns (bool) {
        uint size;
        assembly { size := extcodesize(addr) }
        return size <= 0;
    }

    function updateLock(bool b) onlyOwner public {
        
        require(isLock != b," updateLock new status == old status");
       
        isLock = b;
       
        if(isLock) {
            stopGame();
        }else{
            startNewGame();
            emit openLockEvent();
        }
    }
}