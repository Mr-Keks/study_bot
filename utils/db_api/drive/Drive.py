import io
import re
from datetime import datetime

from data.config import BOT_TOKEN
import requests
from utils.db_api.drive.Google import Create_Service
from utils.db_api.drive.mimeTypes import mimeTypes
from googleapiclient.http import MediaFileUpload, MediaInMemoryUpload, MediaIoBaseDownload


class Drive:
    CLIENT_SECRET_FILE = 'C:/Python/programs/bots/study_bot/data/client_secret_554888114776_kklv564arnv3av1rkb9qri3p5fhl4i0t_apps.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    async def create_group_folder(self, group_name: str):
        file_metadata = {
            'name': group_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        group_folder = self.service.files().create(body=file_metadata).execute()
        return group_folder.get('id')

    async def create_drive_folder(self, parent_folder, drive_folder_name):
        file_metadata = {
            'name': drive_folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder]
        }

        subject_folder_id = self.service.files().create(body=file_metadata).execute()
        return subject_folder_id.get('id')

    async def upload_home_work(self, home_work_files: list, files_mime: list, drive_folder: str, files_path: list):
        # check folder exist
        query = f"parents = 'application/vnd.google-apps.folder'"

        response = self.service.files().list(q="mimeType='application/vnd.google-apps.folder'").execute()
        drive_folders = response.get('files')
        home_work_folder_name = str(datetime.today().date().__str__()) + f'({drive_folder})'

        home_work_folder_id = ""
        if (home_work_folder_name in [folder_in_drive.get('name') for folder_in_drive in drive_folders]) is False:
            home_work_folder_id = await self.create_drive_folder(drive_folder, home_work_folder_name)
        else:
            for folder_in_drive in drive_folders:
                if folder_in_drive.get('name') == home_work_folder_name:
                    home_work_folder_id = folder_in_drive.get('id')
                    break
        # write data
        files_id = []
        query = f'parents = {drive_folder}'
        for home_work_file, mimeType, file_path in zip(home_work_files, files_mime, files_path):
            # type_file = re.findall('[.]+[\w]+', file)

            file_metadata = {
                'name': home_work_file,
                'parents': [home_work_folder_id]
            }

            get_file = requests.get(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}')
            media = MediaInMemoryUpload(get_file.content, mimeType)

            response = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            files_id.append(response.get('id'))
        return files_id

    async def download_home_work_files(self, files_id: list):
        if files_id is None:
            return None
        files = {}
        for file_id in files_id:
            request = self.service.files().get_media(fileId=file_id)
            file_name = self.service.files().get(fileId=file_id).execute().get('name')
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fd=fh, request=request)
            done = False

            while not done:
                status, done = downloader.next_chunk()

            fh.seek(0)

            files.update({file_name: fh})
        return files
