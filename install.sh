#!/usr/bin/bash

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

if [ -d $PROJECT_DIR/venv ]
then
  DEL=""
  while [ "$DEL" != "Y" ] && [ "$DEL" != "y" ] && [ "$DEL" != "N" ] && [ "$DEL" != "n" ]
  do
    echo "Virtual environment existente, deletar e reinstalar o ambiente? (Y/N)"
    read DEL
  done
  if [ "$DEL" == "Y" ] || [ "$DEL" == "y" ]
  then
    rm -rf $PROJECT_DIR/venv
  else
    echo "Cancelando instalacao"
    return
  fi
fi

PYTHON_VERSION=`python3 -c 'import sys; version=sys.version_info[:2]; print("python{0}.{1}".format(*version))'`

echo "Criando ambiente virtual Python3"
python3 -m venv $PROJECT_DIR/venv

echo "Ativando virtual environment e instalando dependências"
source $PROJECT_DIR/venv/bin/activate

pip install -r $PROJECT_DIR/requirements.txt

ENV=0
while [ $ENV -gt 3 ] || [ $ENV -lt 1 ]
do
  echo "Escolha a instalacao das chaves keyring:"
  echo "1 - Armazenar chaves"
  echo "2 - Nao armazenar automaticamente"
  read ENV
done

case $ENV in
1)
  echo "Armazenando as chaves..."
  echo "Inserir user_db: "
  read KEY
  python $PROJECT_DIR/src/extras/install_keys.py --subject user_db --secret $KEY
  echo "Inserir a senha do user_db: "
  read KEY
  python $PROJECT_DIR/src/extras/install_keys.py --subject pass_db --secret $KEY
  echo "Inserir o SID do banco: "
  read KEY
  python $PROJECT_DIR/src/extras/install_keys.py --subject sid_db --secret $KEY
  echo "Chaves armazenadas"
  ;;
2)
  echo "As chaves nao foram armazenadas, para utilizar o projeto, você deverá fazer manualmente!"
  ;;
esac

deactivate

echo Ambiente instalado