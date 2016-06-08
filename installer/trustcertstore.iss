[Setup]
AppName = Particle Devices Trusted Certificate
AppVerName = Particle Devices Trusted Certificate 1.0.0.0
AppPublisher = Particle Industries, Inc.
AppPublisherURL = https://particle.io
AppVersion = 1.0.0.0
DefaultDirName = {pf}\Particle\TrustCert
DefaultGroupName = Particle
Compression = lzma
SolidCompression = yes
MinVersion = 5,5
PrivilegesRequired = admin

[Files]
Source: "trustcertstore.exe"; DestDir: "{app}"; Flags: replacesameversion promptifolder;

[Icons]
Name: "{group}\Uninstall Particle Certtificate"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\trustcertstore.exe"; Flags: "runhidden"; StatusMsg: "Installing Particle Certificate (this may take a few seconds) ...";
