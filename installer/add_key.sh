XCODE_KEYCHAIN="${XCODE_KEYCHAIN:-build}"
security import cert.cer -k ~/Library/Keychains/$XCODE_KEYCHAIN -T /usr/bin/codesign
security import key.p12 -k ~/Library/Keychains/$XCODE_KEYCHAIN -P $KEY_PASSWORD -T /usr/bin/codesign
security list-keychains -d user -s login.keychain $XCODE_KEYCHAIN

