import streamlit as st
import os
import json
from datetime import datetime
from typing import Any, Dict, List





# --- File Constants ---
LINEUP_FILE = "weekly_lineup.json"
INVENTORY_FILE = "inventory.json"
INGREDIENT_FILE = "ingredient_inventory.json"
THRESHOLD_FILE = "ingredient_thresholds.json"
EXCLUDE_FILE = "excluded_ingredients.json"

# Helpers for inventory 
# Canonical unit keys to avoid typos in saved JSON
UNIT_OPTIONS = [
    "cans",
    "50lbs bags",   # keep exact label you requested
    "grams",
    "liters",
    "gallons",
]

def load_json(path: str, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return default

def save_json(path: str, data: Any):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def get_all_ingredients_from_recipes(recipes: Dict[str, Any]) -> list[str]:
    names = set()
    for r in recipes.values():
        for ing in r.get("ingredients", {}).keys():
            names.add(ing)
    return sorted(names)

def normalize_thresholds_schema(thresholds: Dict[str, Any]) -> Dict[str, Any]:
    """Upgrade old schema (value-only) to {'min': number, 'unit': 'grams'}."""
    upgraded = {}
    for ing, val in thresholds.items():
        if isinstance(val, dict):
            # ensure both keys
            min_val = val.get("min", 0)
            unit    = val.get("unit", "grams")
            if unit not in UNIT_OPTIONS:
                unit = "grams"
            upgraded[ing] = {"min": min_val, "unit": unit}
        else:
            upgraded[ing] = {"min": float(val) if val is not None else 0.0, "unit": "grams"}
    return upgraded

##


# --- Helpers ---


def get_all_ingredients(recipes: dict) -> list[str]:
    seen = set()
    for r in recipes.values():
        for ing in r.get("ingredients", {}).keys():
            seen.add(ing.strip())
    return sorted(seen)

UNIT_FACTORS = {"g": 1.0, "kg": 1000.0, "lb": 453.59237, "oz": 28.349523125}

def load_json(path: str, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return default
    return default

def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def normalize_inventory_schema(raw: dict) -> tuple[dict, bool]:
    inv, changed = {}, False
    for k, v in (raw or {}).items():
        if isinstance(v, dict):
            amt = float(v.get("amount", 0))
            unit = (v.get("unit") or "g").lower()
        else:
            amt = float(v or 0)
            unit = "g"
            changed = True
        inv[k] = {"amount": amt, "unit": unit}
    return inv, changed


def to_grams(amount: float, unit: str) -> float:
    return float(amount) * UNIT_FACTORS.get((unit or "g").lower(), 1.0)

def ensure_inventory_files(recipes: dict):
    """If files don't exist, initialize from recipes."""
    all_ings = get_all_ingredients(recipes)

    # Create inventory file if missing (all zeros)
    if not os.path.exists(INGREDIENT_FILE):
        inventory = {ing: 0 for ing in all_ings}
        save_json(INGREDIENT_FILE, inventory)

    # Create thresholds file if missing (all zeros)
    if not os.path.exists(THRESHOLD_FILE):
        thresholds = {ing: 0 for ing in all_ings}
        save_json(THRESHOLD_FILE, thresholds)
# --- Recipe Database ---
recipes = {
    "Brownies": {
        "ingredients": {
            "molding solitaire": 483,
            "butter": 380,
            "eggs": 372,
            "sugar": 600,
            "flour": 161,
            "salt": 4
        },
        "instruction": [
            "1) Bake at 350°F for 30 minutes."
        ]
    
},
    "Chai": {
        "ingredients": {
            "cardamom mix": 2000,
            "dry ginger": 4,
            "cinnamon": 4,
            "nutmeg": 2,
            "all spice": 2,
            "black pepper": 2,
            "clove": 1
        }
    },
    "Creme Brulee": {
        "ingredients": {
            "milk": 20300,
            "cream": 6828,
            "sugar": 4400,
            "guar": 72,
            "dry milk": 2800,
            "yolks": 2400,
            "caramel sauce": 3200
        },
        "instruction": [
            "1) Weigh and mix all base ingredients except caramel sauce.",
            "2) Weigh the caramel ingredients and cook on high until the sauce reaches 220°F.",
            "3) Add some of the base into the caramel sauce and keep cooking on low heat until homogeneous.",
            "4) Incorporate the caramel/base mix into the remainder of the base and mix well.",
            "5) Before batch freezing, burn some caramel crust pieces with a torch as mix-in."
        ],
        "subrecipes": {
            "caramel sauce": {
                "ingredients": {
                    "sugar": 3200,
                    "water": 500,
                    "honey": 50
                },
                "instruction": [
                    "1) Combine sugar, water, and honey.",
                    "2) Cook on medium-high heat until sugar dissolves.",
                    "3) Raise heat and cook until mixture reaches 220°F."
                ]
            }
        }
    },
    "Creme Fraiche": {
        "ingredients": {
            "milk": 6902,
            "sugar": 5220,
            "guar": 58,
            "dry milk": 2030,
            "yolks": 290,
            "sour cream": 14500
        },
        "instruction": []
    },
    "Crumble": {
        "ingredients": {
            "flour": 223,
            "sugar": 388,
            "cinnamon": 8,
            "butter": 272
        },
        "instruction": [
            "1) Melt the butter.",
            "2) Briefly mix ingredients on the mixer, and remove them before they form a homogeneous mix.",
            "3) Bake for 15 minutes at 350°F."
        ],
        "subrecipes": {}
    },
    "Cookie Dough": {
        "ingredients": {
            "butter": 396,
            "sugar": 344,
            "brown sugar": 386,
            "pasteurized egg whites": 92,
            "pasteurized egg yolks": 90,
            "vanilla extract": 16,
            "flour": 646,
            "salt": 6
        },
        "instruction": [],
        "subrecipes": {}
    },
    "Dulce de Leche": {
        "ingredients": {
            "milk": 22775,
            "cream": 8000,
            "sugar": 2550,
            "guar": 75,
            "dry milk": 1000,
            "yolks": 2000,
            "dulce de leche heladero": 13600
        },
        "instruction": []
    },
    "Earl Grey": {
        "ingredients": {
            "milk": 11016,
            "cream": 4000,
            "sugar": 3300,
            "guar": 44,
            "dry milk": 800,
            "yolks": 500,
            "earl grey": 400
        },
        "instruction": []
    },
    "Fresh Mint": {
        "ingredients": {
            "milk": 31140,
            "cream": 6500,
            "sugar": 8500,
            "guar": 110,
            "dry milk": 3000,
            "yolks": 750,
            "mint": 1250,
            "blanched mint": 500
        },
        "instruction": [
            "Day 1: Prepare Mint-Infused Milk",
            "1) Heat 2 gallons of milk (to be subtracted from the base) with some fresh mint to 250°F for 2 hours.",
            "2) After 2 hours, cover and refrigerate overnight to infuse the flavor.",
            "Day 2: Prepare Blanched Mint Purée",
            "3) 3 hours ahead, place 2 gallons of water in the freezer for ice water bath.",
            "4) Bring 2 gallons of fresh water to a boil.",
            "5) Carefully submerge the remaining fresh mint into the boiling water for 30 seconds.",
            "6) Immediately drain and shock the mint in the ice water bath to preserve its green color.",
            "7) Drain the mint and blend until very fine and smooth.",
            "Final Steps:",
            "8) Strain the infused milk from Day 1, pressing the mint to extract flavor.",
            "9) Mix the strained mint milk and blended mint purée with the remaining base ingredients until homogeneous."
        ],
        "subrecipes": {}
    },
   "Ginger": {
    "ingredients": {
        "milk": 936,
        "cream": 380,
        "sugar": 190,
        "guar": 4,
        "dry milk": 110,
        "yolks": 80,
        "caramelized ginger": 300
    },
    "instruction": [],
    "subrecipes": {}
}
,
"Ginger Caramelized": {
    "ingredients": {
        "honey": 20,
        "water": 228,
        "sugar": 173,
        "ginger": 125
    },
    "instruction": [
        "Caramelize the Ginger",
        "1) Cut the Ginger into little pieces.",
        "2) Cook the Water, Sugar and Honey on high until the sugar dissolves.",
        "3) Add the cut Ginger and bring to a boil.",
        "4) Simmer for 5 minutes."
    ],
    "subrecipes": { }
}
,
    "Graham Cracker Crust": {
        "ingredients": {
            "graham cracker crumble": 338,
            "butter": 310,
            "sugar": 352
        },
        "instruction": [
            "1) Process graham crackers on the Robocoupe.",
            "2) Mix ingredients on the mixer.",
            "3) Press ingredients down on a flat pan.",
            "4) Bake for 15 minutes at 325°F."
        ],
        "subrecipes": {}
    },
    "Green Tea": {
        "ingredients": {
            "milk": 1223,
            "cream": 300,
            "sugar": 330,
            "guar": 4,
            "dry milk": 100,
            "yolks": 20,
            "green tea": 23
        },
        "instruction": []
    },
    "Honeycomb": {
        "ingredients": {
            "sugar": 3000,
            "honey": 50,
            "water": 1450,
            "baking soda": 250
        },
        "instruction": [
            "1) Cook on medium heat, stirring constantly until sugar dissolves.",
            "2) Once sugar is completely dissolved, stop stirring.",
            "3) Continue cooking on high until 300°F.",
            "4) Add the baking soda and stir.",
            "5) Pour the rising honeycomb on previously greased trays and let cool."
        ],
        "subrecipes": {}
    },
    "Lemon Bar": {
        "ingredients": {
            "crust": 566,
            "filling": 1362
        },
        "instruction": [
            "1) Bake the crust at 350°F for 15 minutes.",
            "2) Pour filling onto baked crust and bake at 350°F for 20 minutes."
        ],
        "subrecipes": {
            "crust": {
                "ingredients": {
                    "butter": 225,
                    "flour": 240,
                    "sugar": 100,
                    "salt": 1
                },
                "instruction": [
                    "1) Process all crust ingredients in a food processor until smooth.",
                    "2) Press into a greased pan and bake for 15 minutes at 325°F."
                ]
            },
            "filling": {
                "ingredients": {
                    "eggs (each)": 12,
                    "lemon juice": 360,
                    "sugar": 900,
                    "flour": 90
                },
                "instruction": [
                    "1) Beat all filling ingredients in a bowl until fully dissolved.",
                    "2) Pour on top of the baked crust and bake for 20 minutes at 325°F."
                ]
            }
        }
    },
    "Lemon Sorbet": {
        "ingredients": {
            "water": 5442,
            "lemon": 3500,
            "pectin": 87,
            "guar gum": 12,
            "sugar": 2625
        },
        "instruction": [],
        "subrecipes": {}
    },
    "Peach Preserves": {
        "ingredients": {
            "peaches": 1350,
            "sugar": 1250,
            "lemon": 82
        },
        "instruction": [
            "1) Combine cored peaches and sugar and let stand for 3 hours.",
            "2) Bring to boil, stirring occasionally.",
            "3) Cook until it reaches 220°F and syrup is thick."
        ],
        "subrecipes": {}
    },
    "Pear Sorbet": {
        "ingredients": {
            "water": 5500,
            "pectin": 100,
            "sugar": 3500,
            "pear": 10600,
            "lemon": 300
        },
        "instruction": [
            "1) Quarter the pears and remove their seeds.",
            "2) Fill a pot with the quartered pears and weigh.",
            "3) Add water to completely cover the pears.",
            "4) Weigh the water + pears in the pot.",
            "5) Cook until pears are soft and translucent.",
            "6) Re-weigh cooked pear+water mix.",
            "7) Add enough water to make up the difference between step 4 and 6.",
            "8) Process all the ingredients in a blender until smooth."
        ],
        "subrecipes": {}
    },
    "Pistachio": {
        "ingredients": {
            "milk": 32640,
            "cream": 750,
            "sugar": 8250,
            "guar": 110,
            "dry milk": 2750,
            "yolks": 1000,
            "pistachio paste": 4500
        },
        "instruction": [
            "1) If pistachios are raw, roast them at 300°F for 8 minutes.",
            "2) Mix the roasted pistachios and the pistachio oil in the Robocoupe for 10 minutes, then blend for 15 minutes until very smooth."
        ],
        "subrecipes": {
            "pistachio paste": {
                "ingredients": {
                    "roasted pistachios": 2967,
                    "pistachio oil": 1532
                },
                "instruction": [
                    "1) Roast the pistachios if raw.",
                    "2) Blend pistachios with pistachio oil until smooth and creamy."
                ]
            }
        }
    },
    "Pumpkin": {
        "ingredients": {
            "milk": 7611,
            "cream": 5290,
            "sugar": 2300,
            "guar": 46,
            "dry milk": 690,
            "yolks": 1150,
            "pumpkin": 2990,
            "brown sugar": 2300,
            "cinnamon": 67,
            "nutmeg": 25,
            "ginger": 122,
            "port": 409
        }
        },
    "Strawberry Preserves": {
        "ingredients": {
            "strawberries": 1250,
            "sugar": 1150,
            "pectin": 11,
            "lemon": 89
        },
        "instruction": [
            "1) Combine strawberries and sugar and let stand for 3 hours.",
            "2) Bring to boil, stirring occasionally.",
            "3) Cook until it reaches 220°F and syrup is thick."
        ],
        "subrecipes": {}
    },
    "Toffee": {
        "ingredients": {
            "butter": 863,
            "sugar": 779,
            "honey": 17,
            "salt": 4
        },
        "instruction": [
            "1) Cook on medium heat, stirring constantly until sugar dissolves.",
            "2) Once sugar is completely dissolved, stop stirring.",
            "3) Continue cooking on high until 300°F."
        ],
        "subrecipes": {}
    }, 
    "ricotta": {
        "ingredients": {
            "milk": 15822,
            "cream": 2420,
            "sugar": 5143,
            "guar": 61,
            "dry milk": 1664,
            "yolks": 605,
            "ricotta": 4538
        }},
        
    "vanilla": {
        "ingredients": {
            "milk": 28637,
            "cream": 10806,
            "sugar": 8915,
            "guar": 135,
            "dry milk": 2972,
            "yolks": 2161,
            "vanilla extract": 243,
            "vanilla seeds": 162
        },
        "instruction": [
            "1) Combine all ingredients.",
            "2) Pasteurize the mix.",
            "3) Chill, batch freeze, and pack."]
    } ,
    "whisky": {
        "ingredients": {
            "milk": 1031,
            "cream": 440,
            "sugar": 315,
            "guar": 4,
            "dry milk": 110,
            "yolks": 60,
            "whisky": 40,
                    },
        "instruction": [
            "1) Combine all ingredients.",
            "2) Pasteurize the mix.",
            "3) Chill, batch freeze, and pack."
        ]
    }}

###
###
# --- Recipe schema normalizer (ensures keys exist) ---
def normalize_recipes_schema(recipes: dict) -> dict:
    for name, r in list(recipes.items()):
        if not isinstance(r, dict):
            continue
        r.setdefault("ingredients", {})
        # always ensure instruction exists and is a list
        instr = r.get("instruction", [])
        if instr is None:
            instr = []
        elif isinstance(instr, str):
            instr = [instr]
        r["instruction"] = instr
        # always ensure subrecipes exists and is a dict
        r.setdefault("subrecipes", {})
        # also normalize subrecipes
        for sname, s in r["subrecipes"].items():
            if not isinstance(s, dict):
                continue
            s.setdefault("ingredients", {})
            sinstr = s.get("instruction", [])
            if sinstr is None:
                sinstr = []
            elif isinstance(sinstr, str):
                sinstr = [sinstr]
            s["instruction"] = sinstr
    return recipes

# call this immediately after defining/importing recipes
recipes = normalize_recipes_schema(recipes)
###
def _unwrap_recipe(obj):
    """Return the dict if scaler returned (dict, factor)."""
    if isinstance(obj, tuple) and isinstance(obj[0], dict):
        return obj[0]
    return obj if isinstance(obj, dict) else {}

def make_scaled_recipe(base_recipe: dict, new_ingredients: dict) -> dict:
    """Ensure scaled recipe carries instructions and subrecipes."""
    return {
        "ingredients": new_ingredients or {},
        "instruction": base_recipe.get("instruction", []) or [],
        "subrecipes": base_recipe.get("subrecipes", {}) or {},
    }

def _render_instructions_block(title: str, steps: list[str]):
    if not steps:
        return
    with st.expander(title, expanded=True):
        for line in steps:
            st.markdown(f"- {line}")

def _render_subrecipes(subrecipes: dict):
    if not subrecipes:
        return
    st.markdown("### 🧩 Sub-recipes")
    for sname, srec in subrecipes.items():
        with st.expander(f"Subrecipe: {sname}", expanded=False):
            ings = srec.get("ingredients", {})
            if ings:
                st.markdown("**Ingredients**")
                for k, v in ings.items():
                    st.write(f"- {k}: {v:g}")
            _render_instructions_block("Instructions", srec.get("instruction", []))

###
def render_ingredients_block(ingredients: dict):
    """Render ingredients, showing gallons + grams for milk."""
    if not ingredients:
        return

    st.markdown("### 📋 Ingredients")

    G_PER_GALLON_MILK = 3785  # adjust if you want

    for k, v in ingredients.items():
        try:
            grams = float(v)
        except Exception:
            # Non-numeric values (e.g., "to taste")
            st.write(f"- {k}: {v}")
            continue

        line = f"- {k}: {grams:g} g"

        if k.lower() == "milk":
            whole_gal = int(grams // G_PER_GALLON_MILK)
            rem_g = grams - whole_gal * G_PER_GALLON_MILK
            line += f" ({whole_gal} gal + {rem_g:.0f} g)"

        st.write(line)

###
def show_scaled_result(selected_name: str, scaled_result, recipes_dict: dict):
    """Print ingredients + instructions + subrecipes (scaled or base)."""
    base = recipes_dict.get(selected_name, {})
    rec = _unwrap_recipe(scaled_result)

    # If scaler returned only ingredients, re-attach instructions/subrecipes
    if rec and "ingredients" in rec and not rec.get("instruction"):
        rec = make_scaled_recipe(base, rec["ingredients"])

    # Last fallback: if rec is empty, just use base
    if not rec:
        rec = base

    # ----- INGREDIENTS (with milk in gallons) -----
    render_ingredients_block(rec.get("ingredients", {}))

    # ----- MAIN INSTRUCTIONS -----
    _render_instructions_block("🛠️ Instructions", rec.get("instruction", []))

    # ----- SUBRECIPES -----
    _render_subrecipes(rec.get("subrecipes", {}))



recipe_names = sorted(recipes.keys())

if not recipe_names:
    st.error("No recipes found.")
    st.stop()

# Heal / initialize state
current_sel = st.session_state.get("selected_recipe")
if current_sel not in recipe_names:
    current_sel = recipe_names[0]
    st.session_state["selected_recipe"] = current_sel

# Main dropdown
selected_name = st.selectbox(
    "Choose a recipe",
    recipe_names,
    index=recipe_names.index(current_sel),
    key="selected_recipe",
)

# Resolve recipe
rec = recipes.get(selected_name)
if not isinstance(rec, dict):
    st.error("Invalid recipe.")
    st.stop()

###


# Heal / initialize session selection
current_sel = st.session_state.get("selected_recipe")
if current_sel not in recipe_names:
    current_sel = recipe_names[0]
    st.session_state["selected_recipe"] = current_sel



# Resolve recipe dict
rec = recipes.get(selected_name)
if not isinstance(rec, dict):
    st.info("Pick a recipe to view details.")
    st.stop()

###



# Resolve recipe dict
rec = recipes.get(selected_name)
if not isinstance(rec, dict):
    st.info("Pick a recipe to view details.")
    st.stop()





current_sel = st.session_state.get("selected_recipe")
if current_sel not in recipe_names:
    st.session_state["selected_recipe"] = recipe_names[0]
    current_sel = recipe_names[0]


# --- Resolve recipe object + guard ---
rec = recipes.get(selected_name)
if not isinstance(rec, dict):
    st.info("Pick a recipe to view details.")
    st.stop()


# --- Helpers ---
def as_steps(obj):
    v = (obj or {}).get("instruction")
    if v is None:
        return []
    return v if isinstance(v, list) else [str(v)]



# Keep state stable across reruns
selected_name = st.session_state.get("selected_recipe")

# If nothing selected yet, default to the first recipe
if not selected_name:
    selected_name = recipe_names[0]
    st.session_state["selected_recipe"] = selected_name



# Heal session value if it points to a recipe that no longer exists
current_sel = st.session_state.get("selected_recipe")
if current_sel not in recipe_names:
    st.session_state["selected_recipe"] = recipe_names[0]
    current_sel = recipe_names[0]



# --- Resolve recipe object + guard ---
rec = recipes.get(selected_name)
if not isinstance(rec, dict):
    st.info("Pick a recipe to view details.")
    st.stop()
###
# ========================= SCALING UI (single source of truth) =========================
import re

def _slugify(s: str) -> str:
    return re.sub(r'[^a-z0-9]+', '_', (s or 'x').lower()).strip('_')

# Where this UI renders: "main", "sidebar", "tab_scale", etc.
SCOPE = "main"
NS_SCALE = f"scale__{SCOPE}__{_slugify(selected_name)}"

def k(s: str) -> str:
    return f"{NS_SCALE}__{s}"

# Clear stale per-recipe scaling keys when switching recipe
if st.session_state.get("prev_recipe_for_scale") != selected_name:
    for _k in list(st.session_state.keys()):
        if isinstance(_k, str) and _k.startswith("scale__"):
            st.session_state.pop(_k)
    st.session_state["prev_recipe_for_scale"] = selected_name

st.subheader("Scale")

# Method selector
scale_mode = st.radio(
    "Method",
    [
        "Target batch weight (g)",
        "Container: 5 L",
        "Container: 1.5 gal",
        "Containers: combo (5 L + 1.5 gal)",
        "Scale by ingredient weight",
        "Multiplier x",
    ],
    horizontal=True,
    key=k("mode"),
)

# Volume density (only when needed)
density_g_per_ml = None
if scale_mode in {"Container: 5 L", "Container: 1.5 gal", "Containers: combo (5 L + 1.5 gal)"}:
    density_g_per_ml = st.number_input(
        "Mix density (g/mL)",
        min_value=0.5, max_value=1.5, value=1.03, step=0.01,
        key=k("density"),
    )

# Constants
GAL_TO_L     = 3.785411784
VOL_5L_L     = 5.0
VOL_1_5GAL_L = 1.5 * GAL_TO_L  # ≈ 5.678 L

# Inputs
base_ings = rec.get("ingredients", {})
original_weight = float(sum(base_ings.values()) or 0.0)

# --- Scaling logic ---
info_lines: list[str] = []
scale_factor = 1.0
target_weight = None

if scale_mode == "Target batch weight (g)":
    target_weight = st.number_input(
        "Target weight (g)",
        min_value=1.0,
        value=float(original_weight or 1000.0),
        step=100.0,
        key=k("target_weight"),
    )
    scale_factor = (target_weight / original_weight) if original_weight else 1.0
    info_lines.append(f"Target weight: {target_weight:,.0f} g")

elif scale_mode == "Container: 5 L":
    n_5l = st.number_input("How many 5 L pans?", min_value=1, value=1, step=1, key=k("n5l"))
    total_l = n_5l * VOL_5L_L
    density_g_per_ml = density_g_per_ml or 1.03
    target_weight = total_l * 1000.0 * density_g_per_ml
    scale_factor = (target_weight / original_weight) if original_weight else 1.0
    info_lines += [f"Total volume: {total_l:,.2f} L", f"Target weight: {target_weight:,.0f} g"]

elif scale_mode == "Container: 1.5 gal":
    n_15 = st.number_input("How many 1.5 gal tubs?", min_value=1, value=1, step=1, key=k("n15"))
    total_l = n_15 * VOL_1_5GAL_L
    density_g_per_ml = density_g_per_ml or 1.03
    target_weight = total_l * 1000.0 * density_g_per_ml
    scale_factor = (target_weight / original_weight) if original_weight else 1.0
    info_lines += [f"Total volume: {total_l:,.2f} L", f"Target weight: {target_weight:,.0f} g"]

elif scale_mode == "Containers: combo (5 L + 1.5 gal)":
    col_a, col_b = st.columns(2)
    with col_a:
        n_5l = st.number_input("5 L pans", min_value=0, value=1, step=1, key=k("n5l_combo"))
    with col_b:
        n_15 = st.number_input("1.5 gal tubs", min_value=0, value=0, step=1, key=k("n15_combo"))
    total_l = n_5l * VOL_5L_L + n_15 * VOL_1_5GAL_L
    if total_l <= 0:
        st.warning("Set at least one container.")
        total_l = 0.0
    density_g_per_ml = density_g_per_ml or 1.03
    target_weight = total_l * 1000.0 * density_g_per_ml
    scale_factor = (target_weight / original_weight) if original_weight else 1.0
    info_lines += [
        f"5 L pans: {n_5l}  |  1.5 gal tubs: {n_15}",
        f"Total volume: {total_l:,.2f} L",
        f"Target weight: {target_weight:,.0f} g",
    ]

elif scale_mode == "Scale by ingredient weight":
    if not base_ings:
        st.warning("This recipe has no ingredients.")
        scale_factor = 1.0
    else:
        ing_names = list(base_ings.keys())
        anchor_ing = st.selectbox("Anchor ingredient", ing_names, key=k("anchor_ing"))
        available_g = st.number_input(
            f"Available {anchor_ing} (g)",
            min_value=0.0,
            value=float(base_ings.get(anchor_ing, 0.0)),
            step=10.0,
            key=k("available_anchor"),
        )
        base_req = float(base_ings.get(anchor_ing, 0.0))
        if base_req <= 0:
            st.warning(f"Anchor ingredient '{anchor_ing}' has 0 g in the base recipe.")
            scale_factor = 1.0
        else:
            scale_factor = available_g / base_req
            info_lines.append(f"Scale factor from {anchor_ing}: ×{scale_factor:.3f}")

else:  # "Multiplier x"
    scale_factor = st.number_input(
        "Multiplier",
        min_value=0.01,
        value=1.0,
        step=0.1,
        key=k("multiplier"),
    )
    info_lines.append(f"Scale factor: ×{scale_factor:.3f}")

# --- Apply scaling ---
scaled = {ing: round(float(qty) * scale_factor, 2) for ing, qty in base_ings.items()}
total_scaled = round(sum(scaled.values()), 2)
# --- Display summary ---
st.metric("Total batch weight (g)", f"{total_scaled:,.2f}")
if density_g_per_ml and total_scaled > 0:
    est_l = total_scaled / (density_g_per_ml * 1000.0)
    st.caption(f"Estimated volume: {est_l:,.2f} L @ {density_g_per_ml:.2f} g/mL")

for line in info_lines:
    st.caption(line)

# 🔹 Show ingredients + instructions + subrecipes in one unified block
# show_scaled_result(
#     selected_name,
#     {"ingredients": scaled},  # scaled result only; helper will reattach instructions
#     recipes,
# )
###
# 🔹 Show ingredients + instructions + subrecipes in one unified block
show_scaled_result(
    selected_name,
    {"ingredients": scaled},  # scaled result only; helper will reattach instructions
    recipes,
)


###
# ---------- Step-by-step execution ----------
import re
def _slugify(s: str) -> str:
    return re.sub(r'[^a-z0-9]+', '_', (s or 'x').lower()).strip('_')

st.subheader("Execute batch (step-by-step)")
key_prefix = f"bs_{_slugify(selected_name)}"

# Use scaled if available; otherwise fall back to base ingredients
scaled_for_steps = (locals().get("scaled") or rec.get("ingredients", {})) or {}

step_key  = f"{key_prefix}_step"
order_key = f"{key_prefix}_order"

# Init session state
if step_key not in st.session_state:
    st.session_state[step_key] = None
if order_key not in st.session_state or not isinstance(st.session_state[order_key], list):
    st.session_state[order_key] = list(scaled_for_steps.keys())

# Controls
start_clicked = st.button("▶️ Start batch", key=f"{key_prefix}_start")
if start_clicked:
    st.session_state[step_key]  = 0
    st.session_state[order_key] = list(scaled_for_steps.keys())

step  = st.session_state[step_key]
order = st.session_state[order_key]

if step is not None:
    if step < len(order):
        ing = order[step]
        grams = float(scaled_for_steps.get(ing, 0))
        st.info(f"**{ing} {grams:.0f} grams**")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.button("⬅️ Back", key=f"{key_prefix}_back",
                      disabled=(step == 0),
                      on_click=lambda: st.session_state.update({step_key: max(0, step - 1)}))
        with c2:
            st.button("⏹ Reset", key=f"{key_prefix}_reset",
                      on_click=lambda: st.session_state.update({step_key: None}))
        with c3:
            st.button("Next ➡️", key=f"{key_prefix}_next",
                      on_click=lambda: st.session_state.update({step_key: step + 1}))
    else:
        st.success("✅ Batch complete")
        st.button("Start over", key=f"{key_prefix}_restart",
                  on_click=lambda: st.session_state.update({step_key: 0}))

####
# ingredient inventory code 
def ingredient_inventory_section():
    st.header("Ingredient Inventory")
    ns = "ii4"  # namespace to avoid duplicate widget keys

    # --- Collect all ingredients from recipes + subrecipes ---
    all_ingredients = set()
    for recipe in recipes.values():
        all_ingredients.update(recipe.get("ingredients", {}).keys())
        for sub in recipe.get("subrecipes", {}).values():
            all_ingredients.update(sub.get("ingredients", {}).keys())
    all_ingredients = sorted({ing.strip() for ing in all_ingredients})

    # --- Exclude list (load, edit, save) ---
    excluded_ingredients = load_json(EXCLUDE_FILE, [])
    st.subheader("Exclude Ingredients from Inventory")
    exclude_list = st.multiselect(
        "Select ingredients to exclude",
        all_ingredients,
        default=[e for e in excluded_ingredients if e in all_ingredients],
        key=f"{ns}_exclude",
    )
    if st.button("Save Exclusion List", key=f"{ns}_save_exclude"):
        save_json(EXCLUDE_FILE, exclude_list)
        st.success("Excluded ingredients list saved.")

    # --- Load & normalize inventory file (auto-migrate numbers -> {amount, unit}) ---
    raw_inv = load_json(INGREDIENT_FILE, {})
    inv, changed = normalize_inventory_schema(raw_inv)
    # Ensure every known ingredient exists in the file
    for ing in all_ingredients:
        inv.setdefault(ing, {"amount": 0.0, "unit": "g"})
    if changed:
        save_json(INGREDIENT_FILE, inv)  # one-time migration

    # --- Filter UI ---
    q = st.text_input("Filter ingredients", "", key=f"{ns}_filter").strip().lower()
    items = {k: v for k, v in inv.items() if (k in all_ingredients) and (k not in exclude_list) and (q in k.lower())}

    # --- Editable grid (3 columns) ---
    cols = st.columns(3)
    unit_options = ["g", "kg", "lb", "oz"]
    updated = {}
    for i, (name, item) in enumerate(sorted(items.items())):
        with cols[i % 3]:
            amt = st.number_input(
                name,
                min_value=0.0,
                value=float(item.get("amount", 0.0)),
                step=1.0,
                key=f"{ns}_amt_{name}",
            )
            try:
                unit_idx = unit_options.index((item.get("unit") or "g").lower())
            except ValueError:
                unit_idx = 0
            unit = st.selectbox(
                "Unit",
                unit_options,
                index=unit_idx,
                key=f"{ns}_unit_{name}",
            )
            updated[name] = {"amount": amt, "unit": unit}

    # --- Save ---
    if st.button("💾 Save ingredient inventory", key=f"{ns}_save"):
        inv.update(updated)
        save_json(INGREDIENT_FILE, inv)
        st.success("Ingredient inventory saved.")

    # --- Summary table (shows entered unit + grams) ---
    summary = {
        k: f"{v['amount']:.2f} {v['unit']}  ({to_grams(v['amount'], v['unit']):,.0f} g)"
        for k, v in items.items()
    }
    st.dataframe(summary, use_container_width=True)



    if st.button("Save Ingredient Inventory"):
        with open(INGREDIENT_FILE, "w") as f:
            json.dump(ingredient_inventory, f, indent=2)
        with open(THRESHOLD_FILE, "w") as f:
            json.dump(min_thresholds, f, indent=2)
        st.success("Ingredient inventory and thresholds saved.")

    if os.path.exists(INGREDIENT_FILE):
        st.markdown("#### Current Ingredient Inventory")
        with open(INGREDIENT_FILE) as f:
            data = json.load(f)
        filtered_data = {k: v for k, v in data.items() if k not in exclude_list}
        st.dataframe({k: f"{v['amount']} {v['unit']}" for k, v in filtered_data.items()}, use_container_width=True)

    if os.path.exists(THRESHOLD_FILE):
        st.markdown("#### Ingredients Needing Reorder")
        with open(INGREDIENT_FILE) as f:
            inventory = json.load(f)
        with open(THRESHOLD_FILE) as f:
            thresholds = json.load(f)
        needs_order = {
            ing: f"{inventory[ing]['amount']} < {thresholds[ing]} {inventory[ing]['unit']}"
            for ing in thresholds if ing not in exclude_list and ing in inventory and inventory[ing]["amount"] < thresholds[ing]
        }
        if needs_order:
            st.error("⚠️ Order Needed:")
            st.dataframe(needs_order)
        else:
            st.success("✅ All ingredients above minimum thresholds.")

import streamlit as st

def set_min_inventory_section(recipes: Dict[str, Any]):
    st.header("Set Minimum Inventory Levels")

    # Build the ingredient list from recipes (your request)
    all_ingredients = get_all_ingredients_from_recipes(recipes)
    if not all_ingredients:
        st.info("No ingredients found in recipes.")
        return

    # Load & normalize existing thresholds
    thresholds_raw = load_json(THRESHOLD_FILE, {})
    thresholds = normalize_thresholds_schema(thresholds_raw)

    st.caption("Pick a minimum level and unit for each ingredient. Units are informational — no conversion is applied.")

    # Editable grid
    cols = st.columns([3, 2, 2])
    cols[0].markdown("**Ingredient**")
    cols[1].markdown("**Min Level**")
    cols[2].markdown("**Unit**")

    # Collect edits (avoid duplicate keys using ingredient names)
    edited = {}
    for ing in all_ingredients:
        current_min  = thresholds.get(ing, {}).get("min", 0.0)
        current_unit = thresholds.get(ing, {}).get("unit", "grams")
        with st.container():
            c1, c2, c3 = st.columns([3, 2, 2])
            c1.write(ing)
            new_min = c2.number_input(
                "min_"+ing, value=float(current_min), min_value=0.0, step=1.0, format="%.2f", label_visibility="collapsed"
            )
            new_unit = c3.selectbox(
                "unit_"+ing, options=UNIT_OPTIONS,
                index=UNIT_OPTIONS.index(current_unit) if current_unit in UNIT_OPTIONS else UNIT_OPTIONS.index("grams"),
                label_visibility="collapsed",
            )
            edited[ing] = {"min": new_min, "unit": new_unit}

    if st.button("💾 Save Minimums & Units", type="primary"):
        save_json(THRESHOLD_FILE, edited)
        st.success("Minimum inventory levels and units saved.")





####


# --- Sidebar navigation ---
page = st.sidebar.radio("Go to", ["Batching System", "Flavor Inventory", "Ingredient Inventory", "Set Min Inventory"], key="sidebar_nav")

# if page == "Batching System":
#     batching_system_section()

# elif page == "Flavor Inventory":
#     flavor_inventory_section()

# elif page == "Ingredient Inventory":
#     ingredient_inventory_section()

# elif page == "Set Min Inventory":
#     set_min_inventory_section(recipes)


# --- Utility Functions ---
def get_total_weight(recipe):
    return sum(recipe["ingredients"].values())

def scale_recipe_to_target_weight(recipe, target_weight):
    original_weight = get_total_weight(recipe)
    scale_factor = target_weight / original_weight
    adjusted_main = {k: round(v * scale_factor) for k, v in recipe["ingredients"].items()}
    return {"ingredients": adjusted_main, "instruction": recipe.get("instruction", [])}, scale_factor

def adjust_recipe_with_constraints(recipe, available_ingredients):
    base_ingredients = recipe.get("ingredients", {})
    ratios = [amt / base_ingredients[ing] for ing, amt in available_ingredients.items()
              if ing in base_ingredients and base_ingredients[ing] != 0]
    scale_factor = min(ratios) if ratios else 1
    adjusted = {k: round(v * scale_factor) for k, v in base_ingredients.items()}

    # 🔧 Ensure we keep instruction/subrecipes in the result:
    scaled_recipe = make_scaled_recipe(recipe, adjusted)
    return scaled_recipe, scale_factor



# --- Ingredient Inventory Section ---
def ingredient_inventory_section():
    st.subheader("📦 Ingredient Inventory Control")

    # Collect all ingredients from recipes and subrecipes
    all_ingredients = set()
    for recipe in recipes.values():
        all_ingredients.update(recipe.get("ingredients", {}).keys())
        for sub in recipe.get("subrecipes", {}).values():
            all_ingredients.update(sub.get("ingredients", {}).keys())
    all_ingredients = sorted(all_ingredients)

    # Load exclusion list
    excluded_ingredients = []
    if os.path.exists(EXCLUDE_FILE):
        with open(EXCLUDE_FILE) as f:
            excluded_ingredients = json.load(f)

    st.markdown("#### Exclude Ingredients from Inventory")
    exclude_list = st.multiselect(
        "Select ingredients to exclude",
        all_ingredients,
        default=excluded_ingredients,
        key="exclude_list"
    )
    if st.button("Save Exclusion List", key="save_exclude_btn"):
        with open(EXCLUDE_FILE, "w") as f:
            json.dump(exclude_list, f, indent=2)
        st.success("Excluded ingredients list saved.")

    # Load thresholds (mins + units) and existing inventory
    thresholds = normalize_thresholds_schema(load_json(THRESHOLD_FILE, {}))
    existing_inventory = load_json(INGREDIENT_FILE, {})  # {ing: {"amount": x, "unit": "..."}}

    st.markdown("#### Enter Inventory (units come from Set Min Inventory)")
    ingredient_inventory = {}

    # Inputs for inventory only; labels show the unit chosen in Set Min page
    for ing in all_ingredients:
        if ing in exclude_list:
            continue
        unit = thresholds.get(ing, {}).get("unit", "grams")
        prev_amount = 0.0
        if isinstance(existing_inventory.get(ing), dict):
            prev_amount = float(existing_inventory[ing].get("amount", 0.0))

        qty = st.number_input(
            f"{ing} ({unit})",
            min_value=0.0,
            step=1.0,
            format="%f",
            key=f"inv_{ing}",
            value=prev_amount
        )
        ingredient_inventory[ing] = {"amount": qty, "unit": unit}

    if st.button("Save Ingredient Inventory", key="save_inventory_btn"):
        with open(INGREDIENT_FILE, "w") as f:
            json.dump(ingredient_inventory, f, indent=2)
        st.success("Ingredient inventory saved.")

    # Show current inventory
    if os.path.exists(INGREDIENT_FILE):
        st.markdown("#### Current Ingredient Inventory")
        with open(INGREDIENT_FILE) as f:
            data = json.load(f)
        filtered_data = {k: f"{v.get('amount', 0)} {v.get('unit', '')}"
                         for k, v in data.items() if k not in exclude_list}
        st.dataframe(filtered_data, use_container_width=True)

    # Reorder check using mins + units from thresholds
    if os.path.exists(INGREDIENT_FILE):
        st.markdown("#### Ingredients Needing Reorder")
        with open(INGREDIENT_FILE) as f:
            inventory = json.load(f)

        needs_order = {}
        for ing, th in thresholds.items():
            if ing in exclude_list or ing not in inventory:
                continue
            amount = float(inventory[ing].get("amount", 0.0))
            min_level = float(th.get("min", 0.0))
            unit = th.get("unit", inventory[ing].get("unit", ""))
            if amount < min_level:
                needs_order[ing] = f"{amount} {unit} < {min_level} {unit}"

        if needs_order:
            st.error("⚠️ Order Needed:")
            st.dataframe(needs_order, use_container_width=True)
        else:
            st.success("✅ All ingredients above minimum thresholds.")


####
# def flavor_inventory_section():
#     st.subheader("🍦 Flavor & Topping Inventory Control")

    # --- Load data ---
    if os.path.exists(LINEUP_FILE):
        with open(LINEUP_FILE) as f:
            lineup = json.load(f)
    else:
        lineup = []

    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE) as f:
            inventory = json.load(f)
    else:
        inventory = {}

    # --- 1. Weekly Lineup ---
    st.markdown("#### 1. Set Weekly Flavor Lineup")
    lineup_input = st.text_area("Flavors (comma-separated)", value=", ".join(lineup), key="lineup_input")
    if st.button("Update Lineup", key="update_lineup_btn"):
        lineup = [flavor.strip() for flavor in lineup_input.split(",") if flavor.strip()]
        inventory = {flavor: data for flavor, data in inventory.items() if flavor in lineup}
        with open(LINEUP_FILE, "w") as f:
            json.dump(lineup, f)
        with open(INVENTORY_FILE, "w") as f:
            json.dump(inventory, f)
        st.success("✅ Lineup updated and inventory cleaned.")

    # --- 2. Update Inventory ---
    st.markdown("#### 2. Update Inventory")
    if not lineup:
        st.warning("⚠️ Please set the weekly lineup first.")
        return

    selected_flavor = st.selectbox("Select a flavor to update", lineup, key="flavor_select")
    quarts = st.number_input("Enter quarts available", min_value=0, step=1, key="quarts_input")

    if st.button("Submit Inventory", key="submit_inventory_btn"):
        inventory[selected_flavor] = {
            "quarts": quarts,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        with open(INVENTORY_FILE, "w") as f:
            json.dump(inventory, f)
        st.success(f"✅ Inventory updated for {selected_flavor}")

    # --- 3. Show Inventory Table ---
    st.markdown("#### 3. Current Inventory")
    if inventory:
        sorted_inventory = sorted(inventory.items(), key=lambda x: x[1]["quarts"], reverse=True)
        table = {
            "Flavor": [flavor for flavor, _ in sorted_inventory],
            "Quarts": [info["quarts"] for _, info in sorted_inventory],
            "Last Updated": [info["last_updated"] for _, info in sorted_inventory],
        }
        st.dataframe(table, use_container_width=True)
    else:
        st.info("No inventory records yet.")







# --- Utility Functions ---
def get_total_weight(recipe):
    return sum(recipe["ingredients"].values())

def scale_recipe_to_target_weight(recipe, target_weight):
    original_weight = get_total_weight(recipe)
    scale_factor = target_weight / original_weight
    adjusted_main = {k: round(v * scale_factor) for k, v in recipe["ingredients"].items()}
    return {"ingredients": adjusted_main, "instruction": recipe.get("instruction", [])}, scale_factor

def adjust_recipe_with_constraints(recipe, available_ingredients):
    base_ingredients = recipe.get("ingredients", {})
    ratios = [amt / base_ingredients[ing] for ing, amt in available_ingredients.items() if ing in base_ingredients and base_ingredients[ing] != 0]
    scale_factor = min(ratios) if ratios else 1
    adjusted = {k: round(v * scale_factor) for k, v in base_ingredients.items()}
    return adjusted, scale_factor

# --- Recipe Adjuster Section ---
# ... (no changes here for brevity) ...

# --- Ingredient Inventory Section ---

# min inventory section

def set_min_inventory_section(recipes: dict):
    st.header("Set Minimum Inventory Levels")

    # If files are missing, don't error—initialize from recipes
    ensure_inventory_files(recipes)

    # Load what we have; if the JSONs exist but are empty/corrupt, fall back
    all_ings = get_all_ingredients(recipes)
    current_thresholds = load_json(THRESHOLD_FILE, {ing: 0 for ing in all_ings})

    # Make sure we include any newly added ingredients that weren’t in the file
    for ing in all_ings:
        current_thresholds.setdefault(ing, 0)

    # Render inputs
    st.caption("Enter the minimum units you want to keep on hand for each ingredient.")
    cols = st.columns(3)
    updated = {}

    for i, ing in enumerate(all_ings):
        with cols[i % 3]:
            updated[ing] = st.number_input(
                f"{ing}",
                min_value=0.0,
                value=float(current_thresholds.get(ing, 0)),
                step=1.0,
                key=f"min_inv_{ing}"
            )

    if st.button("💾 Save minimum thresholds"):
        save_json(THRESHOLD_FILE, updated)
        st.success("Minimum thresholds saved.")

    # Optional helper: show where the files live
    with st.expander("⚙️ Files"):
        st.write(f"Inventory file: `{INGREDIENT_FILE}`")
        st.write(f"Thresholds file: `{THRESHOLD_FILE}`")






# --- Utility Functions ---
def get_total_weight(recipe):
    return sum(recipe["ingredients"].values())

def scale_recipe_to_target_weight(recipe, target_weight):
    original_weight = get_total_weight(recipe)
    scale_factor = target_weight / original_weight
    adjusted_main = {k: round(v * scale_factor) for k, v in recipe["ingredients"].items()}
    return {"ingredients": adjusted_main, "instruction": recipe.get("instruction", [])}, scale_factor

def adjust_recipe_with_constraints(recipe, available_ingredients):
    base_ingredients = recipe.get("ingredients", {})
    ratios = [amt / base_ingredients[ing] for ing, amt in available_ingredients.items() if ing in base_ingredients and base_ingredients[ing] != 0]
    scale_factor = min(ratios) if ratios else 1
    adjusted = {k: round(v * scale_factor) for k, v in base_ingredients.items()}
    return adjusted, scale_factor

# --- Ingredient Inventory Section ---
def ingredient_inventory_section():
    st.subheader("📦 Ingredient Inventory Control")

    bulk_units = {
        "milk": "gallons",
        "cream": "half gallons",
        "sugar": "50 lb bags",
        "dry milk": "50 lb bags",
        "flour": "50 lb bags",
        "brown sugar": "50 lb bags",
        "butter": "cases"
    }

    all_ingredients = set()
    for recipe in recipes.values():
        all_ingredients.update(recipe.get("ingredients", {}).keys())
        for sub in recipe.get("subrecipes", {}).values():
            all_ingredients.update(sub.get("ingredients", {}).keys())

    excluded_ingredients = []
    if os.path.exists(EXCLUDE_FILE):
        with open(EXCLUDE_FILE) as f:
            excluded_ingredients = json.load(f)

    st.markdown("#### Exclude Ingredients from Inventory")
    exclude_list = st.multiselect("Select ingredients to exclude", sorted(all_ingredients), default=excluded_ingredients)
    if st.button("Save Exclusion List"):
        with open(EXCLUDE_FILE, "w") as f:
            json.dump(exclude_list, f, indent=2)
        st.success("Excluded ingredients list saved.")

    ingredient_inventory = {}
    min_thresholds = {}

    st.markdown("#### Enter Inventory and Minimum Thresholds")
    for ing in sorted(all_ingredients):
        if ing in exclude_list:
            continue
        unit = bulk_units.get(ing, "grams")
        col1, col2 = st.columns(2)
        with col1:
            qty = st.number_input(f"{ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"inv_{ing}")
        with col2:
            threshold = st.number_input(f"Min {ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"min_{ing}")
        ingredient_inventory[ing] = {"amount": qty, "unit": unit}
        min_thresholds[ing] = threshold

    if st.button("Save Ingredient Inventory"):
        with open(INGREDIENT_FILE, "w") as f:
            json.dump(ingredient_inventory, f, indent=2)
        with open(THRESHOLD_FILE, "w") as f:
            json.dump(min_thresholds, f, indent=2)
        st.success("Ingredient inventory and thresholds saved.")

    if os.path.exists(INGREDIENT_FILE):
        st.markdown("#### Current Ingredient Inventory")
        with open(INGREDIENT_FILE) as f:
            data = json.load(f)
        filtered_data = {k: v for k, v in data.items() if k not in exclude_list}
        st.dataframe({k: f"{v['amount']} {v['unit']}" for k, v in filtered_data.items()}, use_container_width=True)

    if os.path.exists(THRESHOLD_FILE):
        st.markdown("#### Ingredients Needing Reorder")
        with open(INGREDIENT_FILE) as f:
            inventory = json.load(f)
        with open(THRESHOLD_FILE) as f:
            thresholds = json.load(f)
        needs_order = {
            ing: f"{inventory[ing]['amount']} < {thresholds[ing]} {inventory[ing]['unit']}"
            for ing in thresholds if ing not in exclude_list and ing in inventory and inventory[ing]["amount"] < thresholds[ing]
        }
        if needs_order:
            st.error("⚠️ Order Needed:")
            st.dataframe(needs_order)
        else:
            st.success("✅ All ingredients above minimum thresholds.")

