import copy
import os
from pydoc import doc
import random
import sys
import re
import json
import ftplib
import shutil
import socket
import zipfile
import datetime
import webbrowser
import hashlib
import subprocess
import logging
import logging.handlers

try:
    import c4d
except:
    pass

import sys, os
import json
import shutil
import time

__version__ = "1.0.10"

OCTANE_RENDERENGINE = 10379526
RANCH_OUTPUT = "C:\\MAXON\\Output"
RANCH_CURRENT_JOB = "C:\\Maxon\\Currentjob"
OUTPUT_FORMAT = ""
OUTPUT_PASSE_FORMAT = ""
RANCH_LOGREPORT = "C:\\Users\\mohbakh\\Pictures\\car\\Ranch_SDK_Log.txt"

FROM = ""
MULTIPASS = ""
WIDHT = ""
MULTIPASS_OUTPUT = ""
HEIGTH = ""
TO = ""
RENDERER = ""
MAIN_SCENE = ""
REGULAR_OUTPUT = ""
TILE = 0
CURENT_FRAME = 0


# COMMAND  C:\Maxon\C4D2023\Commandline.exe g_licenseUsername=$Env:g_licenseUsername  g_licensePassword=$Env:g_licensePassword -sdk_scene_path "C:\\Users\\mohbakh\\Pictures\\car\\sdk.c4d"


def get_c4d_scene_path():
    for i, ar in enumerate(sys.argv):
        if ar == "-sdk_scene_path":
            scene_path = sys.argv[i + 1]
            return scene_path
    return ""


class Logger(logging.Logger):
    """
    Logger creates a new logger, outputing to a file (FileHandler).
    """

    MAX_LOG_SIZE = 5 * 1024 * 1024  # Size threshold before rotation
    BACKUP_COUNT = 3  # Number of log rotate

    def __init__(self, log_path=""):
        super().__init__("ranchecker")

        self.file_handler = logging.handlers.RotatingFileHandler(
            RANCH_LOGREPORT, maxBytes=self.MAX_LOG_SIZE, backupCount=self.BACKUP_COUNT
        )

        self.file_handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)-8s: %(message)s", "%Y-%m-%d %H:%M:%S")
        )
        self.file_handler.setLevel(logging.DEBUG)  # log everything in file
        self.addHandler(self.file_handler)

    def close_file(self):
        self.file_handler.close()

    # methods below for a context management (with Logger(...) as logger:)
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_file()


class Thread(c4d.threading.C4DThread):
    def start(self):
        self.Start()

    def join(self):
        self.Wait(False)

    def Main(self):
        self.run()


class Handler:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.infos = []
        self.oks = []


class Worker(Thread, Handler):
    def __init__(self, takes_info="", sdk_doc_path="", use_ftp=False):
        Thread.__init__(self)
        Handler.__init__(self)
        self.sdk_doc_path = sdk_doc_path
        self.scene_dir = os.path.dirname(self.sdk_doc_path)
        self.scene_name_ext = os.path.basename(self.sdk_doc_path)
        self.scene_name = os.path.splitext(self.scene_name_ext)[0]
        self.temp_folder = os.path.join(self.scene_dir, "__RANCHecker__" + self.scene_name)
        self.zip_name = os.path.splitext(self.scene_name)[0] + ".vuc"
        self.zip_path = os.path.join(self.scene_dir, self.zip_name)
        self.use_ftp = use_ftp
        self.saved = None
        self.info = {}
        self.assets = []
        self.missing_assets = []

        self.source_doc = c4d.documents.GetActiveDocument()

        self.logger = Logger()
        self.logger.debug("Worker")

    def _write_info_file(self):
        self.info["main_scene"] = self.scene_name_ext
        json_info_file = os.path.join(self.temp_folder, "RANCHecker.info")
        self.logger.debug("_write_info_file")
        with open(json_info_file, "w") as _file:
            json.dump(self.info, _file, indent=4, ensure_ascii=False)

    def _remove_temp(self):
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder, ignore_errors=True)
            self.logger.debug("_remove_temp")

    def _remove_archive(self, zip_path):
        try:
            os.remove(zip_path)
        except:
            self.logger.debug("_remove_archive")

    def _create_archive(self):
        try:
            content = os.walk(self.temp_folder)
            self._zip = zipfile.ZipFile(self.zip_path, "w", zipfile.ZIP_DEFLATED, allowZip64=True)
            for root, _, files in content:
                self.logger.debug(files)
                for i, _file in enumerate(files):
                    self.logger.debug(_file)
                    absolut_path = os.path.join(root, _file)
                    self.logger.debug("absolut_path " + absolut_path)
                    archive_path = absolut_path.replace(self.temp_folder, "")
                    self._zip.write(absolut_path, archive_path)

            self._zip.close()
        except:
            if self._zip:
                self._zip.close()
                self._remove_archive(self.zip_path)

    def run(self):
        self.logger.debug("run")
        # self.__save_RANCH_doc()
        # self.__upload_ftp_assets()
        # return
        # self.__write_single_node()  # call first write_log_file
        # self.__write_takes_info()
        # self.__write_render_tile()
        # self.__write_log_file()
        # self.__write_network_path()
        # self.__kill_doc()
        # self.logger.close_file()

    def _load_doc(self):
        load_doc = c4d.documents.LoadDocument(
            self.sdk_doc_path,
            c4d.SCENEFILTER_OBJECTS | c4d.SCENEFILTER_MATERIALS | c4d.SCENEFILTER_PROGRESSALLOWED,
        )
        return load_doc

    def _save_project_with_assets(self):
        self.source_doc = self._load_doc()
        self.logger.debug(self.source_doc)
        self.saved = c4d.documents.SaveProject(
            self.source_doc,
            c4d.SAVEPROJECT_ASSETS
            | c4d.SAVEPROJECT_SCENEFILE
            | c4d.SAVEPROJECT_DONTFAILONMISSINGASSETS
            | c4d.SAVEPROJECT_PROGRESSALLOWED
            | c4d.SAVEPROJECT_DONTTOUCHDOCUMENT
            | c4d.SAVEPROJECT_USEDOCUMENTNAMEASFILENAME,
            self.temp_folder,
            self.assets,
            self.missing_assets,
        )
        return self.saved

    def start_synchronous(self):
        if self.sdk_doc_path and os.path.exists(self.sdk_doc_path):
            temp_dir = os.path.dirname(self.sdk_doc_path)
            self._save_project_with_assets()

    def start_asynchronous(self):
        self.logger.debug("start_asynchronous")
        self._write_info_file()
        self._create_archive()
        self._remove_temp()
        # self.start()


def PluginStart():
    scene_path = get_c4d_scene_path()
    if scene_path:
        worcker = Worker(sdk_doc_path=scene_path)
        worcker.start_synchronous()
        # worcker.global_checks()
        worcker.start_asynchronous()
        return True


def PluginMessage(id, data):
    if id == c4d.C4DPL_STARTACTIVITY:
        scene_path = get_c4d_scene_path()

        scene_dir = os.path.dirname(scene_path)
        scene_name_ext = os.path.basename(scene_path)
        scene_name = os.path.splitext(scene_name_ext)[0]

        zip_name = os.path.splitext(scene_name)[0] + ".vuc"
        zip_path = os.path.join(scene_dir, zip_name)

        if not os.path.exists(zip_path):
            PluginStart()
            return True
        else:
            return False

    return False


if __name__ == "__main__" and "doctest" in sys.argv:
    import doctest

    sys.exit(doctest.testmod()[0])
