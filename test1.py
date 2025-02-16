import random
from typing import List, Optional

class Element:
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self.name

class BasicElement(Element):
    pass

class CompoundElement(Element):
    def __init__(self, name: str, components: List[Element]):
        super().__init__(name)
        self._components = components

    @property
    def components(self) -> List[Element]:
        return self._components

class Recipe:
    def __init__(self, element1: str, element2: str, result: str):
        self.element1 = element1
        self.element2 = element2
        self.result = result

    def can_create(self, elem1: str, elem2: str) -> bool:
        return {self.element1, self.element2} == {elem1, elem2}

class Request:
    def __init__(self, required_element: str):
        self._required_element = required_element

    @property
    def required_element(self) -> str:
        return self._required_element

    def __str__(self) -> str:
        return f"Create: {self.required_element}"

    def calculate_points(self) -> int:
        return 10  # Default points for a standard request

class ComplexRequest(Request):
    def __init__(self, required_element: str, num_elements: int):
        super().__init__(required_element)
        self._num_elements = num_elements

    def calculate_points(self) -> int:
        return self._num_elements * 5  # Points based on the number of elements

class Alchemy:
    def __init__(self):
        self._elements = self._create_elements()
        self._recipes = self._create_recipes()
        self._discovered_elements = {e.name for e in self._elements}

    def _create_elements(self) -> List[BasicElement]:
        return [BasicElement(name) for name in ["Water", "Fire", "Earth", "Air", "Metal", "Wood"]]

    def _create_recipes(self) -> List[Recipe]:
        return [
            Recipe("Water", "Fire", "Steam"),
            Recipe("Water", "Earth", "Mud"),
            Recipe("Fire", "Air", "Smoke"),
            Recipe("Earth", "Air", "Dust"),
            Recipe("Wood", "Fire", "Charcoal"),
            Recipe("Metal", "Fire", "Liquid Metal"),
            Recipe("Water", "Air", "Cloud"),
            Recipe("Steam", "Air", "Cloud"),
            Recipe("Mud", "Earth", "Clay"),
        ]

    def combine(self, elem1: Element, elem2: Element) -> Optional[CompoundElement]:
        for recipe in self._recipes:
            if recipe.can_create(elem1.name, elem2.name):
                return CompoundElement(recipe.result, [elem1, elem2])
        return None

    @property
    def discovered_elements(self) -> List[str]:
        return self._discovered_elements

    def add_discovered_element(self, element: str) -> None:
        self._discovered_elements.add(element)

class AlchemyGame:
    def __init__(self):
        self._alchemy = Alchemy()
        self._request = self._generate_request()
        self._score = 0

    def _generate_request(self) -> Optional[Request]:
        undiscovered_elements = [
            recipe.result for recipe in self._alchemy._create_recipes() 
            if recipe.result not in self._alchemy.discovered_elements
        ]
        if not undiscovered_elements:
            return None
        
        required_element = random.choice(undiscovered_elements)
        if any(recipe.result == required_element for recipe in self._alchemy._create_recipes()):
            return Request(required_element)  # Standard request
        
        num_elements = random.randint(2, 3)  # For complex request
        return ComplexRequest(required_element, num_elements)

    def play(self) -> None:
        print("Welcome to the Alchemy Game!")
        while True:
            print(f"\nCurrent Score: {self._score}")
            if self._request:
                print("Current request to fulfill:")
                print(self._request)

            print("\nAvailable elements: " + ", ".join(self._alchemy.discovered_elements))
            print("Type 'exit' to quit the game.")
            elem1 = input("Enter the first element: ")
            if elem1.lower() == 'exit':
                break

            elem2 = input("Enter the second element: ")
            if elem2.lower() == 'exit':
                break

            elem1_obj = self._get_element(elem1)
            elem2_obj = self._get_element(elem2)

            if elem1_obj and elem2_obj:
                result = self._alchemy.combine(elem1_obj, elem2_obj)
                if result:
                    self._alchemy.add_discovered_element(result.name)
                    print(f"You created: {result}")

                    # Count basic elements in the created compound
                    basic_count = self._alchemy.count_basic_elements(result)
                    print(f"Total basic elements in {result.name}: {basic_count}")

                    self._check_request(result)
                    if self._check_win_condition():
                        print("Congratulations! You've discovered all elements!")
                        break
                else:
                    print("No combination found for these elements.")
            else:
                print("One or both elements are not valid.")

    def _check_request(self, created_element: CompoundElement) -> None:
        if created_element.name == self._request.required_element:
            points = self._request.calculate_points()
            print(f"Request fulfilled: {self._request}")
            self._score += points
            print(f"You earned {points} points! Total Score: {self._score}")
            self._request = self._generate_request()  # Generate a new request

    def _check_win_condition(self) -> bool:
        total_elements = len(self._alchemy._create_elements()) + len(self._alchemy._create_recipes())
        return len(self._alchemy.discovered_elements) == total_elements

    def _get_element(self, name: str) -> Optional[Element]:
        for element in self._alchemy._create_elements():
            if element.name.lower() == name.lower():
                return element
        return Element(name) if name in self._alchemy.discovered_elements else None

if __name__ == "__main__":
    game = AlchemyGame()
    game.play()