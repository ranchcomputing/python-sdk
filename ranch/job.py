"""Module describing a Job."""


class Job(object):
    def __init__(
        self,
        connection,
        archive_path: str,
        job_name: str,
        priority: str,
        renderer_id: int,
    ) -> None:
        """_summary_



        :param connection: _description_
        :type connection: _type_
        :param archive_path: _description_
        :type archive_path: str
        :param job_name: _description_
        :type job_name: str
        :param priority: _description_
        :type priority: str
        :param renderer_id: _description_
        :type renderer_id: int
        """
        self._connection = connection
        self.archive_path = archive_path
        self.job_name = job_name
        self.priority = priority
        self.renderer_id = renderer_id
        self._data = {}

    def set_email(self, email):
        """_summary_



        :param email: _description_
        :type email: _type_
        :return: _description_
        :rtype: _type_
        """
        self._data["email"] = email
        return email

    def set_priority(self, priority):
        """_summary_



        :param priority: _description_
        :type priority: _type_
        :return: _description_
        :rtype: _type_
        """
        self._data["priority_id"] = priority
        return priority

    def set_renderer_id(self, renderer_id):
        """_summary_



        :param renderer_id: _description_
        :type renderer_id: _type_
        :return: _description_
        :rtype: _type_
        """
        self._data["renderer_id"] = renderer_id
        return renderer_id

    def set_specific_frames(self, frames: str) -> dict:
        """_summary_



        :param frames: _description_
        :type frames: str
        :return: _description_
        :rtype: dict
        """
        specific_frames = {"type": "specific", "specific_frames": frames}
        self._data["frames"] = specific_frames
        return specific_frames

    @property
    def get_job_name(self):
        """_summary_



        :return: _description_
        :rtype: _type_
        """
        return self.job_name

    @property
    def get_archive_path(self):
        """_summary_



        :return: _description_
        :rtype: _type_
        """
        return self.archive_path

    def create(self) -> dict:
        """_summary_



        :return: _description_
        :rtype: dict
        """
        self._data["disclaimer"] = True
        self._data["email"] = self._connection.get_email
        self._data["renderer_id"] = self.renderer_id
        self._data["priority_id"] = self.priority
        return self._connection._post("api/projects", self._data)
