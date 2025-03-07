# coding=utf-8
# Copyright 2022 The HuggingFace Team. All rights reserved.
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
import unittest

import requests
import torch
from parameterized import parameterized
from PIL import Image
from testing_bettertransformer_utils import BetterTransformersTestMixin
from transformers import AutoFeatureExtractor, AutoModel, AutoProcessor

from optimum.bettertransformer import BetterTransformer
from optimum.utils.testing_utils import grid_parameters


ALL_VISION_MODELS_TO_TEST = [
    "hf-internal-testing/tiny-random-ViTModel",
    "hf-internal-testing/tiny-random-YolosModel",
    "hf-internal-testing/tiny-random-ViTMAEModel",
    "hf-internal-testing/tiny-random-ViTMSNModel",
    "hf-internal-testing/tiny-random-deit",
]


ALL_VISION_TEXT_MODELS_TO_TEST = [
    "hf-internal-testing/tiny-vilt-random-vqa",
]

ALL_ZERO_SHOT_IMAGE_CLASSIFICATION = [
    "hf-internal-testing/tiny-random-clip-zero-shot-image-classification",  # with quick_gelu
    "laion/CLIP-ViT-B-32-laion2B-s34B-b79K",  # with gelu
]


class BetterTransformersVisionTest(BetterTransformersTestMixin, unittest.TestCase):
    r"""
    Testing suite for Vision Models - tests all the tests defined in `BetterTransformersTestMixin`
    """
    all_models_to_test = ALL_VISION_MODELS_TO_TEST

    def prepare_inputs_for_class(self, model_id=None):
        url = "http://images.cocodataset.org/val2017/000000039769.jpg"
        image = Image.open(requests.get(url, stream=True).raw)

        # Use the same feature extractor for everyone
        feature_extractor = AutoFeatureExtractor.from_pretrained("hf-internal-testing/tiny-random-ViTModel")
        inputs = feature_extractor(images=image, return_tensors="pt")
        return inputs

    @parameterized.expand(
        grid_parameters(
            {
                "model_id": all_models_to_test,
                "keep_original_model": [True, False],
            }
        )
    )
    def test_invert_modules(self, test_name: str, model_id, keep_original_model=False):
        super().test_invert_modules(model_id=model_id, keep_original_model=keep_original_model)

    @parameterized.expand(
        grid_parameters(
            {
                "model_id": all_models_to_test,
                "keep_original_model": [True, False],
            }
        )
    )
    def test_save_load_invertible(self, test_name: str, model_id, keep_original_model=False):
        super().test_save_load_invertible(model_id=model_id, keep_original_model=keep_original_model)

    @parameterized.expand(
        grid_parameters(
            {
                "model_id": all_models_to_test,
                "keep_original_model": [True, False],
            }
        )
    )
    def test_invert_model_logits(self, test_name: str, model_id, keep_original_model=False):
        super().test_invert_model_logits(model_id=model_id, keep_original_model=keep_original_model)

    @parameterized.expand(
        grid_parameters(
            {
                "model_id": all_models_to_test,
                "keep_original_model": [True, False],
            }
        )
    )
    def test_raise_save_pretrained_error(self, test_name: str, model_id, keep_original_model=False):
        super().test_raise_save_pretrained_error(model_id=model_id, keep_original_model=keep_original_model)


class BetterTransformersViLTTest(BetterTransformersTestMixin, unittest.TestCase):
    r"""
    Testing suite for Vision and Text Models - tests all the tests defined in `BetterTransformersTestMixin`
    """
    all_models_to_test = ALL_VISION_TEXT_MODELS_TO_TEST

    def prepare_inputs_for_class(self, model_id=None):
        url = "http://images.cocodataset.org/val2017/000000039769.jpg"
        image = Image.open(requests.get(url, stream=True).raw)
        text = "How many cats are there?"

        # Model takes image and text as input
        processor = AutoProcessor.from_pretrained(model_id)
        inputs = processor(images=image, text=text, return_tensors="pt")
        return inputs

    @parameterized.expand(
        grid_parameters(
            {
                "model_id": all_models_to_test,
                "keep_original_model": [True, False],
            }
        )
    )
    def test_invert_modules(self, test_name: str, model_id, keep_original_model=False):
        super().test_invert_modules(model_id=model_id, keep_original_model=keep_original_model)

    @parameterized.expand(
        grid_parameters(
            {
                "model_id": all_models_to_test,
                "keep_original_model": [True, False],
            }
        )
    )
    def test_save_load_invertible(self, test_name: str, model_id, keep_original_model=False):
        super().test_save_load_invertible(model_id=model_id, keep_original_model=keep_original_model)

    @parameterized.expand(
        grid_parameters(
            {
                "model_id": all_models_to_test,
                "keep_original_model": [True, False],
            }
        )
    )
    def test_invert_model_logits(self, test_name: str, model_id, keep_original_model=False):
        super().test_invert_model_logits(model_id=model_id, keep_original_model=keep_original_model)

    @parameterized.expand(
        grid_parameters(
            {
                "model_id": all_models_to_test,
                "keep_original_model": [True, False],
            }
        )
    )
    def test_raise_save_pretrained_error(self, test_name: str, model_id, keep_original_model=False):
        super().test_raise_save_pretrained_error(model_id=model_id, keep_original_model=keep_original_model)


class BetterTransformersCLIPTest(BetterTransformersTestMixin, unittest.TestCase):
    r"""
    Testing suite for Vision and Text Models - tests all the tests defined in `BetterTransformersTestMixin`
    """
    all_models_to_test = ALL_ZERO_SHOT_IMAGE_CLASSIFICATION

    def prepare_inputs_for_class(self, model_id, **preprocessor_kwargs):
        url = "http://images.cocodataset.org/val2017/000000039769.jpg"
        image = Image.open(requests.get(url, stream=True).raw)
        text = ["a photo", "a photo of dog", "a photo of two big cats"]

        # Model takes image and text as input
        processor = AutoProcessor.from_pretrained(model_id)
        inputs = processor(images=image, text=text, return_tensors="pt", **preprocessor_kwargs)
        return inputs

    def compare_outputs(self, hf_hidden_states, bt_hidden_states, atol: float, model_name: str):
        # CLIP returns a 2D tensor
        self.assert_equal(
            tensor1=hf_hidden_states,
            tensor2=bt_hidden_states,
            atol=atol,
            model_name=model_name,
        )

    # run the test over all possible combinations of `model_id` and `padding`
    @parameterized.expand(
        grid_parameters(
            {
                "model_id": ALL_ZERO_SHOT_IMAGE_CLASSIFICATION,
                "padding": ["max_length", True],
            }
        )
    )
    def test_logits(self, test_name: str, model_id, padding, max_length=20):
        super().test_logits([model_id], padding=padding, max_length=max_length)

    @parameterized.expand(
        grid_parameters(
            {
                "model_id": ALL_ZERO_SHOT_IMAGE_CLASSIFICATION,
                "padding": ["max_length", True],
            }
        )
    )
    def test_raise_autocast(self, test_name: str, model_id, padding, max_length=20):
        super().test_raise_autocast([model_id], padding=padding, max_length=max_length)

    @parameterized.expand(
        grid_parameters(
            {
                "model_id": ALL_ZERO_SHOT_IMAGE_CLASSIFICATION,
                "padding": ["max_length", True],
            }
        )
    )
    def test_raise_train(self, test_name: str, model_id, padding, max_length=20):
        super().test_raise_train([model_id], padding=padding, max_length=max_length)

    @parameterized.expand(
        grid_parameters(
            {
                "model_id": all_models_to_test,
                "keep_original_model": [True, False],
            }
        )
    )
    def test_invert_modules(self, test_name: str, model_id, keep_original_model=False):
        super().test_invert_modules(model_id=model_id, keep_original_model=keep_original_model)

    @parameterized.expand(
        grid_parameters(
            {
                "model_id": all_models_to_test,
                "keep_original_model": [True, False],
            }
        )
    )
    def test_save_load_invertible(self, test_name: str, model_id, keep_original_model=False):
        super().test_save_load_invertible(model_id=model_id, keep_original_model=keep_original_model)

    @parameterized.expand(
        grid_parameters(
            {
                "model_id": all_models_to_test,
                "keep_original_model": [True, False],
                "padding": ["max_length", True],
            }
        )
    )
    def test_invert_model_logits(self, test_name: str, model_id, keep_original_model=False, padding=True):
        r"""
        Test that the inverse converted model and hf model have the same logits
        """
        # get hf and bt model
        hf_model = AutoModel.from_pretrained(model_id)
        # get bt model and invert it
        bt_model = BetterTransformer.transform(hf_model, keep_original_model=keep_original_model)
        bt_model = BetterTransformer.reverse(bt_model)

        # get inputs
        inputs = self.prepare_inputs_for_class(model_id, padding=padding)

        # get outputs
        torch.manual_seed(42)
        output_bt = bt_model(**inputs)

        # create a new model
        hf_model = AutoModel.from_pretrained(model_id)

        torch.manual_seed(42)
        output_hf = hf_model(**inputs)

        # Assert that the outputs are the same
        self.assertTrue(torch.allclose(output_bt[0], output_hf[0], atol=1e-3))

    @parameterized.expand(
        grid_parameters(
            {
                "model_id": all_models_to_test,
                "keep_original_model": [True, False],
            }
        )
    )
    def test_raise_save_pretrained_error(
        self, test_name: str, model_id, keep_original_model=False, **preprocessor_kwargs
    ):
        super().test_raise_save_pretrained_error(model_id=model_id, keep_original_model=keep_original_model)
