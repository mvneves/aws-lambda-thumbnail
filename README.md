# AWS Lambda para criação de thumbnails de imagens do S3

A função é acionada quando uma imagem é enviada ao bucket de origem, gera uma miniatura com metade do tamanho e a
grava no bucket de destino.

## Buckets de origem e destino

O nome do bucket de destino é fixo no código (`lambda_function.py`, linha 37): ele precisa se chamar
**`<bucket-de-origem>-resized`**. Exemplo:

| Bucket | Nome |
|---|---|
| Origem | `thumbs-seunome` |
| Destino | `thumbs-seunome-resized` |

Nomes de bucket são únicos no mundo inteiro: use um nome próprio.

> **Atenção:** configure o gatilho **somente no bucket de origem**. Se o gatilho estiver no bucket onde a função grava
> as miniaturas, cada miniatura dispara a função de novo, criando um laço de invocações que consome os créditos do
> laboratório.

## Como implantar a lambda

1. Criar os buckets do S3 de origem e destino (veja os nomes acima).
2. Criar o pacote de implantação `lambda_function.zip` (veja abaixo).
3. Criar a função Lambda:
   - **Runtime:** Python 3.12 (o mesmo usado em `--python-version` ao criar o pacote; se forem diferentes, o Pillow
     não carrega e a função falha com `ImportError`)
   - **Arquitetura:** x86_64
   - **Permissões:** em *Change default execution role*, escolha **Use an existing role** e selecione **LabRole**. No
     AWS Academy Learner Lab não é possível criar a *role* que o console sugere.
4. Fazer upload do pacote de implantação (`lambda_function.zip`) em **Code > Upload from > .zip file**.
5. Em **Configuration > General configuration**, aumentar o *timeout* para 30 segundos e a memória para 512 MB
   (o padrão de 3 segundos não basta para imagens grandes).
6. Configurar o gatilho para eventos de criação do S3 (**Add trigger > S3**, evento *All object create events*) no
   bucket de **origem**.

## Como testar

- Fazer upload de uma imagem (JPEG ou PNG) para o bucket de origem.
- Uma versão em miniatura da imagem, com o prefixo `resized-`, será salva no bucket de destino.
- Se nada aparecer, consulte os logs da função em **Monitor > View CloudWatch logs**.

## Preparação do pacote de implantação

Instalar dependências (compiladas para o ambiente Linux do Lambda e para o Python 3.12):

```
mkdir package
pip install \
--platform manylinux2014_x86_64 \
--target=package \
--implementation cp \
--python-version 3.12 \
--only-binary=:all: --upgrade \
pillow boto3
```

Criar pacote de implantação:
```
cd package
zip -r ../lambda_function.zip .
cd ..
zip lambda_function.zip lambda_function.py
```
