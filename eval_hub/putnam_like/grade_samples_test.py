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

import pathlib
import tempfile
import unittest

from eval_hub.putnam_like import grade_samples


class FindExistingGradeTest(unittest.TestCase):

  def setUp(self):
    super().setUp()
    self.temp_dir = tempfile.TemporaryDirectory()
    self.addCleanup(self.temp_dir.cleanup)
    self.sample_dir = pathlib.Path(self.temp_dir.name)
    self.sample_path = self.sample_dir / "sample_001.md"
    self.sample_path.write_text("solution", encoding="utf-8")

  def test_finds_same_model_grade_from_earlier_run(self):
    grade_path = self.sample_dir / (
        "grade_gemini-2.5-pro_20260101-000000_sample_001.json"
    )
    grade_path.write_text("{}", encoding="utf-8")

    self.assertEqual(
        grade_samples.find_existing_grade(
            self.sample_path, "gemini-2.5-pro"
        ),
        grade_path,
    )

  def test_ignores_grade_from_different_model(self):
    grade_path = self.sample_dir / (
        "grade_gemini-2.0-flash_20260101-000000_sample_001.json"
    )
    grade_path.write_text("{}", encoding="utf-8")

    self.assertIsNone(
        grade_samples.find_existing_grade(
            self.sample_path, "gemini-2.5-pro"
        )
    )

  def test_ignores_grade_for_different_sample_with_shared_suffix(self):
    grade_path = self.sample_dir / (
        "grade_gemini-2.5-pro_20260101-000000_other_sample_001.json"
    )
    grade_path.write_text("{}", encoding="utf-8")

    self.assertIsNone(
        grade_samples.find_existing_grade(
            self.sample_path, "gemini-2.5-pro"
        )
    )


if __name__ == "__main__":
  unittest.main()
