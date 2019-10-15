# PyStegano-CLI
→PyStegano-CLI Version - A Tool to hide AES encrypted Strings in files

usage: aufruf.py [-h] [-s SAVE] [-pwd Password] [-encf File for encryption]
                 [-decf File for decryption] [-mes Message to hide]
                 [{gen}]

    ____        _____ __                                     ________    ____
   / __ \__  __/ ___// /____  ____ _____ _____  ____        / ____/ /   /  _/
  / /_/ / / / /\__ \/ __/ _ \/ __ `/ __ `/ __ \/ __ \______/ /   / /    / /  
 / ____/ /_/ /___/ / /_/  __/ /_/ / /_/ / / / / /_/ /_____/ /___/ /____/ /   
/_/    \__, //____/\__/\___/\__, /\__,_/_/ /_/\____/      \____/_____/___/   
      /____/               /____/      Version 1.0
      
      Coded by PiereLucas       |       github.com/pierelucas  

positional arguments:
  {gen}                 Generate new keyfile, backup old, ignore all 'n exit
                        PyStegano

optional arguments:
  -h, --help            show this help message and exit
  -s SAVE, --save SAVE  Save the output to a given filename
  -pwd Password, --password Password
  -encf File for encryption, --enc-filepath File for encryption
  -decf File for decryption, --dec-filepath File for decryption
  -mes Message to hide, --message Message to hide
