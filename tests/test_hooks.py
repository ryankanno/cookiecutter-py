#!/usr/bin/env python
#
# Copyright © 2020 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

"""Tests hooks."""

import tempfile
from pathlib import Path

import pytest

from hooks import post_gen_project
from hooks.post_gen_project import manage_author_files
from hooks.post_gen_project import manage_direnv_files
from hooks.post_gen_project import manage_github_files
from hooks.post_gen_project import remove_path
from hooks.post_gen_project import uncomment_pyproject_python_dependency
from hooks.post_gen_project import update_pyproject_version
from hooks.pre_gen_project import validate_dependabot
from hooks.pre_gen_project import validate_supported_python_versions


def test_remove_path() -> None:
    with tempfile.NamedTemporaryFile(delete=False) as ntf:
        temp_path = Path(ntf.name)
        remove_path(temp_path)
        assert not temp_path.exists()


@pytest.fixture
def project_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    github_dir = tmp_path / ".github"
    github_dir.mkdir()
    (github_dir / "workflows").mkdir()
    monkeypatch.setattr(post_gen_project, "PROJECT_ROOT_DIR", tmp_path)
    monkeypatch.setattr(post_gen_project, "PROJECT_GITHUB", github_dir)
    return tmp_path


def test_manage_direnv_files_removes_envrc_when_disabled(
    project_root: Path,
) -> None:
    envrc = project_root / ".envrc"
    envrc.touch()
    manage_direnv_files("n")
    assert not envrc.exists()


def test_manage_direnv_files_keeps_envrc_when_enabled(
    project_root: Path,
) -> None:
    envrc = project_root / ".envrc"
    envrc.touch()
    manage_direnv_files("y")
    assert envrc.exists()


def test_manage_author_files_removes_authors_when_disabled(
    project_root: Path,
) -> None:
    authors = project_root / "AUTHORS.rst"
    authors.touch()
    manage_author_files("n")
    assert not authors.exists()


def test_manage_author_files_keeps_authors_when_enabled(
    project_root: Path,
) -> None:
    authors = project_root / "AUTHORS.rst"
    authors.touch()
    manage_author_files("y")
    assert authors.exists()


def _seed_github_tree(github: Path) -> dict[str, Path]:
    dependabot = github / "dependabot.yml"
    labeler = github / "labeler.yml"
    release_drafter = github / "release-drafter.yml"
    workflows = github / "workflows"
    automerge = workflows / "auto-approve-merge-dependabot.yml"
    publish = workflows / "publish.yml"
    for f in (dependabot, labeler, release_drafter, automerge, publish):
        f.touch()
    return {
        "dependabot": dependabot,
        "labeler": labeler,
        "release_drafter": release_drafter,
        "automerge": automerge,
        "publish": publish,
        "workflows": workflows,
    }


def test_manage_github_files_removes_dependabot_when_disabled(
    project_root: Path,
) -> None:
    paths = _seed_github_tree(project_root / ".github")
    manage_github_files("n", "y", "y")
    assert not paths["dependabot"].exists()
    assert not paths["automerge"].exists()
    assert paths["publish"].exists()
    assert paths["labeler"].exists()


def test_manage_github_files_removes_only_automerge_when_flag_off(
    project_root: Path,
) -> None:
    paths = _seed_github_tree(project_root / ".github")
    manage_github_files("y", "n", "y")
    assert paths["dependabot"].exists()
    assert not paths["automerge"].exists()
    assert paths["publish"].exists()


def test_manage_github_files_removes_workflows_when_actions_disabled(
    project_root: Path,
) -> None:
    paths = _seed_github_tree(project_root / ".github")
    manage_github_files("n", "n", "n")
    assert not paths["labeler"].exists()
    assert not paths["release_drafter"].exists()
    assert not paths["workflows"].exists()
    assert not paths["publish"].exists()
    assert not (project_root / ".github").exists()


def test_manage_github_files_keeps_publish_yml_when_actions_enabled(
    project_root: Path,
) -> None:
    paths = _seed_github_tree(project_root / ".github")
    manage_github_files("y", "y", "y")
    assert paths["publish"].exists()
    assert paths["workflows"].exists()


def test_update_pyproject_version_replaces_placeholder(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nversion = "0.0.0"\n')
    update_pyproject_version("1.2.3")
    contents = pyproject.read_text()
    assert "version = '1.2.3'" in contents
    assert 'version = "0.0.0"' not in contents


def test_update_pyproject_version_noop_when_file_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    update_pyproject_version("1.2.3")
    assert not (tmp_path / "pyproject.toml").exists()


def test_uncomment_pyproject_python_dependency_uncomments_lines(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        "[tool.poetry.dependencies]\n"
        '# python = "^3.11"\n'
        'requests = "^2.0"\n'
    )
    uncomment_pyproject_python_dependency()
    contents = pyproject.read_text()
    assert 'python = "^3.11"' in contents
    assert '# python = "^3.11"' not in contents
    assert 'requests = "^2.0"' in contents


def test_uncomment_pyproject_python_dependency_noop_when_file_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    uncomment_pyproject_python_dependency()
    assert not (tmp_path / "pyproject.toml").exists()


def test_with_unsupported_python_versions() -> None:
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        validate_supported_python_versions("foo")

    assert isinstance(pytest_wrapped_e.value, SystemExit)
    assert pytest_wrapped_e.value.code == 1


def test_with_supported_python_versions() -> None:
    validate_supported_python_versions(
        "3.10, 3.11, pypy3.10, pypy3.11",
    )  # noqa: B950


def test_with_invalid_dependabot_settings() -> None:
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        validate_dependabot(False, True, True)

    assert isinstance(pytest_wrapped_e.value, SystemExit)
    assert pytest_wrapped_e.value.code == 1

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        validate_dependabot(False, True, False)

    assert isinstance(pytest_wrapped_e.value, SystemExit)
    assert pytest_wrapped_e.value.code == 1

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        validate_dependabot(True, True, False)

    assert isinstance(pytest_wrapped_e.value, SystemExit)
    assert pytest_wrapped_e.value.code == 1

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        validate_dependabot(False, True, False)

    assert isinstance(pytest_wrapped_e.value, SystemExit)
    assert pytest_wrapped_e.value.code == 1


def test_with_valid_dependabot_settings() -> None:
    validate_dependabot(True, True, True)
    validate_dependabot(True, False, True)
    validate_dependabot(True, False, False)
    validate_dependabot(False, False, False)


# vim: fenc=utf-8
# vim: filetype=python
