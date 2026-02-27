// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title AccessControl
 * @dev Manage agent permissions on blockchain
 */
contract AccessControl {
    // Role definitions
    bytes32 public constant AGENT_ROLE = keccak256("AGENT_ROLE");
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant SYSTEM_ROLE = keccak256("SYSTEM_ROLE");

    // Events
    event RoleGranted(
        bytes32 indexed role,
        address indexed account,
        address indexed sender,
        uint256 timestamp
    );

    event RoleRevoked(
        bytes32 indexed role,
        address indexed account,
        address indexed sender,
        uint256 timestamp
    );

    // State variables
    mapping(bytes32 => mapping(address => bool)) private roles;
    mapping(address => string) private agentTypes;

    address public owner;

    constructor() {
        owner = msg.sender;
        // Grant admin role to owner
        _grantRole(ADMIN_ROLE, msg.sender);
        _grantRole(SYSTEM_ROLE, msg.sender);
    }

    modifier onlyRole(bytes32 role) {
        require(hasRole(role, msg.sender), "Access denied: insufficient permissions");
        _;
    }

    /**
     * @dev Grant role to account
     * @param role Role to grant
     * @param account Account address
     */
    function grantRole(bytes32 role, address account) external onlyRole(ADMIN_ROLE) {
        _grantRole(role, account);
    }

    /**
     * @dev Grant agent role with type
     * @param account Agent address
     * @param agentType Type of agent (MPESA_AGENT, BRAND_AMBASSADOR, CARE_CENTER)
     */
    function grantAgentRole(
        address account,
        string memory agentType
    ) external onlyRole(ADMIN_ROLE) {
        _grantRole(AGENT_ROLE, account);
        agentTypes[account] = agentType;
    }

    /**
     * @dev Revoke role from account
     * @param role Role to revoke
     * @param account Account address
     */
    function revokeRole(bytes32 role, address account) external onlyRole(ADMIN_ROLE) {
        require(account != owner, "Cannot revoke owner's roles");
        _revokeRole(role, account);
    }

    /**
     * @dev Check if account has role
     * @param role Role to check
     * @param account Account address
     * @return True if account has role
     */
    function hasRole(bytes32 role, address account) public view returns (bool) {
        return roles[role][account];
    }

    /**
     * @dev Get agent type
     * @param account Agent address
     * @return Agent type string
     */
    function getAgentType(address account) external view returns (string memory) {
        return agentTypes[account];
    }

    // Internal functions
    function _grantRole(bytes32 role, address account) private {
        if (!roles[role][account]) {
            roles[role][account] = true;
            emit RoleGranted(role, account, msg.sender, block.timestamp);
        }
    }

    function _revokeRole(bytes32 role, address account) private {
        if (roles[role][account]) {
            roles[role][account] = false;
            emit RoleRevoked(role, account, msg.sender, block.timestamp);
        }
    }
}