import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


# ==============================
# CATEGORIAS
# ==============================

categorias = {
    '.jpg': 'Imagens',
    '.jpeg': 'Imagens',
    '.png': 'Imagens',
    '.gif': 'Imagens',
    '.ico': 'Imagens',

    '.pdf': 'Documentos',

    '.mp3': 'Musicas',
    '.wav': 'Musicas',

    '.mp4': 'Videos',
    '.avi': 'Videos',
    '.flv': 'Videos',

    '.txt': 'Textos',

    '.py': 'Programas',

    '.exe': 'Aplicativos'
}


# ==============================
# JANELA
# ==============================

janela = tk.Tk()
janela.title("FILEFLOW")
janela.geometry("850x600")
janela.minsize(750, 500)


# ==============================
# CORES
# ==============================

FUNDO = "#1e1e1e"
PAINEL = "#252526"
CAMPO = "#333333"
TEXTO = "#ffffff"
TEXTO_SECUNDARIO = "#aaaaaa"
BOTAO = "#0078d4"
BOTAO_HOVER = "#1a8cff"
SUCESSO = "#4caf50"
ERRO = "#f44336"


janela.configure(bg=FUNDO)


# ==============================
# ESTILO
# ==============================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TButton",
    font=("Segoe UI", 10),
    padding=8
)

style.configure(
    "TCombobox",
    font=("Segoe UI", 10),
    padding=5
)


# ==============================
# TÍTULO
# ==============================

titulo = tk.Label(
    janela,
    text="📁 FILEFLOW",
    font=("Segoe UI", 24, "bold"),
    bg=FUNDO,
    fg=TEXTO
)

titulo.pack(pady=(25, 5))


subtitulo = tk.Label(
    janela,
    text="Organize seus arquivos automaticamente por categoria",
    font=("Segoe UI", 11),
    bg=FUNDO,
    fg=TEXTO_SECUNDARIO
)

subtitulo.pack(pady=(0, 20))


# ==============================
# PAINEL DA PASTA
# ==============================

painel_pasta = tk.Frame(
    janela,
    bg=PAINEL,
    padx=20,
    pady=20
)

painel_pasta.pack(
    fill="x",
    padx=30
)


label_pasta = tk.Label(
    painel_pasta,
    text="Pasta para organizar",
    font=("Segoe UI", 11, "bold"),
    bg=PAINEL,
    fg=TEXTO
)

label_pasta.pack(anchor="w")


# ==============================
# CAMPO DA PASTA
# ==============================

frame_caminho = tk.Frame(
    painel_pasta,
    bg=PAINEL
)

frame_caminho.pack(
    fill="x",
    pady=(10, 0)
)


pasta_var = tk.StringVar()


entrada_pasta = tk.Entry(
    frame_caminho,
    textvariable=pasta_var,
    font=("Segoe UI", 11),
    bg=CAMPO,
    fg=TEXTO,
    insertbackground=TEXTO,
    relief="flat"
)

entrada_pasta.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=8
)


def escolher_pasta():
    pasta = filedialog.askdirectory(
        title="Escolha a pasta que deseja organizar"
    )

    if pasta:
        pasta_var.set(pasta)
        organizar()


botao_pasta = tk.Button(
    frame_caminho,
    text="📂 Escolher pasta",
    command=escolher_pasta,
    bg=BOTAO,
    fg="white",
    activebackground=BOTAO_HOVER,
    activeforeground="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    cursor="hand2",
    padx=15,
    pady=8
)

botao_pasta.pack(
    side="right",
    padx=(10, 0)
)


# ==============================
# ESTATÍSTICAS
# ==============================

frame_stats = tk.Frame(
    janela,
    bg=FUNDO
)

frame_stats.pack(
    fill="x",
    padx=30,
    pady=20
)


def criar_stat(parent, titulo, valor):
    frame = tk.Frame(
        parent,
        bg=PAINEL,
        padx=20,
        pady=15
    )

    frame.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5
    )

    tk.Label(
        frame,
        text=titulo,
        font=("Segoe UI", 10),
        bg=PAINEL,
        fg=TEXTO_SECUNDARIO
    ).pack()

    label = tk.Label(
        frame,
        text=valor,
        font=("Segoe UI", 22, "bold"),
        bg=PAINEL,
        fg=TEXTO
    )

    label.pack()

    return label


label_encontrados = criar_stat(
    frame_stats,
    "Encontrados",
    "0"
)

label_organizados = criar_stat(
    frame_stats,
    "Organizados",
    "0"
)

label_sem_categoria = criar_stat(
    frame_stats,
    "Sem categoria",
    "0"
)


# ==============================
# LOG
# ==============================

tk.Label(
    janela,
    text="Atividade",
    font=("Segoe UI", 11, "bold"),
    bg=FUNDO,
    fg=TEXTO
).pack(
    anchor="w",
    padx=35
)


frame_log = tk.Frame(
    janela,
    bg=PAINEL
)

frame_log.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=(8, 15)
)


log = tk.Text(
    frame_log,
    height=8,
    bg=PAINEL,
    fg=TEXTO,
    insertbackground=TEXTO,
    font=("Consolas", 10),
    relief="flat",
    wrap="word"
)

log.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


def escrever_log(texto):
    log.insert("end", texto + "\n")
    log.see("end")


# ==============================
# ORGANIZAR
# ==============================

def organizar():

    pasta_origem = pasta_var.get().strip()

    if not pasta_origem:
        messagebox.showwarning(
            "Pasta não selecionada",
            "Escolha uma pasta antes de continuar."
        )
        return

    if not os.path.exists(pasta_origem):
        messagebox.showerror(
            "Erro",
            "Essa pasta não existe."
        )
        return

    if not os.path.isdir(pasta_origem):
        messagebox.showerror(
            "Erro",
            "O caminho selecionado não é uma pasta."
        )
        return

    confirmacao = messagebox.askyesno(
        "Confirmar organização",
        f"Deseja organizar esta pasta?\n\n{pasta_origem}"
    )

    if not confirmacao:
        escrever_log("Operação cancelada.")
        return

    arquivos = os.listdir(pasta_origem)

    quantidade_arquivos = 0
    quantidade_organizados = 0
    quantidade_sem_categoria = 0

    escrever_log("")
    escrever_log("=" * 50)
    escrever_log("INICIANDO ORGANIZAÇÃO")
    escrever_log("=" * 50)

    for arquivo in arquivos:

        caminho = os.path.join(
            pasta_origem,
            arquivo
        )

        if os.path.isfile(caminho):

            quantidade_arquivos += 1

            nome, extensao = os.path.splitext(arquivo)

            extensao = extensao.lower()

            pasta = categorias.get(extensao)

            if pasta:

                destino = os.path.join(
                    pasta_origem,
                    pasta
                )

                if not os.path.exists(destino):
                    os.mkdir(destino)

                try:

                    shutil.move(
                        caminho,
                        os.path.join(
                            destino,
                            arquivo
                        )
                    )

                    quantidade_organizados += 1

                    escrever_log(
                        f"✓ {arquivo} → {pasta}"
                    )

                except Exception as erro:

                    escrever_log(
                        f"✗ Erro ao mover {arquivo}: {erro}"
                    )

            else:

                quantidade_sem_categoria += 1

                escrever_log(
                    f"• {arquivo} → sem categoria"
                )

    # Atualiza estatísticas

    label_encontrados.config(
        text=str(quantidade_arquivos)
    )

    label_organizados.config(
        text=str(quantidade_organizados)
    )

    label_sem_categoria.config(
        text=str(quantidade_sem_categoria)
    )

    escrever_log("")
    escrever_log("=" * 50)
    escrever_log("ORGANIZAÇÃO CONCLUÍDA")
    escrever_log("=" * 50)

    messagebox.showinfo(
        "Concluído",
        f"Organização concluída!\n\n"
        f"Arquivos encontrados: {quantidade_arquivos}\n"
        f"Arquivos organizados: {quantidade_organizados}\n"
        f"Sem categoria: {quantidade_sem_categoria}"
    )


# ==============================
# BOTÃO ORGANIZAR
# ==============================

botao_organizar = tk.Button(
    janela,
    text="▶  FILEFLOW",
    command=organizar,
    bg=BOTAO,
    fg="white",
    activebackground=BOTAO_HOVER,
    activeforeground="white",
    font=("Segoe UI", 12, "bold"),
    relief="flat",
    cursor="hand2",
    padx=20,
    pady=12
)

botao_organizar.pack(
    pady=(0, 25)
)


# ==============================
# INICIAR
# ==============================

janela.mainloop()