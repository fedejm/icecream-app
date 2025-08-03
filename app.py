
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
            "1) Combine all ingredients.",
            "2) Pasteurize the mix.",
            "3) Chill, batch freeze, and pack."
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
            "crust":{
            "butter": 225,
            "flour": 240,
            "sugar": 100,
            "salt": 1
                    },
        "instructions": [
            "1) process all ingredients on robocoupe until smooth.",
            "2) on a greased pan, cook the crust for 15 minutes at 350 F."
        ],
        "subrecipes": {
            "filling": {
                "ingredients": {
                    "eggs (each)": 12,
                    "lemon juice": 360,
                    "sugar": 900,
                    "flout": 90,
                },
                "instructions": [
                    "1) beat all the filling ingredients in a bowl until fully dissolved.",
                    "2) pour on top of the crust and bake for 20 minutes at 350 F."
                ]
            }
        }
        }      
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
    st.success(f"Scaled recipe to {round(target_weight)} g")
    st.subheader(f"Scaled {selected} Recipe:")
    for ing, amt in scaled_recipe["ingredients"].items():
        st.write(f"{ing}: {amt} g")
    if scaled_recipe.get("subrecipes"):
        for name, sub in scaled_recipe["subrecipes"].items():
            st.subheader(f"Subrecipe: {name}")
            for ing, amt in sub["ingredients"].items():
                st.write(f"{ing}: {amt} g")
    if scaled_recipe.get("instructions"):
        st.subheader("Instructions")
        for step in scaled_recipe["instructions"]:
            st.markdown(f"- {step}")


# import streamlit as st

# # --- Recipes ---
# recipes = {
#     "Vanilla": {
#         "ingredients": {
#             "milk": 28510,
#             "cream": 10000,
#             "sugar": 8250,
#             "guar": 110,
#             "dry_milk": 2500,
#             "yolks": 500,
#             "vanilla extract": 100,
#             "vanilla seeds": 90
#         },
#         "instructions": [
#             "1) Mix all ingredients thoroughly.",
#             "2) Pasteurize the mix.",
#             "3) Chill and batch freeze."
#         ]
#     }
#     # Add more recipes here
# }

# # --- Helper Functions ---
# def get_total_weight(recipe):
#     return sum(recipe["ingredients"].values())

# def scale_recipe_to_target_weight(recipe, target_weight):
#     original_weight = get_total_weight(recipe)
#     scale_factor = target_weight / original_weight
#     adjusted = {k: round(v * scale_factor) for k, v in recipe["ingredients"].items()}
#     return adjusted, scale_factor

# def adjust_recipe_with_constraints(recipe, available_ingredients):
#     base_ingredients = recipe["ingredients"]
#     ratios = [
#         available_ingredients[ing] / base_ingredients[ing]
#         for ing in available_ingredients
#         if ing in base_ingredients and base_ingredients[ing] != 0
#     ]
#     scale_factor = min(ratios) if ratios else 1
#     adjusted = {k: round(v * scale_factor) for k, v in base_ingredients.items()}
#     return adjusted, scale_factor

# # --- UI ---
# st.title("Ice Cream Recipe Adjuster")

# selected = st.selectbox("Choose a recipe", list(recipes.keys()))
# recipe = recipes[selected]

# scale_mode = st.selectbox(
#     "Scaling method",
#     (
#         "Total weight (grams)",
#         "1.5 gallon tubs",
#         "5 liter pans",
#         "Mix of tubs and pans",
#         "Available ingredient amounts"
#     )
# )

# target_weight = None
# show_ingredient_inputs = False

# if scale_mode == "Total weight (grams)":
#     w = st.text_input("Enter target total weight (g)")
#     if w.strip():
#         try:
#             target_weight = float(w)
#         except ValueError:
#             st.error("Invalid number")

# elif scale_mode == "1.5 gallon tubs":
#     tubs = st.number_input("Tubs (1.5 gal)", min_value=0, step=1)
#     target_weight = tubs * 4275

# elif scale_mode == "5 liter pans":
#     pans = st.number_input("Pans (5L)", min_value=0, step=1)
#     target_weight = pans * 3750

# elif scale_mode == "Mix of tubs and pans":
#     tubs = st.number_input("Tubs", min_value=0, step=1)
#     pans = st.number_input("Pans", min_value=0, step=1)
#     target_weight = tubs * 4275 + pans * 3750

# elif scale_mode == "Available ingredient amounts":
#     show_ingredient_inputs = True

# # --- Perform Scaling ---
# if target_weight:
#     scaled, factor = scale_recipe_to_target_weight(recipe, target_weight)
#     st.success(f"Scaled to {round(target_weight)} g (x{factor:.2f})")
#     st.subheader("Scaled Recipe:")
#     for k, v in scaled.items():
#         st.write(f"{k}: {v} g")
#     if recipe.get("instructions"):
#         st.subheader("Instructions:")
#         for step in recipe["instructions"]:
#             st.markdown(f"- {step}")

# # --- Ingredient Constraint ---
# if show_ingredient_inputs:
#     st.subheader("Enter Available Ingredient Amounts")
#     available = {}
#     for ing in recipe["ingredients"]:
#         val = st.text_input(f"{ing}", "")
#         if val:
#             try:
#                 available[ing] = float(val)
#             except ValueError:
#                 st.error(f"Invalid input for {ing}")

#     if st.button("Adjust Recipe Based on Ingredients"):
#         adjusted, scale = adjust_recipe_with_constraints(recipe, available)
#         st.success(f"Adjusted Recipe (x{scale:.2f})")
#         for ing, amt in adjusted.items():
#             st.write(f"{ing}: {amt} g")

# # import streamlit as st



# # # --- Recipes ---
# # recipes = {
# #     "vanilla": {
# #         "ingredients": {
# #             "milk": 28510,
# #             "cream": 10000,
# #             "sugar": 8250,
# #             "guar": 110,
# #             "dry_milk": 2500,
# #             "yolks": 500,
# #             "vanilla extract": 100,
# #             "vanilla seeds": 90
# #         },
# #         "instructions": [
# #             "1) Mix all ingredients thoroughly.",
# #             "2) Pasteurize the mix.",
# #             "3) Chill and batch freeze."
#         ]
#     },

#     "Dulce de Leche": {
#         "ingredients": {
#             "milk": 24775,
#             "cream": 7500,
#             "sugar": 2550,
#             "guar": 75,
#             "dry milk": 1000,
#             "yolks": 500,
#             "deulce de leche heladero": 90
#         },
#         "instructions": [
#             "1) Combine all ingredients.",
#             "2) Pasteurize the mix.",
#             "3) Chill, batch freeze, and pack."
#         ]
#     },

#     "Creme Brulee": {
#         "ingredients": {
#             "milk": 20300,
#             "cream": 6828,
#             "sugar": 4400,
#             "guar": 72,
#             "dry milk": 2800,
#             "yolks": 2400,
#             "caramel sauce": 3200
#         },
#         "instructions": [
#             "1) Weigh and mix all base ingredients except caramel sauce.",
#             "2) Weigh the caramel ingredients and cook on high until the sauce reaches 220°F.",
#             "3) Add some of the base into the caramel sauce and keep cooking on low heat until homogeneous.",
#             "4) Incorporate the caramel/base mix into the remainder of the base and mix well.",
#             "5) Before batch freezing, burn some caramel crust pieces with a torch as mix-in."
#         ],
#         "subrecipes": {
#             "caramel sauce": {
#                 "ingredients": {
#                     "sugar": 3200,
#                     "water": 500,
#                     "honey": 50
#                 },
#                 "instructions": [
#                     "1) Combine sugar, water, and honey.",
#                     "2) Cook on medium-high heat until sugar dissolves.",
#                     "3) Raise heat and cook until mixture reaches 220°F."
#                 ]
#             }
#         }
#     },

#     "Fresh Mint": {
#         "ingredients": {
#             "milk": 31140,
#             "cream": 6500,
#             "sugar": 8500,
#             "guar": 110,
#             "dry milk": 3000,
#             "yolks": 750,
#             "mint": 1250,
#             "blanched mint": 500
#         },
#         "instructions": [
#             "Day 1: Prepare Mint-Infused Milk",
#             "1) Heat 2 gallons of milk (to be subtracted from the base) with some fresh mint to 250°F for 2 hours.",
#             "2) After 2 hours, cover and refrigerate overnight to infuse the flavor.",
#             "",
#             "Day 2: Prepare Blanched Mint Purée",
#             "3) 3 hours ahead, place 2 gallons of water in the freezer for ice water bath.",
#             "4) Bring 2 gallons of fresh water to a boil.",
#             "5) Carefully submerge the remaining fresh mint into the boiling water for 30 seconds.",
#             "6) Immediately drain and shock the mint in the ice water bath to preserve its green color.",
#             "7) Drain the mint and blend until very fine and smooth.",
#             "",
#             "Final Steps:",
#             "8) Strain the infused milk from Day 1, pressing the mint to extract flavor.",
#             "9) Mix the strained mint milk and blended mint purée with the remaining base ingredients until homogeneous."
#         ],
#         "subrecipes": {}
#     },

#     "Pistachio": {
#         "ingredients": {
#             "milk": 32640,
#             "cream": 750,
#             "sugar": 8250,
#             "guar": 110,
#             "dry milk": 2750,
#             "yolks": 1000,
#             "pistachio paste": 4500
#         },
#         "instructions": [
#             "1) If pistachios are raw, roast them at 300°F for 8 minutes.",
#             "2) Mix the roasted pistachios and the pistachio oil in the Robocoupe for 10 minutes, then blend for 15 minutes until very smooth."
#         ],
#         "subrecipes": {
#             "pistachio paste": {
#                 "ingredients": {
#                     "roasted pistachios": 2967,
#                     "pistachio oil": 1532
#                 },
#                 "instructions": [
#                     "1) Roast the pistachios if raw.",
#                     "2) Blend pistachios with pistachio oil until smooth and creamy."
#                 ]
#             }
#         }
#     }
# }

# # --- Scaling Functions ---
# def get_total_weight(recipe):
#     return sum(recipe["ingredients"].values())

# def scale_recipe_to_target_weight(recipe, target_weight):
#     original_weight = get_total_weight(recipe)
#     scale_factor = target_weight / original_weight
#     adjusted_main = {
#         k: round(v * scale_factor) for k, v in recipe["ingredients"].items()
#     }

#     scaled = {
#         "ingredients": adjusted_main,
#         "instructions": recipe.get("instructions", [])
#     }

#     if "subrecipes" in recipe:
#         scaled["subrecipes"] = {}
#         for name, sub in recipe["subrecipes"].items():
#             scaled_sub = {
#                 "ingredients": {
#                     k: round(v * scale_factor) for k, v in sub["ingredients"].items()
#                 },
#                 "instructions": sub.get("instructions", [])
#             }
#             scaled["subrecipes"][name] = scaled_sub

#     return scaled, scale_factor

# def adjust_recipe_with_constraints(recipe, available_ingredients):
#     base_ingredients = recipe.get("ingredients", {})
#     ratios = []
#     for ing, amt in available_ingredients.items():
#         if ing in base_ingredients and base_ingredients[ing] != 0:
#             ratios.append(amt / base_ingredients[ing])
#     scale_factor = min(ratios) if ratios else 1
#     adjusted = {k: round(v * scale_factor) for k, v in base_ingredients.items()}
#     return {"ingredients": adjusted, "instructions": recipe.get("instructions", [])}, scale_factor

# # --- UI ---
# st.title("Ice Cream Recipe Adjuster")

# # Select recipe
# selected = st.selectbox("Choose a recipe", list(recipes.keys()))
# recipe = recipes[selected]

# # --- Scaling Method ---
# st.subheader("Choose how you want to scale the recipe:")
# scale_mode = st.selectbox(
#     "Scaling method",
#     (
#         "Total weight (grams)",
#         "1.5 gallon tubs",
#         "5 liter pans",
#         "Mix of tubs and pans",
#         "Available ingredient amounts"
#     )
# )

# target_weight = None
# show_ingredient_inputs = False

# if scale_mode == "Total weight (grams)":
#     w = st.text_input("Enter target total weight (g)", "")
#     if w.strip():
#         try:
#             target_weight = float(w)
#         except ValueError:
#             st.error("Enter a valid number for total weight")

# elif scale_mode == "1.5 gallon tubs":
#     tubs = st.number_input("Number of 1.5 gallon tubs", min_value=0, step=1)
#     target_weight = tubs * 4275

# elif scale_mode == "5 liter pans":
#     pans = st.number_input("Number of 5 liter pans", min_value=0, step=1)
#     target_weight = pans * 3750

# elif scale_mode == "Mix of tubs and pans":
#     tubs = st.number_input("Number of 1.5 gallon tubs", min_value=0, step=1)
#     pans = st.number_input("Number of 5 liter pans", min_value=0, step=1)
#     target_weight = tubs * 4275 + pans * 3750

# elif scale_mode == "Available ingredient amounts":
#     show_ingredient_inputs = True

# # Scaling method
# st.subheader("Choose how you want to scale the recipe:")
# scale_mode = st.selectbox(
#     "Scaling method",
#     (
#         "Total weight (grams)",
#         "Available ingredient amounts"
#     )
# )

# target_weight = None
# scaled_recipe = recipe
# scale_factor = 1

# if scale_mode == "Total weight (grams)":
#     w = st.text_input("Enter target total weight (g)", "")
#     if w.strip():
#         try:
#             target_weight = float(w)
#             scaled_recipe, scale_factor = scale_recipe_to_target_weight(recipe, target_weight)
#         except ValueError:
#             st.error("Please enter a valid number")

# elif scale_mode == "Available ingredient amounts":
#     st.subheader("Enter available ingredient amounts (grams)")
#     available_inputs = {}
#     for ing in recipe["ingredients"]:
#         val = st.text_input(f"{ing}", "")
#         if val.strip():
#             try:
#                 available_inputs[ing] = float(val)
#             except ValueError:
#                 st.error(f"Invalid input for {ing}")

#     if st.button("Adjust Recipe"):
#         scaled_recipe, scale_factor = adjust_recipe_with_constraints(recipe, available_inputs)
#         st.success(f"Adjusted recipe (scale factor: {scale_factor:.2f})")

# Display result
if scaled_recipe:
    st.subheader(f"Scaled Recipe: {selected}")
    for ing, amt in scaled_recipe["ingredients"].items():
        st.write(f"• {ing}: {amt} g")

    if "subrecipes" in scaled_recipe:
        for subname, sub in scaled_recipe["subrecipes"].items():
            st.subheader(f"Subrecipe: {subname}")
            for ing, amt in sub["ingredients"].items():
                st.write(f"  • {ing}: {amt} g")

    if scaled_recipe.get("instructions"):
        st.subheader("Instructions")
        for step in scaled_recipe["instructions"]:
            st.markdown(f"- {step}")



# import streamlit as st

# # --- Recipes ---
# recipes = {
#     "vanilla": {
#         "ingredients": {
#             "milk": 28510,
#             "cream": 10000,
#             "sugar": 8250,
#             "guar": 110,
#             "dry_milk": 2500,
#             "yolks": 500,
#             "vanilla extract": 100,
#             "vanilla seeds": 90
#         },
#         "instructions": [
#             "1) Mix all ingredients thoroughly.",
#             "2) Pasteurize the mix.",
#             "3) Chill and batch freeze."
#         ]
#     },

#     "Dulce de Leche": {
#         "ingredients": {
#             "milk": 24775,
#             "cream": 7500,
#             "sugar": 2550,
#             "guar": 75,
#             "dry milk": 1000,
#             "yolks": 500,
#             "deulce de leche heladero": 90
#         },
#         "instructions": [
#             "1) Combine all ingredients.",
#             "2) Pasteurize the mix.",
#             "3) Chill, batch freeze, and pack."
#         ]
#     },

#     "Creme Brulee": {
#         "ingredients": {
#             "milk": 20300,
#             "cream": 6828,
#             "sugar": 4400,
#             "guar": 72,
#             "dry milk": 2800,
#             "yolks": 2400,
#             "caramel sauce": 3200
#         },
#         "instructions": [
#             "1) Weigh and mix all base ingredients except caramel sauce.",
#             "2) Weigh the caramel ingredients and cook on high until the sauce reaches 220°F.",
#             "3) Add some of the base into the caramel sauce and keep cooking on low heat until homogeneous.",
#             "4) Incorporate the caramel/base mix into the remainder of the base and mix well.",
#             "5) Before batch freezing, burn some caramel crust pieces with a torch as mix-in."
#         ],
#         "subrecipes": {
#             "caramel sauce": {
#                 "ingredients": {
#                     "sugar": 3200,
#                     "water": 500,
#                     "honey": 50
#                 },
#                 "instructions": [
#                     "1) Combine sugar, water, and honey.",
#                     "2) Cook on medium-high heat until sugar dissolves.",
#                     "3) Raise heat and cook until mixture reaches 220°F."
#                 ]
#             }
#         }
#     },

#     "Fresh Mint": {
#         "ingredients": {
#             "milk": 31140,
#             "cream": 6500,
#             "sugar": 8500,
#             "guar": 110,
#             "dry milk": 3000,
#             "yolks": 750,
#             "mint": 1250,
#             "blanched mint": 500
#         },
#         "instructions": [
#             "Day 1: Prepare Mint-Infused Milk",
#             "1) Heat 2 gallons of milk (to be subtracted from the base) with some fresh mint to 250°F for 2 hours.",
#             "2) After 2 hours, cover and refrigerate overnight to infuse the flavor.",
#             "",
#             "Day 2: Prepare Blanched Mint Purée",
#             "3) 3 hours ahead, place 2 gallons of water in the freezer for ice water bath.",
#             "4) Bring 2 gallons of fresh water to a boil.",
#             "5) Carefully submerge the remaining fresh mint into the boiling water for 30 seconds.",
#             "6) Immediately drain and shock the mint in the ice water bath to preserve its green color.",
#             "7) Drain the mint and blend until very fine and smooth.",
#             "",
#             "Final Steps:",
#             "8) Strain the infused milk from Day 1, pressing the mint to extract flavor.",
#             "9) Mix the strained mint milk and blended mint purée with the remaining base ingredients until homogeneous."
#         ],
#         "subrecipes": {}
#     },

#     "Pistachio": {
#         "ingredients": {
#             "milk": 32640,
#             "cream": 750,
#             "sugar": 8250,
#             "guar": 110,
#             "dry milk": 2750,
#             "yolks": 1000,
#             "pistachio paste": 4500
#         },
#         "instructions": [
#             "1) If pistachios are raw, roast them at 300°F for 8 minutes.",
#             "2) Mix the roasted pistachios and the pistachio oil in the Robocoupe for 10 minutes, then blend for 15 minutes until very smooth."
#         ],
#         "subrecipes": {
#             "pistachio paste": {
#                 "ingredients": {
#                     "roasted pistachios": 2967,
#                     "pistachio oil": 1532
#                 },
#                 "instructions": [
#                     "1) Roast the pistachios if raw.",
#                     "2) Blend pistachios with pistachio oil until smooth and creamy."
#                 ]
#             }
#         }
#     }
# }

# # --- Scaling Functions ---
# def get_total_weight(recipe):
#     return sum(recipe["ingredients"].values())

# def scale_recipe_to_target_weight(recipe, target_weight):
#     original_weight = get_total_weight(recipe)
#     scale_factor = target_weight / original_weight
#     adjusted_main = {
#         k: round(v * scale_factor) for k, v in recipe["ingredients"].items()
#     }

#     scaled = {
#         "ingredients": adjusted_main,
#         "instructions": recipe.get("instructions", [])
#     }

#     if "subrecipes" in recipe:
#         scaled["subrecipes"] = {}
#         for name, sub in recipe["subrecipes"].items():
#             scaled_sub = {
#                 "ingredients": {
#                     k: round(v * scale_factor) for k, v in sub["ingredients"].items()
#                 },
#                 "instructions": sub.get("instructions", [])
#             }
#             scaled["subrecipes"][name] = scaled_sub

#     return scaled, scale_factor
# def adjust_recipe_with_constraints(recipe, available_ingredients):
#     base_ingredients = recipe.get("ingredients", {})
#     ratios = []
#     for ing, amt in available_ingredients.items():
#         if ing in base_ingredients and base_ingredients[ing] != 0:
#             ratios.append(amt / base_ingredients[ing])
#     scale_factor = min(ratios) if ratios else 1
#     adjusted = {
#         k: round(v * scale_factor) for k, v in base_ingredients.items()
#     }
#     return adjusted, scale_factor





# def adjust_recipe_with_constraints(recipe, available_ingredients):
#     base_ingredients = recipe.get("ingredients", {})
#     ratios = []
#     for ing, amt in available_ingredients.items():
#         if ing in base_ingredients and base_ingredients[ing] != 0:
#             ratios.append(amt / base_ingredients[ing])
#     scale_factor = min(ratios) if ratios else 1



# # # --- Recipes ---
# # recipes = {
# #     "vanilla": {
# #         "ingredients":{
# #         "milk": 28510,
# #         "cream": 10000,
# #         "sugar": 8250,
# #         "guar": 110,
# #         "dry_milk": 2500,
# #         "yolks": 500,
# #         "vanilla extract": 100,
# #         "vanilla seeds": 90
# #     },

# #     "Dulce de Leche": {
# #         "milk": 24775,
# #         "cream": 7500,
# #         "sugar": 2550,
# #         "guar": 75,
# #         "dry milk": 1000,
# #         "yolks": 500,
# #         "deulce de leche heladero": 90
# #     },

# #     "Creme Brulee": {
# #         "ingredients": {
# #             "milk": 20300,
# #             "cream": 6828,
# #             "sugar": 4400,
# #             "guar": 72,
# #             "dry milk": 2800,
# #             "yolks": 2400,
# #             "caramel sauce": 3200  # total weight from sub-recipe
# #         },
# #         "instructions": [
# #             "1) Weigh and mix all base ingredients except caramel sauce.",
# #             "2) Weigh the Caramel Ingredients and cook on high until the sauce reaches 220°F.",
# #             "3) Add some of the base into the caramel sauce and keep cooking on low heat until homogeneous.",
# #             "4) Incorporate the Caramel/Base mix into the remainder of the base and mix well.",
# #             "5) Before batch freezing, burn some caramel crust pieces with a torch as mix-in."
# #         ],
# #         "subrecipes": {
# #             "caramel sauce": {
# #                 "ingredients": {
# #                     "sugar": 3200,
# #                     "water": 500,
# #                     "honey": 50
# #                 },
# #                 "instructions": [
# #                     "1) Combine sugar, water, and honey.",
# #                     "2) Cook on medium-high heat until sugar dissolves.",
# #                     "3) Raise heat and cook until mixture reaches 220°F."
# #                 ]
# #             }
# #         }
# #     },


# #     "Fresh Mint": {
# #         "ingredients": {
# #             "milk": 31140,
# #             "cream": 6500,
# #             "sugar": 8500,
# #             "guar": 110,
# #             "dry milk": 3000,
# #             "yolks": 750,
# #             "mint": 1250,
# #             "blanched mint": 500  # total weight from sub-recipe
# #         },
# #         "instructions": [
# #             "Day 1: Prepare Mint-Infused Milk",
# #         "1) Heat 2 gallons of milk (to be subtracted from the base) with some fresh mint to 250°F for 2 hours.",
# #         "2) After 2 hours, cover and refrigerate overnight to infuse the flavor.",
# #         "",
# #         "Day 2: Prepare Blanched Mint Purée",
# #         "3) 3 hours ahead, place 2 gallons of water in the freezer for ice water bath.",
# #         "4) Bring 2 gallons of fresh water to a boil.",
# #         "5) Carefully submerge the remaining fresh mint into the boiling water for 30 seconds.",
# #         "6) Immediately drain and shock the mint in the ice water bath to preserve its green color.",
# #         "7) Drain the mint and blend until very fine and smooth.",
# #         "",
# #         "Final Steps:",
# #         "8) Strain the infused milk from Day 1, pressing the mint to extract flavor.",
# #         "9) Mix the strained mint milk and blended mint purée with the remaining base ingredients until homogeneous."
# #         ],
# #         "subrecipes": {
# #             "caramel sauce": {
# #                 "ingredients": {
# #                     "sugar": 3200,
# #                     "water": 500,
# #                     "honey": 50
# #                 },
# #                 "instructions": [
# #                     "1) Combine sugar, water, and honey.",
# #                     "2) Cook on medium-high heat until sugar dissolves.",
# #                     "3) Raise heat and cook until mixture reaches 220°F."
# #                 ]
# #             }
# #         }
# #     },
# #     "Pistachio": {
# #         "ingredients": {
# #             "milk": 32640,
# #             "cream": 750,
# #             "sugar": 8250,
# #             "guar": 110,
# #             "dry milk": 2750,
# #             "yolks": 1000,
# #             "pistachio paste": 4500  # total weight from sub-recipe
# #         },
# #         "instructions": [
# #             "1) If pistachios are raw, roast them at 300°F for 8 minutes.",
# #             "2) Mix the roasted pistachios and the pistachio oil in the Robocoupe for 10 minutes, then blend for 15 minutes until very smooth."
# #         ],
# #         "subrecipes": {
# #             "pistachio paste": {
# #                 "ingredients": {
# #                     "roasted pistachios": 2967,
# #                     "pistachio oil": 1532
# #                 },
# #                 "instructions": [
# #                     "1) Roast the pistachios if raw.",
# #                     "2) Blend pistachios with pistachio oil until smooth and creamy."
# #                 ]
# #             }
# #         }
# #     }
# # }


# # # --- Recipes ---
# # recipes = {
# #     "vanilla": {
# #         "milk": 28510,
# #         "cream": 10000,
# #         "sugar": 8250,
# #         "guar": 110,
# #         "dry_milk": 2500,
# #         "yolks": 500,
# #         "vanilla extract": 100,
# #         "vanilla seeds": 90
# #     },
    
# #     "Dulce de Leche": {
# #         "milk": 24775,
# #         "cream": 7500,
# #         "sugar": 2550,
# #         "guar": 75,
# #         "dry milk": 1000,
# #         "yolks": 500,
# #         "deulce de leche heladero": 90
# #     },
# #         "Creme Brulee": {
# #         "ingredients": {
# #             "milk": 20300,
# #             "cream": 6828,
# #             "sugar": 4400,
# #             "guar": 72,
# #             "dry milk": 2800,
# #             "yolks": 2400,
# #             "caramel sauce": 3200  # total weight from sub-recipe
# #         },
# #         "instructions": [
# #             "1) Weigh and mix all base ingredients except caramel sauce.",
# #             "2) Weigh the Caramel Ingredients and cook on high until the sauce reaches 220 F.",
# #             "3) Add some of the base into the caramel sauce and keep cooking on low heat until homogeneous",
# #             "4) In corporate the Caramel/Base mix into the reminder of the base and mix well",
# #             "5) Before batch freezing, burn some caramel crust pieces with a torch as mix-in."
# #         ],
# #         "subrecipes": {
# #             "caramel sauce": {
# #                 "ingredients": {
# #                     "sugar": 3200,
# #                     "water": 500,
# #                     "honey": 50
# #                 },
# # "Pistachio": {
# #     "ingredients": {
# #         "milk": 32640,
# #         "cream": 750,
# #         "sugar": 8250,
# #         "guar": 110,
# #         "dry milk": 2750,
# #         "yolks": 1000,
# #         "pistachio paste": 4500  # total weight from sub-recipe
# #     },
# #     "instructions": [
# #         "1) If pistachios are raw, roast them at 300°F for 8 minutes.",
# #         "2) Mix the roasted pistachios and the pistachio oil in the Robocoupe for 10 minutes, then blend for 15 minutes."
# #     ],
# #     "subrecipes": {
# #         "pistachio paste": {
# #             "ingredients": {
# #                 "roasted pistachios": 2967,
# #                 "pistachio oil": 1532
# #             },
# #             "instructions": [
# #                 "1) Roast the pistachios if raw.",
# #                 "2) Blend pistachios with pistachio oil until smooth and creamy."
# #             ]
# #         }
# #     }
# # }

#         # "Pistachio": {
#         # "ingredients": {
#         #     "milk": 32640,
#         #     "cream": 750,
#         #     "sugar": 8250,
#         #     "guar": 110,
#         #     "dry milk": 2750,
#         #     "yolks": 1000,
#         #     "pistachio paste": 4500  # total weight from sub-recipe
#         # },
#         # "instructions": [
#         #     "1) If Pistachios are raw, roast them at 300 F for 8 minutes.",
#         #     "2) Mix the Rasted Pistachios and the Pistachio Oil on the robocoupe for 10 minutes and then on the blender for 15 minutes",
            
#         # ],
#         # "subrecipes": {
#         #     "pistachio paste": {
#         #         "ingredients": {
#         #             "roasted pistachios": 2967,
#         #             "pistachio oil": 1532,
#         #                             }}

# # --- Scaling Functions ---
# def get_total_weight(recipe):
#     return sum(recipe["ingredients"].values())

# def scale_recipe_to_target_weight(recipe, target_weight):
#     original_weight = get_total_weight(recipe)
#     scale_factor = target_weight / original_weight
#     adjusted_main = {
#         k: round(v * scale_factor) for k, v in recipe["ingredients"].items()
#     }

#     scaled = {
#         "ingredients": adjusted_main,
#         "instructions": recipe.get("instructions", [])
#     }

#     if "subrecipes" in recipe:
#         scaled["subrecipes"] = {}
#         for name, sub in recipe["subrecipes"].items():
#             scaled_sub = {
#                 "ingredients": {
#                     k: round(v * scale_factor) for k, v in sub["ingredients"].items()
#                 },
#                 "instructions": sub.get("instructions", [])
#             }
#             scaled["subrecipes"][name] = scaled_sub

#     return scaled, scale_factor

# def adjust_recipe_with_constraints(recipe, available_ingredients):
#     ratios = []
#     for ing, amt in available_ingredients.items():
#         if ing in recipe and recipe[ing] != 0:
#             ratios.append(amt / recipe[ing])
#     scale_factor = min(ratios) if ratios else 1
#     adjusted = {k: round(v * scale_factor) for k, v in recipe.items()}
#     return adjusted, scale_factor

# # --- UI ---
# st.title("Ice Cream Recipe Adjuster")

# # Select recipe
# selected = st.selectbox("Choose a recipe", list(recipes.keys()))
# recipe = recipes[selected]

# # --- Scaling Method ---
# st.subheader("Choose how you want to scale the recipe:")
# scale_mode = st.selectbox(
#     "Scaling method",
#     (
#         "Total weight (grams)",
#         "1.5 gallon tubs",
#         "5 liter pans",
#         "Mix of tubs and pans",
#         "Available ingredient amounts"
#     )
# )

# target_weight = None
# show_ingredient_inputs = False

# if scale_mode == "Total weight (grams)":
#     w = st.text_input("Enter target total weight (g)", "")
#     if w.strip():
#         try:
#             target_weight = float(w)
#         except ValueError:
#             st.error("Enter a valid number for total weight")

# elif scale_mode == "1.5 gallon tubs":
#     tubs = st.number_input("Number of 1.5 gallon tubs", min_value=0, step=1)
#     target_weight = tubs * 4275

# elif scale_mode == "5 liter pans":
#     pans = st.number_input("Number of 5 liter pans", min_value=0, step=1)
#     target_weight = pans * 3750

# elif scale_mode == "Mix of tubs and pans":
#     tubs = st.number_input("Tubs", min_value=0, step=1)
#     pans = st.number_input("Pans", min_value=0, step=1)
#     target_weight = tubs * 4275 + pans * 3750

# elif scale_mode == "Available ingredient amounts":
#     show_ingredient_inputs = True

# # --- Scale recipe if target weight is defined ---
# scaled_recipe = recipe
# scale_factor = 1

# if target_weight:
#     scaled_recipe, scale_factor = scale_recipe_to_target_weight(recipe, target_weight)
#     st.success(f"Scaled recipe to {round(target_weight)} g (scale factor: {scale_factor:.2f})")
#     st.subheader(f"Scaled {selected} Recipe:")
#     st.session_state.adjusted_recipe = scaled_recipe

#     main_total = sum(scaled_recipe["ingredients"].values())
#     sub_total = 0
#     if "subrecipes" in scaled_recipe:
#         for sub in scaled_recipe["subrecipes"].values():
#             sub_total += sum(sub["ingredients"].values())

#     st.session_state.adjusted_total = round(main_total + sub_total)
#     st.session_state.processing_mode = False
#     st.session_state.current_step = 0

#     for ing, amt in scaled_recipe["ingredients"].items():
#         st.write(f"{ing}: {amt} g")

#     if "subrecipes" in scaled_recipe:
#         for sub_name, sub in scaled_recipe["subrecipes"].items():
#             st.subheader(f"Subrecipe: {sub_name}")
#             for ing, amt in sub["ingredients"].items():
#                 st.write(f"{ing}: {amt} g")

#     if scaled_recipe.get("instructions"):
#         st.subheader("Instructions")
#         for step in scaled_recipe["instructions"]:
#             st.markdown(f"- {step}")

#     st.button("Process Recipe", on_click=lambda: st.session_state.update({
#         "processing_mode": True,
#         "current_step": 0
#     }))


# # # --- Scaling Functions ---
# # def get_total_weight(recipe):
# #     return sum(recipe["ingredients"].values())

    
# # # --- Scaling Functions ---
# # # def get_total_weight(recipe):
# # #     return sum(recipe.values())

# # # def scale_recipe_to_target_weight(recipe, target_weight):
# # #     original_weight = get_total_weight(recipe)
# # #     scale_factor = target_weight / original_weight
# # #     adjusted = {k: round(v * scale_factor) for k, v in recipe.items()}
# # #     return adjusted, scale_factor
# # def scale_recipe_to_target_weight(recipe, target_weight):
# #     original_weight = get_total_weight(recipe)
# #     scale_factor = target_weight / original_weight
# #     adjusted_main = {
# #         k: round(v * scale_factor) for k, v in recipe["ingredients"].items()
# #     }

# #     scaled = {
# #         "ingredients": adjusted_main,
# #         "instructions": recipe.get("instructions", [])
# #     }

# #     if "subrecipes" in recipe:
# #         scaled["subrecipes"] = {}
# #         for name, sub in recipe["subrecipes"].items():
# #             scaled_sub = {
# #                 "ingredients": {
# #                     k: round(v * scale_factor) for k, v in sub["ingredients"].items()
# #                 },
# #                 "instructions": sub.get("instructions", [])
# #             }
# #             scaled["subrecipes"][name] = scaled_sub

# #     return scaled, scale_factor

# # def adjust_recipe_with_constraints(recipe, available_ingredients):
# #     ratios = []
# #     for ing, amt in available_ingredients.items():
# #         if ing in recipe and recipe[ing] != 0:
# #             ratios.append(amt / recipe[ing])
# #     scale_factor = min(ratios) if ratios else 1
# #     adjusted = {k: round(v * scale_factor) for k, v in recipe.items()}
# #     return adjusted, scale_factor

# # # --- UI ---
# # st.title("Ice Cream Recipe Adjuster")

# # # Select recipe
# # selected = st.selectbox("Choose a recipe", list(recipes.keys()))
# # recipe = recipes[selected]

# # # --- Scaling Method ---
# # st.subheader("Choose how you want to scale the recipe:")
# # scale_mode = st.selectbox(
# #     "Scaling method",
# #     (
# #         "Total weight (grams)",
# #         "1.5 gallon tubs",
# #         "5 liter pans",
# #         "Mix of tubs and pans",
# #         "Available ingredient amounts"
# #     )
# # )

# # target_weight = None
# # show_ingredient_inputs = False

# # if scale_mode == "Total weight (grams)":
# #     w = st.text_input("Enter target total weight (g)", "")
# #     if w.strip():
# #         try:
# #             target_weight = float(w)
# #         except ValueError:
# #             st.error("Enter a valid number for total weight")

# # elif scale_mode == "1.5 gallon tubs":
# #     tubs = st.number_input("Number of 1.5 gallon tubs", min_value=0, step=1)
# #     target_weight = tubs * 4275

# # elif scale_mode == "5 liter pans":
# #     pans = st.number_input("Number of 5 liter pans", min_value=0, step=1)
# #     target_weight = pans * 3750

# # elif scale_mode == "Mix of tubs and pans":
# #     tubs = st.number_input("Tubs", min_value=0, step=1)
# #     pans = st.number_input("Pans", min_value=0, step=1)
# #     target_weight = tubs * 4275 + pans * 3750

# # elif scale_mode == "Available ingredient amounts":
# #     show_ingredient_inputs = True

# # # --- Scale recipe if target weight is defined ---
# # scaled_recipe = recipe
# # scale_factor = 1

# # if target_weight:
# #     scaled_recipe, scale_factor = scale_recipe_to_target_weight(recipe, target_weight)
# #     st.success(f"Scaled recipe to {round(target_weight)} g (scale factor: {scale_factor:.2f})")
# #     st.subheader(f"Scaled {selected} Recipe:")
# #     st.session_state.adjusted_recipe = scaled_recipe
# #     st.session_state.adjusted_total = round(sum(scaled_recipe.values()))
# #     st.session_state.processing_mode = False
# #     st.session_state.current_step = 0

# #     for ing, amt in scaled_recipe.items():
# #         st.write(f"{ing}: {amt} g")

# #     st.button("Process Recipe", on_click=lambda: st.session_state.update({
# #         "processing_mode": True,
# #         "current_step": 0
# #     }))


# # # --- Available Ingredient Input Mode ---
# # if show_ingredient_inputs:
# #     st.subheader("Enter available ingredient amounts (in grams)")
# #     st.write("Leave blank if you have the full amount for an ingredient.")

# #     available_inputs = {}
# #     for ing in recipe:
# #         val = st.text_input(f"{ing}", "")
# #         if val.strip():
# #             try:
# #                 available_inputs[ing] = float(val)
# #             except ValueError:
# #                 st.error(f"Invalid input for {ing}")

# #     if st.button("Adjust Recipe Based on Ingredients"):
# #         adjusted, limit_scale = adjust_recipe_with_constraints(recipe, available_inputs)
# #         st.session_state.adjusted_recipe = adjusted
# #         st.session_state.adjusted_total = round(sum(adjusted.values()))
# #         st.session_state.processing_mode = False
# #         st.session_state.current_step = 0

# #         st.success(f"Adjusted recipe (scale factor: {limit_scale:.2f})")
# #         st.subheader(f"Final Adjusted Recipe (Total: {st.session_state.adjusted_total} g):")
# #         for ing, amt in st.session_state.adjusted_recipe.items():
# #             st.write(f"{ing}: {amt} g")

# #         st.button("Process Recipe", on_click=lambda: st.session_state.update({
# #             "processing_mode": True,
# #             "current_step": 0
# #         }))
# # # --- Step-by-step processing screen ---
# # if st.session_state.get("processing_mode", False):
# #     adjusted = st.session_state.get("adjusted_recipe", None)
# #     if not adjusted:
# #         st.error("No adjusted recipe found. Please scale or adjust a recipe first.")
# #     else:
# #         step = st.session_state.get("current_step", 0)
# #         ingredients = list(adjusted.items())

# #         if step < len(ingredients):
# #             ing, amt = ingredients[step]
# #             st.header(f"Step {step + 1} of {len(ingredients)}")
# #             st.subheader(f"🧪 {ing}: {amt} g")

# #             if st.button("Next"):
# #                 st.session_state.current_step += 1
# #         else:
# #             st.success("✅ All ingredients processed!")
# #             if st.button("Reset"):
# #                 st.session_state.processing_mode = False
# #                 st.session_state.current_step = 0

# # # # --- Step-by-step processing screen ---
# # # if st.session_state.get("processing_mode", False):
# # #     adjusted = st.session_state.get("adjusted_recipe", {})
# # #     step = st.session_state.get("current_step", 0)
# # #     ingredients = list(adjusted.items())

# # #     if step < len(ingredients):
# # #         ing, amt = ingredients[step]
# # #         st.header(f"Step {step + 1} of {len(ingredients)}")
# # #         st.subheader(f"🧪 {ing}: {amt} g")

# # #         if st.button("Next"):
# # #             st.session_state.current_step += 1
# # #     else:
# # #         st.success("✅ All ingredients processed!")
# # #         if st.button("Reset"):
# # #             st.session_state.processing_mode = False
# # #             st.session_state.current_step = 0



# # # # --- Scaling Function ---
# # # def get_total_weight(recipe):
# # #     return sum(recipe.values())

# # # def scale_recipe_to_target_weight(recipe, target_weight):
# # #     original_weight = get_total_weight(recipe)
# # #     scale_factor = target_weight / original_weight
# # #     adjusted = {k: round(v * scale_factor) for k, v in recipe.items()}
# # #     return adjusted, scale_factor


# # # def adjust_recipe_with_constraints(recipe, available_ingredients):
# # #     ratios = []
# # #     for ing, amt in available_ingredients.items():
# # #         if ing in recipe and recipe[ing] != 0:
# # #             ratios.append(amt / recipe[ing])
# # #     scale_factor = min(ratios) if ratios else 1
# # #     adjusted = {k: round(v * scale_factor) for k, v in recipe.items()}
# # #     return adjusted, scale_factor

# # # # --- Streamlit App ---
# # # st.title("Ice Cream Recipe Adjuster")

# # # # Select recipe
# # # selected = st.selectbox("Choose a recipe", list(recipes.keys()))
# # # recipe = recipes[selected]

# # # st.subheader("Enter available amounts (in grams)")
# # # st.write("Leave blank if you have the full amount for an ingredient.")

# # # # Collect available inputs
# # # available_inputs = {}
# # # for ing in recipe:
# # #     val = st.text_input(f"{ing}", "")
# # #     if val.strip():
# # #         try:
# # #             available_inputs[ing] = float(val)
# # #         except ValueError:
# # #             st.error(f"Invalid input for {ing}")

# # # # # Button to adjust
# # # #  if st.button("Adjust Recipe"):
# # # #     adjusted, scale = adjust_recipe_with_constraints(recipe, available_inputs)
# # # #     st.success(f"Scale factor: {scale:.2f}")
# # # #     st.subheader("Adjusted Recipe:")
# # # #     for ing, amt in adjusted.items():
# # # #         st.write(f"{ing}: {amt} g")

# # # # --- Final Adjusted Output ---
# # # if st.button("Adjust Recipe Based on Ingredients"):
# # #     adjusted, limit_scale = adjust_recipe_with_constraints(scaled_recipe, available_inputs)
# # #     st.session_state.adjusted_recipe = adjusted
# # #     st.session_state.adjusted_total = round(sum(adjusted.values()))
# # #     st.session_state.processing_mode = False
# # #     st.session_state.current_step = 0

# # #     st.success(f"Adjusted recipe (scale factor: {limit_scale:.2f})")
# # #     st.subheader(f"Final Adjusted Recipe (Total: {st.session_state.adjusted_total} g):")
# # #     for ing, amt in st.session_state.adjusted_recipe.items():
# # #         st.write(f"{ing}: {amt} g")

# # #     st.button("Process Recipe", on_click=lambda: st.session_state.update({
# # #         "processing_mode": True,
# # #         "current_step": 0
# # #     }))

# # # # --- Step-by-step processing screen ---
# # # if st.session_state.get("processing_mode", False):
# # #     adjusted = st.session_state.get("adjusted_recipe", {})
# # #     step = st.session_state.get("current_step", 0)
# # #     ingredients = list(adjusted.items())

# # #     if step < len(ingredients):
# # #         ing, amt = ingredients[step]
# # #         st.header(f"Step {step + 1} of {len(ingredients)}")
# # #         st.subheader(f"🧪 {ing}: {amt} g")

# # #         if st.button("Next"):
# # #             st.session_state.current_step += 1
# # #     else:
# # #         st.success("✅ All ingredients processed!")
# # #         if st.button("Reset"):
# # #             st.session_state.processing_mode = False
# # #             st.session_state.current_step = 0


# # # st.subheader("Choose how you want to scale the recipe:")

# # # scale_mode = st.selectbox(
# # #     "Scaling method",
# # #     ("Total weight (grams)", "1.5 gallon tubs", "5 liter pans", "Mix of tubs and pans")
# # # )

# # # target_weight = None

# # # if scale_mode == "Total weight (grams)":
# # #     w = st.text_input("Enter target total weight (g)", "")
# # #     if w.strip():
# # #         try:
# # #             target_weight = float(w)
# # #         except ValueError:
# # #             st.error("Enter a valid number for total weight")

# # # elif scale_mode == "1.5 gallon tubs":
# # #     tubs = st.number_input("Number of 1.5 gallon tubs", min_value=0, step=1)
# # #     target_weight = tubs * 4275  # approx 0.75 g/mL × 5.7L

# # # elif scale_mode == "5 liter pans":
# # #     pans = st.number_input("Number of 5 liter pans", min_value=0, step=1)
# # #     target_weight = pans * 3750

# # # elif scale_mode == "Mix of tubs and pans":
# # #     tubs = st.number_input("Tubs", min_value=0, step=1)
# # #     pans = st.number_input("Pans", min_value=0, step=1)
# # #     target_weight = tubs * 4275 + pans * 3750

# # # # Scale recipe if a target weight is set
# # # scaled_recipe = recipe
# # # scale_factor = 1

# # # if target_weight:
# # #     scaled_recipe, scale_factor = scale_recipe_to_target_weight(recipe, target_weight)
# # #     st.success(f"Scaled recipe to {round(target_weight)} g (scale factor: {scale_factor:.2f})")


# # # --- Scaling Functions ---
# # # def get_total_weight(recipe):
# # #     return sum(recipe.values())

# # # def scale_recipe_to_target_weight(recipe, target_weight):
# # #     original_weight = get_total_weight(recipe)
# # #     scale_factor = target_weight / original_weight
# # #     adjusted = {k: round(v * scale_factor) for k, v in recipe.items()}
# # #     return adjusted, scale_factor

# # # def adjust_recipe_with_constraints(recipe, available_ingredients):
# # #     ratios = []
# # #     for ing, amt in available_ingredients.items():
# # #         if ing in recipe and recipe[ing] != 0:
# # #             ratios.append(amt / recipe[ing])
# # #     scale_factor = min(ratios) if ratios else 1
# # #     adjusted = {k: round(v * scale_factor) for k, v in recipe.items()}
# # #     return adjusted, scale_factor

# # # # --- UI ---
# # # st.title("Ice Cream Recipe Adjuster")

# # # # Select recipe
# # # selected = st.selectbox("Choose a recipe", list(recipes.keys()))
# # # recipe = recipes[selected]

# # # # --- Scaling Input ---
# # # st.subheader("Choose how you want to scale the recipe:")
# # # scale_mode = st.selectbox(
# # #     "Scaling method",
# # #     ("Total weight (grams)", "1.5 gallon tubs", "5 liter pans", "Mix of tubs and pans")
# # # )

# # # target_weight = None

# # # if scale_mode == "Total weight (grams)":
# # #     w = st.text_input("Enter target total weight (g)", "")
# # #     if w.strip():
# # #         try:
# # #             target_weight = float(w)
# # #         except ValueError:
# # #             st.error("Enter a valid number for total weight")

# # # elif scale_mode == "1.5 gallon tubs":
# # #     tubs = st.number_input("Number of 1.5 gallon tubs", min_value=0, step=1)
# # #     target_weight = tubs * 4275

# # # elif scale_mode == "5 liter pans":
# # #     pans = st.number_input("Number of 5 liter pans", min_value=0, step=1)
# # #     target_weight = pans * 3750

# # # elif scale_mode == "Mix of tubs and pans":
# # #     tubs = st.number_input("Tubs", min_value=0, step=1)
# # #     pans = st.number_input("Pans", min_value=0, step=1)
# # #     target_weight = tubs * 4275 + pans * 3750

# # # # --- Scale recipe if target weight is defined ---
# # # scaled_recipe = recipe
# # # scale_factor = 1

# # # if target_weight:
# # #     scaled_recipe, scale_factor = scale_recipe_to_target_weight(recipe, target_weight)
# # #     st.success(f"Scaled recipe to {round(target_weight)} g (scale factor: {scale_factor:.2f})")

# # # # --- Ingredient availability input ---
# # # st.subheader("Enter available ingredient amounts (in grams)")
# # # st.write("Leave blank if you have the full amount for an ingredient.")

# # # available_inputs = {}
# # # for ing in scaled_recipe:
# # #     val = st.text_input(f"{ing}", "")
# # #     if val.strip():
# # #         try:
# # #             available_inputs[ing] = float(val)
# # #         except ValueError:
# # #             st.error(f"Invalid input for {ing}")

# # # # --- Final Adjusted Output ---
# # # if st.button("Adjust Recipe Based on Ingredients"):
# # #     adjusted, limit_scale = adjust_recipe_with_constraints(scaled_recipe, available_inputs)
# # #     st.session_state.adjusted_recipe = adjusted
# # #     st.session_state.adjusted_total = round(sum(adjusted.values()))
# # #     st.session_state.processing_mode = False
# # #     st.session_state.current_step = 0

# # #     st.success(f"Adjusted recipe (scale factor: {limit_scale:.2f})")
# # #     st.subheader(f"Final Adjusted Recipe (Total: {st.session_state.adjusted_total} g):")
# # #     for ing, amt in st.session_state.adjusted_recipe.items():
# # #         st.write(f"{ing}: {amt} g")

# # #     st.button("Process Recipe", on_click=lambda: st.session_state.update({
# # #         "processing_mode": True,
# # #         "current_step": 0
# # #     }))

# # # # --- Step-by-step processing screen ---
# # # if st.session_state.get("processing_mode", False):
# # #     adjusted = st.session_state.get("adjusted_recipe", {})
# # #     step = st.session_state.get("current_step", 0)
# # #     ingredients = list(adjusted.items())

# # #     if step < len(ingredients):
# # #         ing, amt = ingredients[step]
# # #         st.header(f"Step {step + 1} of {len(ingredients)}")
# # #         st.subheader(f"🧪 {ing}: {amt} g")

# # #         if st.button("Next"):
# # #             st.session_state.current_step += 1
# # #     else:
# # #         st.success("✅ All ingredients processed!")
# # #         if st.button("Reset"):
# # #             st.session_state.processing_mode = False
# # #             st.session_state.current_step = 0



# #updated 072525












