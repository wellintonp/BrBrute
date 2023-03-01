# BrBrute
BrBute é um script simples de força bruta para páginas de login do site, destina-se a ser um projeto de estudos e não se destina a uso criminoso.

[![Callow](logo.svg "BrBrute")](#)

## Requirements

1. Python 3.10+
2. Google chrome
3. [ChromeDriver](https://chromedriver.chromium.org/)

**Nota:** Use a versão do ChromeDriver correspondente à sua versão do Chrome.

## Instalação

- Clone o repositório

```sh
git clone github.com/maximousblk/callow.git
```

- Instalar dependências:

```sh
pip3 install -r requirements.txt
```

## Atualizando

Se você deseja obter as atualizações mais recentes do BrBrute:

```sh
git pull
```

## Começo rápido

Se você estiver fazendo isso pela primeira vez, poderá testá-lo com segurança em sandbox

1. Execute `BrBrute.py` no diretório de principal
2. Digite a URL para o login
3. Vá para a página de login
4. Abra as ferramentas do desenvolvedor usando `Ctrl` + `Shift` + `I`
5. Digite o seletor css para as tags `<input>` para o campo de nome de usuário e senha
6. Digite o nome de usuário ou e-mail do alvo
7. Digite a localização do dicionário/lista de senhas e pressione Enter

## Argumentos

Você também pode passar essas opções na forma de argumentos.

Essas são as opções para o BrBrute

| Opção    | Função                           |
| -------- | -------------------------------- |
| `--site` | Site (somente http/https)        |
| `--usel` | Input do nome de usuário         |
| `--psel` | Input da senha                   |
| `--user` | Nome do usuário a atacar         |
| `--pass` | Lista de senhas                  |

## Pendência

- [X] Compatibilidade com Python 3.x
- [X] Compatibilidade entre plataformas
- [ ] Suporte a proxy/Tor

## Isenção de responsabilidade

> Este projeto (BrBrute) e seus colaboradores não apóiam ou se responsabilizam por qualquer forma de ato antiético. Este software é apenas para fins educacionais e não se destina a causar nenhum dano.

## License

BrBrute está disponível gratuitamente sob o [GPL-3.0 license](https://www.gnu.org/licenses/gpl-3.0.en.html) e pode ser usado para fins comerciais e não comerciais.
