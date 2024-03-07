# Fall-Into-oblivion
FALL-INTO-OBLIVION: Um Estranho Cesto do Lixo

O objetivo principal deste projeto é construir uma aplicação que simule a funcionalidade do Recycle Bin dos sistemas operativos modernos, mas de uma forma alternativa pouco convencional. Na verdade, a aplicação a desenvolver deve estar constantemente a monitorizar uma pasta chamada FALL-INTO-OBLIVION, e cifrar automaticamente todos os ﬁcheiros que aí forem colocados. Deve também calcular um valor resumo, um Message Authentication
Code (MAC) ou uma assinatura digital do ﬁcheiro. A chave usada para cifrar o ﬁcheiro e calcular o MAC deve ser gerada automaticamente para cada ﬁcheiro, mas derivada de um Personal Identiﬁcation Number (PIN) de 3 ou 4 dígitos. Se um utilizador desejar reaver o seu ﬁcheiro mais tarde, tem de adivinhar o código com que foi cifrado e autenticado. Tem 3 hipóteses para conseguir decifrar o ﬁcheiro. Depois dessas 3 tentativas, o ﬁcheiro deve ser eliminado do sistema operativo.
De uma forma geral, pode-se dizer que a aplicação a desenvolver deve:
permitir cifrar ﬁcheiros, guardando o resultado numa pasta chamada FALL-INTO-OBLIVION;
calcular o valor de hash do ﬁcheiro, guardando também o resultado junto com o criptograma (em ﬁcheiros separados);
gerar automaticamente um PIN, e usá-lo como chave para cifrar cada ﬁcheiro; 
calcular o MAC dos criptogramas;
permitir decifrar o ﬁcheiro por via da adivinhação do PIN. Só devem ser permitidas até 3 tentativas;
veriﬁcar a integridade do ﬁcheiro no caso do PIN ter sido adivinhado.

A aplicação pode correr em modo Client Line Interface (CLI) ou em modo gráﬁco (ﬁca ao critério dos executantes). Devem usar cifras e mecanismos de autenticação de mensagens de qualidade (e.g., Advanced Encryption Standard em modo Cipher Block Chaining (AES-CBC) e Hash MAC Secure Hash Algorithm 256 (HMAC-SHA256)). Podem fortalecer o trabalho e solidiﬁcar o conhecimento através da implementação das seguintes funciona-
lidades:
substituir os MACs por assinaturas digitais (o programa deve então também permitir gerar as chaves pública e privadas);
permitir que o utilizador escolha a cifra a utilizar e o comprimento da chave de cifra;
permitir que o utilizador escolha a função de hash a usar; 
ter um help completo e intuitivo.

Uma versão muito básica deste trabalho pode utilizar chamadas ao sistema (comandos OpenSSL). A forma ideal de implementar o trabalho passar por integrar os mecanismos criptográﬁcos na própria aplicação. Pensem numa forma de atacar o sistema (uma falha da sua implementação) e dediquem-lhe um pequeno intervalo de tempo na apresentação.
---
