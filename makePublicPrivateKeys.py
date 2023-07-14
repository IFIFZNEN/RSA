import random, sys, os, primeNum, cryptomath

def main():
    # Create a public/private keypair with 1024 bit keys:
    print('Создание ключевых файлов...')
    makeKeyFiles('al_sweigart', 1024)
    print('Сделаны ключевые файлы.')

def generateKey(keySize):
    # Creates a public/private keys keySize bits in size.
    p = 0
    q = 0
    # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
    print('Генерация простых чисел p & q...')
    while p == q:
        p = primeNum.generateLargePrime(keySize)
        q = primeNum.generateLargePrime(keySize)
    n = p * q

    # Step 2: Create a number e that is relatively prime to (p-1)*(q-1):
    print('Генерация e, которая относительно проста для (p-1)*(q-1)...')
    while True:
        # Keep trying random numbers for e  until one is valid:
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    # Step 3: Calculate d, the mod inverse of e:
    print('Вычисление d, которое является модулем, обратным e...')
    d = cryptomath.findModInverse(e, (p - 1) * (q - 1))

    publicKey = (n, e)
    privateKey = (n, d)

    print('Public key:', publicKey)
    print('Private key:', privateKey)

    return (publicKey, privateKey)


def makeKeyFiles(name, keySize):


    # Our safety check will prevent us from overwriting our old key files:
    if os.path.exists('%s_pubkey.txt' % (name)) or os.path.exists('%s_privkey.txt' % (name)):
        sys.exit('ПРЕДУПРЕЖДЕНИЕ: Файл %s_pubkey.txt или %s_privkey.txt уже существует! Используйте другое имя или удалите эти файлы и повторно запустите эту программу.' % (name, name))

    publicKey, privateKey = generateKey(keySize)

    print()
    print('Открытый ключ представляет собой %s и %s-значный номер.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
    print('Запись открытого ключа в файл %s_pubkey.txt ...' % (name))
    fo = open('%s_pubkey.txt' % (name), 'w')
    fo.write('%s,%s,%s' % (keySize, publicKey[0], publicKey[1]))
    fo.close()

    print()
    print('Закрытый ключ состоит из %s и %s-значного числа.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
    print('Запись закрытого ключа в файл%s_privkey.txt ...' % (name))
    fo = open('%s_privkey.txt' % (name), 'w')
    fo.write('%s,%s,%s' % (keySize, privateKey[0], privateKey[1]))
    fo.close()


# If makePublicPrivateKeys.py is run (instead of imported as a module),
# call the main() function:
if __name__ == '__main__':
    main()
