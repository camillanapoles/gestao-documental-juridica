# Configuração para Empacotamento Android

Este documento descreve os passos necessários para empacotar a aplicação web para Android usando o framework Capacitor.

## Pré-requisitos

- Node.js e npm instalados
- Android Studio instalado
- JDK 11 ou superior
- Capacitor CLI

## Passos para Empacotamento

1. Instalar dependências do Capacitor
2. Inicializar projeto Capacitor
3. Adicionar plataforma Android
4. Configurar permissões e recursos
5. Construir aplicação web
6. Copiar arquivos para o projeto Android
7. Abrir no Android Studio e gerar APK

## Instruções Detalhadas

```bash
# 1. Instalar Capacitor
npm install @capacitor/core @capacitor/cli @capacitor/android

# 2. Inicializar Capacitor
npx cap init "Gestão Documental Jurídica" "com.docjur.app" --web-dir=build

# 3. Adicionar plataforma Android
npx cap add android

# 4. Construir aplicação web
# (Certifique-se que os arquivos estáticos estão na pasta 'build')

# 5. Copiar arquivos para o projeto Android
npx cap copy android

# 6. Abrir no Android Studio
npx cap open android
```

## Configurações Específicas para Android

No arquivo `android/app/src/main/AndroidManifest.xml`, adicione as seguintes permissões:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.CAMERA" />
```

## Geração do APK

1. No Android Studio, selecione "Build" > "Build Bundle(s) / APK(s)" > "Build APK(s)"
2. O APK será gerado em `android/app/build/outputs/apk/debug/app-debug.apk`

## Configuração do Servidor

Certifique-se de que o servidor backend esteja configurado para aceitar requisições do aplicativo Android, adicionando os cabeçalhos CORS apropriados.
