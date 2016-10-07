echo "Creating Keychain"
sudo security create-keychain -p $XCODE_KEYCHAIN_PASSWORD $XCODE_KEYCHAIN
echo "Importing Certificate"
sudo security import cert.cer -k ~/Library/Keychains/$XCODE_KEYCHAIN -T /usr/bin/codesign
echo "Importing key"
sudo security import key.p12  -x -k ~/Library/Keychains/$XCODE_KEYCHAIN -P $KEY_PASSWORD  -T /usr/bin/codesign
echo "List keychains"
sudo security list-keychains -d user -s login.keychain $XCODE_KEYCHAIN
