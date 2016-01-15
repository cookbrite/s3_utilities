# Restoring buckets and directories from S3

This is a program that can quickly undelete files, folders, or entire buckets en masse from AWS S3 versioned buckets, which comes in handy if you accidentally delete something you wanted to keep. To use this program, your bucket must have [versioning enabled](http://docs.aws.amazon.com/AmazonS3/latest/UG/enable-bucket-versioning.html).

## To restore an entire bucket:
`./s3_undelete.py -b some_test_bucket -u`

## To restore a directory within a bucket:
`./s3_undelete.py -b some_test_bucket -f some\ test\ folder -u`

## To restore one object within a directory:
`./s3_undelete.py -b some_test_bucket -k “some/test/file.jpg” -u`

*note: you must have the entire key name (including directories) in order to perform this operation.*

## To delete an object:
`./s3_undelete.py -b some_test_bucket -k “some/test/file.jpg” -d`

*this will prompt the user to confirm before deleting*

## To delete a folder:
`./s3_undelete.py -b some_test_bucket -f some\ test \folder -d`

*this will prompt the user to confirm before deleting each object within a directory*

# License
MIT License


# Contributing
We welcome contributions. Contact me at holly@metabrite.com (or submit a pull request).
