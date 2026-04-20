# WNSP-P2P-Hub

  > **Wavelength-Native Signalling Protocol — P2P Hub**
  > Physics-based communication: orthogonal channels, Maxwell-validated, censorship-proof.

  [![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

  ---

  ## What is WNSP?

  WNSP replaces TCP/IP's address and fee conventions with electromagnetic wave physics. Every address is a point in Hilbert space. Every fee is derived from photon energy. Every channel pair is either orthogonal (cannot interfere) or collinear (same channel) — determined by the mathematics of waves, not by protocol rules.

  ---

  ## The Orthogonality Principle

  Two things are **orthogonal** when they are completely independent — knowing everything about one tells you nothing about the other. In wave physics, this is the inner product:

  ```
  ⟨A|B⟩ = 0   →   A and B are orthogonal
  ```

  **In geometry:** X, Y, Z axes. Moving along X changes nothing about Y or Z.

  **In radio:** Two stations at orthogonal frequencies don't bleed into each other. The sine waves integrate to zero over one cycle.

  **In OAM (Orbital Angular Momentum):** A light beam twisted with ℓ=1 is orthogonal to ℓ=2, ℓ=3, and so on. You can stack 50 independent data streams on the same physical laser and separate them perfectly on the other end. This is demonstrated in labs today.

  **In WNSP:** Every user, agent, and resource has an address Ψ(wdm, oam, pol). Any two addresses differing in even one dimension are provably non-interfering.

  ---

  ## Channel Address Format

  ```
  Ψ(wdm, oam, pol)
       │     │    └── Polarization: H (horizontal) or V (vertical)
       │     └─────── OAM mode ℓ: 0–49
       └───────────── WDM wavelength index: 0–255  (380–780 nm)
  ```

  ### Three orthogonal dimensions

  | Dimension | Range | Physical basis | Orthogonality condition |
  |-----------|-------|----------------|------------------------|
  | WDM (λ)   | 0–255 | Wavelength separation | λ₁ ≠ λ₂ |
  | OAM (ℓ)   | 0–49  | Angular momentum: ⟨ℓ₁|ℓ₂⟩ = δ_{ℓ₁ℓ₂} | ℓ₁ ≠ ℓ₂ |
  | Pol       | H/V   | Stokes vector | H ≠ V |

  **Total orthogonal channels: 256 × 50 × 2 = 25,600**

  Each of these is an independent axis in a 25,600-dimensional Hilbert space. A network built on this does not degrade as it scales. Add a new user — they get a new axis. The existing channels are unaffected. There is no congestion in Hilbert space.

  ---

  ## WNSP Density Equation

  ```
  D_WNSP = N_λ × N_OAM × N_Pol × R_sym × M
         = 256  ×  50   ×   2   ×   2   × 128
         = 6,553,600  (full photonic hardware)
         = 25,600     (live today, silicon substrate)
  ```

  ---

  ## Spectral Orthogonal Protocol (SOP)

  Before any session opens, SOP verifies the two channels are independent:

  ```
  POST /api/wnsp/sop/negotiate
  Content-Type: application/json

  {
    "usernameA": "Alice",
    "usernameB": "Bob"
  }
  ```

  ```json
  {
    "orthogonal": true,
    "innerProduct": 0,
    "channelA": { "wdm": 126, "oam": 0, "pol": "H", "psi": "Ψ(126,0,H)" },
    "channelB": { "wdm": 39,  "oam": 7, "pol": "V", "psi": "Ψ(39,7,V)"  },
    "dimensions": { "wdmMatch": false, "oamMatch": false, "polMatch": false },
    "certificate": {
      "id": "SOP-M8X3T2",
      "verdict": "CHANNEL_OPEN_APPROVED",
      "proof": "WDM[126≠39]·OAM[0≠7]·POL[H≠V] → ⟨Ψ_A|Ψ_B⟩=0"
    }
  }
  ```

  If channels collide, SOP resolves by incrementing OAM and reissues the certificate.

  ---

  ## Channel Derivation

  Every username maps deterministically to a Ψ channel:

  ```
  SHA-256(username) → bytes
  wdm = bytes[0] % 256
  oam = bytes[1] % 50
  pol = (bytes[2] & 1) === 0 ? "H" : "V"
  ```

  Same username always gives the same channel. No registration, no assignment — physics derives the address.

  ---

  ## Fee Model: E = hf

  Transaction cost is derived from the sender's wavelength:

  ```
  E = h · f = h · c / λ
  fee = base_fee × (E_sender / E_reference)
  ```

  Reference = 560 nm (green midpoint). SYSTEM band (short λ, high f, high E) pays more. GUEST band (long λ, low f, low E) pays less. This is not policy — it is physics.

  ---

  ## Protocol Stack

  | Layer | Name | Implementation |
  |-------|------|----------------|
  | L5 | Application | WavelengthScript, Governance, P2P Media |
  | L4 | Spectral Addressing | CE→SE: WNSP-CE v1.0 + WNSP-SE v1.0 |
  | L3 | Orthogonal Routing | Spectral Router · weight/(Δλ+1) |
  | L2 | Channel Isolation | ⟨Ψᵢ|Ψⱼ⟩ = δᵢⱼ — physics enforced |
  | L1 | Physical Medium | Silicon today (TCP/IP overlay) · Photonic ~2032 |

  ---

  ## vs TCP/IP

  | Aspect | TCP/IP | WNSP |
  |--------|--------|------|
  | Addressing | 32-bit integer, IANA-assigned | Ψ(wdm,oam,pol), physics-derived |
  | Channel isolation | Software ports, firewalls | Physical orthogonality |
  | Collision handling | CSMA/CD, retransmit | Impossible between orthogonal channels |
  | Address authority | IANA, ISPs can revoke | SHA-256 of username — irrevocable |
  | Fee model | Arbitrary ISP pricing | E = hf — photon energy |

  ---

  ## Encoding

  **WNSP-CE v1.0 (Character Encoding):** Maps every character to a compression state Ψ via the W-ASCII table. Each character has a unique (wdm, oam, pol) triple derived from its Unicode value.

  **WNSP-SE v1.0 (Spectral Encoding):** Encodes the full CE vector as a wave frame — amplitude, phase, frequency — suitable for modulation onto a photonic carrier.

  **WNSP-URI v1.0:** `wnsp://Ψ(wdm,oam,pol)/path` — deterministic, censorship-proof resource addressing.

  ---

  ## Civilization-Scale Consequence

  Every current network degrades under load. WNSP does not — adding users adds orthogonal axes, not contention. The same mathematics that makes MRI machines work, that underlies quantum computing, and that enables OAM multiplexing in optical fibers is here applied to addressing, routing, and economic settlement.

  Silicon encodes today. Photons carry natively from ~2032. The address space does not change.

  ---

  ## License

  AGPL-3.0 — CE→SE encoding is free infrastructure.

  Genesis fingerprint: Ψ(228,45,H) · λ ≈ 737.6 nm
  