# Documentação do Ambiente de Demonstração

## Visão Geral
Este documento descreve o ambiente de demonstração criado para o Sistema de Gestão Documental Jurídica, uma solução alternativa implementada devido a limitações estruturais identificadas no ambiente de CI/CD do GitHub Actions.

## Estrutura do Ambiente de Demonstração
O ambiente de demonstração consiste em uma página web estática que ilustra as principais funcionalidades e o design da aplicação. Esta abordagem foi escolhida para permitir a visualização do conceito e da experiência do usuário, enquanto contornamos as limitações técnicas do pipeline de deploy automatizado.

### Arquivos e Diretórios
- `/demo/index.html` - Página principal de demonstração
- `/demo/assets/` - Recursos estáticos (imagens, CSS, JS)
- `/docs/` - Documentação detalhada do projeto

## Funcionalidades Demonstradas
O ambiente de demonstração ilustra as seguintes funcionalidades principais:

1. **Interface Centrada no Usuário**
   - Design intuitivo e acessível
   - Navegação simplificada
   - Linguagem clara e não-técnica

2. **Gestão de Documentos**
   - Upload simplificado
   - Checklist incremental
   - Visualização integrada de documentos

3. **Comunicação Contextual**
   - Troca de mensagens por documento
   - Anotações em documentos
   - Histórico de comunicações

4. **Segurança e Privacidade**
   - Armazenamento seguro
   - Controle de acesso
   - Proteção de dados

## Como Acessar o Ambiente de Demonstração
O ambiente de demonstração pode ser acessado de duas formas:

1. **Localmente**:
   - Clone o repositório: `git clone https://github.com/camillanapoles/gestao-documental-juridica.git`
   - Navegue até o diretório: `cd gestao-documental-juridica/demo`
   - Abra o arquivo `index.html` em qualquer navegador moderno

2. **Online** (quando disponível):
   - Acesse: `https://camillanapoles.github.io/gestao-documental-juridica/demo/`

## Limitações do Ambiente de Demonstração
É importante notar que este ambiente de demonstração tem as seguintes limitações:

1. **Funcionalidade Limitada**: Trata-se de uma demonstração visual, sem funcionalidades de backend implementadas
2. **Dados Estáticos**: Não há persistência de dados ou interações reais com banco de dados
3. **Sem Autenticação**: O sistema de login e autenticação é apenas visual

## Próximos Passos
Para uma implementação completa e funcional, recomendamos:

1. Resolver os problemas estruturais do ambiente CI/CD
2. Implementar o backend completo com Flask e SQLAlchemy
3. Configurar o armazenamento S3 para documentos
4. Estabelecer um pipeline de CI/CD alternativo

## Contato para Suporte
Para qualquer dúvida ou suporte relacionado ao ambiente de demonstração, entre em contato através de:
- Email: suporte@docjur.com.br
- GitHub: Abra uma issue no repositório
