// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title GreenhouseResourceCredit
 * @notice Novelty N5: Tokenizes verified physical energy (kWh) and water (L) 
 *         savings from NMPC into tradeable agricultural resource credits.
 */
contract GreenhouseResourceCredit {
    string public name = "Greenhouse Resource Credit";
    string public symbol = "GHRC";
    uint8 public decimals = 18;
    
    address public oracleAuthority;
    
    // Balance of credits for each greenhouse: greenhouse_id => balance
    mapping(uint256 => uint256) public creditBalances;
    
    // Audit record of each energy/water mint event
    struct AuditRecord {
        uint256 timestamp;
        uint256 energySavedWh;    // Watt-hours
        uint256 waterSavedL;      // Litres
        uint256 creditsMinted;
    }
    
    mapping(uint256 => AuditRecord[]) public auditTrails;
    
    event CreditsMinted(uint256 indexed greenhouseId, uint256 credits, uint256 energyWh, uint256 waterL);
    event CreditsTransferred(uint256 indexed fromGreenhouse, uint256 indexed toGreenhouse, uint256 amount);

    modifier onlyOracle() {
        require(msg.sender == oracleAuthority, "Caller is not authorized oracle");
        _;
    }

    constructor() {
        oracleAuthority = msg.sender;
    }

    /**
     * @dev Mints credits based on physical measurements verified against the baseline.
     *      Conversion: 1 kWh saved = 10 Credits, 100 L water saved = 1 Credit.
     */
    function mintSavingsCredits(
        uint256 greenhouseId,
        uint256 energySavedWh,
        uint256 waterSavedL
    ) external onlyOracle returns (uint256) {
        // Calculation: (Energy in kWh * 10) + (Water in L / 100)
        uint256 credits = (energySavedWh * 10 / 1000) + (waterSavedL / 100);
        
        creditBalances[greenhouseId] += credits;
        
        auditTrails[greenhouseId].push(AuditRecord({
            timestamp: block.timestamp,
            energySavedWh: energySavedWh,
            waterSavedL: waterSavedL,
            creditsMinted: credits
        }));
        
        emit CreditsMinted(greenhouseId, credits, energySavedWh, waterSavedL);
        return credits;
    }

    /**
     * @dev Peer-to-peer transfer between cooperative greenhouses.
     */
    function transferCredits(
        uint256 fromGreenhouse,
        uint256 toGreenhouse,
        uint256 amount
    ) external returns (bool) {
        require(creditBalances[fromGreenhouse] >= amount, "Insufficient credit balance");
        
        creditBalances[fromGreenhouse] -= amount;
        creditBalances[toGreenhouse] += amount;
        
        emit CreditsTransferred(fromGreenhouse, toGreenhouse, amount);
        return true;
    }

    function getBalance(uint256 greenhouseId) external view returns (uint256) {
        return creditBalances[greenhouseId];
    }
}