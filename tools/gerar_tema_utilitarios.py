# -*- coding: utf-8 -*-
"""Gera css/tema-utilitarios.css: reaponta as cores do Tailwind usadas no painel
para os tokens da Lube (css/tema-lube.css).

Por que existe: o index.html e o HTML montado pelo JavaScript usam centenas de
classes como `text-cyan-300`, `bg-red-950/60` e `border-slate-800`. Em vez de
reescrever cada uma, este script lê as classes que o arquivo realmente usa e
escreve uma regra para cada uma, apontando para o token da família de cor. Cor de
estado (verde, âmbar, vermelho) vira o token de estado; o ciano, que era o acento
do painel antigo, vira o azul da marca; bordas neutras viram a linha do tema.

Rodar depois de mexer em classes de cor:  python -I tools/gerar_tema_utilitarios.py
"""
import io
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE = os.path.join(RAIZ, "index.html")
SAIDA = os.path.join(RAIZ, "css", "tema-utilitarios.css")

FAMILIA = {
    "cyan": "azul", "sky": "azul", "lube-blue": "azul",
    "blue": "info", "indigo": "info",
    "red": "perigo", "rose": "perigo", "lube-red": "perigo",
    "emerald": "ok", "green": "ok", "lime": "ok",
    "amber": "atencao", "yellow": "atencao", "orange": "atencao",
    "purple": "violeta", "violet": "violeta", "fuchsia": "violeta",
    "teal": "teal", "pink": "rosa",
}
NEUTRAS = {"slate", "gray", "zinc", "neutral", "stone"}
TXT = {"azul": "--azul-txt", "info": "--info", "perigo": "--perigo", "ok": "--ok", "atencao": "--atencao",
       "violeta": "--violeta", "teal": "--teal", "rosa": "--rosa"}
BG = {"azul": "--azul-bg", "info": "--info-bg", "perigo": "--perigo-bg", "ok": "--ok-bg", "atencao": "--atencao-bg",
      "violeta": "--violeta-bg", "teal": "--teal-bg", "rosa": "--rosa-bg"}
SOLIDO = dict(TXT, azul="--azul-solido")

VARIANTES = ("hover", "focus", "dark", "placeholder", "group-hover", "focus-within")
PADRAO = re.compile(
    r"(?<![\w:-])((?:(?:%s):)*)(text|bg|border|border-l|border-t|border-b|border-r|divide|ring|accent)-"
    r"([a-z]+(?:-[a-z]+)?)-(\d{2,3})(?:/(\d{1,3}))?(?![\w-])" % "|".join(VARIANTES))
PADRAO_BW = re.compile(r"(?<![\w:-])((?:(?:%s):)*)(text|bg|border)-(white|black)(?:/(\d{1,3}))?(?![\w-])" % "|".join(VARIANTES))


def esc(cls):
    return re.sub(r"([:/\[\]#.%()])", r"\\\1", cls)


def seletor(variantes, cls, extra=""):
    base = "." + esc(cls)
    pseudo = ""
    prefixo = ""
    for v in variantes:
        if v == "hover":
            pseudo += ":hover"
        elif v == "focus":
            pseudo += ":focus"
        elif v == "focus-within":
            pseudo += ":focus-within"
        elif v == "dark":
            prefixo = ".dark "
        elif v == "group-hover":
            prefixo = ".group:hover "
        elif v == "placeholder":
            pseudo += "::placeholder"
    return prefixo + base + pseudo + extra


def mix(var, pct):
    return "color-mix(in srgb, var(%s) %d%%, transparent)" % (var, pct)


def valor(prop, cor, tom, op):
    """Devolve a cor CSS para a classe, ou None para deixar como está."""
    tom = int(tom)
    op = int(op) if op else None
    if cor in NEUTRAS:
        if prop == "text":
            return "var(--t1)" if tom <= 200 else "var(--t2)" if tom == 300 else "var(--t3)" if tom <= 600 else "var(--t1)"
        if prop == "bg":
            if tom >= 800:
                return "var(--s2)"
            if tom == 700:
                return "var(--s3)"
            if tom == 600:
                return "var(--linha-2)"
            return "var(--s2)" if tom <= 200 else None
        if prop.startswith("border") or prop == "divide":
            return "var(--linha-2)" if tom in (500, 600) else "var(--linha)"
        if prop == "ring":
            return "var(--linha-2)"
        return None
    fam = FAMILIA.get(cor)
    if not fam:
        return None
    if prop == "text":
        return "var(%s)" % TXT[fam]
    if prop == "bg":
        if tom >= 800 or tom <= 200:
            return "var(%s)" % BG[fam]
        if op is not None and op < 50:
            return mix(SOLIDO[fam], max(op, 12))
        return "var(%s)" % SOLIDO[fam]
    if prop.startswith("border") or prop == "divide":
        if fam == "azul":
            # o ciano era a borda de tudo; na cara nova, borda neutra
            if op is None:
                return "var(--ouro-linha)"
            return "var(--linha-2)" if op >= 40 else "var(--linha)"
        return mix(TXT[fam], min(int((op or 60) * 1.1), 70))
    if prop in ("ring", "accent"):
        return "var(--ouro-linha)" if fam == "azul" else "var(%s)" % TXT[fam]
    return None


def regra(variantes, prop, cls, cor_css):
    if prop == "text":
        if "placeholder" in variantes:
            return "%s { color: %s !important; }" % (seletor(variantes, cls), cor_css)
        return "%s { color: %s !important; }" % (seletor(variantes, cls), cor_css)
    if prop == "bg":
        return "%s { background-color: %s !important; }" % (seletor(variantes, cls), cor_css)
    if prop == "divide":
        return "%s { border-color: %s !important; }" % (seletor(variantes, cls, " > * + *"), cor_css)
    if prop == "ring":
        return "%s { --tw-ring-color: %s !important; }" % (seletor(variantes, cls), cor_css)
    if prop == "accent":
        return "%s { accent-color: %s !important; }" % (seletor(variantes, cls), cor_css)
    lado = {"border": "border-color", "border-l": "border-left-color", "border-t": "border-top-color",
            "border-b": "border-bottom-color", "border-r": "border-right-color"}[prop]
    return "%s { %s: %s !important; }" % (seletor(variantes, cls), lado, cor_css)


def main():
    texto = io.open(FONTE, encoding="utf-8").read()
    regras = {}
    for m in PADRAO.finditer(texto):
        variantes = [v for v in m.group(1).split(":") if v]
        prop, cor, tom, op = m.group(2), m.group(3), m.group(4), m.group(5)
        if cor not in FAMILIA and cor not in NEUTRAS:
            continue
        if "focus" in variantes and prop in ("border", "ring"):
            cor_css = "var(--ouro-linha)"
        else:
            cor_css = valor(prop, cor, tom, op)
        if not cor_css:
            continue
        cls = m.group(0)
        regras[cls] = regra(variantes, prop, cls, cor_css)

    for m in PADRAO_BW.finditer(texto):
        variantes = [v for v in m.group(1).split(":") if v]
        prop, cor, op = m.group(2), m.group(3), m.group(4)
        cls = m.group(0)
        if cor == "white":
            if prop == "text":
                cor_css = "var(--t1)"
            elif prop == "bg":
                if not op:
                    continue  # placa da logo e botão do assistente: branco de propósito
                cor_css = "var(--luz)"
            else:
                cor_css = "var(--linha)"
        else:
            if prop == "bg" and op:
                cor_css = "var(--veu)"
            else:
                continue
        regras[cls] = regra(variantes, prop, cls, cor_css)

    # Os seletores com variante dark:/hover: são mais específicos e vêm depois.
    ordenadas = sorted(regras.items(), key=lambda kv: (kv[0].count(":"), kv[0]))
    cab = ("/* GERADO por tools/gerar_tema_utilitarios.py — não editar à mão.\n"
           "   Reaponta %d classes de cor do Tailwind para os tokens de css/tema-lube.css. */\n" % len(ordenadas))
    corpo = "\n".join(r for _, r in ordenadas)
    # texto branco em botão de fundo sólido continua branco (vem depois e é mais específico)
    extra = ("\n.bg-lube-red.text-white, .bg-red-600.text-white, .bg-purple-600.text-white, .bg-amber-500.text-white,"
             " .bg-blue-600.text-white, .bg-lube-navy.text-white, .bg-emerald-600.text-white { color: #fff !important; }\n"
             ".bg-lube-navy { background-color: var(--azul) !important; }\n")
    io.open(SAIDA, "w", encoding="utf-8", newline="\n").write(cab + corpo + extra)
    print("%d regras em %s" % (len(ordenadas), SAIDA))


if __name__ == "__main__":
    main()
