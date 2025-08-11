import streamlit as st
import os
import json
from datetime import datetime

# --- Sidebar navigation ---
page = st.sidebar.radio("Go to", ["Batching System", "Flavor Inventory", "Ingredient Inventory", "Set Min Inventory"], key="sidebar_nav")

# --- File Constants ---
LINEUP_FILE = "weekly_lineup.json"
INVENTORY_FILE = "inventory.json"
INGREDIENT_FILE = "ingredient_inventory.json"
THRESHOLD_FILE = "ingredient_thresholds.json"
EXCLUDE_FILE = "excluded_ingredients.json"
# --- Helpers ---
def get_all_ingredients(recipes: dict) -> list[str]:
    seen = set()
    for r in recipes.values():
        for ing in r.get("ingredients", {}).keys():
            seen.add(ing.strip())
    return sorted(seen)

def load_json(path: str, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return default
    return default

def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

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
    all_ingredients = sorted(set(all_ingredients))

    excluded_ingredients = []
    if os.path.exists(EXCLUDE_FILE):
        with open(EXCLUDE_FILE) as f:
            excluded_ingredients = json.load(f)

    st.markdown("#### Exclude Ingredients from Inventory")
    exclude_list = st.multiselect("Select ingredients to exclude", all_ingredients, default=excluded_ingredients, key="exclude_list")
    if st.button("Save Exclusion List", key="save_exclude_btn"):
        with open(EXCLUDE_FILE, "w") as f:
            json.dump(exclude_list, f, indent=2)
        st.success("Excluded ingredients list saved.")

    ingredient_inventory = {}
    min_thresholds = {}

    st.markdown("#### Enter Inventory and Minimum Thresholds")
    for ing in all_ingredients:
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

    if st.button("Save Ingredient Inventory", key="save_inventory_btn"):
        with open(INGREDIENT_FILE, "w") as f:
            json.dump(ingredient_inventory, f, indent=2)
        with open(THRESHOLD_FILE, "w") as f:
            json.dump(min_thresholds, f, indent=2)
        st.success("Ingredient inventory and thresholds saved.")

    if os.path.exists(INGREDIENT_FILE):
        st.markdown("#### Current Ingredient Inventory")
        with open(INGREDIENT_FILE) as f:
            data = json.load(f)
        filtered_data = {k: f"{v['amount']} {v['unit']}" for k, v in data.items() if k not in exclude_list}
        st.dataframe(filtered_data, use_container_width=True)

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
def batching_system_section():
    st.subheader("⚙️ Manual Batching System")

    recipe_name = st.selectbox("Select Recipe", list(recipes.keys()), key="batch_recipe_select_v2")
    recipe = recipes[recipe_name]

    # --- Scaling method selection ---
    st.markdown("### 🔧 Choose Scaling Method")
    scale_mode = st.selectbox(
        "Scale recipe by:",
        ["Total weight (grams)", "1.5 gallon tubs", "5 liter pans", "Mix of tubs and pans", "Available ingredient amounts"],
        key="scaling_method"
    )

    scaled_recipe = None
    scale_factor = None
    target_weight = None

    # --- 1. Total weight ---
    if scale_mode == "Total weight (grams)":
        target_weight = st.number_input("Enter total target weight (g)", min_value=100.0, step=100.0, key="weight_input")

    # --- 2. 1.5 gallon tubs (approx. 4275g per tub) ---
    elif scale_mode == "1.5 gallon tubs":
        tubs = st.number_input("Number of 1.5 gallon tubs", min_value=0, step=1, key="tub_input")
        target_weight = tubs * 4275

    # --- 3. 5 liter pans (approx. 3750g per pan) ---
    elif scale_mode == "5 liter pans":
        pans = st.number_input("Number of 5L pans", min_value=0, step=1, key="pan_input")
        target_weight = pans * 3750

    # --- 4. Mix of tubs and pans ---
    elif scale_mode == "Mix of tubs and pans":
        tubs = st.number_input("Number of 1.5 gallon tubs", min_value=0, step=1, key="mixed_tub_input")
        pans = st.number_input("Number of 5L pans", min_value=0, step=1, key="mixed_pan_input")
        target_weight = tubs * 4275 + pans * 3750

    # --- 5. Available ingredients ---
    elif scale_mode == "Available ingredient amounts":
        st.markdown("Enter available amounts (in grams):")
        available_ingredients = {}
        for ing in recipe["ingredients"].keys():
            val = st.text_input(f"{ing}:", key=f"available_{ing}")
            if val.strip():
                try:
                    available_ingredients[ing] = float(val)
                except ValueError:
                    st.error(f"Invalid number for {ing}")
        if st.button("Adjust Based on Ingredients", key="adjust_by_available"):
            adjusted, scale_factor = adjust_recipe_with_constraints(recipe, available_ingredients)
            scaled_recipe = {
                "ingredients": adjusted,
                "instructions": recipe.get("instructions", [])
            }
            target_weight = sum(adjusted.values())
            st.success(f"Recipe scaled to {round(target_weight)} g (scale factor: {round(scale_factor * 100)}%)")

    # --- Perform scaling ---
    if scale_mode != "Available ingredient amounts" and target_weight:
        scaled_recipe, scale_factor = scale_recipe_to_target_weight(recipe, target_weight)
        st.success(f"Recipe scaled to {round(target_weight)} g (scale factor: {round(scale_factor * 100)}%)")

    # --- Display ingredients ---
    if scaled_recipe:
        st.markdown("### 📋 Scaled Ingredients")
        for ing, amt in scaled_recipe["ingredients"].items():
            st.write(f"- {amt} grams {ing}")

        # --- Display instructions if any ---
        if scaled_recipe.get("instructions"):
            st.markdown("### 🧾 Instructions")
            for step in scaled_recipe["instructions"]:
                st.markdown(f"- {step}")

        # --- Step-by-step mode ---
        st.markdown("---")
        st.markdown("### 🧪 Step-by-Step Weighing")

        if "step_index" not in st.session_state:
            st.session_state.step_index = 0

        if st.button("Start Over", key="reset_step"):
            st.session_state.step_index = 0

        steps = list(scaled_recipe["ingredients"].items())
        i = st.session_state.step_index

        if i < len(steps):
            ing, amt = steps[i]
            st.markdown(f"**Step {i+1}/{len(steps)}:** Weigh `{amt} grams of {ing}`")
            if st.button("Next Ingredient", key=f"next_step_{i}"):
                st.session_state.step_index += 1
        else:
            st.success("✅ All ingredients completed!")

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
def flavor_inventory_section():
    st.subheader("🍦 Flavor & Topping Inventory Control")

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



# --- Recipe Database ---
recipes = {
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
                    "2) Press into a greased pan and bake for 15 minutes at 350°F."
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
                    "2) Pour on top of the baked crust and bake for 20 minutes at 350°F."
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


# --- Recipe Database ---
recipes = {
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
                    "2) Press into a greased pan and bake for 15 minutes at 350°F."
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
                    "2) Pour on top of the baked crust and bake for 20 minutes at 350°F."
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

# --- Routing ---
if page == "Ingredient Inventory":
    ingredient_inventory_section()
elif page == "Flavor Inventory":
    flavor_inventory_section()
elif page == "Batching System":
    batching_system_section()
if page == "Set Min Inventory":
    set_min_inventory_section()
