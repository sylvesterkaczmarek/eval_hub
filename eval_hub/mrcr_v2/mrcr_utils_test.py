# Copyright 2026 DeepMind Technologies Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for MRCR V2 generation utilities."""

import unittest
from unittest import mock

from eval_hub.mrcr_v2 import mrcr_utils


def _tokenizer(text: str) -> tuple[list[int], int]:
  tokens = list(range(len(text.split())))
  return tokens, len(tokens)


def _query_group(random_hash: str, answer_prefix: str) -> dict[str, object]:
  return {
      "follow_up_base_prompt_format": (
          f"User: Prepend {random_hash} to the {{index_name}} poem about topic "
          "in a formal style. Do not include any other text in your response.\n\n"
          "Assistant:"
      ),
      "seeds": [
          {"text": f"{answer_prefix}-0", "token_count": 1},
          {"text": f"{answer_prefix}-1", "token_count": 1},
      ],
      "index_positions_of_seeds": [0, 1],
      "context_positions_of_seeds": [(0, 1), (1, 2)],
  }


class MrcrUtilsTest(unittest.TestCase):

  def test_generate_queries_and_answers_respects_sample_limit_across_groups(self):
    query_groups = {
        "group-a": _query_group("aaaaaaaaaaaa", "a"),
        "group-b": _query_group("bbbbbbbbbbbb", "b"),
    }

    samples = mrcr_utils.generate_queries_and_answers(
        query_groups,
        full_transcript="",
        full_token_count=0,
        num_seeds=2,
        sample_limit=1,
        json_style=False,
        tokenizer=_tokenizer,
    )

    self.assertLen(samples, 1)

  @mock.patch.object(mrcr_utils, "generate_queries_and_answers")
  @mock.patch.object(mrcr_utils, "create_final_transcript_and_metadata")
  def test_generate_mrcr_v2_requests_only_remaining_samples(
      self, mock_create_transcript, mock_generate_queries
  ):
    mock_create_transcript.return_value = ({}, "", 10)

    def generate_up_to_two(
        position_updated_rqgs,
        full_transcript,
        full_token_count,
        num_seeds,
        sample_limit,
        json_style,
        tokenizer,
    ):
      del position_updated_rqgs, full_transcript, num_seeds, json_style, tokenizer
      return [
          {"context_len": full_token_count}
          for _ in range(min(2, sample_limit))
      ]

    mock_generate_queries.side_effect = generate_up_to_two

    bucket_samples, _ = mrcr_utils.generate_mrcr_v2(
        relevant_data={},
        irrelevant_data={},
        fewshot_data={},
        num_seeds=2,
        samples_per_bucket=3,
        buckets=[(4096, 8192)],
        static_fewshot=True,
        json_style=False,
        tokenizer=_tokenizer,
    )

    self.assertLen(bucket_samples[(4096, 8192)], 3)
    requested_limits = [call.args[4] for call in mock_generate_queries.call_args_list]
    self.assertEqual(requested_limits, [3, 1])


if __name__ == "__main__":
  unittest.main()
