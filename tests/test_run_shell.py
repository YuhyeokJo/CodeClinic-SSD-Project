import sys
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from shell.commands.fullread import FullRead
from shell.commands.fullwrite import FullWrite
from shell.commands.read import Read
from shell.commands.write import Write
from shell.commands.help import Help
from shell.commands.exit import Exit
from shell.driver import SSDDriver
from shell.run_shell import InteractiveShell, BatchShell, NotExistingTestScriptError, NotExistingFileError, main


def test_main_with_no_arg(capsys, mocker):
    sys.argv = [f"{(Path(__file__).parent.parent / 'shell.py').resolve()}"]
    input_patch = mocker.patch("shell.run_shell.input")
    input_patch.side_effect = [
        "help write",
        "write 3 0x00000001",
        "read 3",
        "fullwrite 0x00000001",
        "fullread",
        "exit"
    ]

    main()

    for output in capsys.readouterr().out.split("\n"):
        if output == "INVALID COMMAND":
            assert False


def test_main_with_shell_script_file(capsys):
    sys.argv = [f"{(Path(__file__).parent.parent / 'shell.py').resolve()}",
                f"{(Path(__file__).parent / 'shell_scripts.txt').resolve()}"]

    main()

    assert capsys.readouterr().out.strip("\n").split("\n") == [
        "1_FullWriteAndReadCompare  ___  Run...Pass",
        "2_PartialLBAWrite  ___  Run...Pass",
        "3_WriteReadAging  ___  Run...Pass",
    ]


"""
Tests using moced ssd driver
"""


@pytest.fixture
def mocked_driver_shell_input(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)
    test_shell = InteractiveShell(driver)
    input_patch = mocker.patch("shell.run_shell.input")

    return driver, test_shell, input_patch


def test_if_builtin_commands_are_registered(mocker: MockerFixture):
    driver = mocker.Mock(spec=SSDDriver)

    test_shell = InteractiveShell(driver)

    assert isinstance(test_shell._commands["write"], Write)
    assert isinstance(test_shell._commands["read"], Read)
    assert isinstance(test_shell._commands["fullwrite"], FullWrite)
    assert isinstance(test_shell._commands["fullread"], FullRead)
    assert isinstance(test_shell._commands["exit"], Exit)
    assert isinstance(test_shell._commands["help"], Help)


def test_not_exist_command_and_exit(capsys, mocked_driver_shell_input):
    # Arrange
    driver, test_shell, input_patch = mocked_driver_shell_input
    input_patch.side_effect = ["not_exist", "exit"]

    # Act
    test_shell.run()

    # Assert
    assert capsys.readouterr().out.strip("\n").split("\n") == [
        "INVALID COMMAND", "[Exit]"
    ]


def test_read_command_input_with_correct_command(capsys, mocked_driver_shell_input):
    # Arrange
    driver, test_shell, input_patch = mocked_driver_shell_input
    driver.read.return_value = "0x00000001"
    input_patch.side_effect = ["read 3", "exit"]

    # Act
    test_shell.run()

    # Assert
    last_shell_line = capsys.readouterr().out.strip("\n").split("\n")[-2]
    assert last_shell_line == "[Read] LBA 3: 0x00000001"


def test_read_command_input_with_wrong_lba(capsys, mocked_driver_shell_input):
    # Arrange
    driver, test_shell, input_patch = mocked_driver_shell_input
    driver.read.return_value = "0x00000001"
    input_patch.side_effect = ["read -1", "exit"]

    # Act
    test_shell.run()

    # Assert
    last_shell_line = capsys.readouterr().out.strip("\n").split("\n")[-2]
    assert last_shell_line == "INVALID COMMAND"


def test_read_command_correctly_until_exit(capsys, mocked_driver_shell_input):
    # Arrange
    driver, test_shell, input_patch = mocked_driver_shell_input
    driver.read.side_effect = ["0x00000003"]
    input_patch.side_effect = ["read 3", "exit"]

    # Act
    test_shell.run()

    # Assert
    last_shell_line = capsys.readouterr().out.strip("\n").split("\n")[-2]
    assert last_shell_line == "[Read] LBA 3: 0x00000003"


def test_mocked_batch_shell_with_correct_file_and_success_script(tmp_path, capsys, mocker: MockerFixture):
    # Arrange
    patch_bash_shell__run_script = mocker.patch("shell.run_shell.BatchShell._run_script")
    patch_bash_shell__run_script.return_value = True

    batch_shell = BatchShell(mocker.Mock(spec=SSDDriver))

    script_collection_file = tmp_path / "shell_scripts.txt"
    script_collection_file.touch()
    with script_collection_file.open("w") as f:
        for script_name in [
            "1_"
        ]:
            f.writelines(script_name)
    batch_shell.script_collection_file_path = script_collection_file

    # Act
    batch_shell.run()

    # Assert
    actual = capsys.readouterr().out.strip("\n")
    assert actual == "1_FullWriteAndReadCompare  ___  Run...Pass"


def test_mocked_batch_shell_with_correct_file_and_fail_script(tmp_path, capsys, mocker: MockerFixture):
    # Arrange
    patch_bash_shell__run_script = mocker.patch("shell.run_shell.BatchShell._run_script")
    patch_bash_shell__run_script.return_value = False

    batch_shell = BatchShell(mocker.Mock(spec=SSDDriver))

    script_collection_file = tmp_path / "shell_scripts.txt"
    script_collection_file.touch()
    with script_collection_file.open("w") as f:
        for script_name in [
            "1_"
        ]:
            f.writelines(script_name)
    batch_shell.script_collection_file_path = script_collection_file

    # Act
    batch_shell.run()

    # Assert
    actual = capsys.readouterr().out.strip("\n")
    assert actual == "1_FullWriteAndReadCompare  ___  Run...Fail"


def test_mocked_batch_shell_with_correct_file_and_multiple_script(tmp_path, capsys, mocker: MockerFixture):
    # Arrange
    patch_bash_shell__run_script = mocker.patch("shell.run_shell.BatchShell._run_script")
    patch_bash_shell__run_script.side_effect = [
        True, True,
        False, False,
        True, True,
    ]

    batch_shell = BatchShell(mocker.Mock(spec=SSDDriver))

    script_collection_file = tmp_path / "shell_scripts.txt"
    script_collection_file.touch()
    with script_collection_file.open("w") as f:
        for script_name in [
            "1_", "1_FullWriteAndReadCompare",
            "2_", "2_PartialLBAWrite",
            "3_", "3_WriteReadAging"
        ]:
            f.writelines(script_name + "\n")
    batch_shell.script_collection_file_path = script_collection_file

    # Act
    batch_shell.run()

    # Assert
    actual = capsys.readouterr().out.strip("\n").split("\n")
    assert actual == [
        "1_FullWriteAndReadCompare  ___  Run...Pass",
        "1_FullWriteAndReadCompare  ___  Run...Pass",
        "2_PartialLBAWrite  ___  Run...Fail",
        "2_PartialLBAWrite  ___  Run...Fail",
        "3_WriteReadAging  ___  Run...Pass",
        "3_WriteReadAging  ___  Run...Pass",
    ]


def test_mocked_batch_shell_with_wrong_file_that_contain_not_existing_test(tmp_path, capsys, mocker: MockerFixture):
    # Arrange
    patch_bash_shell__run_script = mocker.patch("shell.run_shell.BatchShell._run_script")
    patch_bash_shell__run_script.return_value = False

    batch_shell = BatchShell(mocker.Mock(spec=SSDDriver))

    script_collection_file = tmp_path / "shell_scripts.txt"
    script_collection_file.touch()
    with script_collection_file.open("w") as f:
        for script_name in [
            "NotExisting_Script"
        ]:
            f.writelines(script_name)

    with pytest.raises(NotExistingTestScriptError):
        batch_shell.script_collection_file_path = script_collection_file


def test_mocked_batch_shell_with_not_existing_file(tmp_path, capsys, mocker: MockerFixture):
    # Arrange
    patch_bash_shell__run_script = mocker.patch("shell.run_shell.BatchShell._run_script")
    patch_bash_shell__run_script.return_value = False

    batch_shell = BatchShell(mocker.Mock(spec=SSDDriver))

    script_collection_file = tmp_path / "shell_scripts.txt"

    with pytest.raises(NotExistingFileError):
        batch_shell.script_collection_file_path = script_collection_file
