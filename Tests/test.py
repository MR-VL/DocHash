import unittest
from unittest.mock import patch, mock_open

from main import (
    remove_duplicates, write_duplicate, remove_manifest,
    create_manifest, compute_directory,
    get_extension, hash_file, rename_file
)


class DocHash(unittest.TestCase):

    @patch('os.remove')
    def test_remove_duplicates(self, mock_remove):
        # Test when the file exists
        remove_duplicates()
        mock_remove.assert_called_with('duplicate.csv')

        # Test when the file does not exist
        mock_remove.side_effect = FileNotFoundError
        remove_duplicates()
        mock_remove.assert_called_with('duplicate.csv')

    @patch('builtins.open', new_callable=mock_open)
    @patch('main.hash_file', return_value='dummy_hash')
    def test_write_duplicate(self, mock_hash_file, mock_open_file):
        x = 1
        path = 'dummy/path/file.txt'
        directory = 'dummy/path'

        write_duplicate(x, path, directory)
        mock_open_file.assert_called_once_with('duplicate.csv', 'a', newline='')
        mock_open_file().write.assert_called()

    @patch('os.remove')
    def test_remove_manifest(self, mock_remove):
        # Test when the file exists
        remove_manifest()
        mock_remove.assert_called_with('manifest.csv')

        # Test when the file does not exist
        mock_remove.side_effect = FileNotFoundError
        remove_manifest()
        mock_remove.assert_called_with('manifest.csv')

    @patch('builtins.open', new_callable=mock_open)
    def test_create_manifest(self, mock_open_file):
        x = 1
        path = 'dummy/path/file.txt'

        create_manifest(x, path)
        mock_open_file.assert_called_once_with('manifest.csv', 'a', newline='')
        mock_open_file().write.assert_called()

    @patch('os.listdir', return_value=['file1.txt', 'file2.txt'])
    @patch('os.path.isfile', return_value=True)
    @patch('main.hash_file', return_value='dummy_hash')
    @patch('main.rename_file')
    @patch('main.create_manifest')
    def test_compute_directory(self, mock_create_manifest, mock_rename_file, mock_hash_file, mock_isfile, mock_listdir):
        directory = 'dummy/path'
        compute_directory(directory, True)

        mock_listdir.assert_called_with(directory)
        mock_create_manifest.assert_called()
        mock_rename_file.assert_called()

    def test_get_extension(self):
        file_name = 'file.txt'
        extension = get_extension(file_name)
        self.assertEqual(extension, '.txt')

    @patch('os.rename')
    @patch('os.path.exists', return_value=False)
    def test_rename_file(self, mock_exists, mock_rename):
        old_name = 'old_file.txt'
        new_name = 'new_file.txt'

        rename_file(old_name, new_name)
        mock_exists.assert_called_with(new_name)
        mock_rename.assert_called_with(old_name, new_name)

    @patch('hashlib.sha256')
    @patch('builtins.open', new_callable=mock_open, read_data=b'file data')
    def test_hash_file(self, mock_open_file, mock_sha256):
        file_src = 'dummy/path/file.txt'
        old_name = 'file.txt'

        mock_hash = mock_sha256.return_value
        mock_hash.hexdigest.return_value = 'dummy_hash'

        result = hash_file(file_src, old_name)
        mock_open_file.assert_called_once_with(file_src, 'rb')
        self.assertTrue(result.endswith('dummy_hash.txt'))


if __name__ == '__main__':
    unittest.main()
