import pytest
from pytest_mock import MockerFixture

from shell.command_constants import INVALID_COMMAND
from shell.commands.flush import Flush
from shell.driver import SSDDriver

FLUSH_DONE = "[Flush] Done"


def test_flush_correctly(capsys, mocker: MockerFixture):
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.flush.return_value = True
    flush_command = Flush(mocked_ssd)
    actual = flush_command.execute([])
    assert actual == FLUSH_DONE


@pytest.mark.parametrize(
    "wrong_argument", [
        ["1", "11"],
        ["1"],
    ]
)
def test_flush_invalid_result_with_wrong_argument(mocker: MockerFixture, wrong_argument):
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.erase.return_value = True
    flush_command = Flush(mocked_ssd)
    actual = flush_command.execute(wrong_argument)
    assert actual == INVALID_COMMAND
