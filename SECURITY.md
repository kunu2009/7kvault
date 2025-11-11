# Security Policy

## Overview

7K Vault takes security seriously. This document outlines our security practices and how to report vulnerabilities.

## Encryption Details

### Algorithm
- **Encryption**: AES-256 in CBC mode via Fernet (cryptography library)
- **Key Derivation**: PBKDF2-HMAC-SHA256
- **Iterations**: 100,000 (prevents brute force attacks)
- **Salt**: 16-byte random salt (unique per installation)

### Password Storage
- Passwords are **NEVER** stored in plain text
- Only SHA-256 hash of password is stored
- Salt is unique per installation
- No password recovery possible (by design)

### Data Storage
- All media files encrypted before storage
- File metadata encrypted in `media_index.enc`
- Encrypted files use random UUIDs for filenames
- Original filenames only accessible after decryption

## Security Best Practices

### For Users

1. **Strong Password**
   - Use at least 12 characters
   - Mix uppercase, lowercase, numbers, symbols
   - Don't use dictionary words
   - Don't reuse passwords from other services

2. **Password Management**
   - Write down password in a safe place
   - Use a password manager
   - **Never forget your password** - files are unrecoverable

3. **Vault Security**
   - Keep vault folder (`%USERPROFILE%\.secure_vault\`) secure
   - Don't share vault folder without password
   - Lock vault when not in use
   - Consider encrypting backup copies

4. **System Security**
   - Keep Windows updated
   - Use antivirus software
   - Encrypt your hard drive (BitLocker)
   - Use strong Windows password

### For Developers

1. **Code Review**
   - All security-related code requires review
   - Use established cryptography libraries only
   - Never implement custom encryption

2. **Dependencies**
   - Keep cryptography library updated
   - Monitor for security advisories
   - Use trusted packages only

3. **Testing**
   - Test encryption/decryption thoroughly
   - Test password validation
   - Test file deletion security
   - Test for memory leaks (decrypted data)

## Known Limitations

### 🔴 Critical Limitations

1. **No Password Recovery**
   - Forget password = lost data forever
   - This is intentional for security
   - No backdoors exist

2. **In-Memory Decryption**
   - Files decrypted to memory when viewing
   - RAM could be dumped by sophisticated attackers
   - Close viewer when not actively using

3. **Temporary Files**
   - Videos create temp files for playback
   - Deleted after viewing but may persist in disk
   - SSD TRIM may not secure-delete immediately

4. **Python Source**
   - Running from source exposes logic
   - Compiled EXE offers minor obfuscation
   - Not protection against determined reverse engineering

### 🟡 Medium Limitations

1. **Brute Force Protection**
   - 100,000 PBKDF2 iterations slows attacks
   - Still vulnerable to dictionary attacks
   - Use strong, unique passwords

2. **File Metadata**
   - File sizes can leak information
   - Creation dates in vault folder
   - Number of files is visible

3. **Auto-Import Folder**
   - Briefly exposes unencrypted files
   - Files encrypted quickly but not instant
   - Consider manual import for sensitive files

## Threat Model

### ✅ Protects Against

- **Casual snooping**: Family, friends accessing your PC
- **Stolen hard drive**: Without Windows password
- **Malware scanning**: Files are encrypted at rest
- **Cloud sync**: Encrypted files safe to sync
- **Accidental exposure**: Won't appear in file searches

### ⚠️ Limited Protection

- **Sophisticated malware**: Keyloggers can capture password
- **Memory dumps**: Decrypted files in RAM briefly
- **Physical access**: With Windows password compromised
- **State-level actors**: This is not military-grade vault

### ❌ Does NOT Protect Against

- **Keyloggers**: Can capture your password
- **Screen capture**: Can see decrypted media
- **Coercion**: Someone forcing you to open vault
- **Forensics**: Experts may recover temp files
- **Rubber hose cryptanalysis**: Physical threats

## Reporting Vulnerabilities

### What to Report

- Security vulnerabilities in code
- Cryptography implementation issues
- Authentication bypass bugs
- Data exposure issues
- Denial of service vulnerabilities

### What NOT to Report

- Feature requests (use GitHub Issues)
- "Forgot password" as a vulnerability
- Social engineering attacks
- Physical security of user's computer

### How to Report

**For sensitive security issues:**

1. **Do NOT** open a public GitHub issue
2. **Contact**: Email through GitHub profile
3. **Provide**: Detailed description, steps to reproduce
4. **Wait**: Give us time to fix before public disclosure

**For minor issues:**
- Open a GitHub issue with label `security`

### Response Timeline

- **Initial Response**: Within 48 hours
- **Fix Timeline**: Depends on severity
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium: Within 30 days
  - Low: Next release
- **Public Disclosure**: After fix is released

## Security Updates

### How Updates Are Distributed

1. Fix is developed and tested
2. Version number is bumped
3. GitHub Release is published
4. Users notified via README

### Staying Updated

- **Watch** the GitHub repository
- **Star** to get notifications
- Check for updates monthly
- Read release notes

## Audit History

### Self-Audits

- **Initial Release**: December 2025
- **Last Review**: December 2025
- **Next Review**: Scheduled quarterly

### External Audits

- No formal external audits yet
- Open source code available for review
- Community contributions welcome

## Security Acknowledgments

We thank security researchers who responsibly disclose vulnerabilities.

**Hall of Fame** (coming soon):
- [Your name here?]

## Compliance

### GDPR

- No data collected
- No telemetry or analytics
- Everything stored locally
- User has complete control

### Data Protection

- AES-256 is approved for classified data
- PBKDF2 is NIST recommended
- Implementation follows best practices

## Recommendations

### For Personal Use ✅

7K Vault is suitable for:
- Hiding personal photos/videos
- Protecting private documents
- Privacy from family/friends
- Basic security needs

### For Business Use ⚠️

Consider professional solutions for:
- Company confidential data
- Legal/medical records
- Financial information
- Regulated industries

### For High-Security Needs ❌

Use specialized solutions for:
- Government classified data
- Witness protection
- Journalism in oppressive regimes
- Life-threatening situations

## Additional Resources

- [Cryptography Library Docs](https://cryptography.io/)
- [OWASP Password Guidelines](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-3/)

---

**Remember**: Security is only as strong as the weakest link. Use strong passwords, keep your system secure, and understand the limitations.

*Last Updated: December 2025*
