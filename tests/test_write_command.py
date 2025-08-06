import pytest
from pytest_mock import MockerFixture

from shell.commands.write import Write
from shell.driver import SSDDriver


def test_write_correctly(capsys, mocker: MockerFixture):
    """
    올바르게 인수가 전달되었고 ssd가 동작하므로 [WRITE] Done을 반환해야 함
    """
    # arrange
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.write.return_value = True
    write_command = Write(mocked_ssd)

    # act
    actual = write_command.execute(["3", "0x00000001"])

    # assert
    assert actual == "[Write] Done"


@pytest.mark.parametrize(
    "wrong_argument", [
        ["-1", "0x00000001"],
        ["-1", "0x00000001", "additional"],
    ]
)
def test_write_wrongly_with_minus_lba(mocker: MockerFixture, wrong_argument):
    """
    음수 lba가 전달되면 INVALID COMMAND를 반환해야 함
    """
    # arrange
    mocked_ssd = mocker.Mock(spec=SSDDriver)
    mocked_ssd.write.return_value = True
    write_command = Write(mocked_ssd)

    for wrong_arg in wrong_argument:
        # act
        actual = write_command.execute(wrong_arg)

        # assert
        assert actual == "INVALID COMMAND"


def test_write_command():
    ssd_driver = SSDDriver()
    writeCommand = Write(ssd_driver)

    assert f"[Write] Done" == writeCommand.execute(['42', "0x12345678"])
