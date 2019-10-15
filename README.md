# PyStegano CLI Version - A Tool to hide AES encrypted Strings in files

# Usage:

# Generate new Key and backup old:
./pystegano.py gen

# Encryption:
./pystegano.py -pwd PASSWORD -mes MESSAGE -encf FILE

# Decryption:
./pystegano.py -pwd PASSWORD -decf FILE

# Save Output to file:
-s FILE
