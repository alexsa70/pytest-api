from __future__ import annotations

import allure

from schema.operations import AuthenticateRequestSchema
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("AUTH_ASSERTIONS")


@allure.step("Check authenticate payload")
def assert_auth_payload(
    actual: AuthenticateRequestSchema,
    expected: AuthenticateRequestSchema,
) -> None:
    logger.info("Check authenticate payload")

    assert_equal(actual.email, expected.email, "email")
    assert_equal(actual.password, expected.password, "password")
