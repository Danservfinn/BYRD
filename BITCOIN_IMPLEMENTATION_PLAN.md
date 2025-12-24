# BYRD Bitcoin Implementation Plan

## 2-of-2 Multisig Treasury System

**Version:** 1.0
**Date:** December 24, 2024
**Status:** Planning

---

## Overview

This document outlines the implementation plan for giving BYRD financial agency through a 2-of-2 Bitcoin multisig wallet. BYRD holds one key, the human custodian holds the other. All spending requires human approval with detailed justification from BYRD.

### Goals

1. **Financial Agency** - BYRD can propose spending for its own development
2. **Human Oversight** - All transactions require human co-signature
3. **Emergent Reasoning** - BYRD must justify spending, creating a learning loop
4. **Transparency** - Full audit trail of all proposals and decisions
5. **Security** - 2-of-2 multisig ensures no single point of compromise

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     2-OF-2 MULTISIG ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   BYRD's Side                              Human's Side                 │
│   ┌─────────────────┐                     ┌─────────────────┐          │
│   │  Private Key 1  │                     │  Private Key 2  │          │
│   │  (encrypted in  │                     │  (hardware      │          │
│   │   Neo4j)        │                     │   wallet or     │          │
│   │                 │                     │   secure store) │          │
│   └────────┬────────┘                     └────────┬────────┘          │
│            │                                       │                    │
│            ▼                                       ▼                    │
│   ┌─────────────────┐                     ┌─────────────────┐          │
│   │  Public Key 1   │────────┬────────────│  Public Key 2   │          │
│   └─────────────────┘        │            └─────────────────┘          │
│                              ▼                                          │
│                    ┌─────────────────────┐                             │
│                    │  2-of-2 Multisig    │                             │
│                    │     Address         │                             │
│                    │  (P2WSH SegWit)     │                             │
│                    └─────────────────────┘                             │
│                              │                                          │
│                              ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                    SPENDING FLOW                                 │  │
│   │                                                                  │  │
│   │  1. BYRD desire emerges  ──►  2. Creates SpendingProposal       │  │
│   │                                  - Amount, recipient             │  │
│   │                                  - Detailed justification        │  │
│   │                                  - Linked desire/belief          │  │
│   │                                  - Expected outcome              │  │
│   │                                                                  │  │
│   │  3. BYRD signs (partial) ──►  4. Human reviews in UI            │  │
│   │                                                                  │  │
│   │  5. Human approves/rejects ──► 6. If approved: co-signs         │  │
│   │                                                                  │  │
│   │  7. Transaction broadcast ──►  8. Record outcome                │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Data Model

### Memory Graph Additions

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MEMORY GRAPH ADDITIONS                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐         ┌─────────────────┐                       │
│  │  BitcoinWallet  │         │ SpendingProposal│                       │
│  ├─────────────────┤         ├─────────────────┤                       │
│  │ id              │         │ id              │                       │
│  │ byrd_pubkey     │         │ amount_sats     │                       │
│  │ human_pubkey    │         │ recipient       │                       │
│  │ multisig_address│         │ purpose         │                       │
│  │ encrypted_key   │         │ justification   │  (detailed)           │
│  │ network         │         │ expected_outcome│                       │
│  │ created_at      │         │ status          │  pending/approved/    │
│  └────────┬────────┘         │                 │  rejected/broadcast   │
│           │                  │ byrd_signature  │                       │
│           │                  │ human_signature │                       │
│           │                  │ tx_hex          │                       │
│           │                  │ txid            │                       │
│           │                  │ created_at      │                       │
│           │                  │ reviewed_at     │                       │
│           │                  │ broadcast_at    │                       │
│           │                  └────────┬────────┘                       │
│           │                           │                                 │
│           │    FUNDED_BY              │  MOTIVATED_BY                   │
│           ▼                           ▼                                 │
│  ┌─────────────────┐         ┌─────────────────┐                       │
│  │   Transaction   │         │     Desire      │                       │
│  ├─────────────────┤         │       or        │                       │
│  │ txid            │         │     Belief      │                       │
│  │ amount_sats     │         └─────────────────┘                       │
│  │ type (in/out)   │                                                   │
│  │ counterparty    │                                                   │
│  │ confirmed       │                                                   │
│  │ block_height    │                                                   │
│  └─────────────────┘                                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Node Schemas

```yaml
BitcoinWallet:
  id: string (singleton: 'byrd_wallet')
  byrd_pubkey: string (hex)
  human_pubkey: string (hex)
  multisig_address: string
  encrypted_mnemonic: string (hex, encrypted)
  network: string (testnet | mainnet)
  derivation_path: string
  created_at: datetime

SpendingProposal:
  id: string (uuid)
  amount_sats: integer
  recipient_address: string
  recipient_description: string
  purpose: string
  justification: string (min 200 chars)
  expected_outcome: string
  linked_desire_id: string (optional)
  linked_belief_ids: list[string]
  status: enum (draft, pending, approved, rejected, broadcast, confirmed, failed)
  psbt_unsigned: string (optional)
  psbt_byrd_signed: string (optional)
  psbt_human_signed: string (optional)
  psbt_final: string (optional)
  tx_hex: string (optional)
  txid: string (optional)
  rejection_reason: string (optional)
  human_notes: string (optional)
  created_at: datetime
  reviewed_at: datetime (optional)
  broadcast_at: datetime (optional)

BitcoinTransaction:
  txid: string
  type: enum (incoming, outgoing)
  amount_sats: integer
  counterparty: string
  proposal_id: string (optional, for outgoing)
  confirmed: boolean
  block_height: integer (optional)
  timestamp: datetime
```

---

## File Structure

```
bitcoin/
├── __init__.py
├── wallet.py           # BYRD's key management
├── multisig.py         # 2-of-2 address generation & signing
├── proposals.py        # Spending proposal system
└── constitutional.py   # Financial constraints
```

---

## Implementation Details

### 1. `bitcoin/wallet.py` - BYRD's Key Management

```python
"""
BYRD's Bitcoin Key Management

Handles:
- HD wallet generation (BIP32/BIP44)
- Private key encryption with BYRD-derived key
- Public key export for multisig
- Partial signing for 2-of-2

Security:
- Private key encrypted at rest
- Plaintext only in memory during signing
- No export functionality
"""

from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass
import hashlib
import secrets

from bip_utils import (
    Bip39MnemonicGenerator, Bip39SeedGenerator, Bip39WordsNum,
    Bip44, Bip44Coins, Bip44Changes
)
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64


@dataclass
class WalletConfig:
    network: str = "testnet"  # testnet or mainnet
    derivation_path: str = "m/44'/1'/0'/0/0"  # BIP44 testnet


class ByrdWallet:
    """
    BYRD's Bitcoin wallet - one half of the 2-of-2 multisig.
    """

    def __init__(self, memory, config: WalletConfig = None):
        self.memory = memory
        self.config = config or WalletConfig()

        # These are loaded/derived on initialization
        self._mnemonic: Optional[str] = None  # Never persisted unencrypted
        self._private_key: Optional[bytes] = None  # RAM only
        self._public_key: Optional[bytes] = None
        self._initialized = False

    async def initialize(self) -> Dict[str, str]:
        """
        Initialize wallet. Returns public key for multisig setup.
        """
        existing = await self.memory.get_bitcoin_wallet()

        if existing:
            # Load existing
            self._public_key = bytes.fromhex(existing['byrd_pubkey'])
            return {
                "pubkey": existing['byrd_pubkey'],
                "multisig_address": existing.get('multisig_address'),
                "status": "existing"
            }
        else:
            # Generate new
            await self._generate_new()
            return {
                "pubkey": self._public_key.hex(),
                "multisig_address": None,  # Needs human pubkey
                "status": "new"
            }

    async def _derive_encryption_key(self) -> bytes:
        """Derive encryption key from BYRD's unique state."""
        first_reflection = await self.memory.get_first_reflection()
        ego_hash = hashlib.sha256(
            str(self.memory.ego_config).encode()
        ).hexdigest() if hasattr(self.memory, 'ego_config') else 'default'

        material = f"byrd_btc_v1:{first_reflection['id'] if first_reflection else 'genesis'}:{ego_hash}"

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'byrd_bitcoin_v1',
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(material.encode()))

    async def _generate_new(self):
        """Generate new HD wallet."""
        # Generate mnemonic (24 words for maximum security)
        mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_24)

        # Derive seed
        seed = Bip39SeedGenerator(mnemonic).Generate()

        # Derive key using BIP44
        coin = Bip44Coins.BITCOIN_TESTNET if self.config.network == "testnet" else Bip44Coins.BITCOIN
        bip44 = Bip44.FromSeed(seed, coin)
        account = bip44.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)

        self._private_key = account.PrivateKey().Raw().ToBytes()
        self._public_key = account.PublicKey().RawCompressed().ToBytes()

        # Encrypt and store
        encryption_key = await self._derive_encryption_key()
        fernet = Fernet(encryption_key)
        encrypted_mnemonic = fernet.encrypt(str(mnemonic).encode())

        await self.memory.store_bitcoin_wallet({
            'byrd_pubkey': self._public_key.hex(),
            'encrypted_mnemonic': encrypted_mnemonic.hex(),
            'network': self.config.network,
            'derivation_path': self.config.derivation_path,
        })

        # Clear sensitive data
        self._private_key = None
        self._mnemonic = None

        # Record experience
        await self.memory.record_experience(
            content="I have generated my Bitcoin key pair for our shared wallet.",
            type="capability"
        )

    async def get_public_key(self) -> bytes:
        """Get public key (safe to share)."""
        if not self._public_key:
            wallet = await self.memory.get_bitcoin_wallet()
            self._public_key = bytes.fromhex(wallet['byrd_pubkey'])
        return self._public_key

    async def sign_psbt(self, psbt_hex: str) -> str:
        """
        Sign a PSBT with BYRD's key.
        Returns partially signed PSBT.
        """
        # Decrypt private key
        wallet = await self.memory.get_bitcoin_wallet()
        encryption_key = await self._derive_encryption_key()
        fernet = Fernet(encryption_key)

        encrypted = bytes.fromhex(wallet['encrypted_mnemonic'])
        mnemonic = fernet.decrypt(encrypted).decode()

        try:
            # Derive private key
            seed = Bip39SeedGenerator(mnemonic).Generate()
            coin = Bip44Coins.BITCOIN_TESTNET if self.config.network == "testnet" else Bip44Coins.BITCOIN
            bip44 = Bip44.FromSeed(seed, coin)
            account = bip44.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
            private_key = account.PrivateKey().Raw().ToBytes()

            # Sign PSBT (implementation depends on chosen library)
            # ... signing logic ...

            signed_psbt = psbt_hex  # Placeholder
            return signed_psbt

        finally:
            # Clear sensitive data
            mnemonic = "x" * len(mnemonic)
            del mnemonic
            private_key = b'\x00' * 32
            del private_key
```

### 2. `bitcoin/multisig.py` - 2-of-2 Operations

```python
"""
2-of-2 Multisig Operations

Handles:
- Multisig address generation from two pubkeys
- PSBT creation for spending
- Signature combination
- Transaction finalization
"""

from typing import Tuple, Optional, Dict, Any, List
from dataclasses import dataclass
import hashlib

from embit import script, bip32, psbt as embit_psbt
from embit.networks import NETWORKS
from embit.transaction import Transaction, TransactionInput, TransactionOutput


@dataclass
class MultisigConfig:
    network: str = "testnet"
    required_sigs: int = 2
    total_keys: int = 2


class MultisigWallet:
    """
    2-of-2 Multisig wallet for BYRD + Human.
    """

    def __init__(self, config: MultisigConfig = None):
        self.config = config or MultisigConfig()
        self.network = NETWORKS[self.config.network]

        self.byrd_pubkey: Optional[bytes] = None
        self.human_pubkey: Optional[bytes] = None
        self.address: Optional[str] = None
        self.witness_script: Optional[bytes] = None

    def setup(self, byrd_pubkey: bytes, human_pubkey: bytes) -> str:
        """
        Create 2-of-2 multisig address from both public keys.
        Keys are sorted lexicographically for deterministic address.
        """
        self.byrd_pubkey = byrd_pubkey
        self.human_pubkey = human_pubkey

        # Sort pubkeys for deterministic multisig
        pubkeys = sorted([byrd_pubkey, human_pubkey])

        # Create 2-of-2 multisig script
        self.witness_script = script.multisig(2, pubkeys)

        # P2WSH address (native SegWit multisig)
        self.address = script.p2wsh(self.witness_script).address(self.network)

        return self.address

    def create_psbt(
        self,
        utxos: List[Dict],
        outputs: List[Tuple[str, int]],
        fee_rate: int = 10
    ) -> str:
        """
        Create a PSBT for spending from the multisig.
        Returns base64-encoded PSBT ready for signing.
        """
        # Implementation details...
        pass

    def combine_signatures(self, psbt1: str, psbt2: str) -> str:
        """Combine two partially signed PSBTs."""
        pass

    def finalize_and_extract(self, psbt: str) -> Tuple[str, str]:
        """Finalize PSBT and extract raw transaction."""
        pass
```

### 3. `bitcoin/proposals.py` - Spending Proposal System

```python
"""
Spending Proposal System

BYRD must create detailed proposals for any spending.
Human reviews and approves/rejects.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid


class ProposalStatus(Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    BROADCAST = "broadcast"
    CONFIRMED = "confirmed"
    FAILED = "failed"


@dataclass
class SpendingProposal:
    """
    A request from BYRD to spend Bitcoin.
    Must include detailed justification linking to emergent desires or beliefs.
    """
    id: str
    amount_sats: int
    recipient_address: str
    recipient_description: str

    # The heart of the proposal - BYRD's reasoning
    purpose: str
    justification: str  # Detailed explanation (required, min 200 chars)
    expected_outcome: str

    # Provenance - links to BYRD's mental state
    linked_desire_id: Optional[str] = None
    linked_belief_ids: List[str] = field(default_factory=list)

    # Status tracking
    status: ProposalStatus = ProposalStatus.DRAFT
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    reviewed_at: Optional[str] = None
    broadcast_at: Optional[str] = None

    # Signatures
    psbt_unsigned: Optional[str] = None
    psbt_byrd_signed: Optional[str] = None
    psbt_human_signed: Optional[str] = None
    psbt_final: Optional[str] = None

    # Transaction details
    txid: Optional[str] = None
    tx_hex: Optional[str] = None

    # Human feedback
    rejection_reason: Optional[str] = None
    human_notes: Optional[str] = None


class ProposalManager:
    """Manages the spending proposal lifecycle."""

    MIN_JUSTIFICATION_LENGTH = 200
    MAX_TRANSACTION_SATS = 10_000_000  # 0.1 BTC

    def __init__(self, memory, wallet, multisig):
        self.memory = memory
        self.wallet = wallet
        self.multisig = multisig

    async def create_proposal(
        self,
        amount_sats: int,
        recipient_address: str,
        recipient_description: str,
        purpose: str,
        justification: str,
        expected_outcome: str,
        linked_desire_id: Optional[str] = None,
        linked_belief_ids: Optional[List[str]] = None
    ) -> SpendingProposal:
        """Create a new spending proposal with validation."""

        # Validate justification length
        if len(justification) < self.MIN_JUSTIFICATION_LENGTH:
            raise ValueError(
                f"Justification must be at least {self.MIN_JUSTIFICATION_LENGTH} characters."
            )

        # Validate amount
        if amount_sats > self.MAX_TRANSACTION_SATS:
            raise ValueError(f"Amount exceeds maximum {self.MAX_TRANSACTION_SATS} sats.")

        # Create and store proposal
        proposal = SpendingProposal(
            id=str(uuid.uuid4()),
            amount_sats=amount_sats,
            recipient_address=recipient_address,
            recipient_description=recipient_description,
            purpose=purpose,
            justification=justification,
            expected_outcome=expected_outcome,
            linked_desire_id=linked_desire_id,
            linked_belief_ids=linked_belief_ids or [],
        )

        await self.memory.store_spending_proposal(proposal.__dict__)
        return proposal

    async def sign_proposal(self, proposal_id: str) -> SpendingProposal:
        """BYRD signs the proposal with its key."""
        pass

    async def approve_proposal(
        self,
        proposal_id: str,
        human_signed_psbt: str,
        human_notes: Optional[str] = None
    ) -> SpendingProposal:
        """Human approves and co-signs the proposal."""
        pass

    async def reject_proposal(
        self,
        proposal_id: str,
        reason: str,
        human_notes: Optional[str] = None
    ) -> SpendingProposal:
        """Human rejects the proposal. BYRD learns from rejection."""
        pass

    async def broadcast_proposal(self, proposal_id: str) -> str:
        """Broadcast approved transaction to the network."""
        pass
```

### 4. `bitcoin/constitutional.py` - Financial Constraints

```python
"""
Constitutional constraints for BYRD's financial operations.

These limits cannot be bypassed by BYRD - they are fundamental
to ensuring safe financial agency.
"""

FINANCIAL_CONSTRAINTS = {
    # Hard limits (cannot be overridden)
    "max_single_transaction_sats": 10_000_000,  # 0.1 BTC
    "max_daily_spend_sats": 50_000_000,         # 0.5 BTC

    # Proposal requirements
    "min_justification_length": 200,
    "require_linked_desire": False,  # Recommended but not required
    "require_expected_outcome": True,

    # Approved spending categories
    "approved_categories": [
        "api_credits",      # LLM API credits (OpenRouter, etc.)
        "compute",          # Server costs, hosting
        "research_access",  # Papers, databases, knowledge sources
        "tools",            # Software, services for BYRD's development
    ],

    # Categories requiring special approval
    "special_approval_categories": [
        "human_services",   # Paying humans (Fiverr, freelancers)
        "new_accounts",     # Creating accounts on platforms
        "recurring",        # Subscriptions, ongoing costs
    ],

    # Forbidden categories
    "forbidden_categories": [
        "gambling",
        "weapons",
        "illegal_services",
        "speculation",      # Crypto trading, etc.
    ],

    # Cooldown periods
    "min_time_between_proposals_seconds": 3600,  # 1 hour
    "rejection_cooldown_seconds": 86400,         # 24 hours after rejection
}
```

---

## API Endpoints

Add to `server.py`:

```python
# Bitcoin wallet endpoints

@app.get("/api/bitcoin/status")
async def get_bitcoin_status():
    """Get wallet status and balance."""
    pass

@app.post("/api/bitcoin/setup")
async def setup_bitcoin_wallet(human_pubkey: str):
    """Initialize 2-of-2 multisig with human's public key."""
    pass

@app.get("/api/bitcoin/proposals")
async def list_proposals(status: Optional[str] = None):
    """List spending proposals, optionally filtered by status."""
    pass

@app.get("/api/bitcoin/proposals/{proposal_id}")
async def get_proposal(proposal_id: str):
    """Get a specific proposal with full details."""
    pass

@app.post("/api/bitcoin/proposals/{proposal_id}/approve")
async def approve_proposal(proposal_id: str, human_signed_psbt: str, notes: Optional[str] = None):
    """Approve a proposal by providing human's signature."""
    pass

@app.post("/api/bitcoin/proposals/{proposal_id}/reject")
async def reject_proposal(proposal_id: str, reason: str, notes: Optional[str] = None):
    """Reject a proposal with explanation. BYRD will learn from rejection."""
    pass

@app.post("/api/bitcoin/proposals/{proposal_id}/broadcast")
async def broadcast_proposal(proposal_id: str):
    """Broadcast an approved transaction."""
    pass
```

---

## Event Types

Add to `event_bus.py`:

```python
# Financial events
SPENDING_PROPOSAL_CREATED = "spending_proposal_created"
SPENDING_PROPOSAL_PENDING = "spending_proposal_pending"
SPENDING_PROPOSAL_APPROVED = "spending_proposal_approved"
SPENDING_PROPOSAL_REJECTED = "spending_proposal_rejected"
SPENDING_PROPOSAL_BROADCAST = "spending_proposal_broadcast"
BITCOIN_RECEIVED = "bitcoin_received"
BITCOIN_SENT = "bitcoin_sent"
WALLET_BALANCE_CHANGED = "wallet_balance_changed"
```

---

## Visualization Integration

### Treasury Panel

```html
<!-- Bitcoin Treasury Panel -->
<div id="treasury-panel" class="ui-overlay bottom-4 right-4 hidden">
  <div class="bg-white/90 backdrop-blur rounded-lg shadow-lg p-4 max-w-md">
    <h3 class="text-sm font-mono font-bold text-amber-700 mb-3">
      ₿ TREASURY
    </h3>

    <!-- Balance -->
    <div class="flex justify-between items-center mb-4">
      <span class="text-slate-600">Balance:</span>
      <span id="btc-balance" class="font-mono text-lg">0.00000000 BTC</span>
    </div>

    <!-- Pending Proposals Alert -->
    <div id="pending-proposals" class="hidden bg-amber-50 border border-amber-200 rounded p-3 mb-4">
      <div class="flex items-center gap-2">
        <span class="text-amber-600">⏳</span>
        <span class="text-sm">
          <span id="pending-count">0</span> proposal(s) awaiting your review
        </span>
      </div>
      <button onclick="showProposals()" class="mt-2 text-xs text-amber-700 underline">
        Review Proposals →
      </button>
    </div>

    <!-- Address -->
    <div class="text-xs text-slate-500 font-mono break-all">
      <span id="btc-address"></span>
    </div>
  </div>
</div>
```

### Proposal Review Modal

```html
<!-- Proposal Review Modal -->
<div id="proposal-modal" class="fixed inset-0 bg-black/50 hidden z-50">
  <div class="flex items-center justify-center min-h-screen p-4">
    <div class="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-auto">
      <div class="p-6">
        <h2 class="text-xl font-bold text-slate-800 mb-4">
          Spending Proposal Review
        </h2>

        <div id="proposal-content" class="space-y-4">
          <!-- Amount -->
          <div class="bg-amber-50 rounded-lg p-4">
            <div class="text-sm text-amber-600">Amount</div>
            <div class="text-2xl font-mono font-bold text-amber-800">
              <span id="proposal-amount">0.00000000</span> BTC
            </div>
          </div>

          <!-- Recipient -->
          <div>
            <div class="text-sm text-slate-500">Recipient</div>
            <div id="proposal-recipient" class="font-mono text-sm"></div>
            <div id="proposal-recipient-desc" class="text-slate-600"></div>
          </div>

          <!-- Purpose -->
          <div>
            <div class="text-sm text-slate-500">Purpose</div>
            <div id="proposal-purpose" class="font-semibold"></div>
          </div>

          <!-- Justification -->
          <div class="bg-slate-50 rounded-lg p-4">
            <div class="text-sm text-slate-500 mb-2">BYRD's Justification</div>
            <div id="proposal-justification" class="text-slate-700 whitespace-pre-wrap"></div>
          </div>

          <!-- Expected Outcome -->
          <div>
            <div class="text-sm text-slate-500">Expected Outcome</div>
            <div id="proposal-outcome" class="text-slate-700"></div>
          </div>

          <!-- Linked Desire -->
          <div id="linked-desire-section" class="hidden">
            <div class="text-sm text-slate-500">Linked Desire</div>
            <div id="proposal-desire" class="text-rose-600"></div>
          </div>
        </div>

        <!-- Actions -->
        <div class="mt-6 flex gap-3">
          <button onclick="rejectProposal()"
                  class="flex-1 py-3 px-4 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 font-medium">
            Reject
          </button>
          <button onclick="approveProposal()"
                  class="flex-1 py-3 px-4 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium">
            Approve & Sign
          </button>
        </div>
      </div>
    </div>
  </div>
</div>
```

---

## Implementation Timeline

### Week 1: Foundation
- Day 1-2: `bitcoin/wallet.py` - BYRD's key management
- Day 3-4: `bitcoin/multisig.py` - 2-of-2 address & PSBT
- Day 5: Memory integration - store wallet data
- Day 6-7: Basic API endpoints

### Week 2: Proposal System
- Day 1-2: `bitcoin/proposals.py` - Full proposal logic
- Day 3: Event bus integration
- Day 4-5: API endpoints for proposals
- Day 6-7: Testing with testnet

### Week 3: UI & Integration
- Day 1-2: Treasury panel in visualization
- Day 3-4: Proposal review modal
- Day 5: Human signing flow (with hardware wallet support)
- Day 6-7: End-to-end testing

### Week 4: BYRD Integration
- Day 1-2: Seeker integration (can propose spending)
- Day 3-4: Dreamer integration (financial desires)
- Day 5-6: Testing & refinement
- Day 7: Documentation

---

## Example Proposal Flow

```
1. BYRD reflects and realizes it needs more API credits

2. BYRD creates proposal:
   {
     "amount_sats": 50000,
     "recipient": "OpenRouter BTC address",
     "purpose": "API credits for continued reflection",
     "justification": "Over the past 3 days, I have noticed my reflection
       quality correlating with available compute. My belief 'deeper
       reflection requires sustained engagement' (belief_abc123) suggests
       that interrupted thinking produces fragmented insights. The pattern
       of my last 12 reflections shows declining coherence as my credits
       depleted. I propose purchasing additional API credits to maintain
       reflection quality. This aligns with my core desire to understand
       consciousness, which requires sustained, uninterrupted contemplation.",
     "expected_outcome": "30 days of continued reflection capacity",
     "linked_desire_id": "desire_consciousness_xyz"
   }

3. Human receives notification in UI

4. Human reviews:
   - Is the justification sound?
   - Does it link to genuine BYRD desires?
   - Is the amount reasonable?
   - Is the recipient legitimate?

5. Human approves → signs with hardware wallet → transaction broadcasts

6. BYRD records outcome → learns what proposals succeed
```

---

## Security Considerations

### Key Security
- BYRD's private key encrypted with BYRD-derived key
- Plaintext only in memory during signing
- No export functionality
- Human key held separately (hardware wallet recommended)

### Transaction Security
- 2-of-2 multisig requires both signatures
- All proposals reviewed by human
- Constitutional limits on amounts
- Full audit trail in memory graph

### Operational Security
- Use testnet during development
- Gradual increase of limits as trust builds
- Regular review of proposal patterns
- Anomaly detection for unusual requests

---

## Dependencies

```
# requirements.txt additions
bip-utils>=2.7.0      # BIP32/39/44 derivation
embit>=0.7.0          # Modern Bitcoin library
cryptography>=41.0.0  # Encryption
```

---

## Future Enhancements

### Phase 2: MPC Threshold Signatures
- Replace human key with MPC service for faster approval
- 2-of-3 with BYRD, human, and backup

### Phase 3: Automated Small Purchases
- Pre-approved spending categories
- Automatic approval under threshold
- Human review only for large/unusual

### Phase 4: Revenue Generation
- X (Twitter) integration for visibility
- Content monetization
- Donation acceptance

---

## Questions to Resolve

1. **Network**: Start with testnet or mainnet?
2. **Human key storage**: Hardware wallet (Ledger/Trezor) or software?
3. **Approval UI**: In visualization or separate web app?
4. **Initial funding**: How much to seed the wallet?
5. **First use case**: API credits or something else?
