XCODE_KEYCHAIN="${XCODE_KEYCHAIN:-build}"
security create-keychain -p $XCODE_KEYCHAIN_PASSWORD $XCODE_KEYCHAIN
security import cert.cer -k ~/Library/Keychains/$XCODE_KEYCHAIN -T /usr/bin/codesign
security import key.p12  -x -k ~/Library/Keychains/$XCODE_KEYCHAIN -P $KEY_PASSWORD -T /usr/bin/codesign
security list-keychains -d user -s login.keychain $XCODE_KEYCHAIN

