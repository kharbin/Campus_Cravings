import pygame
from ..button import Button
from ..constants import Constants

class RecommendationInterface:
    def __init__(self, screen, font, meal_recommender, user_preference_manager, app):
        self.screen = screen
        self.font = font
        self.meal_recommender = meal_recommender
        self.user_preference_manager = user_preference_manager
        self.app = app
        self.state = app.state
        self.window_width = Constants.WIDTH
        self.window_height = Constants.HEIGHT
        
        # Input fields
        self.allergy_input = ""
        self.allergy_rect = pygame.Rect(self.window_width // 2 - 100, 200, 200, 40)
        self.allergy_active = False
        
        # Buttons
        self.recommend_button = Button(
            self.window_width // 2 - 100, 300, 200, 50, "Get Recommendation",
            self._handle_recommendation, self.font
        )
        self.back_button = Button(
            self.window_width // 2 - 100, 400, 200, 50, "Back",
            lambda: self.state.update({"screen": "customer"}), self.font
        )

    def handle_events(self):
        """Handle user input for the recommendation screen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.allergy_rect.collidepoint(event.pos):
                    self.allergy_active = True
                else:
                    self.allergy_active = False
                self.recommend_button.check_click(event.pos)
                self.back_button.check_click(event.pos)
            if event.type == pygame.KEYDOWN and self.allergy_active:
                if event.key == pygame.K_BACKSPACE:
                    self.allergy_input = self.allergy_input[:-1]
                elif event.unicode.isprintable() and len(self.allergy_input) < 20:
                    self.allergy_input += event.unicode

    def render(self):
        """Render the recommendation screen."""
        self.screen.fill(Constants.CREAM)
        title = self.font.render("Meal Recommendation", True, Constants.CRIMSON)
        self.screen.blit(title, (self.window_width // 2 - title.get_width() // 2, 100))
        
        # Allergy input
        pygame.draw.rect(self.screen, Constants.CREAM, self.allergy_rect)
        pygame.draw.rect(self.screen, Constants.CRIMSON, self.allergy_rect, 2 if not self.allergy_active else 4)
        allergy_text = self.font.render(self.allergy_input or "Enter Allergies", True, Constants.CRIMSON)
        self.screen.blit(allergy_text, (self.allergy_rect.x + 5, self.allergy_rect.y + 5))
        
        # Recommendation result
        if "recommendation" in self.state:
            result_text = self.font.render(self.state["recommendation"], True, Constants.CRIMSON)
            self.screen.blit(result_text, (self.window_width // 2 - result_text.get_width() // 2, 250))
        
        self.recommend_button.draw(self.screen)
        self.back_button.draw(self.screen)
        pygame.display.flip()

    def _handle_recommendation(self):
        """Process the recommendation request."""
        preferences = {"allergies": [self.allergy_input]} if self.allergy_input else {}
        self.user_preference_manager.update_preferences(preferences)
        result = self.meal_recommender.recommend_meal(self.user_preference_manager.get_preferences(), include_location=True)
        self.state["recommendation"] = f"Recommended: {result[0]} at {result[1]}" if isinstance(result, tuple) else f"Recommended: {result}"
