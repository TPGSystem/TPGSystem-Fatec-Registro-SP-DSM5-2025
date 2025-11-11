# ===============================================================
#  GERENCIADOR DE ESTADO GLOBAL DO JOGO
#  ------------------------------------
#  Este arquivo centraliza todas as variáveis que controlam o
#  progresso do jogador no jogo, como:
#     - Personagem selecionado
#     - Áreas (fases) concluídas
#     - Inventário (itens, moedas, etc.)
#     - Flags (marcadores de eventos ou condições)
#
#  O objetivo é ter um único local de referência para o "estado
#  do jogo", evitando dados espalhados por várias classes.
#  Assim, se o jogador voltar para o menu principal, basta
#  chamar STATE.reset() para limpar tudo e recomeçar do zero.
#
#  ► Integração recomendada:
#     - Title.on_enter(): STATE.reset() (ou somente em "Novo Jogo")
#     - Level quando vence: STATE.complete_area("Level_1_2"); STATE.save()
#     - Map ao abrir: consultar STATE.is_area_completed() e STATE.is_area_unlocked()
#     - Em qualquer interação: STATE.add_item(), STATE.set_flag(), etc.
# ===============================================================

from __future__ import annotations

# dataclass facilita classes de dados (gera __init__, __repr__, etc.)
from dataclasses import dataclass, field
from pathlib import Path
import json
import tempfile
import os
from typing import Any


# =========================
# Persistência / versão
# =========================
STATE_VERSION = 1                    # versão do "schema" salvo no JSON (permite migrações futuras)
SAVE_PATH = Path("save/state.json")  # caminho único do arquivo de save

# Centralize aqui os nomes das áreas necessárias para liberar a área final.
# DICA: mantenha essa lista atualizada quando novas fases forem adicionadas.
REQUIRED_FOR_FINAL = {
    "Level_1_1",
    "Level_1_2",
    # acrescente as demais áreas necessárias...
}
# Nome exato da última área (bloqueada até concluir as anteriores)
FINAL_AREA_NAME = "Propugnáculo Além-Mar"

# ---------------------------------------------------------------
# Classe principal que armazena o estado do jogo
# ---------------------------------------------------------------
@dataclass(slots=True)
class GameState:
    """
    Representa o estado global do jogo durante a execução.

    Essa classe guarda as informações principais do progresso do jogador
    (como personagem, fases concluídas e inventário) e permite que sejam
    acessadas e modificadas por qualquer parte do código que precise
    dessas informações.

    ► Por que 'slots=True'?
      - Reduz consumo de memória e evita criação acidental de atributos
        não declarados (erros de digitação, por exemplo).
    """

    # Nome/ID do personagem escolhido na seleção (None se ainda não escolheu)
    selected_character: str | None = None

    # Áreas concluídas pelo jogador (set evita duplicatas e facilita consulta)
    completed_areas: set[str] = field(default_factory=set)

    # Inventário do jogador: nome -> quantidade (ex.: {"Poção": 2, "Moedas": 37})
    inventory: dict[str, int] = field(default_factory=dict)

    # Flags de progresso/eventos: chave -> bool (ex.: {"falou_com_cacique": True})
    flags: dict[str, bool] = field(default_factory=dict)

    # -----------------------------------------------------------
    # Reset total do progresso (útil em "Novo Jogo" ou ao voltar ao Title)
    # -----------------------------------------------------------
    def reset(self):
        """
        Restaura o estado do jogo ao padrão inicial.
        Essa função é chamada quando o jogador retorna ao menu
        principal ou inicia um novo jogo.

        ► Efeitos:
          - Esquece personagem selecionado
          - Limpa áreas concluídas, inventário e flags
          - Não apaga o arquivo de save; apenas o estado em memória
        """
        self.selected_character = None
        self.completed_areas.clear()
        self.inventory.clear()
        self.flags.clear()

    # -------------------------
    # Áreas (fases)
    # -------------------------
    def complete_area(self, area_name: str) -> None:
        """Marca a área como concluída (idempotente)."""
        if area_name:
            self.completed_areas.add(area_name)

    def is_area_completed(self, area_name: str) -> bool:
        """Retorna True se a área já foi concluída."""
        return area_name in self.completed_areas

    def is_area_unlocked(self, area: str) -> bool:
        """
        Regras de desbloqueio de áreas.
        ► Por padrão, todas as áreas estão liberadas, EXCETO a área final,
          que só libera após todas as áreas listadas em REQUIRED_FOR_FINAL
          constarem em completed_areas.
        """
        if area == FINAL_AREA_NAME:
            return REQUIRED_FOR_FINAL.issubset(self.completed_areas)
        return True

    # -------------------------
    # Inventário
    # -------------------------
    def add_item(self, name: str, qty: int = 1) -> None:
        """
        Adiciona 'qty' unidades do item 'name' ao inventário.
        Ignora quantidades <= 0 e nomes vazios.
        """
        if qty <= 0 or not name:
            return
        self.inventory[name] = self.inventory.get(name, 0) + qty

    def remove_item(self, name: str, qty: int = 1) -> None:
        """
        Remove 'qty' unidades do item 'name'. Se chegar a 0, remove a chave.
        Ignora se o item não existe ou se qty <= 0.
        """
        if qty <= 0 or name not in self.inventory:
            return
        new_qty = max(0, self.inventory[name] - qty)
        if new_qty == 0:
            del self.inventory[name]
        else:
            self.inventory[name] = new_qty

    # -------------------------
    # Flags (marcadores de progresso/diálogos/eventos)
    # -------------------------
    def set_flag(self, key: str, value: bool = True) -> None:
        """Define (ou atualiza) uma flag booleana."""
        if key:
            self.flags[key] = bool(value)

    def get_flag(self, key: str, default: bool = False) -> bool:
        """Obtém o valor de uma flag (ou 'default' se não existir)."""
        return self.flags.get(key, default)

    # -------------------------
    # Serialização (memória -> dicionário)
    # -------------------------
    def to_dict(self) -> dict[str, Any]:
        """
        Converte o estado atual para um dicionário pronto para salvar em JSON.
        Inclui 'version' para permitir migração de dados no futuro.
        """
        return {
            "version": STATE_VERSION,
            "selected_character": self.selected_character,
            "completed_areas": sorted(self.completed_areas),  # ordena só p/ ficar legível
            "inventory": dict(self.inventory),
            "flags": dict(self.flags),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GameState:
        """
        Constrói um GameState a partir de um dicionário salvo (tolerante a campos faltantes).
        ► Se 'version' do arquivo mudarem no futuro, implemente migrações aqui.
        """
        if not isinstance(data, dict):
            return cls()

        version = data.get("version", 0)
        # Ex.: if version == 0: migrar campos antigos para o novo formato.

        selected_character = data.get("selected_character")
        completed_areas = set(data.get("completed_areas", []))
        inventory = dict(data.get("inventory", {}))
        flags = dict(data.get("flags", {}))

        # Coerção leve de tipos (robustez contra saves antigos/inconsistentes)
        completed_areas = {str(x) for x in completed_areas}
        inventory = {str(k): int(v) for k, v in inventory.items()}
        flags = {str(k): bool(v) for k, v in flags.items()}

        return cls(
            selected_character=(
                selected_character if (selected_character is None or isinstance(selected_character, str))
                else str(selected_character)
            ),
            completed_areas=completed_areas,
            inventory=inventory,
            flags=flags,
        )

    # -------------------------
    # Save / Load (persistência em disco)
    # -------------------------
    def save(self, path: Path = SAVE_PATH) -> None:
        """
        Salva o estado em JSON usando escrita atômica (escreve em arquivo temporário
        e depois substitui o destino). Isso reduz o risco de corrupção do save
        caso o jogo feche no meio do processo.

        ► Dica de uso: chame após eventos relevantes (concluir área, pegar item, etc.).
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_fd, temp_path = tempfile.mkstemp(prefix=".state_tmp_", dir=path.parent)
        try:
            with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
            os.replace(temp_path, path)  # substituição atômica (suportada na maioria dos SOs)
        except Exception:
            # Em caso de erro, remova o temporário e propague a exceção
            try:
                os.remove(temp_path)
            except Exception:
                pass
            raise

    def load(self, path: Path = SAVE_PATH) -> None:
        """
        Carrega o estado salvo, se existir. Em caso de erro de parsing/IO, mantém
        o estado atual e apenas registra um aviso no console.
        ► Importante: copiamos os campos para a instância existente para que
          todas as referências ao STATE global continuem válidas.
        """
        if not path.exists():
            return
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            loaded = self.from_dict(data)
            # Copia campos (mantém o mesmo objeto STATE referenciado pelo projeto)
            self.selected_character = loaded.selected_character
            self.completed_areas = loaded.completed_areas
            self.inventory = loaded.inventory
            self.flags = loaded.flags
        except Exception as e:
            print(f"[WARN] Falha ao carregar estado: {e}")


# ---------------------------------------------------------------
# Instância global única do estado do jogo.
# ---------------------------------------------------------------
# Padrão de uso:
#   from script.game_state import STATE
#   STATE.complete_area("Level_1_2")
#   if STATE.is_area_unlocked("Propugnáculo Além-Mar"): ...
#
# ► Observação:
#   Evite reatribuir STATE = GameState() em outros módulos. Sempre reutilize esta
#   instância compartilhada para não perder referências nas cenas/objetos.
STATE = GameState()
