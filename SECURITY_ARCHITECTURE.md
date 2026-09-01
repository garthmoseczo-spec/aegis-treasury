# Security & Custody Architecture (Overview)

This document outlines recommended security architecture for a custodial deployment of Aegis Treasury. It is a high-level guide — consult a security architect for production designs.

1) Key separation and wallet tiers
- Cold wallets: offline, air-gapped, used for long-term storage. Use multi-signature and hardware signers.
- Hot wallets: online signing for day-to-day operations with strict rate limiting and monitoring.

2) KMS / HSM
- Store master keys in an HSM or cloud KMS (AWS KMS, Azure Key Vault with HSM-backed keys, or on-prem HSM).
- Use envelope encryption: data encrypted with data keys; data keys encrypted with KMS master key.

3) Access controls
- Strong RBAC, least privilege, audited access logs, and hardware MFA for administrative accounts.

4) Transaction approval workflow
- Multi-user approval for high-value transfers.
- Threshold signatures or multi-sig for moving funds from cold storage.

5) Monitoring & incident response
- Real-time monitoring of signing activity, anomaly detection, and automated alerting.
- Incident response plan including key compromise procedures and customer notification.

6) Compliance
- If custodial services run: KYC/AML processes, licensing checks, periodic audits, and insurance (custody insurance).

7) Testing
- External penetration tests and code audits before production.
