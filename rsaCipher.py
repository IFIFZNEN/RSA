import sys

DEFAULT_BLOCK_SIZE = 128
BYTE_SIZE = 256

def main():
    filename = 'encrypted_file.txt' # файл для записи и чтения
    mode = input("Viberite mode [E]ncrypt | [D]ecrypt: ")

    if mode == 'E':
        message = input("Vvedite text: ")
        pubKeyFilename = 'al_sweigart_pubkey.txt'
        print('Ваш текст шифруется и записывается в %s...' % (filename))
        encryptedText = encryptAndWriteToFile(filename, pubKeyFilename, message)

        print('Шифрованный текст:')
        print(encryptedText)

    elif mode == 'D':
        privKeyFilename = 'al_sweigart_privkey.txt'
        print('Читаю из файла %s и продолжаю расшифрование...' % (filename))
        decryptedText = readFromFileAndDecrypt(filename, privKeyFilename)

        print('Расшифрованный текст:')
        print(decryptedText)


def getBlocksFromText(message, blockSize=DEFAULT_BLOCK_SIZE):
    messageBytes = message.encode('ascii') # convert the string to bytes

    blockInts = []
    for blockStart in range(0, len(messageBytes), blockSize):
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(messageBytes))):
            blockInt += messageBytes[i] * (BYTE_SIZE ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize=DEFAULT_BLOCK_SIZE):
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                asciiNumber = blockInt // (BYTE_SIZE ** i)
                blockInt = blockInt % (BYTE_SIZE ** i)
                blockMessage.insert(0, chr(asciiNumber))
        message.extend(blockMessage)
    return ''.join(message)


def encryptMessage(message, key, blockSize=DEFAULT_BLOCK_SIZE):
    encryptedBlocks = []
    n, e = key

    for block in getBlocksFromText(message, blockSize):
        # ciphertext = plaintext ^ e mod n
        encryptedBlocks.append(pow(block, e, n))
    return encryptedBlocks


def decryptMessage(encryptedBlocks, messageLength, key, blockSize=DEFAULT_BLOCK_SIZE):
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
        # plaintext = ciphertext ^ d mod n
        decryptedBlocks.append(pow(block, d, n))
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


def readKeyFile(keyFilename):
    fo = open(keyFilename)
    content = fo.read()
    fo.close()
    keySize, n, EorD = content.split(',')
    return (int(keySize), int(n), int(EorD))


def encryptAndWriteToFile(messageFilename, keyFilename, message, blockSize=DEFAULT_BLOCK_SIZE):
    keySize, n, e = readKeyFile(keyFilename)
    if keySize < blockSize * 8: # * 8 to convert bytes to bits
        sys.exit('ОШИБКА: Размер блока составляет %s бит, а размер ключа - %s бит. Шифр RSA требует, чтобы размер блока был равен или больше размера ключа. Либо уменьшите размер блока.' % (blockSize * 8, keySize))


    # Encrypt the message
    encryptedBlocks = encryptMessage(message, (n, e), blockSize)
    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ','.join(encryptedBlocks)
    encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)
    fo = open(messageFilename, 'w')
    fo.write(encryptedContent)
    fo.close()
    return encryptedContent


def readFromFileAndDecrypt(messageFilename, keyFilename):
    keySize, n, d = readKeyFile(keyFilename)
    fo = open(messageFilename)
    content = fo.read()
    messageLength, blockSize, encryptedMessage = content.split('_')
    messageLength = int(messageLength)
    blockSize = int(blockSize)
    if keySize < blockSize * 8: # * 8 to convert bytes to bits
        sys.exit('ОШИБКА: Размер блока составляет %s бит, а размер ключа - %s бит. Шифр RSA требует, чтобы размер блока был равен или больше размера ключа. Вы указали правильный файл ключа и зашифрованный файл?' % (blockSize * 8, keySize))
    encryptedBlocks = []
    for block in encryptedMessage.split(','):
        encryptedBlocks.append(int(block))
    return decryptMessage(encryptedBlocks, messageLength, (n, d), blockSize)

if __name__ == '__main__':
    main()
