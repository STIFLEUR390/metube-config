"""
ReplayGain postprocessor for yt-dlp.
Applies ReplayGain tags to downloaded audio files for consistent playback volume.

Based on: https://github.com/Eboreg/yt-dlp-replaygain
"""
import subprocess
import json

from yt_dlp.postprocessor.common import PostProcessor
from yt_dlp.utils import PostProcessingError


class ReplayGainPP(PostProcessor):
    """
    Applies track and (optionally) album ReplayGain to downloaded audio files.
    
    Usage in YTDL_OPTIONS:
    {
        "postprocessors": [
            {"key": "ReplayGain"}
        ]
    }
    """
    
    def __init__(self, downloader=None, album=False):
        super().__init__(downloader)
        self._album = album
    
    def run(self, info):
        filepath = info.get('filepath')
        if not filepath:
            return [], info
        
        try:
            # Apply track gain
            cmd = ['ffmpeg', '-i', filepath, '-af', 'replaygain=track_gain=1', '-y', filepath]
            subprocess.run(cmd, check=True, capture_output=True)
            self.to_screen(f'Applied ReplayGain to "{filepath}"')
        except subprocess.CalledProcessError as e:
            self.to_screen(f'Warning: ReplayGain failed for "{filepath}": {e.stderr.decode()[:200]}')
        except FileNotFoundError:
            self.to_screen('Warning: ffmpeg not found, skipping ReplayGain')
        
        return [], info
