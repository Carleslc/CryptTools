# CryptTools

Tools for encryption, decryption and cracking from several cryptographic systems.

- [How to Install](#how-to-install)
- [Tools available](#tools-available)
  - [Caesar](#caesar)
      - [Usage](#usage)
        - [Examples](#examples)
          - [Encrypt a text and save to a file](#encrypt-a-text-and-save-to-a-file)
          - [Encrypt with extra information](#encrypt-with-extra-information)
          - [Decrypt with a known key](#decrypt-with-a-known-key)
          - [Decrypt without knowing the key](#decrypt-without-knowing-the-key)
          - [Advanced features](#advanced-features)
      - [NOTE](#note)
  - [Scytale](#scytale)
      - [Usage](#usage-1)
        - [Examples](#examples-1)
          - [Encrypt a text and save to a file](#encrypt-a-text-and-save-to-a-file-1)
          - [Encrypt with extra information](#encrypt-with-extra-information-1)
          - [Decrypt with a known key](#decrypt-with-a-known-key-1)
          - [Decrypt without knowing the key](#decrypt-without-knowing-the-key-1)
          - [Advanced features](#advanced-features-1)
      - [NOTE](#note-1)
  - [Vigenère](#vigenère)
      - [Usage](#usage-2)
        - [Examples](#examples-2)
          - [Encrypt a text and save to a file](#encrypt-a-text-and-save-to-a-file-2)
          - [Encrypt with extra information](#encrypt-with-extra-information-2)
          - [Decrypt with a known key](#decrypt-with-a-known-key-2)

## How to Install

1. Install **[Python 3.6](https://www.python.org/downloads/)** if you do not have it yet.
2. Clone this repository: `git clone https://github.com/Carleslc/CryptTools.git`
3. Install the following Python dependencies:
```
pip3 install numpy
pip3 install pyenchant
```

## Tools available

_These tools are designed to be useful in the field of computer security and their use is restricted to personal use or under consent. I am not responsible for any illicit use that may occur._

### Caesar

[--> What is the Caesar Cipher? <--](https://en.wikipedia.org/wiki/Caesar_cipher)

#### Usage

`python3 caesar.py --help`
```
usage: caesar.py [-h] [-t TEXT] [-k KEY] [-l LANG] [-V] [-A] [-D]
                 [-T THRESHOLD] [--beep]

optional arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  text to read from. If not specified the program will
                        read from standard input
  -k KEY, --key KEY     key used to encrypt. If no key is provided the program
                        will try to crack and decrypt using the specified
                        language
  -l LANG, --lang LANG  available languages: ['de_DE', 'en_AU', 'en_GB',
                        'en_US', 'fr_FR'] (default: en_US). Only useful if no
                        key is provided
  -V, --verbose         show extra information
  -A, --all             show decrypted text for each tested key
  -D, --debug           show information about text validation
  -T THRESHOLD, --threshold THRESHOLD
                        valid word count percentage to mark the whole text as
                        valid language (default: 50)
  --beep                plays a beep sound when program finishes. May require
                        SOX to be installed
```

##### Examples

###### Encrypt a text and save to a file

**`python3 caesar.py -t "This is the Caesar tool from CryptTools!" -k 5 > test`**
```
Ymnx nx ymj Hfjxfw yttq kwtr HwduyYttqx!
```

`-t` argument is not mandatory, so if you need to encrypt a long text you can skip it, execute `python3 caesar.py -k 5 > test` and then paste your text. When completed press `Return` and then finish the input with `Ctrl+D` so the program will read it.

###### Encrypt with extra information

**`python3 caesar.py -t "This is the Caesar tool from CryptTools!" -k 5 -VA`**
```
Original text most frequent character: t

Ymnx nx ymj Hfjxfw yttq kwtr HwduyYttqx!

Encrypted text most frequent character: y
```

###### Decrypt with a known key

To decrypt you will need to know the shift needed to reallocate each character to its correct character in the alphabet. In the example above the encrypted shift is 5 so the shift needed to decrypt is 26 - 5 = 21, where 26 is the size of the alphabet.

**`python3 caesar.py -k 21 < test`**
```
This is the Caesar tool from CryptTools!
```

###### Decrypt without knowing the key

This method cracks the message with bruteforce and then checks every result validating the language to guess which result is the original text. By default language is English, for other languages read below.

**`python3 caesar.py < test`**
```
This is the Caesar tool from CryptTools!
```

###### Advanced features

Read from a file and print cracked keys:

**`python3 caesar.py -V < test`**
```
Most frequent character: y
Testing 't' (ROT-21)       SUCCESS
Decrypted with ROT-21. Original encryption key: 5
This is the Caesar tool from CryptTools!
```

ROT-X means that each character in the text is shifted X positions in the alphabet.

To decrypt a message without knowing the key you need to know the original text **language**. It is provided with `--lang` option. By default it is `en_US` (American English).

For example, in _Deutsch_ language:

`python3 caesar.py -t "Dies ist das Scytale-Tool von CryptTools!" -k 6`
```
Joky oyz jgy Yiezgrk-Zuur but IxevzZuury!
```

If language is not provided it will try English and it will fail:

**`python3 caesar.py -V -t "Joky oyz jgy Yiezgrk-Zuur but IxevzZuury!"`**
```
Most frequent character: y
Testing 'z' (ROT-1)        
Sorry. None of decrypted results seems to be written in language en_US...
```

Then, providing the correct language:

**`python3 caesar.py -V -t "Joky oyz jgy Yiezgrk-Zuur but IxevzZuury!" --lang "de_DE"`**
```
Most frequent character: y
Testing 's' (ROT-20)       SUCCESS
Decrypted with ROT-20. Original encryption key: 6
Dies ist das Scytale-Tool von CryptTools!
```

You can check all available codes with `python3 caesar.py --help`. You can even install more languages, for that take a look [here](http://pythonhosted.org/pyenchant/tutorial.html#adding-language-dictionaries).

If original text _**language is unknown**_ you still can generate all possible transformations, then you will need to check them manually in order to know which is the correct:

**`python3 caesar.py -V -A -t "Joky oyz jgy Yiezgrk-Zuur but IxevzZuury!"`**
```
Most frequent character: y
Testing 'e' (ROT-6)       Testing decrypted text:
"Puqe uef pme Eokfmxq-Faax haz OdkbfFaaxe!"
Testing 't' (ROT-21)       Testing decrypted text:
"Ejft jtu ebt Tdzubmf-Uppm wpo DszquUppmt!"
...
Testing 's' (ROT-20)       Testing decrypted text:
"Dies ist das Scytale-Tool von CryptTools!"
Testing 'h' (ROT-9)       Testing decrypted text:
"Sxth xhi sph Hrnipat-Idda kdc RgneiIddah!"
...
Testing 'q' (ROT-18)       Testing decrypted text:
"Bgcq gqr byq Qawryjc-Rmmj tml ApwnrRmmjq!"
Testing 'z' (ROT-1)       Testing decrypted text:
"Kplz pza khz Zjfahsl-Avvs cvu JyfwaAvvsz!"

Sorry. None of decrypted results seems to be written in language en_US...
```

Testing order is frequency order (most common letter is tested first).

In addition, with the extra option `-D` you can check the language validation process:

**`python3 caesar.py -VAD < test`**
```
Most frequent character: y
Testing 'e' (ROT-6)       Testing decrypted text:
"Estd td esp Nlpdlc ezzw qczx NcjaeEzzwd!"

estd: False              |  Progress 0%     | Max 88%
td: False                |  Progress 0%     | Max 75%
esp: True                |  Progress 12%    | Max 75%
nlpdlc: False            |  Progress 12%    | Max 62%
ezzw: False              |  Progress 12%    | Max 50%
qczx: False              |  Progress 12%    | Max 38%

Testing 't' (ROT-21)       Testing decrypted text:
"This is the Caesar tool from CryptTools!"

this: True               |  Progress 12%    | Max 100%
is: True                 |  Progress 25%    | Max 100%
the: True                |  Progress 38%    | Max 100%
caesar: False            |  Progress 38%    | Max 88%
tool: True               |  Progress 50%    | SUCCESS

Decrypted with ROT-21. Original encryption key: 5
This is the Caesar tool from CryptTools!
```

`-A` and `-D` options may be too verbose, avoid using them for long texts.

You can also set the permissiveness of the language validation process with the `--threshold -T` option. By default it is set to 50 (half of the text words must be written in the specified language in order to accept it as the original text). Values must be between 1 and 100. Values below 20% are not recommended (an encrypted text may be accepted as decrypted). Higher values indicate toughness, but 100% it is neither recommended (in the text may be non-english nouns and other original but non-english words).

#### NOTE

As you can see, it is too easy to crack this classical cryptographic system so it is not recommended to use it in production software.

### Scytale

[--> What is a Scytale? <--](https://en.wikipedia.org/wiki/Scytale)

#### Usage

`python3 scytale.py --help`

```
usage: scytale.py [-h] [-t TEXT] [-k KEY] [-l LANG] [-V] [-A] [-D]
                  [-T THRESHOLD] [--beep]

optional arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  text to read from. If not specified the program will
                        read from standard input
  -k KEY, --key KEY     key used to encrypt. If no key is provided the program
                        will try to crack and decrypt using the specified
                        language
  -l LANG, --lang LANG  available languages: ['de_DE', 'en_AU', 'en_GB',
                        'en_US', 'fr_FR'] (default: en_US). Only useful if no
                        key is provided
  -V, --verbose         show extra information
  -A, --all             show decrypted text for each tested key
  -D, --debug           show information about text validation
  -T THRESHOLD, --threshold THRESHOLD
                        valid word count percentage to mark the whole text as
                        valid language (default: 50)
  --beep                plays a beep sound when program finishes. May require
                        SOX to be installed
```

##### Examples

###### Encrypt a text and save to a file

**`python3 scytale.py -t "This is the Scytale tool from CryptTools!" -k 5 > test`**
```
Theoohe moi t lsSoCs cor!iyly st p  aft tlrT
```

`-t` argument is not mandatory, so if you need to encrypt a long text you can skip it, execute `python3 scytale.py -k 5 > test` and then paste your text. When completed press `Return` and then finish the input with `Ctrl+D` so the program will read it.

###### Encrypt with extra information

**`python3 scytale.py -t "This is the Scytale tool from CryptTools!" -k 5 -VA`**
```
Testing matrix: 5x9
Text to cipher: "This is the Scytale tool from CryptTools!" (41)
[['T' 'h' 'i' 's' ' ' 'i' 's' ' ' 't']
 ['h' 'e' ' ' 'S' 'c' 'y' 't' 'a' 'l']
 ['e' ' ' 't' 'o' 'o' 'l' ' ' 'f' 'r']
 ['o' 'm' ' ' 'C' 'r' 'y' 'p' 't' 'T']
 ['o' 'o' 'l' 's' '!' ' ' ' ' ' ' ' ']]
Result size: 44
Theoohe moi t lsSoCs cor!iyly st p  aft tlrT
```

That matrix represents the Scytale. To encrypt the text it is written by rows (5) and read by columns (9).

###### Decrypt with a known key

To decrypt you will need to know the columns of the underlying matrix. In the example above they are 9.
If you only have the key 5 (rows) then you can calculate the columns with the text size:
`Columns = Size/Rows`. For example, the encrypted text above has size 44, so 44/5 = 8.8, rounding we have that columns are 9.

**`python3 scytale.py -k 9 < test`**
```
This is the Scytale tool from CryptTools!
```

###### Decrypt without knowing the key

This method cracks the message with bruteforce and then checks every result validating the language to guess which result is the original text. By default language is English, for other languages read below.

**`python3 scytale.py < test`**
```
This is the Scytale tool from CryptTools!
```

###### Advanced features

Read from a file and print cracked keys:

**`python3 scytale.py -V < test`**
```
Text to crack: "Theoohe moi t lsSoCs cor!iyly st p  aft tlrT" (44)
Testing matrix: 9x5       SUCCESS
This is the Scytale tool from CryptTools!
```

To decrypt a message without knowing the key you need to know the original text **language**. It is provided with `--lang` option. By default it is `en_US` (American English).

For example, in _Deutsch_ language:

`python3 scytale.py -t "Dies ist das Scytale-Tool von CryptTools!" -k 6`
```
DtcTnTi yo oedtoCosaalrl sl ysi evp!sS-ot
```

If language is not provided it will try English and it will fail:

**`python3 scytale.py -V -t "DtcTnTi yo oedtoCosaalrl sl ysi evp!sS-ot"`**
```
Text to crack: "DtcTnTi yo oedtoCosaalrl sl ysi evp!sS-ot" (41)
Testing matrix: 2x40       Sorry. None of decrypted results seems to be written in language en_US...
```

Then, providing the correct language:

**`python3 scytale.py -V -t "DtcTnTi yo oedtoCosaalrl sl ysi evp!sS-ot" --lang "de_DE"`**
```
Text to crack: "DtcTnTi yo oedtoCosaalrl sl ysi evp!sS-ot" (41)
Testing matrix: 7x6       SUCCESS
Dies ist das Scytale-Tool von CryptTools!
```

You can check all available codes with `python3 scytale.py --help`. You can even install more languages, for that take a look [here](http://pythonhosted.org/pyenchant/tutorial.html#adding-language-dictionaries).

If original text _**language is unknown**_ you still can generate all possible transformations, then you will need to check them manually in order to know which is the correct:

**`python3 scytale.py -V -A -t "DtcTnTi yo oedtoCosaalrl sl ysi evp!sS-ot"`**
```
Text to crack: "Ddlooiaenoes- ls TCs Sor!icoy sylp tt t  avT" (44)
...
Testing matrix: 2x21       Testing decrypted text:
"DltrclT nsTli  yysoi  oeevdpt!osCSo-soata"
Testing matrix: 21x2       Testing decrypted text:
"Dcniy etCsar lyieps-ttTT oodooalls s v!So"
Testing matrix: 3x14       Testing decrypted text:
"DtytoscCiTo nseTaviap l!yrsolS  -osoeltd"
Testing matrix: 14x3       Testing decrypted text:
"DTioeosl  ivsotn  dCarsy pStcTyotoallse!-"
...
Testing matrix: 9x5       Testing decrypted text:
"DT oasi!ttioCll s c eor eS Tydslyv- nota spo"
Testing matrix: 6x7       Testing decrypted text:
"D tly!tyorsscoCliST o  -nosseoTealvtida p"
Testing matrix: 7x6       Testing decrypted text:
"Dies ist das Scytale-Tool von CryptTools!"
Testing matrix: 8x6       Testing decrypted text:
"Dies is t das S cytale- Tool vo n Crypt Tools!"
...
Testing matrix: 2x40       Testing decrypted text:
"Dtt c T n T i   y o   o e d t o C o s a a l r l   s l   y s i   e v p ! s S - o"
Sorry. None of decrypted results seems to be written in language en_US...
```

In addition, with the extra option `-D` you can check the language validation process:

**`python3 scytale.py -VAD < test`**
```
Text to crack: "Theoohe moi t lsSoCs cor!iyly st p  aft tlrT" (44)
Testing matrix: 1x44       Testing decrypted text:
"Theoohe moi t lsSoCs cor!iyly st p  aft tlrT"

theoohe: False           |  Progress 0%     |   Max 90%
moi: False               |  Progress 0%     |   Max 80%
lssocs: False            |  Progress 0%     |   Max 60%
cor: False               |  Progress 0%     |   Max 50%
iyly: False              |  Progress 0%     |   Max 40%

...

Testing matrix: 2x22       Testing decrypted text:
"Tohre!oioyhley  msoti  pt   lasfSto Ctsl rcT"

tohre: False             |  Progress 0%     |   Max 86%
oioyhley: False          |  Progress 0%     |   Max 71%
msoti: False             |  Progress 0%     |   Max 57%
pt: True                 |  Progress 14%    |   Max 57%
lasfsto: False           |  Progress 14%    |   Max 43%

Testing matrix: 22x2       Testing decrypted text:
"TeoemitlSC o!yys  attrhoh o  soscril tp f lT"

teoemitlsc: False        |  Progress 0%     |   Max 89%
yys: False               |  Progress 0%     |   Max 67%
attrhoh: False           |  Progress 0%     |   Max 56%

...

Testing matrix: 3x15       Testing decrypted text:
"TsshSteo oCpos h  eca ofmrto! iit yltlr yTl"

tsshsteo: False          |  Progress 0%     |   Max 88%
ocpos: False             |  Progress 0%     |   Max 75%
eca: False               |  Progress 0%     |   Max 50%
ofmrto: False            |  Progress 0%     |   Max 38%

Testing matrix: 15x3       Testing decrypted text:
"ToeotsCc!lspa rho i Ssoiyt ftTehm lo ry   tl"

toeotscc: False          |  Progress 0%     |   Max 89%
lspa: False              |  Progress 0%     |   Max 78%
rho: True                |  Progress 11%    |   Max 78%
ssoiyt: False            |  Progress 11%    |   Max 56%
fttehm: False            |  Progress 11%    |   Max 44%

...

Testing matrix: 5x9       Testing decrypted text:
"ToClahisyfe   totcs o otthlr les!pr Si Tmoy"

toclahisyfe: False       |  Progress 0%     |   Max 88%
totcs: False             |  Progress 0%     |   Max 75%
otthlr: False            |  Progress 0%     |   Max 50%
les: False               |  Progress 0%     |   Max 38%

Testing matrix: 9x5       Testing decrypted text:
"This is the Scytale tool from CryptTools!"

this: True               |  Progress 12%    |   Max 100%
is: True                 |  Progress 25%    |   Max 100%
the: True                |  Progress 38%    |   Max 100%
scytale: False           |  Progress 38%    |   Max 88%
tool: True               |  Progress 50%    |   
SUCCESS
This is the Scytale tool from CryptTools!
```

`-A` and `-D` options may be too verbose, avoid using them for long texts.

You can also set the permissiveness of the language validation process with the `--threshold -T` option. By default it is set to 50 (half of the text words must be written in the specified language in order to accept it as the original text). Values must be between 1 and 100. Values below 20% are not recommended (an encrypted text may be accepted as decrypted). Higher values indicate toughness, but 100% it is neither recommended (in the text may be non-english nouns and other original but non-english words).

#### NOTE

As you can see, it is too easy to crack this classical cryptographic system so it is not recommended to use it in production software.

### Vigenère

[--> What is the Vigenère Cipher? <--](https://en.wikipedia.org/wiki/Vigenère_cipher)

#### Usage

`python3 vigenere.py --help`
```
usage: vigenere.py [-h] [-t TEXT] [-k KEY] [--decrypt] [-l LANG] [-V] [-A]
                   [-D] [-T THRESHOLD] [--beep]

optional arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  text to read from. If not specified the program will
                        read from standard input
  -k KEY, --key KEY     key used to encrypt or decrypt. If no key is provided
                        the program will try to crack and decrypt using the
                        specified language
  --decrypt             use the key to decrypt the text
  -l LANG, --lang LANG  available languages: ['de_DE', 'en_AU', 'en_GB',
                        'en_US', 'fr_FR'] (default: en_US). Only useful if no
                        key is provided
  -V, --verbose         show extra information
  -A, --all             show decrypted text for each tested key
  -D, --debug           show information about text validation
  -T THRESHOLD, --threshold THRESHOLD
                        valid word count percentage to mark the whole text as
                        valid language (default: 50)
  --beep                plays a beep sound when program finishes. May require
                        SOX to be installed
```

##### Examples

###### Encrypt a text and save to a file

**`python3 vigenere.py -t "This is the Vigenere tool from CryptTools!" "CRYPT" > test`**
```
Vygh bu kft Okxccxtv rdhn wpdf EiwemVfmal!
```

`-t` argument is not mandatory, so if you need to encrypt a long text you can skip it, execute `python3 vigenere.py "CRYPT" > test` and then paste your text. When completed press `Return` and then finish the input with `Ctrl+D` so the program will read it.

###### Encrypt with extra information

**`python3 vigenere.py -t "This is the Vigenere tool from CryptTools!" "CRYPT" -V`**
```
Key "CRYPT" shifts: [2, 17, 24, 15, 19]
Vygh bu kft Okxccxtv rdhn wpdf EiwemVfmal!
```

###### Decrypt with a known key

To decrypt you will need to know the encryption key. In the example above it is _CRYPT_.
You need to provide the argument `--decrypt` to use the key to decrypt.

**`python3 vigenere.py "CRYPT" --decrypt < test`**
```
This is the Vigenere tool from CryptTools!
```
