import json
import re
import os
from datetime import datetime

DATE = datetime.now()

OUT = """\"\"\"
Class object for {classname}
Documentation: {documentation}

Generated by generator/generator.py - {date}
\"\"\"
from MediaTracker.objects.objects.base import MediaTrackerBase

{inherit}
"""

CLASS = """
class {classname}(MediaTrackerBase):
{properties}
"""

PROP = """
    @property
    def {key}(self):
        return self.attributes.get("{key}", {default})
"""
PROPCLASS = """
    @property
    def {key}(self):
        return {name}(self.attributes.get("{key}", {default}))
"""
PROPLISTCLASS = """
    @property
    def {key}(self):
        return [{name}(x) for x in self.attributes.get("{key}", [])]
"""

FIXSTURE = """\"\"\"
Generated by generator/generator.py - {date}
\"\"\"
import pytest


@pytest.fixture()
def {name}():
    return {content}
"""

TEST = """\"\"\"
Generated by generator/generator.py - {date}
\"\"\"
from {importfile} import {importclass}
from {fixturefile} import {fixture}

def {testname}({fixture}):
    obj = {importclass}({fixture})
{assertions}
"""

INHERIT = []


def get_input():
    with open("generator/input.json", "r") as inputdata:
        return json.loads(inputdata.read())


def generateclass(name, data, primary=False):
    properties = []
    # print(data)
    for key in data:
        print(key)
        if key.startswith("_"):
            continue
        if isinstance(data[key], list):
            if not isinstance(data[key][0], dict) and not isinstance(
                data[key][0], list
            ):
                properties.append(PROP.format(key=key, default=[]))
                continue
            _name = key.split("_")
            _name = "".join([x.title() for x in _name])
            _name = f"{_name}"
            INHERIT.append(generateclass(_name, data[key][0]))
            properties.append(PROPLISTCLASS.format(name=_name, key=key))
            continue
        if isinstance(data[key], dict):
            _name = key.split("_")
            _name = "".join([x.title() for x in _name])
            _name = f"{name}{_name}"
            INHERIT.append(generateclass(_name, data[key]))
            properties.append(PROPCLASS.format(name=_name, key=key, default={}))
            continue
        if isinstance(data[key], bool):
            properties.append(PROP.format(key=key, default=data[key]))
            continue
        if isinstance(data[key], str):
            properties.append(PROP.format(key=key, default='""'))
            continue
        properties.append(PROP.format(key=key, default=None))

    if not primary:
        return CLASS.format(classname=name, properties="".join(properties))
    docs = input("Documentation URL: ")
    classname = input("Main Classname: ")
    INHERIT.append(
        CLASS.format(classname=f"MediaTracker{classname}", properties="".join(properties))
    )

    objectfilename = f"pymediatracker/objects/{'/'.join([x.lower() for x in re.findall('[A-Z][a-z]*', classname)])}.py"
    if not os.path.exists(os.path.dirname(objectfilename)):
        os.makedirs(os.path.dirname(objectfilename))
        with open(os.path.join(os.path.dirname(objectfilename), "__init__.py")) as f:
            f.write()

    with open(
        objectfilename,
        "w",
    ) as objfile:
        objfile.write(
            OUT.format(
                classname=f"MediaTracker{classname}",
                properties=properties,
                documentation=docs,
                inherit="".join(INHERIT),
                date=DATE,
            )
        )

    fixturefilename = f"tests/responses/{'/'.join([x.lower() for x in re.findall('[A-Z][a-z]*', classname)])}_fixture.py"
    fixturename = f"{fixturefilename.split('/')[-1].replace('.py', '')}_response"

    if not os.path.exists(os.path.dirname(fixturefilename)):
        os.makedirs(os.path.dirname(fixturefilename))
    with open(
        fixturefilename,
        "w",
    ) as fixturefile:
        fixturefile.write(
            FIXSTURE.format(
                name=fixturename,
                content=data,
                date=DATE,
            )
        )

    tmpfilename = [x.lower() for x in re.findall("[A-Z][a-z]*", classname)]
    tmpr = tmpfilename.pop()
    tmpfilename.append(f"test_{tmpr}")
    testfilename = f"tests/objects/{'/'.join(tmpfilename)}.py"
    testname = f"test_{tmpr}"
    assertions = []

    for key in data:
        if key.startswith("_"):
            continue
        if not isinstance(data[key], (dict, list)):
            assertions.append(f"    assert obj.{key} == {fixturename}['{key}']")
        if isinstance(data[key], list):
            if not isinstance(data[key][0], (dict, list)):
                assertions.append(
                    f"    assert obj.{key}[0] == {fixturename}['{key}'][0]"
                )
            if isinstance(data[key][0], dict):
                for sakey in data[key][0]:
                    assertions.append(
                        f"    assert obj.{key}[0].{sakey} == {fixturename}['{key}'][0]['{sakey}']"
                    )
        if isinstance(data[key], dict):
            for akey in data[key]:
                if not isinstance(data[key][akey], (dict, list)):
                    assertions.append(
                        f"    assert obj.{key}.{akey} == {fixturename}['{key}']['{akey}']"
                    )
                if isinstance(data[key][akey], list):
                    if not isinstance(data[key][akey][0], (dict, list)):
                        assertions.append(
                            f"    assert obj.{key}.{akey}[0] == {fixturename}['{key}']['{akey}'][0]"
                        )
                    if isinstance(data[key][akey][0], dict):
                        for sakey in data[key][akey][0]:
                            assertions.append(
                                f"    assert obj.{key}.{akey}[0].{sakey} == {fixturename}['{key}']['{akey}'][0]['{sakey}']"
                            )
                if isinstance(data[key][akey], dict):
                    for bkey in data[key][akey]:
                        if not isinstance(data[key][akey][bkey], (dict, list)):
                            assertions.append(
                                f"    assert obj.{key}.{akey}.{bkey} == {fixturename}['{key}']['{akey}']['{bkey}']"
                            )
                        if isinstance(data[key][akey][bkey], list):
                            if not isinstance(data[key][akey][bkey][0], (dict, list)):
                                assertions.append(
                                    f"    assert obj.{key}.{akey}.{bkey}[0] == {fixturename}['{key}']['{akey}']['{bkey}'][0]"
                                )
                            if isinstance(data[key][akey][bkey][0], dict):
                                for sakey in data[key][akey][bkey][0]:
                                    assertions.append(
                                        f"    assert obj.{key}.{akey}.{bkey}[0].{sakey} == {fixturename}['{key}']['{akey}']['{bkey}'][0]['{sakey}']"
                                    )
                        if isinstance(data[key][akey][bkey], dict):
                            for ckey in data[key][akey][bkey]:
                                if not isinstance(
                                    data[key][akey][bkey][ckey], (dict, list)
                                ):
                                    assertions.append(
                                        f"    assert obj.{key}.{akey}.{bkey}.{ckey} == {fixturename}['{key}']['{akey}']['{bkey}']['{ckey}']"
                                    )
                                if isinstance(data[key][akey][bkey][ckey], list):
                                    if not isinstance(
                                        data[key][akey][bkey][ckey][0], (dict, list)
                                    ):
                                        assertions.append(
                                            f"    assert obj.{key}.{akey}.{bkey}.{ckey}[0] == {fixturename}['{key}']['{akey}']['{bkey}']['{ckey}'][0]"
                                        )
                                    if isinstance(data[key][akey][bkey][ckey][0], dict):
                                        for sakey in data[key][akey][bkey][ckey][0]:
                                            assertions.append(
                                                f"    assert obj.{key}.{akey}.{bkey}.{ckey}[0].{sakey} == {fixturename}['{key}']['{akey}']['{bkey}']['{ckey}'][0]['{sakey}']"
                                            )
                                if isinstance(data[key][akey][bkey][ckey], dict):
                                    for dkey in data[key][akey][bkey][ckey]:
                                        if not isinstance(
                                            data[key][akey][bkey][ckey][dkey],
                                            (dict, list),
                                        ):

                                            assertions.append(
                                                f"    assert obj.{key}.{akey}.{bkey}.{ckey}.{dkey} == {fixturename}['{key}']['{akey}']['{bkey}']['{ckey}']['{dkey}']"
                                            )
                                        if isinstance(
                                            data[key][akey][bkey][ckey][dkey], list
                                        ):
                                            if not isinstance(
                                                data[key][akey][bkey][ckey][dkey][0],
                                                (dict, list),
                                            ):
                                                assertions.append(
                                                    f"    assert obj.{key}.{akey}.{bkey}.{ckey}.{dkey}[0] == {fixturename}['{key}']['{akey}']['{bkey}']['{ckey}']['{dkey}'][0]"
                                                )
                                            if isinstance(
                                                data[key][akey][bkey][ckey][dkey][0],
                                                dict,
                                            ):
                                                for sakey in data[key][akey][bkey][
                                                    ckey
                                                ][dkey][0]:
                                                    assertions.append(
                                                        f"    assert obj.{key}.{akey}.{bkey}.{ckey}.{dkey}[0].{sakey} == {fixturename}['{key}']['{akey}']['{bkey}']['{ckey}']['{dkey}'][0]['{sakey}']"
                                                    )
            continue

    if not os.path.exists(os.path.dirname(testfilename)):
        os.makedirs(os.path.dirname(testfilename))
    with open(
        testfilename,
        "w",
    ) as fixturefile:
        fixturefile.write(
            TEST.format(
                importfile=".".join(objectfilename.replace(".py", "").split("/")),
                importclass=f"MediaTracker{classname}",
                fixturefile=".".join(fixturefilename.replace(".py", "").split("/")),
                fixture=fixturename,
                testname=testname,
                assertions="\n".join(assertions),
                date=DATE,
            )
        )


def add_object():
    data = get_input()
    generateclass("", data, True)


add_object()
