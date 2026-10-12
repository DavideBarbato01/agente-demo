import logging
from google.adk.agents import Agent

# Registro delle operazioni (tracciabilità)
logging.basicConfig(filename="audit.log", level=logging.INFO,
                    format="%(asctime)s %(message)s")

# Dati finti: nessun dato personale
SPESE = [
    {"data": "2025-01-05", "fornitore": "Amazon", "categoria": "Ufficio", "importo": 120.50},
    {"data": "2025-01-12", "fornitore": "Trenitalia", "categoria": "Viaggi", "importo": 89.00},
    {"data": "2025-01-20", "fornitore": "Ristorante", "categoria": "Pasti", "importo": 64.30},
    {"data": "2025-02-03", "fornitore": "Google Workspace", "categoria": "Software", "importo": 14.00},
    {"data": "2025-02-10", "fornitore": "Italo", "categoria": "Viaggi", "importo": 112.00},
    {"data": "2025-02-18", "fornitore": "Amazon", "categoria": "Ufficio", "importo": 45.90},
]
BUDGET = {"Ufficio": 150.0, "Viaggi": 150.0, "Pasti": 100.0, "Software": 50.0}


def totale_per_categoria(categoria: str) -> dict:
    """Calcola il totale speso in una categoria (es. "Viaggi", "Ufficio")."""
    logging.info("TOOL totale_per_categoria categoria=%s", categoria)
    righe = [s for s in SPESE if s["categoria"].lower() == categoria.lower()]
    if not righe:
        return {"status": "error", "messaggio": f"Categoria '{categoria}' non trovata."}
    totale = round(sum(s["importo"] for s in righe), 2)
    return {"status": "success", "categoria": categoria,
            "totale_eur": totale, "numero_spese": len(righe)}


def controlla_budget() -> dict:
    """Confronta la spesa di ogni categoria con il budget e segnala gli sforamenti."""
    logging.info("TOOL controlla_budget")
    report = {}
    for cat, budget in BUDGET.items():
        speso = round(sum(s["importo"] for s in SPESE if s["categoria"] == cat), 2)
        report[cat] = {"speso_eur": speso, "budget_eur": budget,
                       "fuori_budget": speso > budget}
    return {"status": "success", "report": report}


root_agent = Agent(
    name="finance_agent",
    model="gemini-3.5-flash",
    description="Assistente spese per l'ufficio amministrazione.",
    instruction=(
        "Sei un assistente per l'ufficio amministrazione. Rispondi in italiano. "
        "Per qualsiasi numero usa SEMPRE i tool: non calcolare a mente e non inventare. "
        "Se un dato non esiste, dillo chiaramente. "
        "Non chiedere né conservare dati personali."
    ),
    tools=[totale_per_categoria, controlla_budget],
)