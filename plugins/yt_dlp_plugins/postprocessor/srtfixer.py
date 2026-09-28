"""
SRT Fixer postprocessor for yt-dlp.
Fixes duplicate lines in auto-generated YouTube subtitles.

Based on: https://github.com/bindestriche/srt_fix
"""
import re

from yt_dlp.postprocessor.common import PostProcessor


class SrtFixerPP(PostProcessor):
    """
    Removes duplicate consecutive lines in SRT subtitle files.
    This is common with YouTube auto-generated subtitles.
    
    Usage in YTDL_OPTIONS:
    {
        "postprocessors": [
            {"key": "SrtFixer"}
        ]
    }
    """
    
    def run(self, info):
        subs = info.get('requested_subtitles') or {}
        
        for lang, sub_info in subs.items():
            filepath = sub_info.get('filepath')
            if not filepath or not filepath.endswith('.srt'):
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                fixed = self._fix_srt(content)
                
                if fixed != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(fixed)
                    self.to_screen(f'Fixed duplicate lines in subtitles: {filepath}')
            except Exception as e:
                self.to_screen(f'Warning: SRT fix failed for {filepath}: {e}')
        
        return [], info
    
    def _fix_srt(self, content):
        """Remove duplicate consecutive lines in SRT content."""
        blocks = content.strip().split('\n\n')
        fixed_blocks = []
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                # SRT block: index, timestamp, subtitle lines
                index = lines[0]
                timestamp = lines[1]
                subtitle_lines = lines[2:]
                
                # Remove consecutive duplicate lines
                deduped = []
                prev = None
                for line in subtitle_lines:
                    if line != prev:
                        deduped.append(line)
                        prev = line
                
                fixed_blocks.append(f'{index}\n{timestamp}\n' + '\n'.join(deduped))
            else:
                fixed_blocks.append(block)
        
        return '\n\n'.join(fixed_blocks) + '\n'
