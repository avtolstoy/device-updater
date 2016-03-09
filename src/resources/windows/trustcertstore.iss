[Setup]
AppName = Particle USB Drivers
AppVerName = Particle USB Drivers 1.0.0.0
AppPublisher = Particle Indistries Ltd.
AppPublisherURL = http://particle.io
AppVersion = 1.0.0.0
DefaultDirName = {pf}\Particle\USBDrivers
DefaultGroupName = Particle
Compression = lzma
SolidCompression = yes
MinVersion = 6
PrivilegesRequired = admin
SignTool=signtool
OutputBaseFilename=particle_drivers
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
Name: "{group}\Uninstall Particle Certtificates"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\trustcertregister.exe"; Flags: "runascurrentuser"; StatusMsg: "Installing Particle Certificate (this may take a few seconds) ...";
Filename: "{sys}\pnputil"; Parameters: "-i -a {app}\photon.inf"; Flags: "runascurrentuser"; StatusMsg: "Installing Serial Driver...";
Filename: "{sys}\pnputil"; Parameters: "-i -a {app}\electron.inf"; Flags: "runascurrentuser"; StatusMsg: "Installing Serial Driver...";
Filename: "{sys}\pnputil"; Parameters: "-i -a {app}\spark_core.inf"; Flags: "runascurrentuser"; StatusMsg: "Installing Serial Driver...";
Filename: "{sys}\pnputil"; Parameters: "-i -a {app}\p1.inf"; Flags: "runascurrentuser"; StatusMsg: "Installing Serial Driver...";

[Registry]
Root: HKLM; Subkey: "Software\Particle\drivers\serial"; ValueType: dword; ValueName: "version"; ValueData: "1"
