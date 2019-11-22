#!/usr/bin/env python3
import io
from grep import main, grep_files, grep_input, print_out_result


def test_integrate_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_integrate_stdin_regex_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    main(['-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_integrate_stdin_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    main(['-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_grep_redex_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref hello?\nngggghhello? or not to hello?\nhel\noh hi mark'))
    main(['hello?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref hello?\nngggghhello? or not to hello?\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_file_regex_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('GroundControltoMajorTom\nGroundControltoMajortim\n'
                                    'Ten, Ton, Tep,SevenSixFiveFourThreeTinOneLift off')
    monkeypatch.chdir(tmp_path)
    main(['-E', 'T?m', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'GroundControltoMajorTom\nGroundControltoMajortim\n'


def test_integrate_file_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('Donot\ngogentleintotthatgoodnight\ngogogo\n'
                                    'gioio\ngggggg\nog\ngottagofast')
    monkeypatch.chdir(tmp_path)
    main(['-c', 'go', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_file_regex_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('dejavut\ndddekkk;slkl\nvoooouu\n'
                                    'vousaveszvu\nredex\nog\nvvvviiivivivivovovlk')
    monkeypatch.chdir(tmp_path)
    main(['-c', '-E', 'v*u', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    main(['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_files_regex_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('oooofklklklklkmmmm\nalllllienssssua??\n')
    (tmp_path / 'b.txt').write_text('oooofofofo\nkkokkkkk\n')
    monkeypatch.chdir(tmp_path)
    main(['-E', 'o*f', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:oooofofofo\na.txt:oooofklklklklkmmmm\n'


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_integrate_files_regex_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('helodddrknsmldfrnd\nururuuruurnrunfrst\nofffffcrs')
    (tmp_path / 'b.txt').write_text('lalalalla\nallstrkkm\nlilalolulyllelzlxlcl')
    monkeypatch.chdir(tmp_path)
    main(['-c', '-E', 'l*a', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:3\na.txt:0\n'


def test_invalid_file_name(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('dejavut\ndddekkk;slkl\nvoooouu\n'
                                    'vousaveszvu\nredex\nog\nvvvviiivivivivovovlk')
    monkeypatch.chdir(tmp_path)
    main(['-c', '-E', 'v*u', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'File not found\n'


def test_attempt_at_integration_testing(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    (tmp_path / 'c.txt').write_text('pref neesvsvsvdle\nneedssssssle suf\n')
    (tmp_path / 'd.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    main(['-c', 'needle', 'a.txt', 'b.txt', 'c.txt', 'c.txt', 'd1.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:2\nb.txt:1\nc.txt:0\nc.txt:0\nFile not found\n'


def test_is_a_directory(tmp_path, monkeypatch, capsys):
    direct = tmp_path / 'name'
    direct.mkdir()
    monkeypatch.chdir(tmp_path)
    main(['-c', '-E', 'v*u', 'name'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Is a directory: name\n'


def test_grep_files_directory(tmp_path, monkeypatch, capsys):
    direct = tmp_path / 'name'
    direct.mkdir()
    monkeypatch.chdir(tmp_path)
    grep_files(['name'], 'abc', True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Is a directory: name\n'


def test_grep_files_file_not_found(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('dejavut\ndddekkk;slkl\nvoooouu\n'
                                    'vousaveszvu\nredex\nog\nvvvviiivivivivovovlk')
    monkeypatch.chdir(tmp_path)
    grep_files(['name'], 'abc', True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'File not found\n'


def test_grep_print_out(capsys):
    print_out_result(['a.txt:1', 'b.txt:10000'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\nb.txt:10000\n'


def test_grep_input_file(tmp_path, monkeypatch):
    needle = 'needle'
    p = tmp_path / 'a.txt'
    p.write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    with p.open() as f:
        line = grep_input(f, needle, False)
        assert line == ['pref needle suf']


def test_grep_input_stdin():
    output = io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    needle = 'needle'
    lines = grep_input(output, needle, False)
    assert lines == ['pref needle?', 'needle? suf', 'pref needle? suf']


def test_grep_input_stdin_is_count():
    output = io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    needle = 'needle'
    lines = grep_input(output, needle, True)
    assert lines == ['3']


def test_grep_input_stdin_is_regex():
    output = io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    needle = 'need?'
    lines = grep_input(output, needle, False)
    assert lines == ['pref needle?', 'needle? suf', 'the needl', 'pref needle? suf']


def test_grep_input_stdin_is_regex_is_amount():
    output = io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf')
    needle = 'need?'
    lines = grep_input(output, needle, True)
    assert lines == ['4']


def test_grep_input_files(tmp_path, monkeypatch, capsys):
    needle = 'needle'
    p = tmp_path / 'a.txt'
    f = tmp_path / 'b.txt'
    p.write_text('the needl\npref needle suf')
    f.write_text('the needlejnkejbsvkj\npref needlescassuf')
    monkeypatch.chdir(tmp_path)
    grep_files(['a.txt', 'b.txt'], needle, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\nb.txt:2\n'
