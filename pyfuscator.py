# -*- coding: UTF-8 -*-
import os, base64, sys, time, zlib, marshal, random, string
from pprint import pformat

# Emoji unicode list
alphabet = [
    "\U0001f600", "\U0001f603", "\U0001f604", "\U0001f601", "\U0001f605",
    "\U0001f923", "\U0001f602", "\U0001f609", "\U0001f60A", "\U0001f61b",
]

MAX_STR_LEN = 70
OFFSET = 10

# Basic colors
black="\033[0;30m"
red="\033[0;31m"
green="\033[0;32m"
yellow="\033[0;33m"  
blue="\033[0;34m"
purple="\033[0;35m"
cyan="\033[0;36m"
white="\033[0;37m"

# Snippets
ask = green + '\n[' + white + '?' + green + '] '+ yellow
success = green + '\n[' + white + '√' + green + '] '
error = red + '\n[' + white + '!' + red + '] '
info= yellow + '\n[' + white + '+' + yellow + '] '+ cyan

# Current Directory
pwd=os.getcwd()

# Logo actualizado
logo=f"""{green}╔═══╗──────────────────╔╗
{yellow}║╔═╗║──────────────────║║
{red}║╚═╝╠╗─╔╗╔══╦═╗╔══╦══╦═╝╠══╗
{cyan}║╔══╣║─║║║║═╣╔╗╣╔═╣╔╗║╔╗║║═╣
{green}║║──║╚═╝║║║═╣║║║╚═╣╚╝║╚╝║║═╣
{yellow}╚╝──╚═╗╔╝╚══╩╝╚╩══╩══╩══╩══╝
{red} ────╔═╝║
{cyan} ────╚══╝ PyFuscator Pro v3.0
{yellow}══════════════════════════════
{cyan}[ Developer: Ghost Developer ]
{blue}[ GitHub: github.com/CHICO-CP ]
{green}[ Telegram: t.me/Gh0stDeveloper ]
{yellow}══════════════════════════════"""

# Normal slowly printer
def sprint(sentence, second=0.05):
    for word in sentence + '\n':
        sys.stdout.write(word)
        sys.stdout.flush()
        time.sleep(second)

# About section of script
def about():
    os.system("clear")
    sprint(logo, 0.01)
    print(f"{cyan}[ToolName]  {purple} :[PyFuscator Pro]")
    print(f"{cyan}[Version]   {purple} :[3.0]")
    print(f"{cyan}[Author]    {purple} :[Ghost Developer]")
    print(f"{cyan}[Github]    {purple} :[https://github.com/CHICO-CP]")
    print(f"{cyan}[Telegram] {purple}  :[t.me/Gh0stDeveloper]")
    print(f"{cyan}[Methods]   {purple} :[Base64, Zlib, Marshal, Emoji, XOR, Multi-Layer]")
    ret=input(ask+"1 for main menu, 0 for exit  > "+green)
    if ret=="1":
        main()
    else: 
        exit()

# Custom path chooser
def mover(out_file):
    move= input(ask+"Moving to a custom route?(y/n) > "+green)
    if move=="y":
        mpath=input(ask+"Enter the path > "+ green)
        if os.path.exists(mpath):
            os.system(f'''mv -f "{out_file}" "{mpath}" ''')
            sprint(f"{success}{out_file} moved to {mpath}\n")
        else:
            sprint(error+"Path do not exist!\n")
    else:
        print("\n")
    exit()


def obfuscate(VARIABLE_NAME, file_content):
    b64_content = base64.b64encode(file_content.encode()).decode()
    index = 0
    code = f'{VARIABLE_NAME} = ""\n'
    for _ in range(int(len(b64_content) / OFFSET) + 1):
        _str = ''
        for char in b64_content[index:index + OFFSET]:
            byte = str(hex(ord(char)))[2:]
            if len(byte) < 2:
                byte = '0' + byte
            _str += '\\x' + str(byte)
        code += f'{VARIABLE_NAME} += "{_str}"\n'
        index += OFFSET
    code += f'exec(__import__("\\x62\\x61\\x73\\x65\\x36\\x34").b64decode({VARIABLE_NAME}.encode("\\x75\\x74\\x66\\x2d\\x38")).decode("\\x75\\x74\\x66\\x2d\\x38"))'
    return code

def chunk_string(in_s, n):
    """Chunk string to max length of n"""
    return "\n".join(
        "{}\\".format(in_s[i : i + n]) for i in range(0, len(in_s), n)
    ).rstrip("\\")

def encode_string(in_s, alphabet):
    d1 = dict(enumerate(alphabet))
    d2 = {v: k for k, v in d1.items()}
    return (
        'exec("".join(map(chr,[int("".join(str({}[i]) for i in x.split())) for x in\n'
        '"{}"\n.split("  ")])))\n'.format(
            pformat(d2),
            chunk_string(
                "  ".join(" ".join(d1[int(i)] for i in str(ord(c))) for c in in_s),
                MAX_STR_LEN,
            ),
        )
    )


def obfuscate_base64_zlib_marshal(file_content):
    """NUEVO: Base64 + Zlib + Marshal"""
    var_name = "enc_data"
    # Comprimir con zlib
    compressed = zlib.compress(file_content.encode())
    # Serializar con marshal
    marshaled = marshal.dumps(compressed)
    # Codificar en base64
    b64_encoded = base64.b64encode(marshaled).decode()
    
    code = f'''# Encrypted by Ghost Developer
# GitHub: github.com/CHICO-CP
# Telegram: t.me/Gh0stDeveloper

import base64, zlib, marshal

{var_name} = "{b64_encoded}"

# Decodificación
decoded = base64.b64decode({var_name})
unmarshaled = marshal.loads(decoded)
decompressed = zlib.decompress(unmarshaled)
exec(decompressed.decode())'''
    return code

def obfuscate_base64_marshal(file_content):
    """NUEVO: Base64 + Marshal"""
    var_name = "enc_payload"
    # Serializar con marshal
    marshaled = marshal.dumps(file_content.encode())
    # Codificar en base64
    b64_encoded = base64.b64encode(marshaled).decode()
    
    code = f'''# Encrypted by Ghost Developer
# GitHub: github.com/CHICO-CP
# Telegram: t.me/Gh0stDeveloper

import base64, marshal

{var_name} = "{b64_encoded}"

# Decodificación
decoded = base64.b64decode({var_name})
unmarshaled = marshal.loads(decoded)
exec(unmarshaled.decode())'''
    return code

def obfuscate_zlib_marshal(file_content):
    """NUEVO: Zlib + Marshal"""
    var_name = "compressed_data"
    # Comprimir con zlib
    compressed = zlib.compress(file_content.encode())
    # Serializar con marshal
    marshaled = marshal.dumps(compressed)
    
    code = f'''# Encrypted by Ghost Developer
# GitHub: github.com/CHICO-CP
# Telegram: t.me/Gh0stDeveloper

import zlib, marshal

{var_name} = {marshaled}

# Decodificación
unmarshaled = marshal.loads({var_name})
decompressed = zlib.decompress(unmarshaled)
exec(decompressed.decode())'''
    return code

def obfuscate_xor_base64(file_content):
    """NUEVO: XOR + Base64"""
    var_name = "xor_data"
    key = 42
    # Aplicar XOR
    xor_encoded = ''.join(chr(ord(c) ^ key) for c in file_content)
    # Codificar en base64
    b64_encoded = base64.b64encode(xor_encoded.encode()).decode()
    
    code = f'''# Encrypted by Ghost Developer
# GitHub: github.com/CHICO-CP
# Telegram: t.me/Gh0stDeveloper

import base64

{var_name} = "{b64_encoded}"
key = {key}

# Decodificación
decoded = base64.b64decode({var_name}).decode()
xor_decoded = ''.join(chr(ord(c) ^ key) for c in decoded)
exec(xor_decoded)'''
    return code

def obfuscate_double_base64(file_content):
    """NUEVO: Base64 Doble"""
    var_name = "double_b64"
    # Doble codificación base64
    first_pass = base64.b64encode(file_content.encode()).decode()
    second_pass = base64.b64encode(first_pass.encode()).decode()
    
    code = f'''# Encrypted by Ghost Developer
# GitHub: github.com/CHICO-CP
# Telegram: t.me/Gh0stDeveloper

import base64

{var_name} = "{second_pass}"

# Decodificación doble
first_decode = base64.b64decode({var_name}).decode()
second_decode = base64.b64decode(first_decode).decode()
exec(second_decode)'''
    return code

def obfuscate_multi_layer(file_content, layers=3):
    """NUEVO: Cifrado Multicapa"""
    var_name = "multi_data"
    current_content = file_content
    
    # Aplicar múltiples capas
    for i in range(layers):
        if i % 3 == 0:
            current_content = base64.b64encode(current_content.encode()).decode()
        elif i % 3 == 1:
            current_content = base64.b64encode(zlib.compress(current_content.encode())).decode()
        else:
            key = 42
            current_content = ''.join(chr(ord(c) ^ key) for c in current_content)
    
    code = f'''# Encrypted by Ghost Developer
# GitHub: github.com/CHICO-CP
# Telegram: t.me/Gh0stDeveloper

import base64, zlib

{var_name} = "{current_content}"
layers = {layers}

# Descifrado multicapa
data = {var_name}
for layer in range(layers):
    current_layer = layers - layer - 1
    if current_layer % 3 == 0:
        # XOR
        key = 42
        data = ''.join(chr(ord(c) ^ key) for c in data)
    elif current_layer % 3 == 1:
        # Zlib
        data = zlib.decompress(base64.b64decode(data)).decode()
    else:
        # Base64
        data = base64.b64decode(data).decode()

exec(data)'''
    return code

def obfuscate_bytearray_base64(file_content):
    """NUEVO: Bytearray + Base64"""
    var_name = "byte_data"
    # Convertir a bytearray y luego base64
    byte_data = bytearray(file_content.encode())
    b64_encoded = base64.b64encode(bytes(byte_data)).decode()
    
    code = f'''# Encrypted by Ghost Developer
# GitHub: github.com/CHICO-CP
# Telegram: t.me/Gh0stDeveloper

import base64

{var_name} = "{b64_encoded}"

# Decodificación
decoded = base64.b64decode({var_name})
exec(bytearray(decoded).decode())'''
    return code


def encryptsh():
    in_file = input(ask + "Input Filename  > "+cyan)
    if not os.path.exists(in_file):
        sprint(error+'File not found')
        os.system("sleep 2")
        encryptsh()
    os.system("bash-obfuscate " + in_file + " -o .temp")
    if not os.path.exists(".temp"):
        try:
            sprint(info+"Installing Bash-Obfuscate....\n")
            os.system("apt install nodejs -y && npm install -g bash-obfuscate")
            os.system("bash-obfuscate " + in_file + " -o .temp")
        except:
            sprint(error+" Bash-Obfuscate not installed! Install it by:\n"+green+"[+] \"apt install nodejs -y && npm install -g bash-obfuscate\"")
            exit(1)
    out_file= input(ask + "Output Filename  > " + green)   
    with open(".temp",'r') as temp_f, open(out_file,'w') as out_f:
        filedata = temp_f.read()
        out_f.write("# Encrypted by Ghost Developer\n# GitHub: github.com/CHICO-CP\n# Telegram: t.me/Gh0stDeveloper\n\n"+filedata)
    os.remove(".temp")
    sprint(f"{success}{out_file} saved in {pwd}")
    mover(out_file)

# Decrypt bash code by "eval"
def decryptsh():
    in_file = input(ask + "Input File  > "+cyan)
    if not os.path.exists(in_file):
        print(error+' File not found')
        os.system("sleep 2")
        decryptsh()
    with open(in_file,'r') as in_f, open(".temp1",'w') as temp_f:
        filedata = in_f.read()
        if not (filedata.find("eval") != -1):
            sprint(error+" Cannot be decrypted!")
            exit()
        newdata = filedata.replace("eval","echo")
        temp_f.write(newdata)
    out_file = input(ask + "Output File  > " +green)
    os.system("bash .temp1 > .temp2")
    os.remove(".temp1")
    with open(".temp2",'r') as temp_f2, open(out_file,'w') as out_f:
        filedata = temp_f2.read()
        out_f.write("# Encrypted by Ghost Developer\n# GitHub: github.com/CHICO-CP\n# Telegram: t.me/Gh0stDeveloper\n\n"+filedata)
    os.remove(".temp2")
    sprint(f"{success}{out_file} saved in {pwd}")
    mover(out_file)

# Encrypting python file into base64 variable (ORIGINAL)
def encryptvar():
    var = "Ghost_Developer"
    iteration = 50
    in_file = input(ask + "Input file: "+cyan)
    if not os.path.isfile(in_file):
        print(error+' File not found')
        os.system("sleep 2")
        encryptvar()
    out_file = input(ask + "Output file: " + green)
    with open(in_file, 'r', encoding='utf-8', errors='ignore') as in_f,open(out_file, 'w') as out_f:
       file_content = in_f.read()
       obfuscated_content = obfuscate(var * iteration, file_content)
       out_f.write("# Encrypted by Ghost Developer\n# GitHub: github.com/CHICO-CP\n# Telegram: t.me/Gh0stDeveloper\n\n"+obfuscated_content)
    sprint(f"{success}{out_file} saved in {pwd}")
    mover(out_file)

# Encrypting python file into emoji (ORIGINAL)
def encryptem():
    in_file= input(ask +"Input File: "+cyan )
    if not os.path.isfile(in_file):
        print(error+' File not found')
        os.system("sleep 2")
        encryptem()
    out_file= input(ask + "Output File: " + green)
    with open(in_file) as in_f, open(out_file, "w", encoding="utf-8") as out_f:
        out_f.write("# Encrypted by Ghost Developer\n# GitHub: github.com/CHICO-CP\n# Telegram: t.me/Gh0stDeveloper\n\n")
        out_f.write(encode_string(in_f.read(), alphabet))
        sprint(f"{success}{out_file} saved in {pwd}")
        mover(out_file)


def encrypt_b64_zlib_marshal():
    """NUEVO: Base64 + Zlib + Marshal"""
    in_file = input(ask + "Input file: "+cyan)
    if not os.path.isfile(in_file):
        print(error+' File not found')
        os.system("sleep 2")
        encrypt_b64_zlib_marshal()
    out_file = input(ask + "Output file: " + green)
    with open(in_file, 'r', encoding='utf-8', errors='ignore') as in_f,open(out_file, 'w') as out_f:
       file_content = in_f.read()
       obfuscated_content = obfuscate_base64_zlib_marshal(file_content)
       out_f.write(obfuscated_content)
    sprint(f"{success}{out_file} saved in {pwd}")
    mover(out_file)

def encrypt_b64_marshal():
    """NUEVO: Base64 + Marshal"""
    in_file = input(ask + "Input file: "+cyan)
    if not os.path.isfile(in_file):
        print(error+' File not found')
        os.system("sleep 2")
        encrypt_b64_marshal()
    out_file = input(ask + "Output file: " + green)
    with open(in_file, 'r', encoding='utf-8', errors='ignore') as in_f,open(out_file, 'w') as out_f:
       file_content = in_f.read()
       obfuscated_content = obfuscate_base64_marshal(file_content)
       out_f.write(obfuscated_content)
    sprint(f"{success}{out_file} saved in {pwd}")
    mover(out_file)

def encrypt_zlib_marshal():
    """NUEVO: Zlib + Marshal"""
    in_file = input(ask + "Input file: "+cyan)
    if not os.path.isfile(in_file):
        print(error+' File not found')
        os.system("sleep 2")
        encrypt_zlib_marshal()
    out_file = input(ask + "Output file: " + green)
    with open(in_file, 'r', encoding='utf-8', errors='ignore') as in_f,open(out_file, 'w') as out_f:
       file_content = in_f.read()
       obfuscated_content = obfuscate_zlib_marshal(file_content)
       out_f.write(obfuscated_content)
    sprint(f"{success}{out_file} saved in {pwd}")
    mover(out_file)

def encrypt_xor_b64():
    """NUEVO: XOR + Base64"""
    in_file = input(ask + "Input file: "+cyan)
    if not os.path.isfile(in_file):
        print(error+' File not found')
        os.system("sleep 2")
        encrypt_xor_b64()
    out_file = input(ask + "Output file: " + green)
    with open(in_file, 'r', encoding='utf-8', errors='ignore') as in_f,open(out_file, 'w') as out_f:
       file_content = in_f.read()
       obfuscated_content = obfuscate_xor_base64(file_content)
       out_f.write(obfuscated_content)
    sprint(f"{success}{out_file} saved in {pwd}")
    mover(out_file)

def encrypt_double_b64():
    """NUEVO: Double Base64"""
    in_file = input(ask + "Input file: "+cyan)
    if not os.path.isfile(in_file):
        print(error+' File not found')
        os.system("sleep 2")
        encrypt_double_b64()
    out_file = input(ask + "Output file: " + green)
    with open(in_file, 'r', encoding='utf-8', errors='ignore') as in_f,open(out_file, 'w') as out_f:
       file_content = in_f.read()
       obfuscated_content = obfuscate_double_base64(file_content)
       out_f.write(obfuscated_content)
    sprint(f"{success}{out_file} saved in {pwd}")
    mover(out_file)

def encrypt_multi_layer():
    """NUEVO: Multi-Layer Encryption"""
    in_file = input(ask + "Input file: "+cyan)
    if not os.path.isfile(in_file):
        print(error+' File not found')
        os.system("sleep 2")
        encrypt_multi_layer()
    out_file = input(ask + "Output file: " + green)
    with open(in_file, 'r', encoding='utf-8', errors='ignore') as in_f,open(out_file, 'w') as out_f:
       file_content = in_f.read()
       obfuscated_content = obfuscate_multi_layer(file_content)
       out_f.write(obfuscated_content)
    sprint(f"{success}{out_file} saved in {pwd}")
    mover(out_file)

def encrypt_bytearray_b64():
    """NUEVO: Bytearray + Base64"""
    in_file = input(ask + "Input file: "+cyan)
    if not os.path.isfile(in_file):
        print(error+' File not found')
        os.system("sleep 2")
        encrypt_bytearray_b64()
    out_file = input(ask + "Output file: " + green)
    with open(in_file, 'r', encoding='utf-8', errors='ignore') as in_f,open(out_file, 'w') as out_f:
       file_content = in_f.read()
       obfuscated_content = obfuscate_bytearray_base64(file_content)
       out_f.write(obfuscated_content)
    sprint(f"{success}{out_file} saved in {pwd}")
    mover(out_file)


# Main function
def main():
    os.system("clear")
    sprint(logo, 0.01)
    print(f"\n{cyan}╔══════════════════════════════════╗")
    print(f"{cyan}║         ENCRYPTION MENU         ║")
    print(f"{cyan}╚══════════════════════════════════╝{white}")
    
    print(f"\n{yellow}┌─ {green}BASH ENCRYPTION{white}")
    print(f"{green}[1]{yellow} Encrypt Bash")
    print(f"{green}[2]{yellow} Decrypt Bash")
    
    print(f"\n{yellow}┌─ {green}PYTHON ENCRYPTION - BASIC{white}")
    print(f"{green}[3]{yellow} Base64 Standard")
    print(f"{green}[4]{yellow} Emoji Encryption")
    
    print(f"\n{yellow}┌─ {green}PYTHON ENCRYPTION - ADVANCED{white}")
    print(f"{green}[5]{yellow} Base64 + Zlib + Marshal")
    print(f"{green}[6]{yellow} Base64 + Marshal")
    print(f"{green}[7]{yellow} Zlib + Marshal")
    print(f"{green}[8]{yellow} XOR + Base64")
    print(f"{green}[9]{yellow} Double Base64")
    print(f"{green}[10]{yellow} Multi-Layer (3 layers)")
    print(f"{green}[11]{yellow} Bytearray + Base64")
    
    print(f"\n{yellow}┌─ {green}OTHER OPTIONS{white}")
    print(f"{green}[12]{yellow} About")
    print(f"{green}[0]{yellow} Exit")
    
    choose = input(f"{ask}{blue}Choose an option : {cyan}")
    
    if choose == "1" or choose == "01":
        encryptsh()
    elif choose == "2" or choose == "02":
        decryptsh()
    elif choose == "3" or choose == "03":
        encryptvar()
    elif choose == "4" or choose == "04":
        encryptem()
    elif choose == "5" or choose == "05":
        encrypt_b64_zlib_marshal()
    elif choose == "6" or choose == "06":
        encrypt_b64_marshal()
    elif choose == "7" or choose == "07":
        encrypt_zlib_marshal()
    elif choose == "8" or choose == "08":
        encrypt_xor_b64()
    elif choose == "9" or choose == "09":
        encrypt_double_b64()
    elif choose == "10":
        encrypt_multi_layer()
    elif choose == "11":
        encrypt_bytearray_b64()
    elif choose == "12":
        about()
    elif choose == "0":
        exit()
    else:
        sprint(error+'Wrong input!')
        os.system("sleep 2")
        main()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sprint(info+"Thanks for using. Have a good day!")
        exit()
    except Exception as e:
        sprint(error+str(e))