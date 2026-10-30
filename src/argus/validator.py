from email_validator import validate_email
from email_validator.exceptions import EmailSyntaxError

from argus.models.entity import Entity, EntityType
from argus.models.record import Record


class Validator:
    def __init__(self) -> None:
        pass

    def _is_email(self, email: str) -> bool:
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailSyntaxError:
            return False

    def _infer_record_attribute(self, value: str) -> EntityType:
        if self._is_email(value):
            return EntityType.EMAIL

        return EntityType.UNKNOWN

    def _get_verdict(self, guesses: list[EntityType]) -> EntityType:
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

    def _make_acc_guess(
        self, records: list[Record]
    ) -> tuple[dict[str, list[EntityType]], dict[int, dict[str, EntityType]]]:
        acc_guessed: dict[str, list[EntityType]] = {}
        individual_guess: dict[int, dict[str, EntityType]] = {}

        for index, record in enumerate(records):
            individual_guess[index] = {}
            for field_k, field_v in record.fields.items():
                guessed_type = self._infer_record_attribute(field_v)
                individual_guess[index][field_k] = guessed_type

                if field_k in acc_guessed.keys():
                    acc_guessed[field_k].append(guessed_type)
                else:
                    acc_guessed[field_k] = [guessed_type]

        return (acc_guessed, individual_guess)

    def make_grouped_entities(self, records: list[Record]) -> list[list[Entity]]:
        acc_guessed, individual_guess = self._make_acc_guess(records)
        acc_verdict: dict[str, EntityType] = {}
        for field_name, field_guesses in acc_guessed.items():
            field_verdict = self._get_verdict(field_guesses)
            acc_verdict[field_name] = field_verdict

        entities = []
        for index, record in enumerate(records):
            group = []
            for field_k, field_v in record.fields.items():
                verdict = acc_verdict[field_k]
                guess = individual_guess[index][field_k]

                trusted = verdict == guess
                if guess == EntityType.UNKNOWN:
                    trusted = False

                entity = Entity(
                    type=verdict,
                    trusted=trusted,
                    source=record.source,
                    line=record.line,
                    properties={field_k: field_v},
                )

                group.append(entity)
            entities.append(group)

        return entities
