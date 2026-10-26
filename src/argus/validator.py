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
        print(
            "first: ",
            first,
            "\ttotal: ",
            len(guesses),
            "\ttotal n_u: ",
            total_not_unknown,
            "\tpercent: ",
            percent,
            "%",
        )

        if len(sorted_props) > 1 and first_int == sorted_props[1][1]:
            return EntityType.UNKNOWN
        elif percent >= 75:
            return first[0]

        return EntityType.UNKNOWN

    def make_grouped_entities(self, records: list[Record]) -> list[list[Entity]]:
        entities: list[list[Entity]] = []
        records_attributes: dict[str, list[EntityType]] = {}
        for record in records:
            # group = []

            for key, value in record.fields.items():
                guess = self.infer_record_attribute(value)

                if key in records_attributes.keys():
                    records_attributes[key].append(guess)
                else:
                    records_attributes[key] = [guess]

        for key, type_ls in records_attributes.items():
            verdict = self.get_verdict(type_ls)
            print(key, " >> ", verdict)

        #             for key, value in record.fields.items():
        #                 type = EntityType.UNKNOWN
        #                 if "mail" in key and self.is_email(value):
        #                     type = EntityType.EMAIL
        #                     print(key, value)
        #
        #                 entity = Entity(
        #                     type=type,
        #                     source=record.source,
        #                     line=record.line,
        #                     properties=value,
        #                 )
        #
        #                 group.append(entity)
        #             entities.append(group)

        return entities
