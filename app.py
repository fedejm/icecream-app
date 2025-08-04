
import streamlit as st

# --- Recipes ---
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
            "3) Bake for 15 minmmutes at 350 F."
            ""
            
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
        "instructions": [
            
            
            
        ],
        "subrecipes": {},
    },"Dulce de Leche": {
        "ingredients": {
            "milk": 24775,
            "cream": 7500,
            "sugar": 2550,
            "guar": 75,
            "dry milk": 1000,
            "yolks": 500,
            "dulce de leche heladero": 90
        },
        "instructions": [
            
        ]
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
            "",
            "Day 2: Prepare Blanched Mint Purée",
            "3) 3 hours ahead, place 2 gallons of water in the freezer for ice water bath.",
            "4) Bring 2 gallons of fresh water to a boil.",
            "5) Carefully submerge the remaining fresh mint into the boiling water for 30 seconds.",
            "6) Immediately drain and shock the mint in the ice water bath to preserve its green color.",
            "7) Drain the mint and blend until very fine and smooth.",
            "",
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
            "4) Bake for 15 minmmutes at 325 F."
            ""
            
        ],
        "subrecipes": {}
    },
    "Honeycomb": {
        "ingredients": {
            "sugar": 3000,
            "honey": 50,
            "water": 1450,
            "baking soda": 250,
            },
        "instructions": [
            "1) Cook on medium heat, stirring constantly until sugar dissolves.",
            "2) Once sugar is completely dissolved, stop stirring.",
            "3) Continue cooking on high until 300 F.",
            "4) Add the baking soda and stir.",
            "5) Pour the rising honeycomb on previously greased trays and let cool."
            ""
            
        ],
        "subrecipes": {}
    },
    "Lemon Bar": {
    "ingredients": {
        "crust": 566,  # butter + flour + sugar + salt
        "filling": 1362  # estimated weight
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
}
,


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
            
            "1) combine strawberries and sugar and let stand for 3 hours.",
            "2) bring to boil, stirring occasionally.",
            "3) cook until it reaches 220 F and syrup is thick."
            ""
            
        ],
        "subrecipes": {}
    },
    "Toffee": {
        "ingredients": {
            "butter": 863,
            "sugar": 779,
            "honey": 17,
            "salt": 4,
            },
        "instructions": [
            
            "1) Cook on medium heat, stirring constantly until sugar dissolves.",
            "2) Once sugar is completely dissolved, stop stirring.",
            "3) Continue cooking on high until 300 F."
            ""
            
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

# --- Scaling Functions ---
def get_total_weight(recipe):
    return sum(recipe["ingredients"].values())

def scale_recipe_to_target_weight(recipe, target_weight):
    original_weight = get_total_weight(recipe)
    scale_factor = target_weight / original_weight
    adjusted_main = {k: round(v * scale_factor) for k, v in recipe["ingredients"].items()}

    scaled = {
        "ingredients": adjusted_main,
        "instructions": recipe.get("instructions", [])
    }

    if "subrecipes" in recipe:
        scaled["subrecipes"] = {}
        for name, sub in recipe["subrecipes"].items():
            scaled_sub = {
                "ingredients": {k: round(v * scale_factor) for k, v in sub["ingredients"].items()},
                "instructions": sub.get("instructions", [])
            }
            scaled["subrecipes"][name] = scaled_sub

    return scaled, scale_factor

def adjust_recipe_with_constraints(recipe, available_ingredients):
    base_ingredients = recipe.get("ingredients", {})
    ratios = [amt / base_ingredients[ing] for ing, amt in available_ingredients.items() if ing in base_ingredients and base_ingredients[ing] != 0]
    scale_factor = min(ratios) if ratios else 1
    adjusted = {k: round(v * scale_factor) for k, v in base_ingredients.items()}
    return adjusted, scale_factor

# --- Streamlit App ---
st.title("Ice Cream Recipe Adjuster")

selected = st.selectbox("Choose a recipe", list(recipes.keys()))
recipe = recipes[selected]

st.subheader("Choose how you want to scale the recipe:")
scale_mode = st.selectbox("Scaling method", ["Total weight (grams)", "1.5 gallon tubs", "5 liter pans", "Mix of tubs and pans", "Available ingredient amounts"])

target_weight = None
scaled_recipe = None

if scale_mode == "Total weight (grams)":
    w = st.text_input("Enter target total weight (g)", "")
    if w.strip():
        try:
            target_weight = float(w)
        except ValueError:
            st.error("Enter a valid number for total weight")

elif scale_mode == "1.5 gallon tubs":
    tubs = st.number_input("Number of 1.5 gallon tubs", min_value=0, step=1)
    target_weight = tubs * 4275

elif scale_mode == "5 liter pans":
    pans = st.number_input("Number of 5 liter pans", min_value=0, step=1)
    target_weight = pans * 3750

elif scale_mode == "Mix of tubs and pans":
    tubs = st.number_input("Tubs", min_value=0, step=1)
    pans = st.number_input("Pans", min_value=0, step=1)
    target_weight = tubs * 4275 + pans * 3750

if target_weight:
    scaled_recipe, scale_factor = scale_recipe_to_target_weight(recipe, target_weight)

if scale_mode == "Available ingredient amounts":
    st.subheader("Enter available ingredient amounts (g):")
    available_inputs = {}
    for ing in recipe["ingredients"]:
        val = st.text_input(f"{ing}", "")
        if val.strip():
            try:
                available_inputs[ing] = float(val)
            except ValueError:
                st.error(f"Invalid input for {ing}")

    if st.button("Adjust Recipe Based on Ingredients"):
        adjusted, limit_scale = adjust_recipe_with_constraints(recipe, available_inputs)
        st.session_state.adjusted_recipe = adjusted
        st.session_state.adjusted_total = round(sum(adjusted.values()))
        st.success(f"Adjusted recipe (scale factor: {limit_scale:.2f})")
        st.subheader(f"Final Adjusted Recipe:")
        for ing, amt in adjusted.items():
            st.write(f"{ing}: {amt} g")

if scaled_recipe:
    st.markdown("---")
    st.success(f"Scaled recipe to {round(target_weight)} g")
    st.subheader(f"Scaled {selected} Recipe")

    # --- Main Ingredients ---
    st.subheader("Main Ingredients")
    for ing, amt in scaled_recipe["ingredients"].items():
        st.write(f"• {ing}: {amt} g")

    # --- Subrecipes ---
    if "subrecipes" in scaled_recipe:
        for subname, sub in scaled_recipe["subrecipes"].items():
            st.subheader(f"Subrecipe: {subname}")
            for ing, amt in sub.get("ingredients", {}).items():
                st.write(f"• {ing}: {amt} g")

    # --- Instructions ---
    if scaled_recipe.get("instructions"):
        st.subheader("Instructions")
        for step in scaled_recipe["instructions"]:
            st.markdown(f"- {step}")
# --- Step-by-Step Ingredient Mode ---
st.markdown("---")
st.subheader("🧪 Step-by-Step Weighing")

# Initialize step index safely
if "step_index" not in st.session_state:
    st.session_state.step_index = 0

if st.button("Start Step-by-Step Mode"):
    st.session_state.step_index = 0

if scaled_recipe:
    # Flatten ingredients and subrecipes
    all_ingredients = list(scaled_recipe["ingredients"].items())

    if "subrecipes" in scaled_recipe:
        for subname, sub in scaled_recipe["subrecipes"].items():
            all_ingredients.append((f"[{subname}]", None))  # Section header
            all_ingredients.extend(list(sub["ingredients"].items()))

    step = st.session_state.step_index

    if step < len(all_ingredients):
        label, amount = all_ingredients[step]

        if amount is None:
            st.markdown(f"### {label}")  # e.g., [crust]
        else:
            st.markdown(f"### {label}: {round(amount)} grams")

        if st.button("Next"):
            st.session_state.step_index += 1
    else:
        st.success("✅ All ingredients completed!")
        if st.button("Restart"):
            st.session_state.step_index = 0




# if scaled_recipe:
#     st.success(f"Scaled recipe to {round(target_weight)} g")
#     st.subheader(f"Scaled {selected} Recipe:")
#     for ing, amt in scaled_recipe["ingredients"].items():
#         st.write(f"{ing}: {amt} g")
#     if scaled_recipe.get("subrecipes"):
#         for name, sub in scaled_recipe["subrecipes"].items():
#             st.subheader(f"Subrecipe: {name}")
#             for ing, amt in sub["ingredients"].items():
#                 st.write(f"{ing}: {amt} g")
#     if scaled_recipe.get("instructions"):
#         st.subheader("Instructions")
#         for step in scaled_recipe["instructions"]:
#             st.markdown(f"- {step}")



# # Display result
# if scaled_recipe:
#     st.subheader(f"Scaled Recipe: {selected}")
#     for ing, amt in scaled_recipe["ingredients"].items():
#         st.write(f"• {ing}: {amt} g")

#     if "subrecipes" in scaled_recipe:
#         for subname, sub in scaled_recipe["subrecipes"].items():
#             st.subheader(f"Subrecipe: {subname}")
#             for ing, amt in sub["ingredients"].items():
#                 st.write(f"  • {ing}: {amt} g")

#     if scaled_recipe.get("instructions"):
#         st.subheader("Instructions")
#         for step in scaled_recipe["instructions"]:
#             st.markdown(f"- {step}")






















