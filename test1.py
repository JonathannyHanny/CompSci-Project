import random
import time
from typing import List, Optional



#Element Class
class Element:
    def __init__(self, name: str):
        self._name = name  # Private attribute, gonna stop labeling most of these cause I dont wanna label every single one

    @property
    def name(self) -> str:
        return self._name  # Read-only property, gonna stop labeling most of these cause I dont wanna label every single one

    def __str__(self) -> str:
        return self.name  #String for request representation so element can be fetched without turning into a request object thingy

#Basic element, inherited from element
class BasicElement(Element):
    pass  #Just the element class but renamed cause its cooler and maybe more readable(?) this way

#Compound element, inherited from element
class CompoundElement(Element):
    def __init__(self, name: str, components: List[Element]):
        super().__init__(name)  
        self._components = components  

    @property
    def components(self) -> List[Element]:
        return self._components  #Components property access



#Combine elements 
class Recipe:
    def __init__(self, element1: str, element2: str, result: str):
        self.element1 = element1  # First element in the recipe
        self.element2 = element2  # Second element in the recipe
        self.result = result  # Result

    def can_create(self, elem1: str, elem2: str) -> bool:
        return {self.element1, self.element2} == {elem1, elem2}  # Check if the elements can create the result



# Base class for requests
class Request:
    def __init__(self, required_element: str):
        self._required_element = required_element  #Request element

    @property
    def required_element(self) -> str:
        return self._required_element  #Read request element
    
    def calculate_points(self) -> int:
        return 10  # Default is 10 points

    def __str__(self) -> str:
        return f"Create: {self.required_element}"  #String request representation so instructions for request can be fetched without turning into a request object thingy

#More complex request, inherited
class ComplexRequest(Request):
    def __init__(self, required_element: str, num_elements: int):
        super().__init__(required_element)  #Steals from the base class cause it's evil
        self._num_elements = num_elements  # Number of complex components

    def calculate_points(self) -> int:
        return 10 + (self._num_elements * 5)  #Polymorphism to calculate points for more complex requests


#Handles alchemy mechanics
class Alchemy:
    def __init__(self):
        self._base_elements = ["Water", "Fire", "Earth", "Air", "Metal", "Wood"]  # List of basic elements
        self._elements = self._create_elements()  # Create basic elements
        self._recipes = self._create_recipes()  # Create recipes for combining elements
        self._discovered_elements = {e.name for e in self._elements}  # Set of discovered elements

    def _create_elements(self) -> List[BasicElement]:
        return [BasicElement(name) for name in self._base_elements]  # Create Basic elements

    def _create_recipes(self) -> List[Recipe]:
        return [
            Recipe("Water", "Fire", "Steam"),
            Recipe("Water", "Earth", "Mud"),
            Recipe("Fire", "Air", "Smoke"),
            Recipe("Earth", "Air", "Dust"),
            Recipe("Wood", "Fire", "Charcoal"),
            Recipe("Metal", "Fire", "Liquid Metal"),
            Recipe("Steam", "Air", "Cloud"),
            Recipe("Mud", "Earth", "Clay"),
        ]  # Define the recipes for the game

    def combine(self, elem1: Element, elem2: Element) -> Optional[CompoundElement]:
        for recipe in self._recipes:
            if recipe.can_create(elem1.name, elem2.name):  # Checks if it can be created
                return CompoundElement(recipe.result, [elem1, elem2])  # Return result if successful
        return None  # Return None if no combination found

    @property
    def discovered_elements(self) -> List[str]:
        return self._discovered_elements  # Property to access discovered elements

    def add_discovered_element(self, element: str) -> None:
        self._discovered_elements.add(element)  # Add a newly discovered element

    def get_components_from_recipe(self, result: str) -> Optional[List[str]]:
        for recipe in self._recipes:
            if recipe.result == result:
                return [recipe.element1, recipe.element2]  # Return the components of the recipe
        return None  # Return None if no recipe found for the result




#Main game loop logic
class AlchemyGame:
    def __init__(self, time_limit: int):
        self._alchemy = Alchemy()  #Alchemy class
        self._request = self._generate_request()  # Generate 1st request
        self._score = 0  # Start score
        self._start_time = time.time()  # Records start time
        self._time_limit = time_limit  # Sets time limit
        self._time_increase = 15  # Amount of time to add for each completed request


    def _generate_request(self) -> Optional[Request]:
        undiscovered_elements = [
            recipe.result for recipe in self._alchemy._create_recipes()  # Sets uncreated recipes as undiscovered elements
            if recipe.result not in self._alchemy.discovered_elements  # If recipe not already discovered
        ]
        
        if not undiscovered_elements:
            return None  # Return None if no undiscovered elements
        
        required_element = random.choice(undiscovered_elements)  # Randomly select a required element
        if any(recipe.result == required_element for recipe in self._alchemy._create_recipes()): # Check if the request is in recipes
        
            components = self._alchemy.get_components_from_recipe(required_element) # Get components of the required element from recipes
            
            if components:
                num_compound_elements = sum(
                    1 for component in components if component not in self._alchemy._base_elements #Checks if component is not basic thus compound
                )

                if num_compound_elements > 0:
                    return ComplexRequest(required_element, num_compound_elements)  # Generate a complex request based on the count
                
            return Request(required_element)  # Fallback to a standard request


    def play(self) -> None:
        print("\n𝐀𝐋𝐂𝐇𝐄𝐌𝐘 𝐑𝐔𝐒𝐇\nStarting time limit is 60 Seconds.") # Title
        while True:
            elapsed_time = time.time() - self._start_time  # Calculate time spent
            if elapsed_time > self._time_limit: # Time up
                print("\nTime's up! Your final score is:", self._score)  
                break
            
            print(f"\nCurrent Score: {self._score}")
            if self._request:
                print("Current request to fulfill:") #blah blah blah blah blah text stuff
                print(self._request) # Request

            print("\nAvailable elements: " + ", ".join(self._alchemy.discovered_elements)) # Shows available elements
            print("Type 'exit' to quit the game.") 
            elem1 = input("Enter the first element: ") #blah blah blah blah blah text stuff
            if elem1.lower() == 'exit':
                break

            elem2 = input("Enter the second element: ") #blah blah blah blah blah text stuff
            if elem2.lower() == 'exit':
                break

            elem1_obj = self._get_element(elem1)  # Get the first element object
            elem2_obj = self._get_element(elem2)  # Get the second element object

            if elem1_obj and elem2_obj:
                result = self._alchemy.combine(elem1_obj, elem2_obj)  # Combine elements
                if result:
                    self._alchemy.add_discovered_element(result.name)  # Add the created element to discovered
                    print(f"You created: {result}\n")

                    # Count compound elements in the created compound

                    self._check_request(result)  # Check if the request is fulfilled
                    if self._check_win_condition():  # Win condition
                        print("Congratulations! You've discovered all elements!")  
                        break
                else:
                    print("No combination found for these elements.") # Nope
            else:
                print("One or both elements are not valid.") # Nope


    def _check_request(self, created_element: CompoundElement) -> None: # Checks if request is completed
        if created_element.name == self._request.required_element:
            print(f"Request fulfilled: {self._request}")
            # Get points from the request's calculate_points method
            print(self._request)
            points = self._request.calculate_points()  # Use polymorphism to get points
            self._score += points  # Update the score
            print(f"You earned {points} points! Total Score: {self._score}")

            # Edit the time limit
            self._time_limit += self._time_increase
            print(f"New time limit: {self._time_limit} seconds")

            self._request = self._generate_request()  # Generate a new request
        
        
    def _check_win_condition(self) -> bool: # Checks win condition
        total_elements = len(self._alchemy._create_elements()) + len(self._alchemy._create_recipes())
        return len(self._alchemy.discovered_elements) == total_elements  # Check if all elements are discovered


    def _get_element(self, name: str) -> Optional[Element]:  # Gets element
        # Check against base elements
        for element in self._alchemy._create_elements():
            if element.name.lower() == name.lower():
                return element  # Return the element if found

        # Check against discovered elements, lowercased
        if name.lower() in (e.lower() for e in self._alchemy.discovered_elements):
            return Element(name)  # Return a new element if discovered

        return None  # Return None if not found

#Start game
if __name__ == "__main__":
    time_limit = 60  # Set initial time limit
    game = AlchemyGame(time_limit)  # Create instance of game
    game.play()  # Start