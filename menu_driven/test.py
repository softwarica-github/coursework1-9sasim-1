import unittest
from unittest.mock import Mock, patch, mock_open
import methods  # Import your methods module
from buffer import Buffer

class TestMethods(unittest.TestCase):

    @patch('socket.socket')
    @patch('methods.buffer.Buffer')  # Patch the Buffer class in methods module
    def test_receive(self, mock_buffer, mock_socket):
        mock_s = mock_socket.return_value
        mock_conn = mock_socket.return_value
        mock_conn.recv.side_effect = [
            b'md5', b'file.txt', b'10', b'fake_data', b''
        ]

        mock_s.accept.return_value = (mock_conn, ('127.0.0.1', 12345))

        mock_buf = mock_buffer.return_value
        mock_buf.get_utf8.side_effect = ['md5', 'file.txt', '10', '', None]

        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.return_value.write.return_value = None
            methods.receive()  # No need to pass mock socket object here

        # TODO: Add assertions based on your expected behavior
        mock_s.bind.assert_called_with(('', 2345))
        mock_s.listen.assert_called_with(10)
        mock_s.accept.assert_called()

if __name__ == '__main__':
    unittest.main()
