from enum import Enum, auto
import random


# ** *************************************************************************
class DirtDistribution(Enum):
    UNKNOWN = "unknown"
    UNIFORM = "uniform"
    LEFT_SKEW = "left_skew"
    RIGHT_SKEW = "right_skew"
    RANDOM = "random"
    CENTER = "center"
    BIMODAL = "bimodal"
    STEP = "step"
    ALTERNATING = "alternating"
    ZERO = "zero"

    # Returns list of all possible dirt distribution names as strings ie 'uniform' 'skewed' (not types)
    @classmethod
    def all_values(cls):
        labels = [d.value for d in cls]
        return sorted(labels, key=lambda x: (x == "unknown", x))

    # Returns list of all possible dirt distribution names as strings ie 'uniform' 'skewed' (not types)
    # Leaves out the UNKNOWN class since it's not used in real distributions
    @classmethod
    def real_values(cls):
        return [d for d in cls if d != cls.UNKNOWN]

    # Converts a single DirtDistribution to a string representation
    def __str__(self):
        return f"{self.value}"

    # Factory method returns a DirtDistribution based on a string like 'uniform'
    @classmethod
    def from_string(cls, value: str):
        for d in cls:
            if d.value == value:
                return d
        raise ValueError(f"Invalid DirtDistribution: {value}")

    # Factory method that returns a random DirtDistribution (but not UNKNOWN)
    @classmethod
    def random_real(cls):
        return random.choice([d for d in cls if d != cls.UNKNOWN])

    # API to return a list of floats for dirt falling likelihood in the rooms
    def generate_distribution_odds(self, room_count):
        if self == DirtDistribution.UNIFORM:
            return self._generate_uniform(room_count)

        elif self == DirtDistribution.RANDOM:
            return self._generate_random(room_count)

        elif self == DirtDistribution.LEFT_SKEW:
            return self._generate_left_skew(room_count)
        
        elif self == DirtDistribution.RIGHT_SKEW:
            return self._generate_right_skew(room_count)
        
        elif self == DirtDistribution.CENTER:
            return self._generate_center(room_count)

        elif self == DirtDistribution.BIMODAL:
            return self._generate_bimodal(room_count)

        elif self == DirtDistribution.STEP:
            return self._generate_step(room_count)

        elif self == DirtDistribution.ALTERNATING:
            return self._generate_alternating(room_count)

        elif self == DirtDistribution.ZERO:
            return self._generate_zero(room_count)

        else:
            raise ValueError("Unknown distribution - cannot have a set of odds")

    def _generate_uniform(self, room_count) -> list:
        uniform_odds = 0.15
        return [uniform_odds] * room_count

    def _generate_random(self, room_count, p_max=0.20, p_min=0.05) -> list:
        return [round(random.uniform(p_min, p_max), 3) for _ in range(room_count)]

    def _generate_left_skew(self, room_count, p_max=0.25, p_min=0.05) -> list:
        """Produce a geometrically decreasing sequence of dirt probabilities across rooms,
        from p_max (first room) down to p_min (last room)."""
        if room_count == 1:
            return [p_max]

        odds = []
        for i in range(room_count):
            t = i / (room_count - 1)
            p = p_max * (p_min / p_max) ** t
            p_rounded = round(p, 3)
            odds.append(p_rounded)

        return odds
    
    def _generate_right_skew(self, room_count, p_max=0.25, p_min=0.05) -> list:
        return list(reversed(self._generate_left_skew(room_count)))
    
    def _generate_center(self, room_count, p_min=0.05, p_max=0.25):
        mid = (room_count - 1) / 2
        odds = []
        for i in range(room_count):
            dist = abs(i - mid) / mid
            p = p_max - (p_max - p_min) * dist
            odds.append(round(p, 3))
        return odds
    
    def _generate_bimodal(self, room_count, p_min=0.05, p_max=0.25):
        mid = (room_count - 1) / 2
        odds = []
        for i in range(room_count):
            dist = abs(i - mid) / mid
            p = p_min + (p_max - p_min) * dist
            odds.append(round(p, 3))
        return odds
    
    def _generate_step(self, room_count, p_min=0.05, p_max=0.25):
        split_index = room_count // 2
        return [p_min] * split_index + [p_max] * (room_count - split_index)
    
    def _generate_alternating(self, room_count, p_min=0.05, p_max=0.25):
        return [
            round(p_max if i % 2 == 0 else p_min, 3)
            for i in range(room_count)
        ]

    def _generate_zero(self, room_count) -> list:
        return [0.0] * room_count
