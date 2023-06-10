import win32clipboard
import ctypes

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def get_clip_format_name(format_id):
    """Return the name of the clipboard format with the given ID"""
    return win32clipboard.GetClipboardFormatName(format_id)

def list_clip_formats():
    """Return a list of available clipboard formats"""
    formats = []
    format_id = 0
    while True:
        format_id = user32.EnumClipboardFormats(format_id)
        if format_id == 0:
            err = kernel32.GetLastError()
            if err != 0:
                raise ctypes.WinError(err)
            break
        formats.append(format_id)
    return formats

def get_clipboard_data(format_id):
    """Return clipboard data for the given format ID"""
    win32clipboard.OpenClipboard()
    try:
        if not win32clipboard.IsClipboardFormatAvailable(format_id):
            raise ValueError(f"Format {format_id} not available")
        return win32clipboard.GetClipboardData(format_id)
    finally:
        win32clipboard.CloseClipboard()
