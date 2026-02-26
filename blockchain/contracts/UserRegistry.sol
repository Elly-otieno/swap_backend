// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title UserRegistry
 * @dev Store user identity hashes (simplified ZK proofs) on blockchain
 */
contract UserRegistry {
    // Events
    event UserRegistered(
        bytes32 indexed phoneHash,
        bytes32 identityHash,
        uint256 timestamp
    );

    event IdentityUpdated(
        bytes32 indexed phoneHash,
        bytes32 newIdentityHash,
        uint256 timestamp
    );

    // Mapping: phoneHash => identityHash
    mapping(bytes32 => bytes32) private identities;

    // Mapping: phoneHash => registration timestamp
    mapping(bytes32 => uint256) private registrationTimestamps;

    // Owner address (system wallet)
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    /**
     * @dev Register user identity hash
     * @param phoneHash Keccak256 hash of phone number
     * @param identityHash Keccak256 hash of biometric + ID data
     */
    function registerUser(
        bytes32 phoneHash,
        bytes32 identityHash
    ) external onlyOwner {
        require(identityHash != bytes32(0), "Identity hash cannot be empty");
        require(identities[phoneHash] == bytes32(0), "User already registered");

        identities[phoneHash] = identityHash;
        registrationTimestamps[phoneHash] = block.timestamp;

        emit UserRegistered(phoneHash, identityHash, block.timestamp);
    }

    /**
     * @dev Update user identity hash (e.g., after biometric update)
     * @param phoneHash Keccak256 hash of phone number
     * @param newIdentityHash New identity hash
     */
    function updateIdentity(
        bytes32 phoneHash,
        bytes32 newIdentityHash
    ) external onlyOwner {
        require(newIdentityHash != bytes32(0), "Identity hash cannot be empty");
        require(identities[phoneHash] != bytes32(0), "User not registered");

        identities[phoneHash] = newIdentityHash;

        emit IdentityUpdated(phoneHash, newIdentityHash, block.timestamp);
    }

    /**
     * @dev Get user identity hash
     * @param phoneHash Keccak256 hash of phone number
     * @return Identity hash
     */
    function getUserIdentity(bytes32 phoneHash) external view returns (bytes32) {
        return identities[phoneHash];
    }

    /**
     * @dev Check if user is registered
     * @param phoneHash Keccak256 hash of phone number
     * @return True if registered
     */
    function isUserRegistered(bytes32 phoneHash) external view returns (bool) {
        return identities[phoneHash] != bytes32(0);
    }

    /**
     * @dev Get registration timestamp
     * @param phoneHash Keccak256 hash of phone number
     * @return Timestamp of registration
     */
    function getRegistrationTimestamp(bytes32 phoneHash) external view returns (uint256) {
        return registrationTimestamps[phoneHash];
    }
}