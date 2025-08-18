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
recipes = {"Brownies": {
        "ingredients": {
            "molding solitaire": 483,
            "butter": 380,
            "eggs": 372,
            "sugar": 600,
            "flour": 161,
            "salt": 4
        },
        "instructions": [
            "1) Bake at 350°F for 30 minutes."
            
        ],
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
        "instructions": [
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
                "instructions": [
                    "1) Combine sugar, water, and honey.",
                    "2) Cook on medium-high heat until sugar dissolves.",
                    "3) Raise heat and cook until mixture reaches 220°F."
                ]
            }
        }
    },
    "Crumble": {
        "ingredients": {
            "flour": 223,
            "sugar": 388,
            "cinnamon": 8,
            "butter": 272
        },
        "instructions": [
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
        "instructions": [],
        "subrecipes": {}
    },
    "Dulce de Leche": {
        "ingredients": {
            "milk": 24775,
            "cream": 7500,
            "sugar": 2550,
            "guar": 75,
            "dry milk": 1000,
            "yolks": 500,
            "dulce de leche heladero": 90
        },
        "instructions": []
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
        "instructions": [
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
    "Graham Cracker Crust": {
        "ingredients": {
            "graham cracker crumble": 338,
            "butter": 310,
            "sugar": 352
        },
        "instructions": [
            "1) Process graham crackers on the Robocoupe.",
            "2) Mix ingredients on the mixer.",
            "3) Press ingredients down on a flat pan.",
            "4) Bake for 15 minutes at 325°F."
        ],
        "subrecipes": {}
    },
    "Honeycomb": {
        "ingredients": {
            "sugar": 3000,
            "honey": 50,
            "water": 1450,
            "baking soda": 250
        },
        "instructions": [
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
        "instructions": [
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
                "instructions": [
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
                "instructions": [
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
        "instructions": [],
        "subrecipes": {}
    },
    "Peach Preserves": {
        "ingredients": {
            "peaches": 1350,
            "sugar": 1250,
            "lemon": 82
        },
        "instructions": [
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
        "instructions": [
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
        "instructions": [
            "1) If pistachios are raw, roast them at 300°F for 8 minutes.",
            "2) Mix the roasted pistachios and the pistachio oil in the Robocoupe for 10 minutes, then blend for 15 minutes until very smooth."
        ],
        "subrecipes": {
            "pistachio paste": {
                "ingredients": {
                    "roasted pistachios": 2967,
                    "pistachio oil": 1532
                },
                "instructions": [
                    "1) Roast the pistachios if raw.",
                    "2) Blend pistachios with pistachio oil until smooth and creamy."
                ]
            }
        }
    },
    "Strawberry Preserves": {
        "ingredients": {
            "strawberries": 1250,
            "sugar": 1150,
            "pectin": 11,
            "lemon": 89
        },
        "instructions": [
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
        "instructions": [
            "1) Cook on medium heat, stirring constantly until sugar dissolves.",
            "2) Once sugar is completely dissolved, stop stirring.",
            "3) Continue cooking on high until 300°F."
        ],
        "subrecipes": {}
    },
    "vanilla": {
        "ingredients": {
            "milk": 28510,
            "cream": 10000,
            "sugar": 8250,
            "guar": 110,
            "dry milk": 2500,
            "yolks": 500,
            "vanilla extract": 100,
            "vanilla seeds": 90
        },
        "instructions": [
            "1) Combine all ingredients.",
            "2) Pasteurize the mix.",
            "3) Chill, batch freeze, and pack."
        ]
    }
}
# --- Batching System Section ---
# def ():
#     st.subheader("⚙️ Manual Batching System")
#     recipe_name = st.selectbox("Select Recipe", list(recipes.keys()), key="batch_recipe_select")
#     recipe = recipes[recipe_name]

#     st.markdown("### Scale by Target Weight")
#     target_weight = st.number_input("Target total weight (grams)", min_value=100.0, step=100.0, key="batch_target_weight")
#     if target_weight:
#         scaled_recipe, factor = scale_recipe_to_target_weight(recipe, target_weight)
#         st.markdown(f"#### Scaled Ingredients ({round(factor * 100)}%)")
#         for ing, amt in scaled_recipe["ingredients"].items():
#             st.write(f"- {amt} grams {ing}")

#     st.markdown("### Step-by-Step Mode")
#     if "step_i" not in st.session_state:
#         st.session_state.step_i = 0

#     if st.button("Start Over", key="reset_step_btn"):
#         st.session_state.step_i = 0

#     steps = list(scaled_recipe["ingredients"].items())
#     if st.session_state.step_i < len(steps):
#         ing, amt = steps[st.session_state.step_i]
#         st.markdown(f"**Weigh:** {amt} grams of {ing}")
#         if st.button("Next Ingredient", key=f"next_{st.session_state.step_i}"):
#             st.session_state.step_i += 1
#     else:
#         st.success("🎉 All ingredients completed!")
# ###
# def flavor_inventory_section():
#     st.subheader("🍦 Flavor & Topping Inventory Control")

def batching_system_section():
    import math
    st.header("Batching System")
    ns = "bs3"  # namespace for widget keys

    # Files/lineup (fallbacks if constants missing)
    lineup_file = LINEUP_FILE if "LINEUP_FILE" in globals() else "weekly_lineup.json"
    lineup = load_json(lineup_file, [])
    all_recipe_names = sorted(recipes.keys())

    # Filter to weekly lineup
    show_only_lineup = st.checkbox(
        "Show only weekly lineup",
        value=bool(lineup),
        key=f"{ns}_show_only_lineup",
    )
    recipe_options = [r for r in all_recipe_names if (not show_only_lineup or r in lineup)] or all_recipe_names

    # Pick recipe
    selected_recipe = st.selectbox("Recipe", recipe_options, key=f"{ns}_recipe_select")
    base_ings = recipes[selected_recipe].get("ingredients", {})
    original_weight = float(sum(base_ings.values())) if base_ings else 0.0

    # ---------------------------
    # Scaling modes
    # ---------------------------
    st.subheader("Scale")
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
        key=f"{ns}_scale_mode",
    )

    # Volume → grams needs density
    # Default ~1.03 g/mL for liquid ice-cream mix; adjust if you track per-recipe densities.
    if scale_mode in {"Container: 5 L", "Container: 1.5 gal", "Containers: combo (5 L + 1.5 gal)"}:
        density_g_per_ml = st.number_input(
            "Mix density (g/mL)",
            min_value=0.5,
            max_value=1.5,
            value=1.03,
            step=0.01,
            key=f"{ns}_density",
        )
    else:
        density_g_per_ml = None

    # Constants
    GAL_TO_L = 3.785411784
    VOL_5L_L = 5.0
    VOL_1_5GAL_L = 1.5 * GAL_TO_L  # ≈ 5.678 L

    scale_factor = 1.0
    target_weight = None
    info_lines = []

    if scale_mode == "Target batch weight (g)":
        target_weight = st.number_input(
            "Target weight (g)",
            min_value=1.0,
            value=float(original_weight or 1000.0),
            step=100.0,
            key=f"{ns}_target_weight",
        )
        scale_factor = (target_weight / original_weight) if original_weight else 1.0
        info_lines.append(f"Target weight: {target_weight:,.0f} g")

    elif scale_mode == "Container: 5 L":
        n_5l = st.number_input("How many 5 L pans?", min_value=1, value=1, step=1, key=f"{ns}_n5l")
        total_l = n_5l * VOL_5L_L
        target_weight = total_l * 1000.0 * density_g_per_ml
        scale_factor = (target_weight / original_weight) if original_weight else 1.0
        info_lines += [f"Total volume: {total_l:,.2f} L", f"Target weight: {target_weight:,.0f} g"]

    elif scale_mode == "Container: 1.5 gal":
        n_15 = st.number_input("How many 1.5 gal tubs?", min_value=1, value=1, step=1, key=f"{ns}_n15")
        total_l = n_15 * VOL_1_5GAL_L
        target_weight = total_l * 1000.0 * density_g_per_ml
        scale_factor = (target_weight / original_weight) if original_weight else 1.0
        info_lines += [f"Total volume: {total_l:,.2f} L", f"Target weight: {target_weight:,.0f} g"]

    elif scale_mode == "Containers: combo (5 L + 1.5 gal)":
        col_a, col_b = st.columns(2)
        with col_a:
            n_5l = st.number_input("5 L pans", min_value=0, value=1, step=1, key=f"{ns}_n5l_combo")
        with col_b:
            n_15 = st.number_input("1.5 gal tubs", min_value=0, value=0, step=1, key=f"{ns}_n15_combo")

        total_l = n_5l * VOL_5L_L + n_15 * VOL_1_5GAL_L
        if total_l <= 0:
            st.warning("Set at least one container.")
            total_l = 0.0
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
        else:
            ing_names = list(base_ings.keys())
            anchor_ing = st.selectbox("Anchor ingredient", ing_names, key=f"{ns}_anchor_ing")
            available_g = st.number_input(
                f"Available {anchor_ing} (g)",
                min_value=0.0,
                value=float(base_ings.get(anchor_ing, 0.0)),
                step=10.0,
                key=f"{ns}_available_anchor",
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
            key=f"{ns}_multiplier",
        )
        info_lines.append(f"Scale factor: ×{scale_factor:.3f}")

    # Apply scaling
    scaled = {ing: round(qty * scale_factor, 2) for ing, qty in base_ings.items()}
    total_scaled = round(sum(scaled.values()), 2)

    # Display summary
    st.metric("Total batch weight (g)", f"{total_scaled:,.2f}")
    if density_g_per_ml and total_scaled > 0:
        est_l = total_scaled / (density_g_per_ml * 1000.0)
        st.caption(f"Estimated volume: {est_l:,.2f} L @ {density_g_per_ml:.2f} g/mL")

    for line in info_lines:
        st.caption(line)

    with st.expander("📋 Scaled ingredients (all)"):
        for ing, grams in scaled.items():
            st.write(f"- {ing}: {grams:.0f} g")

    # ---------------------------
    # Step-by-step execution
    # ---------------------------
    st.subheader("Execute batch (step-by-step)")
    key_prefix = f"{ns}_{selected_recipe}"

    if f"{key_prefix}_step" not in st.session_state:
        st.session_state[f"{key_prefix}_step"] = None
        st.session_state[f"{key_prefix}_order"] = list(scaled.keys())

    if st.button("▶️ Start batch", key=f"{key_prefix}_start"):
        st.session_state[f"{key_prefix}_step"] = 0
        st.session_state[f"{key_prefix}_order"] = list(scaled.keys())

    step = st.session_state[f"{key_prefix}_step"]
    order = st.session_state[f"{key_prefix}_order"]

    if step is not None:
        if step < len(order):
            ing = order[step]
            grams = scaled.get(ing, 0)
            st.info(f"**{ing} {grams:.0f} grams**")

            c1, c2, c3 = st.columns(3)
            if c1.button("⬅️ Back", key=f"{key_prefix}_back", disabled=(step == 0)):
                st.session_state[f"{key_prefix}_step"] = max(0, step - 1)
                st.stop()
            if c2.button("⏹ Reset", key=f"{key_prefix}_reset"):
                st.session_state[f"{key_prefix}_step"] = None
                st.stop()
            if c3.button("Next ➡️", key=f"{key_prefix}_next"):
                st.session_state[f"{key_prefix}_step"] = step + 1
                st.stop()
        else:
            st.success("✅ Batch complete")
            if st.button("Start over", key=f"{key_prefix}_restart"):
                st.session_state[f"{key_prefix}_step"] = 0
                st.stop()


###
# def batching_system_section():
#     st.header("Batching System")
#     ns = "bs2"  # change this string if you ever hit a duplicate again

#     lineup = load_json(LINEUP_FILE, [])
#     all_recipe_names = sorted(recipes.keys())
#     show_only_lineup = st.checkbox(
#         "Show only weekly lineup",
#         value=bool(lineup),
#         key=f"{ns}_show_only_lineup",
#     )
#     if show_only_lineup and lineup:
#         recipe_options = [r for r in all_recipe_names if r in lineup] or all_recipe_names
#     else:
#         recipe_options = all_recipe_names

#     selected_recipe = st.selectbox("Recipe", recipe_options, key=f"{ns}_recipe_select")
#     base_ings = recipes[selected_recipe].get("ingredients", {})
#     original_weight = sum(base_ings.values()) if base_ings else 0

#     st.subheader("Scale")
#     scale_mode = st.radio(
#         "Method",
#         ["Target batch weight (g)", "Multiplier x"],
#         horizontal=True,
#         key=f"{ns}_scale_mode",
#     )

#     if scale_mode == "Target batch weight (g)":
#         target_weight = st.number_input(
#             "Target weight (g)",
#             min_value=1.0,
#             value=float(original_weight or 1000),
#             step=100.0,
#             key=f"{ns}_target_weight",
#         )
#         scale_factor = (target_weight / original_weight) if original_weight else 1.0
#     else:
#         scale_factor = st.number_input(
#             "Multiplier",
#             min_value=0.01,
#             value=1.0,
#             step=0.1,
#             key=f"{ns}_multiplier",
#         )

#     scaled = {ing: round(qty * scale_factor, 2) for ing, qty in base_ings.items()}
#     total_scaled = round(sum(scaled.values()), 2)

#     st.metric("Total batch weight (g)", f"{total_scaled:,.2f}")
#     with st.expander("📋 Scaled ingredients (all)"):
#         for ing, grams in scaled.items():
#             st.write(f"- {ing}: {grams:.0f} g")

#     st.subheader("Execute batch (step-by-step)")
#     key_prefix = f"{ns}_{selected_recipe}"

#     if f"{key_prefix}_step" not in st.session_state:
#         st.session_state[f"{key_prefix}_step"] = None
#         st.session_state[f"{key_prefix}_order"] = list(scaled.keys())

#     start_clicked = st.button("▶️ Start batch", key=f"{key_prefix}_start")
#     if start_clicked:
#         st.session_state[f"{key_prefix}_step"] = 0
#         st.session_state[f"{key_prefix}_order"] = list(scaled.keys())

#     step = st.session_state[f"{key_prefix}_step"]
#     order = st.session_state[f"{key_prefix}_order"]

#     if step is not None:
#         if step < len(order):
#             ing = order[step]
#             grams = scaled.get(ing, 0)
#             st.info(f"**{ing} {grams:.0f} grams**")

#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 if st.button("⬅️ Back", key=f"{key_prefix}_back", disabled=(step == 0)):
#                     st.session_state[f"{key_prefix}_step"] = max(0, step - 1)
#                     st.stop()
#             with col2:
#                 if st.button("⏹ Reset", key=f"{key_prefix}_reset"):
#                     st.session_state[f"{key_prefix}_step"] = None
#                     st.stop()
#             with col3:
#                 if st.button("Next ➡️", key=f"{key_prefix}_next"):
#                     st.session_state[f"{key_prefix}_step"] = step + 1
#                     st.stop()
#         else:
#             st.success("✅ Batch complete")
#             if st.button("Start over", key=f"{key_prefix}_restart"):
#                 st.session_state[f"{key_prefix}_step"] = 0
#                 st.stop()

###
# def batching_system_section():
#     st.header("Batching System")

#     # Pick recipe (optionally filter to weekly lineup)
#     lineup = load_json(LINEUP_FILE, [])
#     all_recipe_names = sorted(recipes.keys())
#     show_only_lineup = st.checkbox(
#         "Show only weekly lineup",
#         value=bool(lineup),
#         key="bs_show_only_lineup"
#     )
#     if show_only_lineup and lineup:
#         recipe_options = [r for r in all_recipe_names if r in lineup]
#         if not recipe_options:
#             st.warning("No recipes in lineup. Showing all recipes.")
#             recipe_options = all_recipe_names
#     else:
#         recipe_options = all_recipe_names

#     selected_recipe = st.selectbox("Recipe", recipe_options, key="bs_recipe_select")
#     base_ings = recipes[selected_recipe].get("ingredients", {})
#     original_weight = sum(base_ings.values()) if base_ings else 0

#     # Scaling method
#     st.subheader("Scale")
#     scale_mode = st.radio(
#         "Method",
#         ["Target batch weight (g)", "Multiplier x"],
#         horizontal=True,
#         key="bs_scale_mode"
#     )

#     if scale_mode == "Target batch weight (g)":
#         target_weight = st.number_input(
#             "Target weight (g)",
#             min_value=1.0,
#             value=float(original_weight or 1000),
#             step=100.0,
#             key="bs_target_weight"
#         )
#         scale_factor = (target_weight / original_weight) if original_weight else 1.0
#     else:
#         scale_factor = st.number_input(
#             "Multiplier",
#             min_value=0.01,
#             value=1.0,
#             step=0.1,
#             key="bs_multiplier"
#         )

#     scaled = {ing: round(qty * scale_factor, 2) for ing, qty in base_ings.items()}
#     total_scaled = round(sum(scaled.values()), 2)

#     st.metric("Total batch weight (g)", f"{total_scaled:,.2f}")
#     with st.expander("📋 Scaled ingredients (all)"):
#         for ing, grams in scaled.items():
#             st.write(f"- {ing}: {grams:.0f} g")

    # ---------- Step-by-step execution ----------
    st.subheader("Execute batch (step-by-step)")
    key_prefix = f"bs_{selected_recipe}"

    # Initialize step state
    if f"{key_prefix}_step" not in st.session_state:
        st.session_state[f"{key_prefix}_step"] = None
        st.session_state[f"{key_prefix}_order"] = list(scaled.keys())

    # Start / Continue flow
    start_clicked = st.button("▶️ Start batch", key=f"{key_prefix}_start")
    if start_clicked:
        st.session_state[f"{key_prefix}_step"] = 0
        st.session_state[f"{key_prefix}_order"] = list(scaled.keys())

    step = st.session_state[f"{key_prefix}_step"]
    order = st.session_state[f"{key_prefix}_order"]

    if step is not None:
        if step < len(order):
            ing = order[step]
            grams = scaled.get(ing, 0)
            # exact phrasing: "ingredient amount grams"
            st.info(f"**{ing} {grams:.0f} grams**")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("⬅️ Back", key=f"{key_prefix}_back", disabled=(step == 0)):
                    st.session_state[f"{key_prefix}_step"] = max(0, step - 1)
                    st.stop()
            with col2:
                if st.button("⏹ Reset", key=f"{key_prefix}_reset"):
                    st.session_state[f"{key_prefix}_step"] = None
                    st.stop()
            with col3:
                if st.button("Next ➡️", key=f"{key_prefix}_next"):
                    st.session_state[f"{key_prefix}_step"] = step + 1
                    st.stop()
        else:
            st.success("✅ Batch complete")
            if st.button("Start over", key=f"{key_prefix}_restart"):
                st.session_state[f"{key_prefix}_step"] = 0
                st.stop()



def flavor_inventory_section():
    st.header("Flavor Inventory")

    # Pick files safely even if constants are missing elsewhere
    flavor_inventory_file = INVENTORY_FILE if "INVENTORY_FILE" in globals() else "flavor_inventory.json"
    lineup_file = LINEUP_FILE if "LINEUP_FILE" in globals() else "weekly_lineup.json"

    lineup = load_json(lineup_file, [])               # expects a list of flavor names
    all_flavors = sorted(recipes.keys())

    show_only_lineup = st.checkbox(
        "Show only weekly lineup",
        value=bool(lineup),
        key="fi_show_only_lineup"
    )
    flavors = [f for f in all_flavors if (not show_only_lineup or f in lineup)]
    if not flavors:
        st.warning("No lineup found. Showing all recipes.")
        flavors = all_flavors

    # Load current flavor inventory; ensure all flavors are present
    current = load_json(flavor_inventory_file, {name: 0 for name in flavors})
    for name in flavors:
        current.setdefault(name, 0)

    # Filter UI
    filter_text = st.text_input("Filter flavors", "", key="fi_filter").strip().lower()
    display_flavors = [f for f in flavors if filter_text in f.lower()]

    # Editable grid (3 columns)
    cols = st.columns(3)
    updated = {}
    for i, name in enumerate(display_flavors):
        with cols[i % 3]:
            updated[name] = st.number_input(
                name,
                min_value=0.0,
                value=float(current.get(name, 0)),
                step=1.0,
                key=f"fi_qty_{name.replace(' ', '_')}"
            )

    # Add/Remove flavors (optional)
    with st.expander("➕➖ Add or remove flavors"):
        new_name = st.text_input("Add a flavor", "", key="fi_add_name").strip()
        if st.button("Add flavor", key="fi_add_btn") and new_name:
            if new_name not in current:
                current[new_name] = 0
                save_json(flavor_inventory_file, current)
                st.info("Flavor added. Press Save or reload to see it in the grid.")

        to_remove = st.selectbox("Remove a flavor", [""] + sorted(current.keys()), key="fi_remove_sel")
        if st.button("Remove selected", key="fi_remove_btn") and to_remove:
            current.pop(to_remove, None)
            save_json(flavor_inventory_file, current)
            st.info("Flavor removed. Press Save or reload to update the grid.")

    # Save
    if st.button("💾 Save flavor inventory", key="fi_save_btn"):
        current.update(updated)
        save_json(flavor_inventory_file, current)
        st.success("Flavor inventory saved.")

    with st.expander("⚙️ Files"):
        st.write(f"Flavor inventory file: `{flavor_inventory_file}`")
        st.write(f"Weekly lineup file: `{lineup_file}`")
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


####
# def ingredient_inventory_section():
#     st.subheader("📦 Ingredient Inventory Control")

#     bulk_units = {
#         "milk": "gallons",
#         "cream": "half gallons",
#         "sugar": "50 lb bags",
#         "dry milk": "50 lb bags",
#         "flour": "50 lb bags",
#         "brown sugar": "50 lb bags",
#         "butter": "cases"
#     }

#     all_ingredients = set()
#     for recipe in recipes.values():
#         all_ingredients.update(recipe.get("ingredients", {}).keys())
#         for sub in recipe.get("subrecipes", {}).values():
#             all_ingredients.update(sub.get("ingredients", {}).keys())

#     excluded_ingredients = []
#     if os.path.exists(EXCLUDE_FILE):
#         with open(EXCLUDE_FILE) as f:
#             excluded_ingredients = json.load(f)

#     st.markdown("#### Exclude Ingredients from Inventory")
#     exclude_list = st.multiselect("Select ingredients to exclude", sorted(all_ingredients), default=excluded_ingredients)
#     if st.button("Save Exclusion List"):
#         with open(EXCLUDE_FILE, "w") as f:
#             json.dump(exclude_list, f, indent=2)
#         st.success("Excluded ingredients list saved.")

#     ingredient_inventory = {}
#     min_thresholds = {}

#     st.markdown("#### Enter Inventory and Minimum Thresholds")
#     for ing in sorted(all_ingredients):
#         if ing in exclude_list:
#             continue
#         unit = bulk_units.get(ing, "grams")
#         col1, col2 = st.columns(2)
#         with col1:
#             qty = st.number_input(f"{ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"inv_{ing}")
#         with col2:
#             threshold = st.number_input(f"Min {ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"min_{ing}")
#         ingredient_inventory[ing] = {"amount": qty, "unit": unit}
#         min_thresholds[ing] = threshold

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
# def set_min_inventory_section(recipes: dict):
#     st.header("Set Minimum Inventory Levels")
#     ensure_inventory_files(recipes)
#     all_ings = get_all_ingredients(recipes)
#     current = load_json(THRESHOLD_FILE, {ing: 0 for ing in all_ings})
#     for ing in all_ings:
#         current.setdefault(ing, 0)

#     cols = st.columns(3)
#     updated = {}
#     for i, ing in enumerate(all_ings):
#         with cols[i % 3]:
#             updated[ing] = st.number_input(
#                 ing, min_value=0.0, value=float(current.get(ing, 0)), step=1.0, key=f"min_inv_{ing}"
#             )

#     if st.button("💾 Save minimum thresholds"):
#         save_json(THRESHOLD_FILE, updated)
#         st.success("Minimum thresholds saved.")

# --- Sidebar navigation ---
page = st.sidebar.radio("Go to", ["Batching System", "Flavor Inventory", "Ingredient Inventory", "Set Min Inventory"], key="sidebar_nav")

if page == "Batching System":
    batching_system_section()

elif page == "Flavor Inventory":
    flavor_inventory_section()

elif page == "Ingredient Inventory":
    ingredient_inventory_section()

elif page == "Set Min Inventory":
    set_min_inventory_section(recipes)


# --- Utility Functions ---
def get_total_weight(recipe):
    return sum(recipe["ingredients"].values())

def scale_recipe_to_target_weight(recipe, target_weight):
    original_weight = get_total_weight(recipe)
    scale_factor = target_weight / original_weight
    adjusted_main = {k: round(v * scale_factor) for k, v in recipe["ingredients"].items()}
    return {"ingredients": adjusted_main, "instructions": recipe.get("instructions", [])}, scale_factor

def adjust_recipe_with_constraints(recipe, available_ingredients):
    base_ingredients = recipe.get("ingredients", {})
    ratios = [amt / base_ingredients[ing] for ing, amt in available_ingredients.items() if ing in base_ingredients and base_ingredients[ing] != 0]
    scale_factor = min(ratios) if ratios else 1
    adjusted = {k: round(v * scale_factor) for k, v in base_ingredients.items()}
    return adjusted, scale_factor

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

# def ingredient_inventory_section():
#     st.subheader("📦 Ingredient Inventory Control")

#     bulk_units = {
#         "milk": "gallons",
#         "cream": "half gallons",
#         "sugar": "50 lb bags",
#         "dry milk": "50 lb bags",
#         "flour": "50 lb bags",
#         "brown sugar": "50 lb bags",
#         "butter": "cases"
#     }

#     all_ingredients = set()
#     for recipe in recipes.values():
#         all_ingredients.update(recipe.get("ingredients", {}).keys())
#         for sub in recipe.get("subrecipes", {}).values():
#             all_ingredients.update(sub.get("ingredients", {}).keys())
#     all_ingredients = sorted(set(all_ingredients))

#     excluded_ingredients = []
#     if os.path.exists(EXCLUDE_FILE):
#         with open(EXCLUDE_FILE) as f:
#             excluded_ingredients = json.load(f)

#     st.markdown("#### Exclude Ingredients from Inventory")
#     exclude_list = st.multiselect("Select ingredients to exclude", all_ingredients, default=excluded_ingredients, key="exclude_list")
#     if st.button("Save Exclusion List", key="save_exclude_btn"):
#         with open(EXCLUDE_FILE, "w") as f:
#             json.dump(exclude_list, f, indent=2)
#         st.success("Excluded ingredients list saved.")

#     ingredient_inventory = {}
#     min_thresholds = {}

#     st.markdown("#### Enter Inventory and Minimum Thresholds")
#     for ing in all_ingredients:
#         if ing in exclude_list:
#             continue
#         unit = bulk_units.get(ing, "grams")
#         col1, col2 = st.columns(2)
#         with col1:
#             qty = st.number_input(f"{ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"inv_{ing}")
#         with col2:
#             threshold = st.number_input(f"Min {ing} ({unit})", min_value=0.0, step=1.0, format="%f", key=f"min_{ing}")
#         ingredient_inventory[ing] = {"amount": qty, "unit": unit}
#         min_thresholds[ing] = threshold

#     if st.button("Save Ingredient Inventory", key="save_inventory_btn"):
#         with open(INGREDIENT_FILE, "w") as f:
#             json.dump(ingredient_inventory, f, indent=2)
#         with open(THRESHOLD_FILE, "w") as f:
#             json.dump(min_thresholds, f, indent=2)
#         st.success("Ingredient inventory and thresholds saved.")

#     if os.path.exists(INGREDIENT_FILE):
#         st.markdown("#### Current Ingredient Inventory")
#         with open(INGREDIENT_FILE) as f:
#             data = json.load(f)
#         filtered_data = {k: f"{v['amount']} {v['unit']}" for k, v in data.items() if k not in exclude_list}
#         st.dataframe(filtered_data, use_container_width=True)

#     if os.path.exists(THRESHOLD_FILE):
#         st.markdown("#### Ingredients Needing Reorder")
#         with open(INGREDIENT_FILE) as f:
#             inventory = json.load(f)
#         with open(THRESHOLD_FILE) as f:
#             thresholds = json.load(f)
#         needs_order = {
#             ing: f"{inventory[ing]['amount']} < {thresholds[ing]} {inventory[ing]['unit']}"
#             for ing in thresholds if ing not in exclude_list and ing in inventory and inventory[ing]["amount"] < thresholds[ing]
#         }
#         if needs_order:
#             st.error("⚠️ Order Needed:")
#             st.dataframe(needs_order)
#         else:
#             st.success("✅ All ingredients above minimum thresholds.")






# # def batching_system_section():
# #     st.subheader("⚙️ Manual Batching System")

#     recipe_name = st.selectbox("Select Recipe", list(recipes.keys()), key="batch_recipe_select_v2")
#     recipe = recipes[recipe_name]

#     # --- Scaling method selection ---
#     st.markdown("### 🔧 Choose Scaling Method")
#     scale_mode = st.selectbox(
#         "Scale recipe by:",
#         ["Total weight (grams)", "1.5 gallon tubs", "5 liter pans", "Mix of tubs and pans", "Available ingredient amounts"],
#         key="scaling_method"
#     )

#     scaled_recipe = None
#     scale_factor = None
#     target_weight = None

#     # --- 1. Total weight ---
#     if scale_mode == "Total weight (grams)":
#         target_weight = st.number_input("Enter total target weight (g)", min_value=100.0, step=100.0, key="weight_input")

#     # --- 2. 1.5 gallon tubs (approx. 4275g per tub) ---
#     elif scale_mode == "1.5 gallon tubs":
#         tubs = st.number_input("Number of 1.5 gallon tubs", min_value=0, step=1, key="tub_input")
#         target_weight = tubs * 4275

#     # --- 3. 5 liter pans (approx. 3750g per pan) ---
#     elif scale_mode == "5 liter pans":
#         pans = st.number_input("Number of 5L pans", min_value=0, step=1, key="pan_input")
#         target_weight = pans * 3750

#     # --- 4. Mix of tubs and pans ---
#     elif scale_mode == "Mix of tubs and pans":
#         tubs = st.number_input("Number of 1.5 gallon tubs", min_value=0, step=1, key="mixed_tub_input")
#         pans = st.number_input("Number of 5L pans", min_value=0, step=1, key="mixed_pan_input")
#         target_weight = tubs * 4275 + pans * 3750

#     # --- 5. Available ingredients ---
#     elif scale_mode == "Available ingredient amounts":
#         st.markdown("Enter available amounts (in grams):")
#         available_ingredients = {}
#         for ing in recipe["ingredients"].keys():
#             val = st.text_input(f"{ing}:", key=f"available_{ing}")
#             if val.strip():
#                 try:
#                     available_ingredients[ing] = float(val)
#                 except ValueError:
#                     st.error(f"Invalid number for {ing}")
#         if st.button("Adjust Based on Ingredients", key="adjust_by_available"):
#             adjusted, scale_factor = adjust_recipe_with_constraints(recipe, available_ingredients)
#             scaled_recipe = {
#                 "ingredients": adjusted,
#                 "instructions": recipe.get("instructions", [])
#             }
#             target_weight = sum(adjusted.values())
#             st.success(f"Recipe scaled to {round(target_weight)} g (scale factor: {round(scale_factor * 100)}%)")

#     # --- Perform scaling ---
#     if scale_mode != "Available ingredient amounts" and target_weight:
#         scaled_recipe, scale_factor = scale_recipe_to_target_weight(recipe, target_weight)
#         st.success(f"Recipe scaled to {round(target_weight)} g (scale factor: {round(scale_factor * 100)}%)")

#     # --- Display ingredients ---
#     if scaled_recipe:
#         st.markdown("### 📋 Scaled Ingredients")
#         for ing, amt in scaled_recipe["ingredients"].items():
#             st.write(f"- {amt} grams {ing}")

#         # --- Display instructions if any ---
#         if scaled_recipe.get("instructions"):
#             st.markdown("### 🧾 Instructions")
#             for step in scaled_recipe["instructions"]:
#                 st.markdown(f"- {step}")

#         # --- Step-by-step mode ---
#         st.markdown("---")
#         st.markdown("### 🧪 Step-by-Step Weighing")

#         if "step_index" not in st.session_state:
#             st.session_state.step_index = 0

#         if st.button("Start Over", key="reset_step"):
#             st.session_state.step_index = 0

#         steps = list(scaled_recipe["ingredients"].items())
#         i = st.session_state.step_index

#         if i < len(steps):
#             ing, amt = steps[i]
#             st.markdown(f"**Step {i+1}/{len(steps)}:** Weigh `{amt} grams of {ing}`")
#             if st.button("Next Ingredient", key=f"next_step_{i}"):
#                 st.session_state.step_index += 1
#         else:
#             st.success("✅ All ingredients completed!")

# --- Batching System Section ---
# def batching_system_section():
#     st.subheader("⚙️ Manual Batching System")
#     recipe_name = st.selectbox("Select Recipe", list(recipes.keys()), key="batch_recipe_select")
#     recipe = recipes[recipe_name]

#     st.markdown("### Scale by Target Weight")
#     target_weight = st.number_input("Target total weight (grams)", min_value=100.0, step=100.0, key="batch_target_weight")
#     if target_weight:
#         scaled_recipe, factor = scale_recipe_to_target_weight(recipe, target_weight)
#         st.markdown(f"#### Scaled Ingredients ({round(factor * 100)}%)")
#         for ing, amt in scaled_recipe["ingredients"].items():
#             st.write(f"- {amt} grams {ing}")

#     st.markdown("### Step-by-Step Mode")
#     if "step_i" not in st.session_state:
#         st.session_state.step_i = 0

#     if st.button("Start Over", key="reset_step_btn"):
#         st.session_state.step_i = 0

#     steps = list(scaled_recipe["ingredients"].items())
#     if st.session_state.step_i < len(steps):
#         ing, amt = steps[st.session_state.step_i]
#         st.markdown(f"**Weigh:** {amt} grams of {ing}")
#         if st.button("Next Ingredient", key=f"next_{st.session_state.step_i}"):
#             st.session_state.step_i += 1
#     else:
#         st.success("🎉 All ingredients completed!")
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
    return {"ingredients": adjusted_main, "instructions": recipe.get("instructions", [])}, scale_factor

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

# def set_min_inventory_section():
#     st.subheader("📉 Set Minimum Inventory Levels")

#     # Load existing thresholds
#     thresholds = {}
#     if os.path.exists(THRESHOLD_FILE):
#         with open(THRESHOLD_FILE, "r") as f:
#             thresholds = json.load(f)

#     # Load existing ingredient inventory
#     inventory = {}
#     if os.path.exists(INGREDIENT_FILE):
#         with open(INGREDIENT_FILE, "r") as f:
#             inventory = json.load(f)
#     else:
#         st.warning("❗ No ingredient inventory file found.")
#         return

#     if not inventory:
#         st.warning("❗ Ingredient inventory is empty.")
#         return

#     st.markdown("### Set thresholds for each ingredient")

#     # Loop over ingredients to show input fields
#     for ingredient in sorted(inventory.keys()):
#         current_threshold = thresholds.get(ingredient, 0)
#         new_threshold = st.number_input(
#             f"Minimum for {ingredient}",
#             min_value=0,
#             value=current_threshold,
#             step=100,
#             key=f"threshold_{ingredient}"
#         )
#         thresholds[ingredient] = new_threshold

#     if st.button("💾 Save Minimum Thresholds"):
#         with open(THRESHOLD_FILE, "w") as f:
#             json.dump(thresholds, f, indent=2)
#         st.success("✅ Minimum thresholds saved.")






# --- Utility Functions ---
def get_total_weight(recipe):
    return sum(recipe["ingredients"].values())

def scale_recipe_to_target_weight(recipe, target_weight):
    original_weight = get_total_weight(recipe)
    scale_factor = target_weight / original_weight
    adjusted_main = {k: round(v * scale_factor) for k, v in recipe["ingredients"].items()}
    return {"ingredients": adjusted_main, "instructions": recipe.get("instructions", [])}, scale_factor

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
























