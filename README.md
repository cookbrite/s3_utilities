# Restoring buckets and directories from S3

Uses boto to restore accidentally deleted objects from versioned Amazon standard IA S3 bucket.

## To restore an entire bucket:
`$ content_utilities/scripts python s3_undelete.py -b some_test_bucket -u`

## To restore a directory within a bucket:
`$ content_utilities/scripts python s3_undelete.py -b some_test_bucket -f some\ test\ folder -u`

## To restore one object within a directory:
`$ content_utilities/scripts python s3_undelete.py -b some_test_bucket -k “some/test/file.jpg” -u`

*note: you must have the entire key name (including directories) in order to perform this operation.*

## To delete an object:
`$ content_utilities/scripts python s3_undelete.py -b some_test_bucket -k “some/test/file.jpg” -d`

*this will prompt the user to confirm before deleting*

## To delete a folder:
`$ content_utilities/scripts python s3_undelete.py -b some_test_bucket -f some\ test \folder -d`

*this will prompt the user to confirm before deleting each object within a directory*

MIT License 2016, Metabrite Inc.
holly@metabrite.com
