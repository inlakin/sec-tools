# Security Tools

Security and network tools crafted for improving my knowledge and skills.

Many of those tools are adapted and improved from examples of many books.

I will try to write each of those examples in C, Python, and (Perl and/or Ruby). Right now I am focusing on Python as it is a high level scripting language.

Repo structure :

.
├── [Client-Server](https://github.com/inlakin/sec-tools/client-server/)
│   ├── Clients
│   │   ├── TCP Client
│   │   │   ├── C
│   │   │   └── Python
│   │   │       └── tcp_client.py
│   │   └── UDP Client
│   │       └── udp_client.py
│   ├── [PyNetcat](https://github.com/inlakin/sec-tools/client-server/pynetcat/)
│   │   ├── pynetcat.py
│   │   └── README.md
│   └── Servers
│       └── TCP Server
│           └── tcp_server.py
├── [PortScanner](https://github.com/inlakin/sec-tools/portscanner/)
│   ├── C
│   │   ├── portscanner
│   │   ├── portscanner.c
│   │   └── README.md
│   ├── Perl
│   └── Python
│       ├── portscanner.py
│       └── README.md
├── README.md
├── [Trojan](https://github.com/inlakin/sec-tools/trojan/)
│   ├── config
│   │   └── abc.json
│   ├── data
│   │   └── abc
│   ├── modules
│   │   ├── dirlister.py
│   │   └── environment.py
│   ├── README.md
│   └── trojan.py
└── [utils](https://github.com/inlakin/sec-tools/utils/)
    └── stools.sh

