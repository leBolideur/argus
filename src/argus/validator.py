from email_validator import validate_email
from email_validator.exceptions import EmailSyntaxError

from argus.models.entity import Entity, EntityType
from argus.models.record import Record


class Validator:
    def __init__(self) -> None:
        pass

    def is_email(self, email: str) -> bool:
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailSyntaxError:
            return False

    def infer_record_attribute(self, value: str) -> EntityType:
        if self.is_email(value):
            return EntityType.EMAIL

        return EntityType.UNKNOWN

    def get_verdict(self, guesses: list[EntityType]) -> EntityType:
        proposals: dict[EntityType, int] = {}
        for guess in guesses:
            if guess in proposals.keys():
                proposals[guess] += 1
            else:
                proposals[guess] = 1

        sorted_props = sorted(proposals.items(), key=lambda item: item[1], reverse=True)
        first = sorted_props[0]
        first_int = first[1]
        total_not_unknown = len(
            [guess for guess in guesses if guess is not EntityType.UNKNOWN]
        )
        if total_not_unknown == 0:
            return EntityType.UNKNOWN

        percent = first_int * 100 / total_not_unknown

        if len(sorted_props) > 1 and first_int == sorted_props[1][1]:
            return EntityType.UNKNOWN
        elif percent >= 75:
            return first[0]

        return EntityType.UNKNOWN

    def make_grouped_entities(self, records: list[Record]) -> list[list[Entity]]:
        entities: list[list[Entity]] = []
        records_guesses: dict[str, list[EntityType]] = {}
        for record in records:
            group = []

            for key, value in record.fields.items():
                guess = self.infer_record_attribute(value)

                if key in records_guesses.keys():
                    records_guesses[key].append(guess)
                else:
                    records_guesses[key] = [guess]

            for key, type_ls in records_guesses.items():
                guess = self.infer_record_attribute(record.fields[key])
                verdict = self.get_verdict(type_ls)

                entity = Entity(
                    type=verdict,
                    trusted=guess == verdict,
                    source=record.source,
                    line=record.line,
                    properties={key: record.fields[key]},
                )

                group.append(entity)
            entities.append(group)

        return entities
