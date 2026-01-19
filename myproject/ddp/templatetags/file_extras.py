from django import template
import os

register = template.Library()

@register.filter
def file_icon(filename):
    """Return appropriate icon/emoji based on file extension"""
    if not filename:
        return '📄'
    
    ext = os.path.splitext(filename)[1].lower()
    
    icon_map = {
        # Images
        '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️', 
        '.bmp': '🖼️', '.svg': '🖼️', '.webp': '🖼️',
        # Documents
        '.doc': '📝', '.docx': '📝', '.txt': '📝', '.rtf': '📝',
        # PDFs
        '.pdf': '📕',
        # Spreadsheets
        '.xls': '📊', '.xlsx': '📊', '.csv': '📊',
        # Presentations
        '.ppt': '📊', '.pptx': '📊',
        # Videos
        '.mp4': '🎬', '.avi': '🎬', '.mkv': '🎬', '.mov': '🎬', 
        '.wmv': '🎬', '.flv': '🎬', '.webm': '🎬',
        # Audio
        '.mp3': '🎵', '.wav': '🎵', '.flac': '🎵', '.aac': '🎵', 
        '.ogg': '🎵', '.wma': '🎵',
        # Archives
        '.zip': '🗜️', '.rar': '🗜️', '.7z': '🗜️', '.tar': '🗜️', 
        '.gz': '🗜️', '.bz2': '🗜️',
        # Code
        '.py': '🐍', '.js': '📜', '.html': '🌐', '.css': '🎨', 
        '.java': '☕', '.cpp': '⚙️', '.c': '⚙️', '.php': '🐘',
        '.rb': '💎', '.go': '🔵', '.rs': '🦀',
    }
    
    return icon_map.get(ext, '📄')

@register.filter
def format_bytes(bytes_size):
    """Format bytes to human readable format"""
    try:
        bytes_size = int(bytes_size)
    except (ValueError, TypeError):
        return '0 B'
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"

@register.filter
def file_extension(filename):
    """Get file extension from filename"""
    if not filename:
        return ''
    return os.path.splitext(filename)[1].upper().replace('.', '')
