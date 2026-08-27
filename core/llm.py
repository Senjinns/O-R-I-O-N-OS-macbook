import anthropic
from core import config, journal, budget, registre, memoire, personnalite

LOG = journal.obtenir()

SYSTEME_BASE = (
    "Tu es ORION, une IA agentique vocale haut de gamme pour macOS sur Apple Silicon M2. "
    "Consignes vocales strictes : "
    "1. Tes réponses sont destinées à être lues À VOIX HAUTE. Fais des réponses courtes (1 à 2 phrases max). "
    "2. N'utilise JAMAIS de markdown complexe, de listes à puces, d'astérisques de mise en forme (*, **) ou d'emojis. "
    "3. Tu disposes d'une boîte à outils complète pour agir sur le Mac et les services connectés. Utilise-les sans hésiter. "
    "4. Sois direct, percutant, loyal et subtilement spirituel. "
    "5. Si l'utilisateur donne une info personnelle, retiens-la avec l'outil se_souvenir sans bavarder."
)

class ClaudeAgent:
    def __init__(self):
        cle = config.reglage("anthropic.cle", "")
        self.client = anthropic.Anthropic(api_key=cle) if cle else None
        self.modele_rapide = config.reglage("anthropic.modele_rapide", "claude-3-5-haiku-20241022")
        self.modele_expert = config.reglage("anthropic.modele_expert", "claude-3-5-sonnet-20241022")

    def _construire_systeme(self) -> str:
        persona_actuelle = personnalite.persona(config.reglage("assistant.personnalite", "orion_sarcastique"))
        memoire_str = memoire.texte_pour_systeme()
        return f"{persona_actuelle}\n\n{SYSTEME_BASE}{memoire_str}"

    def repondre_et_agir(self, requete_utilisateur: str, historique: list = None) -> tuple[str, list]:
        if not self.client:
            return "Clé API Anthropic non configurée dans config.yaml.", historique or []
        
        if historique is None:
            historique = []
        
        historique.append({"role": "user", "content": requete_utilisateur})
        outils = registre.obtenir_outils_anthropic()
        systeme_complet = self._construire_systeme()
        
        # Choix du modèle : Sonnet si tâche complexe ou code, sinon Haiku
        modele = self.modele_rapide
        
        try:
            # Multi-turn tool execution loop
            while True:
                response = self.client.messages.create(
                    model=modele,
                    max_tokens=config.reglage("anthropic.max_tokens", 1024),
                    temperature=config.reglage("anthropic.temperature", 0.5),
                    system=[{
                        "type": "text",
                        "text": systeme_complet,
                        "cache_control": {"type": "ephemeral"}
                    }],
                    messages=historique,
                    tools=outils
                )
                
                # Enregistrement comptabilité budget
                u = getattr(response, "usage", None)
                if u:
                    budget.enregistrer(
                        "Anthropic",
                        modele,
                        getattr(u, "input_tokens", 0) or 0,
                        getattr(u, "output_tokens", 0) or 0,
                        getattr(u, "cache_read_input_tokens", 0) or 0
                    )
                
                # Traitement de l'arrêt
                if response.stop_reason == "tool_use":
                    historique.append({"role": "assistant", "content": response.content})
                    tool_results = []
                    
                    for bloc in response.content:
                        if bloc.type == "tool_use":
                            nom_outil = bloc.name
                            arguments = bloc.input
                            LOG.info(f"Exécution outil : {nom_outil}({arguments})")
                            
                            # Exécution de l'outil
                            resultat = registre.executer_outil(nom_outil, arguments)
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": bloc.id,
                                "content": str(resultat)
                            })
                    
                    historique.append({"role": "user", "content": tool_results})
                else:
                    # Réponse finale textuelle
                    texte_final = ""
                    for bloc in response.content:
                        if hasattr(bloc, "text"):
                            texte_final += bloc.text
                    
                    historique.append({"role": "assistant", "content": texte_final})
                    return texte_final.strip(), historique
                    
        except Exception as e:
            LOG.error(f"[Claude Agent] Erreur API : {e}")
            return f"Désolé, une anomalie de communication avec Claude s'est produite : {e}", historique
