import unittest

# ======= Input Validation Helpers =======
VALID_DIETARY_RESTRICTIONS = {"vegan", "gluten-free", "vegetarian"}
VALID_ALLERGENS = {"dairy", "soy", "peanut"}
VALID_SORT_CRITERIA = {"calories", "name"}

def canonicalize(value):
    return value.strip().lower()

def valid_input(value, valid_set):
    return canonicalize(value) in valid_set

def log_rejection(value, context):
    print(f"[REJECTED] '{value}' is invalid in context: {context}")

# ======= Filters =======

def apply_dietary_restrictions(items, restrictions):
    clean_restrictions = [canonicalize(r) for r in restrictions if valid_input(r, VALID_DIETARY_RESTRICTIONS)]
    return [
        item for item in items
        if all(r in [canonicalize(d) for d in item["dietary"]] for r in clean_restrictions)
    ]

def filter_by_allergy_info(items, allergens):
    clean_allergens = [canonicalize(a) for a in allergens if valid_input(a, VALID_ALLERGENS)]
    return [
        item for item in items
        if all(a not in [canonicalize(ing) for ing in item.get("allergy_info", [])] for a in clean_allergens)
    ]

def filter_by_calorie_range(items, min_cal, max_cal):
    if not isinstance(min_cal, (int, float)) or not isinstance(max_cal, (int, float)):
        raise ValueError("Calorie range must be numeric")
    return [item for item in items if min_cal <= item["calories"] <= max_cal]

def sort_by_preference(items, criteria):
    if not valid_input(criteria, VALID_SORT_CRITERIA):
        log_rejection(criteria, "sort criteria")
        return items
    key_func = (lambda x: x["calories"]) if canonicalize(criteria) == "calories" else (lambda x: x["item"].lower())
    return sorted(items, key=key_func)

# ======= Unit Tests =======

class TestFoodFilters(unittest.TestCase):

    def setUp(self):
        self.food_list = [
            {"item": "Tofu Salad", "dietary": ["Vegan"], "allergy_info": ["Soy"], "calories": 350},
            {"item": "Chicken Wrap", "dietary": ["Gluten-Free"], "allergy_info": ["Dairy"], "calories": 500},
            {"item": "Fruit Bowl", "dietary": ["Vegan", "Gluten-Free"], "allergy_info": [], "calories": 150}
        ]

    def test_apply_dietary_restrictions(self):
        vegan_items = apply_dietary_restrictions(self.food_list, ["Vegan"])
        self.assertEqual(len(vegan_items), 2)
        self.assertTrue(any(item["item"] == "Tofu Salad" for item in vegan_items))
        self.assertTrue(any(item["item"] == "Fruit Bowl" for item in vegan_items))

    def test_filter_by_allergy_info(self):
        safe_items = filter_by_allergy_info(self.food_list, ["Dairy"])
        self.assertEqual(len(safe_items), 2)
        self.assertFalse(any(item["item"] == "Chicken Wrap" for item in safe_items))

    def test_filter_by_calorie_range(self):
        low_cal_items = filter_by_calorie_range(self.food_list, 100, 400)
        self.assertEqual(len(low_cal_items), 2)
        self.assertTrue(any(item["item"] == "Fruit Bowl" for item in low_cal_items))
        self.assertTrue(any(item["item"] == "Tofu Salad" for item in low_cal_items))

    def test_sort_by_calories(self):
        sorted_items = sort_by_preference(self.food_list, "calories")
        self.assertEqual([item["item"] for item in sorted_items],
                         ["Fruit Bowl", "Tofu Salad", "Chicken Wrap"])

    def test_sort_by_name(self):
        sorted_items = sort_by_preference(self.food_list, "name")
        self.assertEqual([item["item"] for item in sorted_items],
                         ["Chicken Wrap", "Fruit Bowl", "Tofu Salad"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
