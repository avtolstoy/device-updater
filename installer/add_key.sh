sudo security create-keychain -p $XCODE_KEYCHAIN_PASSWORD $XCODE_KEYCHAIN
sudo security import cert.cer -k ~/Library/Keychains/$XCODE_KEYCHAIN -T /usr/bin/codesign
sudo security import key.p12  -x -k ~/Library/Keychains/$XCODE_KEYCHAIN -P $KEY_PASSWORD -T /usr/bin/codesign
sudo security list-keychains -d user -s login.keychain $XCODE_KEYCHAIN
