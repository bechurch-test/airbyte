#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

from pathlib import PosixPath

import pytest
from freezegun import freeze_time
from pytest import LogCaptureFixture
from unit_tests.sources.scenario_based.helpers import verify_discover, verify_read
from unit_tests.sources.scenario_based.scenario_builder import TestScenario
# from unit_tests.sources.streams.concurrent.scenarios.async_incremental_scenarios import (
#     test_incremental_stream_with_slice_boundaries_no_input_state,
#     test_incremental_stream_with_slice_boundaries_with_concurrent_state,
#     test_incremental_stream_with_slice_boundaries_with_legacy_state,
#     test_incremental_stream_without_slice_boundaries_no_input_state,
#     test_incremental_stream_without_slice_boundaries_with_concurrent_state,
#     test_incremental_stream_without_slice_boundaries_with_legacy_state,
# )
from unit_tests.sources.async_cdk.scenario_based.async_concurrent_stream_scenarios import (
    test_concurrent_cdk_multiple_streams,
    test_concurrent_cdk_partition_raises_exception,
    test_concurrent_cdk_single_stream,
    test_concurrent_cdk_single_stream_multiple_partitions,
    test_concurrent_cdk_single_stream_multiple_partitions_concurrency_level_two,
    test_concurrent_cdk_single_stream_with_primary_key,
)

scenarios = [
    test_concurrent_cdk_single_stream,
    test_concurrent_cdk_multiple_streams,
    test_concurrent_cdk_single_stream_multiple_partitions,
    test_concurrent_cdk_single_stream_multiple_partitions_concurrency_level_two,
    test_concurrent_cdk_single_stream_with_primary_key,
    test_concurrent_cdk_partition_raises_exception,
    # test_incremental_stream_with_slice_boundaries,
    # test_incremental_stream_without_slice_boundaries,
    # test_incremental_stream_with_many_slices_but_without_slice_boundaries,
    # test_incremental_stream_with_slice_boundaries_no_input_state,
    # test_incremental_stream_with_slice_boundaries_with_concurrent_state,
    # test_incremental_stream_with_slice_boundaries_with_legacy_state,
    # test_incremental_stream_without_slice_boundaries_no_input_state,
    # test_incremental_stream_without_slice_boundaries_with_concurrent_state,
    # test_incremental_stream_without_slice_boundaries_with_legacy_state,
]


@pytest.mark.parametrize("scenario", scenarios, ids=[s.name for s in scenarios])
@freeze_time("2023-06-09T00:00:00Z")
def test_concurrent_read(scenario: TestScenario) -> None:
    verify_read(scenario)


@pytest.mark.parametrize("scenario", scenarios, ids=[s.name for s in scenarios])
def test_concurrent_discover(tmp_path: PosixPath, scenario: TestScenario) -> None:
    verify_discover(tmp_path, scenario)
