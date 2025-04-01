import logging
import math
from typing import List

from boxing.models.boxers_model import Boxer, update_boxer_stats
from boxing.utils.logger import configure_logger
from boxing.utils.api_utils import get_random


logger = logging.getLogger(__name__)
configure_logger(logger)


class RingModel:
    """A class representing the the boxing match between two boxers in a ring.

    Attributes:
        ring (List[Boxer]): The list of boxers in the ring, up to a max of 2.
    """
    def __init__(self):
        """Initializes RingModel with an empty ring.
        """
        self.ring: List[Boxer] = []

    def fight(self) -> str:
        """Starts a fight between the two boxers in the ring.

        Returns:
            str: The name of the boxer who won the right.

        Raises:
            ValueError: If there are not enough fighters in the ring.
        """
        logger.info("Received request to start a fight in the ring.")
        if len(self.ring) < 2:
            logger.warning("There are not enough fighters in the ring.")
            raise ValueError("There must be two boxers to start a fight.")

        boxer_1, boxer_2 = self.get_boxers()

        skill_1 = self.get_fighting_skill(boxer_1)
        skill_2 = self.get_fighting_skill(boxer_2)

        # Compute the absolute skill difference
        # And normalize using a logistic function for better probability scaling
        delta = abs(skill_1 - skill_2)
        normalized_delta = 1 / (1 + math.e ** (-delta))

        random_number = get_random()

        if random_number < normalized_delta:
            winner = boxer_1
            loser = boxer_2
        else:
            winner = boxer_2
            loser = boxer_1

        update_boxer_stats(winner.id, 'win')
        update_boxer_stats(loser.id, 'loss')

        self.clear_ring()
        logger.info("Fight ended with {winner.name} as victor.")
        return winner.name

    def clear_ring(self):
        """Clears the ring attribute of all boxers.
        """
        logger.info("Received request to clear out ring.")
        if not self.ring:
            return
        self.ring.clear()
        logger.info("Successfully cleared out the ring.")

    def enter_ring(self, boxer: Boxer):
        """Adds a boxer to the ring if there is space.

        Args:
            boxer (Boxer): The boxer to be added to the ring.

        Raises:
            TypeError: If the argument boxer is not of type Boxer.
            ValueError: If the ring attribute already has 2 boxers.
        """
        logger.info(f"Received request to add a boxer to the ring: {boxer.name}")
        
        if not isinstance(boxer, Boxer):
            logger.warning("Type of boxer argument is invalid.")
            raise TypeError(f"Invalid type: Expected 'Boxer', got '{type(boxer).__name__}'")

        if len(self.ring) >= 2:
            logger.warning("There are too many boxers in the ring at the moment.")
            raise ValueError("Ring is full, cannot add more boxers.")

        self.ring.append(boxer)
        logger.info(f"Successfully added boxer, {boxer.name}, to the ring.")

    def get_boxers(self) -> List[Boxer]:
        """Returns the list of boxers in the ring.

        Returns:
            List[Boxer]: The list of boxers in the ring.
        """
        if not self.ring:
            pass
        else:
            pass

        return self.ring

    def get_fighting_skill(self, boxer: Boxer) -> float:
        """Calculates the fighting skill of a boxer based on their attributes.

        Args:
            boxer (Boxer): The boxer to calculate skill for.

        Returns:
            float: The skill level number.
        """
        # Arbitrary calculations
        age_modifier = -1 if boxer.age < 25 else (-2 if boxer.age > 35 else 0)
        skill = (boxer.weight * len(boxer.name)) + (boxer.reach / 10) + age_modifier

        return skill
