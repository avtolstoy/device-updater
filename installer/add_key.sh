echo "Creating Keychain"
security create-keychain -p $XCODE_KEYCHAIN_PASSWORD $XCODE_KEYCHAIN
security unlock-keychain -p $XCODE_KEYCHAIN_PASSWORD $XCODE_KEYCHAIN

echo "Importing Certificate"
# security import cert.cer -k ~/Library/Keychains/$XCODE_KEYCHAIN -T /usr/bin/codesign
echo "Importing key"
security import key.p12  -x -k ~/Library/Keychains/$XCODE_KEYCHAIN -P $KEY_PASSWORD  -T /usr/bin/codesign
echo "List keychains"
security list-keychains -d user -s login.keychain $XCODE_KEYCHAIN
