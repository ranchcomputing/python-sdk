import os

import pytest
import requests
from dotenv import load_dotenv

from ranch import connection
from .mock_connection import MockConnection

# from .mock_job import data


load_dotenv()

RANCH_API_KEY = os.getenv("RANCH_API_KEY")
RANCH_SDK_EMAIL = os.getenv("RANCH_SDK_EMAIL")

class TestConnection:
    def setup_method(self, method):
        self.conn = connection.Connect(RANCH_API_KEY)
        self.mock_conn = MockConnection()

    def teardown_method(self, method):
        del self.conn

    def test_mock_connection(self):
        res = self.mock_conn._post("ranchcomputing.com", {})
        assert res.status_code == 200

    def test_connection_empty_api_key(self):
        assert self.conn.api_key != ""

    # def test_connection_unauthorize_message(self, data):
    #     self.conn._api_key = "key"
    #     archive_path = "C:\\Users\\mohbakh\\Pictures\\car\\sdk.vuc"
    #     res = self.conn.create_job(
    #         archive_path=archive_path, job_name="sdk_job", priority="gpu-low", renderer_id=598
    #     ).create()
    #     assert res.json() == {"message": "wrong X-Auth-Token"}

    # def test_connection_unauthorize_status(self, data):
    #     archive_path = "C:\\Users\\mohbakh\\Pictures\\car\\sdk.vuc"
    #     self.conn._api_key = "key"
    #     res = self.conn.create_job(
    #         archive_path=archive_path, job_name="sdk_job", priority="gpu-low", renderer_id=598
    #     ).create()
    #     assert res.status_code == 401

    def test_create_job(self):
        archive_path = "C:\\Users\\mohbakh\\Pictures\\car\\sdk.vuc"
        job = self.conn.create_job(
            archive_path=archive_path,
            job_name="sdk_job2",
            priority="cpu-low",
            software="cinema4d",
            software_version="R23",
            renderer_name="Arnold",
        ).create()
        assert job.status_code == 200

    def test_create_3dsmax_job(self):
        archive_path = "C:\\Users\\sdk_job.vu3"
        job = self.conn.create_job(
            archive_path=archive_path,
            job_name="sdk_job2",
            priority="cpu-low",
            software="3dsmax",
            software_version="2023",
            renderer_name="Corona",
        ).create()
        assert job.status_code == 200

    def test_submit_3dsmx_job(self):
        archive_path = "C:\\Users\\sdk_job.vu3"
        job = self.conn.create_job(
            archive_path=archive_path,
            job_name="sdk_job",
            priority="cpu-low",
            software="3dsmax",
            software_version="2023",
            renderer_name="Corona",
        )
        res = self.conn.submit(job)
        assert res == True

    def test_submit_job(self):
        archive_path = "C:\\Users\\mohbakh\\Pictures\\car\\sdk.vuc"
        job = self.conn.create_job(
            archive_path=archive_path,
            job_name="sdk_job",
            priority="cpu-low",
            software="cinema4d",
            software_version="R23",
            renderer_name="Arnold",
        )
        res = self.conn.submit(job)
        assert res == True

    def _test_connection_upload(self):
        self.conn.upload()
        # assert res.status_code == 401

    def _test_create_job_success(self, data):
        res = self.conn._job(datat=data).create()
        assert res.json().get("success") == True

    def test_get_email(self):
        res = self.conn.get_email
        assert res == RANCH_SDK_EMAIL

    def test_get_user_buckets(self):
        buckets = self.conn.buckets()
        assert buckets["Buckets"][0]["Name"] == RANCH_SDK_EMAIL

    def test_get_rendering_occupation(self):
        rendering_occupation = self.mock_conn.get_cpu_rendering_occupation
        assert rendering_occupation == 4

    def test_get_queued_occupation(self):
        queued_occupation = self.mock_conn.get_cpu_queued_occupation
        assert queued_occupation == 0

    def test_get_cpu_priority(self):
        priority = self.conn.get_priority("cpu-low")
        assert priority == 1

    def test_get_gpu_priority(self):
        priority = self.conn.get_priority("GPU-Low")
        assert priority == 13

    def test_get_renderer_id(self):
        renderer_id = self.conn.get_renderer_id("cinema4d", "R23", "Arnold")
        assert renderer_id == 443

    def test_get_3dsmax_renderer_id(self):
        renderer_id = self.conn.get_renderer_id("3dsmax", "2023", "Corona")
        assert renderer_id == 550
