# RSA
Открытый ключ, который мы реализуем, основан на алгоритме RSA (Rivest - Shamir - Adleman), предложенном в 1977 году. Название алгоритма образовано первыми буквами фамилий его изобретателей: Рональд Ривест, Ади Шамир и Леонард Адлеман. В RSA используются большие простые числа, содержащие сотни цифр. В алгоритме открытого ключа генерируются два случайных простых числа, которые затем сложным образом комбинируются для создания открытого и закрытого ключей.
RSA (подобно другим криптосистемам с открытым ключом) позволяет не только шифровать послания, но и снабжать цифровой подписью файл или текст. Например, Алиса может зашифровать сообщение своим закрытым ключом, создав таким образом шифротекст, который можно дешифровать только с помощью открытого ключа Алисы. Этот шифротекст становится цифровой подписью к файлу. Фактически он даже не является секретным, так как любой человек в мире может прочитать его с помощью общедоступного открытого ключа Алисы. Суть в другом: шифруя сообщение с помощью своего закрытого ключа Алиса снабжает сообщение цифровой подписью способом, не допускающим ее подделку. Поскольку единственным обладателем закрытого ключа является Алиса, только она могла создать такой шифротекст, а значит, она уже не сможет утверждать, что Боб подделал или изменил сообщение! 
Гарантия того, что подписанные сообщения впоследствии не сможет отрицать своего авторства, называется невозможность отказа (non-repudiation).

Порядок генерирования открытых и закрытых ключей
	В криптосистемах с открытым ключом каждый ключ состоит из двух чисел. Открытым ключом служат числа n и е, закрытым - числа n и d. Эти числа создаются в три этапа:
1. Создайте два очень больших простых числа: р и q. Это должны быть два разных случайных числа. Перемножьте их для получения числа n. 
2. Создайте случайное число е, взаимно простое с числом (р - 1) (q - 1). 
3. Вычислите модульное обращение числа е — это будет число d.
	Число n используется в обоих ключах. Число d должно храниться в тайне, поскольку оно позволяет дешифровывать сообщения. Теперь все готово для написания программы, которая будет генерировать эти ключи.
