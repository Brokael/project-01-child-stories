def format_parent_companion(parent_companion):
    symbols_text = ""

    for symbol in parent_companion.symbol_explanations:
        symbols_text += f"""
- {symbol.story_element}
  → {symbol.symbolic_meaning}
"""

    values_text = "\n".join(
        f"- {value}" for value in parent_companion.core_values
    )

    return f"""
=== POUR LES PARENTS ===

Événement lié :
{parent_companion.linked_event}

Valeurs mises en avant :
{values_text}

Lien avec l'histoire :
{parent_companion.event_explanation}

Éléments de l'histoire à comprendre :
{symbols_text}
"""