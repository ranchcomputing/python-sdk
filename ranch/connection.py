"""Module describing a connection."""

import os
from ranch.exceptions import RanchException
from ranch.uploadJob import UploadJob
from ranch.job import Job
from ._retry import retry

import requests
import boto3
from requests.adapters import HTTPAdapter


SWEB_URL = "https://www.ranchcomputing.com/"
TIME_OUT = 5  # TODO add time out to the env variable

endpoint_url = "http://172.30.50.19:80"  # TODO replace with DNS server


class Connect(object):
    def __init__(self, api_key: str) -> None:
        """_summary_



        :param api_key: _description_
        :type api_key: str
        """
        self.api_key = api_key.strip()
        self._session = requests.session()
        s3_session = boto3.session.Session()
        self._email = self.get_email
        self._s3_client = s3_session.client(
            "s3",
            aws_access_key_id=self._email,
            aws_secret_access_key=self.api_key,
            endpoint_url=endpoint_url,
            verify=False,
        )

    @property
    def _api_key(self) -> str:
        """_summary_



        :return: _description_
        :rtype: str
        """
        return self.api_key

    def get_prioritys(self, farm: str = "cpu") -> dict:
        """_summary_



        :param farm: _description_, defaults to "cpu"
        :type farm: str, optional
        :return: _description_
        :rtype: dict
        """
        url = f"api/ranchtools/farms/{farm}.json"
        return self._get(url=url).json()

    @property
    def get_cpu_rendering_occupation(self) -> int:
        """_summary_



        :return: _description_
        :rtype: int
        """
        response = self.get_prioritys("cpu")
        return response.get("occupation")["rendering"]

    @property
    def get_cpu_queued_occupation(self) -> int:
        """_summary_



        :return: _description_
        :rtype: int
        """
        response = self.get_prioritys("cpu")
        return response.get("occupation")["queued"]

    def get_priority(self, priority: str = "cpu-low") -> int:
        """_summary_



        :param priority: _description_, defaults to "cpu-low"
        :type priority: str, optional
        :return: _description_
        :rtype: int
        """
        # TODO add check for priority string if farm existes
        priority_lower = priority.split("-")[1].lower()
        farm = priority.split("-")[0].lower()
        prioritys = self.get_prioritys(farm)
        for prio in prioritys.get("priorities"):
            if priority_lower == prio["name"].split("-")[1].lower():
                return prio["id"]
        return 1  # TODO handle priorty error

    def get_renderer_id(self, software: str, software_version: str, renderer_name: str) -> int:
        """_summary_



        :param software: _description_
        :type software: str
        :param software_version: _description_
        :type software_version: str
        :param renderer_name: _description_
        :type renderer_name: str
        :return: _description_
        :rtype: int
        """
        url = f"api/ranchtools/ranchecker/{software}.json"
        releases = self._get(url=url).json()
        for release in releases["application"]["releases"]:
            if release["version"] == software_version:
                renderers = release["renderers"]
                for rendere in renderers:
                    if rendere["name"] == renderer_name:
                        return rendere["id"]
        # TODO check exception
        return 0

    @property
    def get_email(self) -> str:
        """_summary_



        :return: _description_
        :rtype: dict
        """
        url = "api/projects/downloadable?secure"  # TODO get url from endpoint
        response = self._get(url=url)
        try:
            email = response.json().get("account")["email"]
            return email
        except:
            return ""

    @_api_key.setter
    def _api_key(self, api_key: str) -> None:
        """_summary_



        :param api_key: _description_
        :type api_key: str
        """
        self.api_key = api_key.strip()

    def _set_header(self, api_key: str) -> dict:
        """_summary_



        :return: _description_
        :rtype: dict
        """
        headers = {"x-auth-token": api_key, "Content-type": "application/json", "Accept": "application/json"}
        return headers

    def creat_job(
        self,
        archive_path: str,
        job_name: str,
        priority: str,
        software: str,
        software_version: str,
        renderer_name: str,
    ):
        """_summary_



        :param archive_path: _description_
        :type archive_path: str
        :param job_name: _description_
        :type job_name: str
        :param priority: _description_
        :type priority: str
        :param software: _description_
        :type software: str
        :param software_version: _description_
        :type software_version: str
        :param renderer_name: _description_
        :type renderer_name: str
        :return: _description_
        :rtype: _type_
        """
        job_renderer_id = self.get_renderer_id(software, software_version, renderer_name)
        job_priority = self.get_priority(priority)
        return Job(self, archive_path, job_name, job_priority, job_renderer_id)

    # @retry
    def _post(self, url: str, data: dict = {}) -> dict:
        """_summary_



        :param url: _description_
        :type url: str
        :param data: _description_
        :type data: dict
        """
        _url = SWEB_URL + url
        # self._session.mount(SWEB_URL, HTTPAdapter(max_retries=50))
        headers = self._set_header(self._api_key)
        self._session.headers.update(headers)
        try:
            return self._session.post(_url, headers=headers, json=data, timeout=TIME_OUT)
        except requests.ConnectionError as e:
            raise RanchException("Internet connection check failed")

    def _get(self, url: str, data: dict = {}) -> dict:
        """_summary_



        :param url: _description_
        :type url: str
        :param data: _description_
        :type data: dict
        """
        _url = SWEB_URL + url
        # self._session.mount(SWEB_URL, HTTPAdapter(max_retries=50))
        headers = self._set_header(self._api_key)
        self._session.headers.update(headers)
        try:
            return self._session.get(_url, headers=headers, data=data, timeout=TIME_OUT)
        except requests.ConnectionError as e:
            raise RanchException("Internet connection check failed")

    def submit(self, job: Job) -> bool:
        """_summary_



        :param job: _description_
        :type job: Job
        :return: _description_
        :rtype: bool
        """
        if not os.path.exists(job.get_archive_path):
            return False
        job_name_extension = os.path.splitext(os.path.basename(job.get_archive_path))[1]
        job_name_ext = job.get_job_name + job_name_extension

        response = job.create()

        if not response.json().get("success"):
            # TODO
            return False
        else:
            metadata = response.json().get("metadata")
            metadata["uploader_name"] = "racnhcomputing python SDK"
            metadata["uploader_version"] = "2.0.0"
            metadata["filename"] = job_name_ext

            tuspload = response.json().get("tuspload")
            upload = UploadJob(
                endpoint=tuspload["endpoint"],
                chunk_size=tuspload.get("chunkSize", None),
                file_path=job.get_archive_path,
                metadata=metadata,
            )
            if upload.run():
                return True
        return False

    def buckets(self) -> list:
        """_summary_



        :return: _description_
        :rtype: list
        """
        if self._s3_client is None:
            return []  # TODO

        return self._s3_client.list_buckets()

    def _call_api(self, url: str, request) -> dict:
        pass
