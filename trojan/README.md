# (very) Simple Trojan 

Experimentation

### Functionnalities :

    [-] Config trojan through a JSON config file. 
    [-] Report exfiltrated data in the `./data/{trojan_id}/` folder
    [ ] Automate Trojan creation (ID, config file, fetching modules, push to FTP, ...)
    [ ] Administrate through SFTP
    [ ] Encryption of modules, configuration, exfiltrated data
    [ ] Automation:
        [ ] backend management for pulled-down data 
    [ ] Attached to another processus (stealth)


### Modules :
    [*] Dirlister
    [*] Environment checker
    [ ] Keylogger
    [ ] Screenshot
    [ ] Webcam
    [ ] Win/Linux hashes 
        [ ] etc/passwd
        [ ] windows
            [ ] XP : C:/Windows/Repair/sam
            [ ] XP : C:/Windows/Repair/system
            or
            [ ] XP : C:/Windows/System32/config/sam
    [ ] WCE - Windows Credentials Editors
    [ ] Sandbox detection
    [ ] List exising process 
    [ ] Checking SSH installation

#### Credits

Adapted from Justin Seitz's "Black Hat Python" book. 
Initially ported towards a Github Trojan C&C (for SSL encryption and the fact that traffic to GitHub is rarely blocked), I wanted to access and administrate it through SFTP and add other modules.