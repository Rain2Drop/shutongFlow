#!/usr/bin/env python3

import sys
import oss2
import time

from .key import calc as calc_key


class Bucket:
    def __init__(self,
                 access_key_id: str, access_key_secret: str,
                 endpoint: str, bucket_name: str):
        auth = oss2.Auth(access_key_id, access_key_secret)
        self._bucket = oss2.Bucket(auth=auth, endpoint=endpoint, bucket_name=bucket_name)

    def _upload_file(self, path: str, retry: int, retry_interval: float, err_handler) -> str:
        """
        Upload a file to the bucket.

        :param path: local file path.
        :param retry: retries on oss failure.
        :param retry_interval: time to sleep on a upload failure.
        :param err_handler:
        :return: key of the file.
        :raise oss2.exceptions.OssError: on oss error.
        """
        key = calc_key(path)

        assert retry >= 0
        max_loop = retry + 1
        for each_try in range(max_loop):
            try:
                result = self._bucket.put_object_from_file(key=key, filename=path)
                assert result.status // 100 == 2
            except oss2.exceptions.OssError as e:
                err_handler(path, e)
                # No sleep required, for the last try
                if each_try != max_loop - 1:
                    time.sleep(retry_interval)
                else:
                    # For the last try, just raise the exception
                    raise

            else:
                return key

        return None

    def upload(self, path: str) -> str:
        """
        Upload a file to bucket.

        :param path: local file path
        :return: key on the bucket.
        :raise oss2.exceptions.OssError: on oss error.
        """
        def err_handler(path, e):
            print(f'Warning: Failed to upload: {path}, response: {e}', file=sys.stderr)

        return self._upload_file(path=path, retry=5, retry_interval=5, err_handler=err_handler)
