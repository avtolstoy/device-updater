[Setup]
AppName = Particle Devices Trusted Certificate
AppVerName = Particle Devices Trusted Certificate 1.0.0.0
AppPublisher = Particle Indistries Ltd.
AppPublisherURL = http://akeo.ie
AppVersion = 1.0.0.0
DefaultDirName = {pf}\Particle\TrustCert
DefaultGroupName = Particle
Compression = lzma
SolidCompression = yes
MinVersion = 6
PrivilegesRequired = admin
SignTool=signtool
OutputBaseFilename=particle_drivers.exe
OutputDir=.

[Files]
Source: "trustcertregister.exe"; DestDir: "{app}"; Flags: replacesameversion promptifolder;
Source: "photon.inf"; DestDir: "{app}"; Flags: replacesameversion promptifolder;
Source: "photon.cat"; DestDir: "{app}"; Flags: replacesameversion promptifolder;
Source: "electron.inf"; DestDir: "{app}"; Flags: replacesameversion promptifolder;
Source: "electron.cat"; DestDir: "{app}"; Flags: replacesameversion promptifolder;
Source: "spark_core.inf"; DestDir: "{app}"; Flags: replacesameversion promptifolder;
Source: "spark_core.cat"; DestDir: "{app}"; Flags: replacesameversion promptifolder;
Source: "p1.inf"; DestDir: "{app}"; Flags: replacesameversion promptifolder;
Source: "p1.cat"; DestDir: "{app}"; Flags: replacesameversion promptifolder;


[Icons]
Name: "{group}\Uninstall Particle Certtificate"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\trustcertregister.exe"; Flags: "runhidden"; StatusMsg: "Installing Particle Certificate (this may take a few seconds) ...";
Filename: "{sys}\pnputil"; Parameters: "{app}\photon.inf"; Flags: "runhidden"; StatusMsg: "Installing Serial Driver...";
Filename: "{sys}\pnputil"; Parameters: "{app}\electron.inf"; Flags: "runhidden"; StatusMsg: "Installing Serial Driver...";
Filename: "{sys}\pnputil"; Parameters: "{app}\spark_core.inf"; Flags: "runhidden"; StatusMsg: "Installing Serial Driver...";
Filename: "{sys}\pnputil"; Parameters: "{app}\p1.inf"; Flags: "runhidden"; StatusMsg: "Installing Serial Driver...";

[Registry]
Root: HKLM; Subkey: "Software\Particle\drivers\serial"; ValueType: dword; ValueName: "version"; ValueData: "1"
