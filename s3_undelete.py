#!/usr/bin/env python

from __future__ import print_function
from boto.s3 import deletemarker
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import argparse

conn = S3Connection()
"""
establish connection with boto
"""

class S3Key(object):
    def __init__(self, name, bucket):
        self.name = name
        self.bucket = conn.get_bucket(bucket)
        self.bucket_string = str(bucket)

    def get_object_versions(self):
        """
        returns a list of the object's versions
        """
        k = Key(self.bucket)
        k.key = self.name
        versions = list(self.bucket.list_versions(self.name))
        return [k.version_id for k in versions]

    def delete_object(self, verify=True):
        """
        deletes an object from a bucket
        """
        k = Key(self.bucket)
        k.key = self.name
        if verify and raw_input('Are you sure you want to delete this? Y/N \n').lower() != 'y':
            return
        k.delete()
        print('{} deleted from {}'.format(self.name, self.bucket_string))

    def undelete_object(self):
        """
        copies previous version to specified object key, effectively making it the 'current' version
        """
        self.bucket.copy_key(self.name, self.bucket_string, self.name,
                             src_version_id=self.get_object_versions()[1])
        print('{} has been restored.'.format(self.name))


def restore_bucket(bucket_name):
    """
    restores all contents of a bucket
    """
    bucket = conn.get_bucket(bucket_name)
    for version in bucket.list_versions():
        if isinstance(version, deletemarker.DeleteMarker) and version.is_latest:
            bucket.delete_key(version.name, version_id=version.version_id)
    print('Bucket \'{}\' has been restored.'.format(bucket_name))


def delete_folder(bucket_name, prefix, verify=True):
    """
    deletes all objects within a folder, makes user confirm each object within the folder
    """
    bucket = conn.get_bucket(bucket_name)
    for key in bucket.list():
        if key.key.startswith(prefix):
            if verify and raw_input('Are you sure you want to delete this? Y/N \n').lower() != 'y':
                return
            key.delete()
            print('{} has been deleted'.format(key))
    print('Folder \'{}\' has been deleted.'.format(prefix))


def restore_folder(bucket_name, prefix):
    """
    restores all contents in a single directory of a bucket
    """
    versions = []
    count = 0
    bucket = conn.get_bucket(bucket_name)
    for version in bucket.list_versions():
        versions.append(version)
    for version in versions:
        count += 1
        if isinstance(version, deletemarker.DeleteMarker) and version.is_latest:
            key = versions[count]
            if key.key.startswith(prefix):
                bucket.delete_key(version.name, version_id=version.version_id)
    print('Folder \'{}\' restored from \'{}\'.'.format(prefix, bucket_name))


def main():
    parser = argparse.ArgumentParser(description='S3 Bucket Restoration')
    parser.add_argument(
        '--bucket', '-b',
        type=str,
        help='the name of the bucket to work from',
        default=None
    )
    parser.add_argument(
        '--folder', '-f',
        type=str,
        help='the name of a folder within a bucket to delete or restore',
        default=None
    )
    parser.add_argument(
        '--key', '-k',
        type=str,
        help='the name of the object to delete or restore',
        default=None
    )
    command = parser.add_mutually_exclusive_group()
    command.add_argument(
        '--all-buckets', '-a',
        help='print a list of all buckets in s3',
        action='store_true', default=False
    )
    command.add_argument(
        '--list-contents', '-l',
        help='print a list of the contents of a bucket',
        action='store_true', default=False
    )
    command.add_argument(
        '--undelete', '-u',
        help='undelete a bucket, directory, or object',
        action='store_true', default=False
    )
    command.add_argument(
        '--delete', '-d',
        help='deletes objects or directories from S3',
        action='store_true', default=False
    )
    args = parser.parse_args()

    if args.all_buckets:
        bucket_list = conn.get_all_buckets()
        for bucket in bucket_list:
            print(bucket.name)

    if args.bucket and args.folder and not args.key:
        if args.undelete:
            restore_folder(args.bucket, args.folder)
        if args.delete:
            delete_folder(args.bucket, args.folder)

    if args.bucket and args.key:
        target = S3Key(args.key, args.bucket)
        if args.undelete:
            target.undelete_object()
        elif args.delete:
            target.delete_object()

    elif args.bucket and not args.key:
        if args.list_contents:
            for key in conn.get_bucket(args.bucket).list():
                print(key.name)

        elif args.undelete and not args.folder:
            restore_bucket(args.bucket)


if __name__ == "__main__":
    main()
