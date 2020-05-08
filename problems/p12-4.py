# In The Name of God
# =======================================
# [] File Name : p12-4.py
#
# [] Creation Date : 09-05-2020
#
# [] Created By : Parham Alvani <parham.alvani@gmail.com>
# =======================================
from __future__ import annotations
import typing
import dataclasses


@dataclasses.dataclass(frozen=True, repr=True)
class Scenario:
    probability: float = dataclasses.field(default=1)
    months: typing.List[int] = dataclasses.field(default_factory=list)

    def append(self, level: int, probability: float) -> Scenario:
        months = self.months.copy()
        months.append(level)
        return Scenario(probability=self.probability * probability, months=months)

    def __len__(self):
        return len(self.months)


def generate_scenarios(
    months: typing.List[typing.List[typing.Tuple[int, float]]]
) -> typing.List[Scenario]:
    scenarios: typing.List[Scenario] = []

    def generator(scenario: Scenario):
        if len(scenario) == len(months):
            scenarios.append(scenario)
            return

        index = len(scenario)

        for (level, propability) in months[index]:
            generator(scenario.append(level, propability))

    generator(Scenario())

    return scenarios


months = [
    [(100, 0.5), (50, 0.25), (250, 0.25)],
    [(100, 0.5), (50, 0.25), (250, 0.25)],
    [(150, 0.5), (50, 0.25), (350, 0.25)],
    [(150, 0.5), (50, 0.25), (350, 0.25)],
]

print(generate_scenarios(months))
