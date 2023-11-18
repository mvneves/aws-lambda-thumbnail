AWS Lambda para criação de thumbnails de imagens do S3


Como implantar a lambda:

- Criar os buckets do S3 de origem e destino​
- Criar a função Lambda​
- Criar o pacote de implantação​
- Fazer upload do pacote de implantação​ (lambda_function.zip)
- Configurar o gatilho para eventos de criação do S3​ no bucket de origem

Como testar:​

- Fazer upload de uma imagem para o bucket de origem​
- Uma versão em miniatura da imagem será salva no bucket de destino​

Preparação do pacote de implantação:

Instalar dependências:

```
mkdir package
pip install \
--platform manylinux2014_x86_64 \
--target=package \
--implementation cp \
--python-version 3.9 \
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
