import pytest


@pytest.fixture(scope='function')
def message_email() -> tuple[str, ...]:
    return (
        ('value is not a valid email address: '
         'The email address is not valid. '
         'It must have exactly one @-sign.'),
        ('value is not a valid email address: '
         'The part after the @-sign is not valid. '
         'It should have a period.'),
        ('value is not a valid email address: '
         'There must be something before the @-sign.'),
        ('Value should have at least 6 items after validation, not 5'),
    )
