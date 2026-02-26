// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title SIMSwapManager
 * @dev Manage SIM swap transactions and verification on blockchain
 */
contract SIMSwapManager {
    // Enums
    enum VerificationType {
        PERSONAL_DETAILS,
        BIOMETRIC,
        ID_DOCUMENT,
        SECURITY_QUESTIONS,
        BIOMETRIC_AND_ID
    }

    enum SwapStatus {
        PENDING,
        VERIFYING,
        APPROVED,
        COMPLETED,
        REJECTED
    }

    // Structs
    struct SIMSwap {
        bytes32 swapId;
        bytes32 phoneHash;
        bytes32 oldSimHash;
        bytes32 newSimHash;
        SwapStatus status;
        bool personalDetailsVerified;
        bool biometricVerified;
        bool idDocumentVerified;
        bool securityQuestionsVerified;
        address approver;
        uint256 timestamp;
    }

    // Events
    event SIMSwapInitiated(
        bytes32 indexed swapId,
        bytes32 indexed phoneHash,
        uint256 timestamp
    );

    event VerificationCompleted(
        bytes32 indexed swapId,
        VerificationType verificationType,
        uint256 timestamp
    );

    event SIMSwapApproved(
        bytes32 indexed swapId,
        address indexed approver,
        uint256 timestamp
    );

    // State variables
    mapping(bytes32 => SIMSwap) private swaps;
    mapping(bytes32 => bytes32[]) private userSwapHistory; // phoneHash => swapIds[]

    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    /**
     * @dev Initiate SIM swap
     * @param phoneHash Hash of phone number
     * @param oldSimHash Hash of old SIM serial
     * @param newSimHash Hash of new SIM serial
     * @return swapId Generated swap ID
     */
    function initiateSIMSwap(
        bytes32 phoneHash,
        bytes32 oldSimHash,
        bytes32 newSimHash
    ) external onlyOwner returns (bytes32) {
        require(phoneHash != bytes32(0), "Phone hash cannot be empty");
        require(newSimHash != bytes32(0), "New SIM hash cannot be empty");

        // Generate swap ID
        bytes32 swapId = keccak256(
            abi.encodePacked(phoneHash, newSimHash, block.timestamp)
        );

        // Create swap record
        swaps[swapId] = SIMSwap({
            swapId: swapId,
            phoneHash: phoneHash,
            oldSimHash: oldSimHash,
            newSimHash: newSimHash,
            status: SwapStatus.PENDING,
            personalDetailsVerified: false,
            biometricVerified: false,
            idDocumentVerified: false,
            securityQuestionsVerified: false,
            approver: address(0),
            timestamp: block.timestamp
        });

        // Add to user history
        userSwapHistory[phoneHash].push(swapId);

        emit SIMSwapInitiated(swapId, phoneHash, block.timestamp);

        return swapId;
    }

    /**
     * @dev Record verification completion
     * @param swapId Swap ID
     * @param verificationType Type of verification completed
     */
    function completeVerification(
        bytes32 swapId,
        VerificationType verificationType
    ) external onlyOwner {
        require(swaps[swapId].timestamp != 0, "Swap does not exist");

        SIMSwap storage swap = swaps[swapId];

        if (verificationType == VerificationType.PERSONAL_DETAILS) {
            swap.personalDetailsVerified = true;
        } else if (verificationType == VerificationType.BIOMETRIC) {
            swap.biometricVerified = true;
        } else if (verificationType == VerificationType.ID_DOCUMENT) {
            swap.idDocumentVerified = true;
        } else if (verificationType == VerificationType.SECURITY_QUESTIONS) {
            swap.securityQuestionsVerified = true;
        } else if (verificationType == VerificationType.BIOMETRIC_AND_ID) {
            swap.biometricVerified = true;
            swap.idDocumentVerified = true;
        }

        swap.status = SwapStatus.VERIFYING;

        emit VerificationCompleted(swapId, verificationType, block.timestamp);
    }

    /**
     * @dev Approve SIM swap (final step)
     * @param swapId Swap ID
     */
    function approveSIMSwap(bytes32 swapId) external onlyOwner {
        require(swaps[swapId].timestamp != 0, "Swap does not exist");

        SIMSwap storage swap = swaps[swapId];

        swap.status = SwapStatus.APPROVED;
        swap.approver = msg.sender;

        emit SIMSwapApproved(swapId, msg.sender, block.timestamp);
    }

    /**
     * @dev Get swap details
     * @param swapId Swap ID
     * @return Swap details
     */
    function getSwapDetails(bytes32 swapId) external view returns (SIMSwap memory) {
        require(swaps[swapId].timestamp != 0, "Swap does not exist");
        return swaps[swapId];
    }

    /**
     * @dev Get user's swap history
     * @param phoneHash Hash of phone number
     * @return Array of swap IDs
     */
    function getUserSwapHistory(bytes32 phoneHash) external view returns (bytes32[] memory) {
        return userSwapHistory[phoneHash];
    }
}