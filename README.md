<img width="2560" height="1292" alt="Image" src="https://github.com/user-attachments/assets/59966978-3648-47b9-a4f9-42c4ded1dea2" />

# 🎬 Django Video Editor & Clipper

Uma aplicação web desenvolvida em **Python** e **Django** que permite aos usuários fazer o upload de vídeos, realizar cortes baseados em intervalos de tempo personalizados e remover o áudio, caso desejem. O processamento do vídeo é feito utilizando a biblioteca **MoviePy**.

---

## ✨ Funcionalidades

* **Upload Seguro:** Suporte a múltiplos formatos de mídia (`.mp4`, `.avi`, `.mov`, `.mkv`, `.flv`, `.wmv`, `.webm`).
* **Corte de Precisão (Subclip):** Define o tempo inicial e final do trecho que deseja salvar.
* **Remoção de Áudio:** Opção via checkbox para silenciar o vídeo final.
* **Gerenciamento Inteligente de Arquivos:** * Geração de nomes de arquivos únicos usando `uuid` para evitar conflitos.
    * Exclusão automática do vídeo original do servidor após o processamento para economizar espaço de armazenamento.
* **Validações de Segurança:** O sistema valida inputs incorretos (valores negativos, tempo final menor que inicial ou tempo maior que a duração total do vídeo).

---

## 🛠️ Tecnologias Utilizadas

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [MoviePy](https://zulko.github.io/moviepy/) (Processamento e edição de vídeo)

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
Certifique-se de ter o **Python 3.x** instalado em sua máquina. O MoviePy também pode exigir o `ffmpeg` instalado no sistema para renderizar certos formatos.

### 1. Clonar o Repositório
```bash
git clone https://github.com/carlosrenandev/reclip-editor-online-django
cd reclip-editor-online-django
