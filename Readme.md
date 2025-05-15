# Brasileirão Assaí - Série A 2024

Aplicação para gerenciamento de partidas e resultados do Campeonato Brasileiro Série A 2024.

## 📋 Visão Geral

Este projeto fornece uma interface gráfica para:

- Visualizar e cadastrar resultados de partidas  
- Gerenciar rodadas do campeonato  
- Adiar partidas  
- Descadastrar resultados  
- Gerar tabela do campeonato  

## 🛠 Tecnologias Utilizadas

- **Python 3.x**  
- **CustomTkinter** – Para interface gráfica moderna  
- **PIL (Python Imaging Library)** – Para manipulação de imagens  
- **Padrão MVC (Model-View-Controller)**  

## 📁 Estrutura do Projeto

O projeto está organizado nos seguintes módulos principais:

### `View`

- `main_window.py` – Janela principal da aplicação  
- `matches_registration.py` – Interface para cadastro de partidas  
- `postpone_match.py` – Interface para adiamento de partidas  
- `unregister_match.py` – Interface para descadastro de partidas  

### `components/` – Componentes customizados de UI

- `button.py` – Botões estilizados  
- `combobox.py` – Combobox estilizados  
- `entry.py` – Campos de entrada estilizados  
- `frame.py` – Frames e containers estilizados  
- `label.py` – Labels estilizados

### `Controller`
- `controller_factory.py` – Adiministra a criação de todos os controllers e também cria os atributos DAO e Service para que possam ser passados por injeção de dependência, oque ajuda no desacoplamento e a não criar várias instâncias desnecessárias.
- `main_window_controller.py` – Controla a rodada selecionada e a geração do arquivo da tabela.  
- `matches_registration_controller.py` – Controla o cadastro dos resultados das partidas.
- `postpone_match_controller.py` – Controla o adiamento de uma partida.
- `round_registration_controller.py` - Controla o registro das partidas de uma rodada.
- `unregister_match_controller.py` - Controla o alteração do resultado ou dos times de uma rodada.

### Outros tópicos importantes
A aplicação é guiada por eventos. A logica para a criação de desses eventos estão no arquivo 'event_manager' dentro da pasta 'utils'. Nessa lógica as views se inscrevem nos eventos e o controller dispara o evento. Por exemplo a view da janela principal se inscreve no evento de acessar uma rodada selecionada. O controller vai disparar esse evento quando o botão for acionado e a view vai direcionar para a janela da rodada correspondente.

O 'RoundService' salva os dados localmente para não precisar acessar o banco de dados toda hora (Como uma cache).

As interações com o banco de dados ocorrem só em arquivos DAOs.

para rodar o codigo o comando é: 'python goldTabela.py'

para gerar o executavel o comando é: 'pyinstaller --onefile --noconsole --icon=Assets/img/icon.ico GoldTabela.py'


- 
