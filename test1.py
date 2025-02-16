class Element:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def combine(self, other):
        raise NotImplementedError("This method should be overridden by subclasses.")

class BasicElement(Element):
    def combine(self, other):
        return None  
    
class CompoundElement(Element):
    def __init__(self, name, components):
        super().__init__(name)
        self.components = components  

    def combine(self, other):
        return None  

class Recipe:
    def __init__(self, element1, element2, result):
        self.element1 = element1
        self.element2 = element2
        self.result = result

    def can_create(self, elem1, elem2):
        return (self.element1 == elem1 and self.element2 == elem2) or \
               (self.element1 == elem2 and self.element2 == elem1)

class Alchemy:
    def __init__(self):
        self.elements = self.create_elements()
        self.recipes = self.create_recipes()
        self.discovered_elements = set()

    def create_elements(self):
        return [
            BasicElement("Water"),
            BasicElement("Fire"),
            BasicElement("Earth"),
            BasicElement("Air"),
            BasicElement("Metal"),
            BasicElement("Wood")
        ]

    def create_recipes(self):
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

    def combine(self, elem1, elem2):
        for recipe in self.recipes:
            if recipe.can_create(elem1.name, elem2.name):
                return CompoundElement(recipe.result, [elem1, elem2])
        return None

class AlchemyGame:
    def __init__(self):
        self.alchemy = Alchemy()
        self.alchemy.discovered_elements = {str(e) for e in self.alchemy.elements}

    def play(self):
        print("Welcome to the Alchemy Game!")
        while True:
            print("\nAvailable elements: " + ", ".join([str(e) for e in self.alchemy.discovered_elements]))
            print("Type 'exit' to quit the game.")
            elem1 = input("Enter the first element: ")
            if elem1.lower() == 'exit':
                break

            elem2 = input("Enter the second element: ")
            if elem2.lower() == 'exit':
                break

            elem1_obj = self.get_element(elem1)
            elem2_obj = self.get_element(elem2)

            if elem1_obj and elem2_obj:
                result = self.alchemy.combine(elem1_obj, elem2_obj)
                if result:
                    self.alchemy.discovered_elements.add(result.name)
                    print(f"You created: {result} from {elem1} and {elem2}")
                else:
                    print("No combination found for these elements.")
            else:
                print("One or both elements are not valid.")

    def get_element(self, name):
        for element in self.alchemy.elements:
            if element.name.lower() == name.lower():
                return element
        if name in self.alchemy.discovered_elements:
            return Element(name)
        return None

if __name__ == "__main__":
    game = AlchemyGame()
    game.play()