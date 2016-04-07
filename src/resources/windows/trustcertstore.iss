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
ArchitecturesInstallIn64BitMode=x64

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
Filename: "{app}\trustcertregister.exe"; Flags: "runhidden"; StatusMsg: "Installing Particle Certificate (this may take a few seconds) ...";
Filename: "{sys}\pnputil.exe"; Parameters: "-i -a photon.inf"; WorkingDir: "{app}"; Flags: "runhidden"; StatusMsg: "Installing Serial Driver...";
Filename: "{sys}\pnputil.exe"; Parameters: "-i -a electron.inf"; WorkingDir: "{app}";Flags: "runhidden"; StatusMsg: "Installing Serial Driver...";
Filename: "{sys}\pnputil.exe"; Parameters: "-i -a spark_core.inf"; WorkingDir: "{app}";Flags: "runhidden"; StatusMsg: "Installing Serial Driver...";
Filename: "{sys}\pnputil.exe"; Parameters: "-i -a p1.inf"; WorkingDir: "{app}";Flags: "runhidden"; StatusMsg: "Installing Serial Driver...";

[Registry]
Root: HKLM; Subkey: "Software\Particle\drivers\serial"; ValueType: dword; ValueName: "version"; ValueData: "1"
