# Copyright 2018-2022 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import pytest
import Pyxsim
from Pyxsim import testers
import os
import sys


@pytest.fixture()
def test_file(request):
    return str(request.node.fspath)


def do_test(
    pcm_format, i2s_role, channel_count, sample_rate, test_file, options, capfd
):

    build_options = []
    output = []
    testname, _ = os.path.splitext(os.path.basename(test_file))

    desc = f"simulation_{pcm_format}_{i2s_role}_{channel_count}in_{channel_count}out_{sample_rate}"
    binary = f"{testname}/bin/{desc}/{testname}_{desc}.xe"

    tester = testers.ComparisonTester(open("pass.expect"))

    loopback_args = (
        "-port tile[0] XS1_PORT_1M 1 0 -port tile[0] XS1_PORT_1I 1 0 "
        + "-port tile[0] XS1_PORT_1N 1 0 -port tile[0] XS1_PORT_1J 1 0 "
        + "-port tile[0] XS1_PORT_1O 1 0 -port tile[0] XS1_PORT_1K 1 0 "
        + "-port tile[0] XS1_PORT_1P 1 0 -port tile[0] XS1_PORT_1L 1 0 "
        + "-port tile[0] XS1_PORT_1A 1 0 -port tile[0] XS1_PORT_1F 1 0 "
    )
    if i2s_role == "slave":
        loopback_args += (
            "-port tile[0] XS1_PORT_1B 1 0 -port tile[0] XS1_PORT_1H 1 0 "  # bclk
        )
        loopback_args += (
            "-port tile[0] XS1_PORT_1C 1 0 -port tile[0] XS1_PORT_1G 1 0 "  # lrclk
        )

    max_cycles = 1500000  # enough to reach the 10 skip + 100 test in sim at 48kHz

    simargs = [
        "--max-cycles",
        str(max_cycles),
        "--plugin",
        "LoopbackPort.dll",
        loopback_args,
    ]

    result = Pyxsim.run_on_simulator(
        binary, simthreads=[], tester=tester, simargs=simargs, capfd=capfd
    )

    return result


@pytest.mark.parametrize("i2s_role", ["master", "slave"])
@pytest.mark.parametrize("pcm_format", ["i2s", "tdm"])
@pytest.mark.parametrize("channel_count", [2, 8, 16])
@pytest.mark.parametrize("sample_rate", ["48khz", "192khz"])
def test_i2s_loopback(
    i2s_role, pcm_format, channel_count, sample_rate, test_file, options, capfd
):

    if pcm_format == "i2s" and channel_count == 16:
        pytest.skip("Invalid parameter combination")

    if pcm_format == "tdm" and channel_count == 2:
        pytest.skip("Invalid parameter combination")

    if pcm_format == "tdm" and sample_rate == "192khz":
        pytest.skip("Invalid parameter combination")

    result = do_test(
        pcm_format, i2s_role, channel_count, sample_rate, test_file, options, capfd
    )

    assert result