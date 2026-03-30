import os
import shutil
import logging

_model = None


def _ensure_ffmpeg():
    """Make ffmpeg available to Whisper by creating a symlink/copy from imageio-ffmpeg."""
    # Check if ffmpeg is already on PATH
    if shutil.which('ffmpeg'):
        return

    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        if not ffmpeg_exe or not os.path.exists(ffmpeg_exe):
            print('Warning: imageio-ffmpeg binary not found')
            return

        # Create a directory with a properly named ffmpeg.exe
        bin_dir = os.path.join(os.path.dirname(__file__), '..', '_ffmpeg_bin')
        bin_dir = os.path.abspath(bin_dir)
        os.makedirs(bin_dir, exist_ok=True)

        target = os.path.join(bin_dir, 'ffmpeg.exe')
        if not os.path.exists(target):
            shutil.copy2(ffmpeg_exe, target)
            print(f'Copied ffmpeg to {target}')

        if bin_dir not in os.environ.get('PATH', ''):
            os.environ['PATH'] = bin_dir + os.pathsep + os.environ.get('PATH', '')
            print(f'Added ffmpeg to PATH: {bin_dir}')

    except ImportError:
        print('Warning: imageio-ffmpeg not installed. Voice transcription will not work.')
    except Exception as e:
        print(f'Warning: Could not set up ffmpeg: {e}')


def _get_model():
    global _model
    if _model is None:
        _ensure_ffmpeg()
        import whisper
        _model = whisper.load_model('base')
        print('Whisper base model loaded successfully')
    return _model


def transcribe(audio_path):
    """Transcribe audio file to English text using Whisper."""
    try:
        model = _get_model()
        result = model.transcribe(audio_path, language='en')
        text = result['text'].strip()
        if text:
            print(f'Transcribed {len(text)} chars from {os.path.basename(audio_path)}')
        else:
            print(f'Warning: empty transcription for {os.path.basename(audio_path)}')
        return text
    except Exception as e:
        logging.error(f'Transcription error: {e}')
        return ''
